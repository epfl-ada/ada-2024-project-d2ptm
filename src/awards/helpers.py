import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from src.utils.helpers import drop_nans, get_total_awards_or_nominations
from src.data import load_awards, load_nominations
from scipy.stats import spearmanr, pearsonr


def get_community_awards_statistics(communities, actor_awards):
    community_awards = {}
    for community_id, community_members in enumerate(communities):
        community_actors = actor_awards[actor_awards['FreebaseActorId'].isin(community_members)]
        total_awards_in_community = community_actors['TotalAwards'].sum()
        awarded_actors_in_community = len(community_actors[community_actors['TotalAwards'] > 0])
        total_actors_in_community = len(community_actors)

        community_awards[community_id] = {
            "total_actors": total_actors_in_community,
            "awarded_actors": awarded_actors_in_community,
            "total_awards": total_awards_in_community,
            "award_density": awarded_actors_in_community / total_actors_in_community if total_actors_in_community > 0 else 0,
        }

    community_sizes = [metrics['total_actors'] for metrics in community_awards.values()]
    award_densities = [metrics['award_density'] for metrics in community_awards.values()]

    high_award_density_clusters = [cid for cid, metrics in community_awards.items() if metrics['award_density'] > 0.8]
    low_award_density_clusters = [cid for cid, metrics in community_awards.items() if metrics['award_density'] < 0.2]

    print(f"Clusters with high award density (>80%): {len(high_award_density_clusters)}")
    print(f"Clusters with low award density (<20%): {len(low_award_density_clusters)}")

    average_award_density = np.mean(award_densities)
    print(f"Average award density across communities: {average_award_density:.2%}")

    return community_sizes, award_densities


def get_linreg_q1(community_sizes, award_densities, boundary):
    log_community_sizes = np.log(community_sizes)
    award_densities = np.array(award_densities)

    X = log_community_sizes.reshape(-1, 1)
    y = award_densities

    pos_indexes = log_community_sizes > np.log(boundary)

    model = LinearRegression()
    model.fit(X[pos_indexes], y[pos_indexes])

    predicted_award_densities = model.predict(X)
    r_squared = r2_score(y[pos_indexes], predicted_award_densities[pos_indexes])

    print(f"R2 score for the linreg fit: {r_squared}")
    return predicted_award_densities


def plot_community_awards_statistics(communities, actor_awards, boundary=20):
    community_sizes, award_densities = get_community_awards_statistics(communities,
                                                                        actor_awards)
    predicted_award_densities = get_linreg_q1(community_sizes, award_densities, boundary)
    community_sizes = np.array(community_sizes)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].scatter(community_sizes, award_densities, alpha=0.7, color="purple", label="Communities")
    axes[0].plot(community_sizes[community_sizes > boundary], predicted_award_densities[community_sizes > boundary],
                 color="orange", label="Linear Regression Line")
    axes[0].set_title("Community Size vs. Award/Nominations Density")
    axes[0].set_xlabel("Community Size (Number of Actors) (log scale)")
    axes[0].set_ylabel("Award/Nominations Density (Proportion of Awarded Actors)")
    axes[0].legend()
    axes[0].grid(True)
    axes[0].set_xscale("log")

    axes[1].boxplot([award_densities, np.array(award_densities)[community_sizes > boundary]], vert=False, patch_artist=True,
                    boxprops=dict(facecolor="skyblue", color="black"), labels=["Full", "Filtered"])
    axes[1].set_title("Box Plot of Award/Nominations Densities Across Communities")
    axes[1].set_xlabel("Proportion of Awarded Actors in Community")
    axes[1].grid(axis="x", linestyle="--", alpha=0.7)

    fig.tight_layout()
    plt.show()


