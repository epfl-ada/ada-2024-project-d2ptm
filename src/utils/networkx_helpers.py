import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def katz_centrality(G):
    """
    Computes the Katz centrality for all nodes in the graph and assigns the computed 
    values as node attributes. Also prints the top 5 nodes with the highest Katz centrality.

    Katz centrality is calculated using an alpha value slightly below the reciprocal 
    of the largest eigenvalue of the graph's adjacency matrix.

    Parameters
    ----------
    G : networkx.Graph
        The input graph for which the Katz centrality is to be computed.

    Returns
    -------
    dict
        A dictionary where keys are node identifiers and values are the corresponding 
        Katz centrality scores.

    Notes
    -----
    - The `katz` centrality values are also added as node attributes in the input graph, 
      accessible via `G.nodes[node]['katz']`.
    - Prints the names and Katz centrality scores of the top 5 nodes with the highest scores.
    """
    # Compute largest eigenvalue
    largest_eigenvalue = max(abs(np.linalg.eigvals(nx.adjacency_matrix(G).todense())))
    # Set alpha slightly below 1 / λ_max
    alpha = 1 / largest_eigenvalue - 0.01
    katz = nx.katz_centrality(G, alpha=alpha)
    nx.set_node_attributes(G, katz, 'katz')
    sorted_katz = sorted(katz.items(), key=lambda x: x[1], reverse=True)
    for actor, katzc in sorted_katz[:5]:
        print(G.nodes[actor]['Name'], 'has katz-centrality: %.3f' %katzc)
    return katz


def closeness_centrality(G):
    """
    Computes the closeness centrality for all nodes in the graph and assigns the computed 
    values as node attributes. Also prints the top 5 nodes with the highest closeness centrality.

    Closeness centrality measures how efficiently a node can reach all other nodes 
    in the graph.

    Parameters
    ----------
    G : networkx.Graph
        The input graph for which the closeness centrality is to be computed.

    Returns
    -------
    dict
        A dictionary where keys are node identifiers and values are the corresponding 
        closeness centrality scores.

    Notes
    -----
    - The `closeness` centrality values are also added as node attributes in the input graph, 
      accessible via `G.nodes[node]['closeness']`.
    - Prints the names and closeness centrality scores of the top 5 nodes with the highest scores.
    """
    closeness = nx.closeness_centrality(G) 
    nx.set_node_attributes(G, closeness, 'closeness')
    sorted_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
    for actor, closec in sorted_closeness[:5]:
        print(G.nodes[actor]['Name'], 'has closeness-centrality: %.3f' %closec)
    return closeness

def betweenness_centrality(G):
    """
    Computes the betweenness centrality for all nodes in the graph and assigns the computed 
    values as node attributes. Also prints the top 5 nodes with the highest betweenness centrality.

    Betweenness centrality measures the number of times a node acts as a bridge along 
    the shortest path between two other nodes. The results are normalized by default.

    Parameters
    ----------
    G : networkx.Graph
        The input graph for which the betweenness centrality is to be computed.

    Returns
    -------
    dict
        A dictionary where keys are node identifiers and values are the corresponding 
        betweenness centrality scores.

    Notes
    -----
    - The `betweenness` centrality values are also added as node attributes in the input graph, 
      accessible via `G.nodes[node]['betweenness']`.
    - Prints the names and betweenness centrality scores of the top 5 nodes with the highest scores.
    """
    bet_centrality = nx.betweenness_centrality(G, normalized = True, endpoints = False) 
    nx.set_node_attributes(G, bet_centrality, 'betweenness')
    sorted_betweenness = sorted(bet_centrality.items(), key=lambda x: x[1], reverse=True)
    for actor, betc in sorted_betweenness[:5]:
        print(G.nodes[actor]['Name'], 'has betweenness-centrality: %.3f' %betc)
    return bet_centrality

