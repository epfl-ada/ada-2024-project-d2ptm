from src.utils.helpers import read_communities
from src.utils.networkx_helpers import katz_centrality, betweenness_centrality, closeness_centrality, importance
from src.utils.actors import ActorStats


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def count_communities_list_occurences(communities_list, actor_l, actor_r):
    sm = 0
    for communities in communities_list:
        has_both = False
        for community in communities:
            if actor_l in community and actor_r in community:
                has_both = True
                break
        sm += 1 if has_both else 0
    return sm


def get_cooccurrences(G):
    ITERATIONS = 100
    G_cooccurrences = nx.Graph()
    communities_list = []
    communities_list_probs = []
    for communities_seed in range(1, 6):
        communities = read_communities(G, f"data/processed/new_communities_US_{communities_seed}.json")
        communities_list.append(communities)
        probs = []
        for community in communities:
            probs.append((len(community) * (len(community) - 1)) // 2)
        probs = np.array(probs, dtype=float)
        probs /= probs.sum()
        communities_list_probs.append(probs)

    cooccs = []
    for i, community in enumerate(communities_list):
        if len(community) == 1:
            continue
        community_to_sample = np.random.choice(len(communities_list_probs[i]), size=ITERATIONS, p=communities_list_probs[i])
        for j in range(ITERATIONS):
            actor_l, actor_r = np.random.choice(communities_list[i][community_to_sample[j]], size=2, replace=False)
            coocc = count_communities_list_occurences(communities_list, actor_l, actor_r)
            cooccs.append(coocc)
    cooccs = np.array(cooccs)
    return cooccs.mean() / 5


def draw_year_distribution(year_data):
    fig, ax = plt.subplots()

    ax.boxplot(year_data)

    ax.set_title('Year of release distribution for clusters')
    ax.set_ylabel(r'Year of release')
    ax.set_xlabel(r'The size of the cluster is decreasing $\longrightarrow$')
    ax.set_xticks([])
    ax.set_ylim((1940, 2015))
    plt.show()


def map_communities(communities_list, actor_id_to_community_list, idx_i, idx_j):
        communities_i = communities_list[idx_i]
        communities_used_j = set()
        map_community = [-1 for _ in range(len(communities_i))]
        matching_percent = [0 for _ in range(len(communities_i))]
        for i, community in enumerate(communities_i):
            count_community = dict()
            for actor_id in community:
                other_community = actor_id_to_community_list[idx_j][actor_id]
                if other_community not in communities_used_j:
                    count_community[other_community] = count_community.get(other_community, 0) + 1
            map_community[i] = max(count_community.items(), key=lambda x: x[1])[0] if len(count_community) > 0 else -1
            if map_community[i] != -1:
                matching_percent[i] = count_community[map_community[i]] / len(community)
                communities_used_j.add(map_community[i])
        return list(zip(map_community, matching_percent))


def generate_graph(communities_list, actor_id_to_community_list, first_nodes_to_consider, generate_from_and_to=None, starting_position=None):
    G = nx.DiGraph()
    for i in range(5):
        for j in range(5):
            if i != j:
                mapping = map_communities(communities_list, actor_id_to_community_list, i, j)
                for idx_from, stats_pair in enumerate(mapping[:first_nodes_to_consider]):
                    from_v = f"{i};{idx_from}"
                    to_v = f"{j};{stats_pair[0]}"
                    add_edge = False
                    if stats_pair[1] > 0.8: #
                        if generate_from_and_to is not None:
                            if i == generate_from_and_to or j == generate_from_and_to:
                                add_edge = True
                            else:
                                add_edge = False
                        else:
                            add_edge = True
                        if starting_position is not None:
                            if int(idx_from) < starting_position or int(stats_pair[0]) < starting_position:
                                add_edge = False
                    if add_edge:
                        G.add_edge(from_v, to_v, weight=round(stats_pair[1], 2))
    return G


def read_community_list(G, communities_list, actor_id_to_community_list):
    for i in range(1, 6):
        communities_US = read_communities(G, f"data/processed/new_communities_US_{i}.json")
        communities_US = sorted(communities_US, key=lambda x: len(x), reverse=True)

        actor_id_to_community = dict()
        for i, community in enumerate(communities_US):
            for actor_id in community:
                actor_id_to_community[actor_id] = i

        actor_id_to_community_list.append(actor_id_to_community)
        communities_list.append(communities_US)


def draw_G(G, k=0.5, iterations=50, seed=1):
    ax = plt.gca()
    ax.set_title("Matching Graph")
    fig = plt.gcf()
    fig.set_figwidth(7)
    fig.set_figheight(6)
    pos=nx.spring_layout(G, k=k, iterations=iterations, seed=seed)
    nx.draw(G,pos, edge_cmap=plt.cm.Reds, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    plt.show()


def cluster_most_popular_genres(cluster, top_k=3):
    sorted_genres = sorted(cluster.cluster_genres().items(), key=lambda x: x[1], reverse=True)
    return sorted_genres[:top_k]


def print_cluster_actor_info(G, characters, movies, cluster):
    
    G_cluster = G.subgraph(cluster.actor_ids)
    actor_stats = ActorStats(characters, movies)

    nx.set_node_attributes(G_cluster, dict([(actor_id, actor_stats.actor_name(actor_id)) for actor_id in G_cluster.nodes()]), 'Name')
    katz = katz_centrality(G_cluster, verbose=False)
    betweennness = betweenness_centrality(G_cluster, verbose=False)
    closeness = closeness_centrality(G_cluster, verbose=False)

    importance(G_cluster, betweennness, closeness, katz)


def get_top_movies_by_revenue(cluster, num_actors_in_movie):
    return cluster.cluster_movies(select_type="half", num_actors_in_movie=num_actors_in_movie).sort_values(by="Revenue", ascending=False)["MovieName"].head(10)


def make_cluster_years_list(graph_stats, size_l, select_type, num_actors_in_movie=None):
    cluster_years_list = []
    for cluster in graph_stats.clusters:
        cluster_years = cluster.cluster_movies(select_type=select_type, num_actors_in_movie=num_actors_in_movie)["ReleaseDate"].apply(lambda x: int(x.year))
        if len(cluster_years) >= size_l:
            cluster_years_list.append(cluster_years)
    return cluster_years_list