def load_awards_and_nominations():
    # load the awards data
    actor_awards = load_awards()
    actor_awards = drop_nans(actor_awards, column="FreebaseActorId") # remove Nan id
    actor_awards['TotalAwards'] = get_total_awards_or_nominations(actor_awards, total_type="Awards")

    total_actors = len(actor_awards)
    awarded_actors = actor_awards[actor_awards['TotalAwards'] > 0]

    probability_award = len(awarded_actors) / total_actors
    print(f"Probability of an actor receiving an award: {probability_award:.2%}")

    actor_nominations = load_nominations()
    actor_nominations = drop_nans(actor_nominations, column="FreebaseActorId") # remove Nan id
    actor_nominations['TotalNominations'] = get_total_awards_or_nominations(actor_nominations, total_type="Nominations")

    nominated_actors = actor_nominations[actor_nominations['TotalNominations'] > 0]

    probability_nominations = len(nominated_actors) / total_actors
    print(f"Probability of an actor receiving nominations: {probability_nominations:.2%}")

    actor_full_awards = pd.merge(actor_nominations, actor_awards, how="inner", on="FreebaseActorId")
    actor_full_awards["TotalAwards"] = actor_full_awards["TotalAwards"] + actor_full_awards["TotalNominations"]

    award_nominated_actors = actor_full_awards[actor_full_awards['TotalAwards'] > 0]

    probability_award_nominations = len(award_nominated_actors) / total_actors
    print(f"Probability of an actor receiving award or nominations: {probability_award_nominations:.2%}")


    return actor_awards, actor_nominations, actor_full_awards


def compute_cluster_metrics_actors(communities, movies, characters_movies, actor_metrics):
    """
    Compute metrics for each community based on actor-level data:
    - Total revenue
    - Total actor awards and nominations
    - Number of actors in the community
    """
    cluster_metrics = {}

    for community_id, community_members in enumerate(communities):
        # Filter the actor for community
        community_actor_metrics = actor_metrics[actor_metrics.FreebaseActorId.isin(community_members)]

        # Calculate total awards/nominations
        # here TotalAwards is awards+nominations
        total_actor_awards = community_actor_metrics['TotalAwards'].sum()

        # Calculate total revenue based on movies
        community_movie_ids = characters_movies[characters_movies.FreebaseActorId.isin(community_members)].FreebaseId.unique()
        total_revenue = movies[movies.FreebaseId.isin(community_movie_ids)]['Revenue'].sum()
        total_revenue_in_billions = total_revenue / 1_000_000_000

        cluster_metrics[community_id] = {
            "total_revenue": float(f"{total_revenue_in_billions:.2f}"),
            "total_actor_awards": total_actor_awards,
            "num_actors": len(community_members)
        }

    return cluster_metrics


def get_linreg_q3(total_awards, total_revenue):

    X = np.array(total_awards).reshape(-1, 1)
    y = total_revenue

    model = LinearRegression()
    model.fit(X, y)

    predicted_revenue = model.predict(X)
    r_squared = r2_score(y, predicted_revenue)

    print(f"R2 score for the linreg fit: {r_squared}")
    return predicted_revenue


def plot_actors_award_nominations_revenue(communities, movies, characters_movies, actor_metrics):
    cluster_metrics_actor_awards = compute_cluster_metrics_actors(communities,
                                    movies, characters_movies, actor_metrics)

    total_revenues_actors = [metrics["total_revenue"] for metrics in cluster_metrics_actor_awards.values()]
    total_actor_awards = [metrics["total_actor_awards"] for metrics in cluster_metrics_actor_awards.values()]
    num_actors = [metrics["num_actors"] for metrics in cluster_metrics_actor_awards.values()]

    total_actor_awards = np.array(total_actor_awards)
    total_revenues_actors = np.array(total_revenues_actors)
    sort_index = np.argsort(total_actor_awards)
    total_revenues_actors = total_revenues_actors[sort_index]
    total_actor_awards = total_actor_awards[sort_index]

    predicted_revenue = get_linreg_q3(total_actor_awards, total_revenues_actors)

    plt.figure(figsize=(10, 6))
    plt.scatter(total_actor_awards, total_revenues_actors, alpha=0.7, color="purple", label="Communities")
    plt.plot(total_actor_awards, predicted_revenue, color="orange", label="Linear Regression Line")
    plt.title("Total Actor Awards/Nominations vs. Total Revenue (by Cluster)")
    plt.xlabel("Total Actor Awards/Nominations (log scale)")
    plt.ylabel("Total Revenue (in billions)")
    plt.xscale("log")
    plt.legend()
    plt.grid(True)
    plt.show()


    print("Spearman correlation:", spearmanr(total_actor_awards, total_revenues_actors))
    print("Pearson correlation:", pearsonr(total_actor_awards, total_revenues_actors))