def importance(G, bet_centrality, closeness, katz):
    """
    Computes a combined centrality score for each node in the graph by averaging 
    the betweenness centrality, closeness centrality, and Katz centrality. The resulting 
    scores are normalized to the range [0, 1] and assigned as node attributes.

    The centrality score for each node is calculated as the mean of its betweenness, 
    closeness, and Katz centrality values, with the scores normalized to ensure consistency.

    Parameters
    ----------
    G : networkx.Graph
        The input graph for which the combined centrality is to be computed.
    bet_centrality : dict
        A dictionary containing the betweenness centrality values for each node in the graph.
    closeness : dict
        A dictionary containing the closeness centrality values for each node in the graph.
    katz : dict
        A dictionary containing the Katz centrality values for each node in the graph.

    Returns
    -------
    None
        The function does not return any data but updates the graph with the computed 
        centrality values as node attributes, accessible via `G.nodes[node]['centrality']`.
        Also prints the top 5 nodes with the highest combined centrality scores.

    Notes
    -----
    - The combined centrality values are averaged and normalized between 0 and 1.
    - The `centrality` values are added as node attributes in the input graph.
    - Prints the names and combined centrality scores of the top 5 nodes with the highest scores.
    """
    centrality = (np.array(list(bet_centrality.values())) + np.array(list(closeness.values())) + np.array(list(katz.values()))) / 3
    centrality = centrality / centrality.max() # Normalize between 0 and 1
    centrality = dict(zip(list(G.nodes), centrality))
    nx.set_node_attributes(G, centrality, 'centrality')
    sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    
    for actor, c in sorted_centrality[:5]:
        print(G.nodes[actor]['Name'], 'has centrality: %.3f' %c)

def visualize_graph(G, output_path, colors=["#252A34", "#FF2E63", "#08D9D6"], k=None, alpha=1.0, node_shape='o'):
    """
    Visualizes the graph with node and edge attributes, saving the visualization to a file.

    The function generates a network visualization using a spring layout, where node sizes and 
    label font sizes are determined by the 'centrality' attribute. The graph is customized with 
    different colors for nodes, edges, and labels. The output is saved as an image file at the specified 
    path and also displayed.

    Parameters
    ----------
    G : networkx.Graph
        The input graph to be visualized.
    output_path : str
        The file path where the generated graph visualization image will be saved.
    colors : list of str, optional
        A list of three color codes used for node labels, edges, and nodes respectively. 
        Defaults to ["#252A34", "#FF2E63", "#08D9D6"].
    k : float, optional
        The optimal distance between nodes in the spring layout. If None, the default layout is used.
    alpha : float, optional
        The transparency level of the edges, where 1.0 is fully opaque. Defaults to 1.0.
    node_shape : str, optional
        The shape of the nodes in the visualization (e.g., 'o' for circles). Defaults to 'o'.

    Returns
    -------
    None
        The function does not return any data but saves the visualization to the specified file path 
        and displays it.
    
    Notes
    -----
    - Node sizes and label font sizes are scaled based on the 'centrality' attribute of the nodes.
    - The 'centrality' values also control the transparency of the nodes and labels.
    - The graph is saved as an image file to the given `output_path`.
    """
    fig = plt.figure(figsize=(19.2, 10.8))
    pos = nx.spring_layout(G, k=k)
    font_sizes = {actor_id:int(centrality*15) for actor_id, centrality in nx.get_node_attributes(G, 'centrality').items()}
    lab = nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'Name'),
                                 font_color=colors[0], font_size=font_sizes, alpha=nx.get_node_attributes(G, 'centrality'))
    ec = nx.draw_networkx_edges(G, pos, edge_color=colors[1], alpha=alpha)
    node_sizes = np.array(list(nx.get_node_attributes(G, 'centrality').values())) * 700
    nc = nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color=colors[2], node_shape=node_shape,
                               node_size=node_sizes, alpha=list(nx.get_node_attributes(G, 'centrality').values()))
    plt.axis('off')
    plt.savefig(output_path)
    plt.show()