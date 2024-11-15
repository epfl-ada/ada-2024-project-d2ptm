from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from src.utils.actors import Cluster


class Graph:
    """
    A graph contains a list of clusters and offers various functions to
    compute and plot specific statistics about it.
    """

    def __init__(self, clusters):
        """
        Creates a Graph object.
        """
        self.clusters = clusters

    @staticmethod
    def init_from_list_of_lists(characters, movies, communities):
        clusters = []
        for community in communities:
            cluster = Cluster(characters=characters, movies=movies, actor_ids=community)
            clusters.append(cluster)
        return Graph(clusters)

    def age_distribution(self, plot=False):
        """
        Gets the distribution of mean ages at release across the clusters.
        Optionally, it can plot a histogram of the mean age distribution across the clusters.

        Parameters
        ----------
        plot : bool, optional
            If True, a histogram displaying the distribution of mean ages at release across clusters will be shown. Defaults to False.

        Returns
        -------
        list of float
            A list containing the mean age at release for each cluster in the graph.
        """
        means = [cluster.cluster_ages() for cluster in self.clusters]
        means = [np.nanmean(elem) for elem in means if len(elem) > 0]
        if plot:
            plt.hist(means)
            plt.title("Distribution of mean age at release accross clusters")
            plt.xlabel("Average age at release")
            plt.ylabel("Number of clusters")
            plt.show()
        return means

    def revenue_distribution(self, plot=False):
        """
        Calculates the distribution of mean revenue generated by actors across the clusters.
        Optionally, it can plot a histogram of the mean revenue distribution across the clusters.

        Parameters
        ----------
        plot : bool, optional
            If True, a histogram displaying the distribution of mean revenue across clusters will be shown. Defaults to False.

        Returns
        -------
        list of float
            A list containing the mean revenue for each cluster in the graph.
        """
        means = []
        for cluster in self.clusters:
            means.append(cluster.cluster_mean_revenue())
        if plot:
            plt.hist(means)
            plt.title("Distribution of mean revenue accross clusters")
            plt.xlabel("Average revenue generated by actors in the cluster")
            plt.ylabel("Number of clusters")
            plt.show()
        return means

    def gender_distribution(self, plot=False):
        """
        Calculates the gender distribution across the clusters.
        For each cluster, the proportion of female and male actors is determined.
        Optionally, it can plot a histogram of the proportion of female actors across clusters.

        Parameters
        ----------
        plot : bool, optional
            If True, a histogram displaying the distribution of female actor proportions across clusters will be shown. Defaults to False.

        Returns
        -------
        list of tuple
            A list of tuples, where each tuple contains:
            - The proportion of female actors (float) in a cluster.
            - The proportion of male actors (float) in the same cluster.
        """

        female_percentages = [cluster.cluster_genders()[0] for cluster in self.clusters]
        # remove -1 from nans
        female_percentages = list(filter(lambda x: x > -1, female_percentages))
        if plot:
            plt.hist(female_percentages)
            plt.title("Gender distribution accross clusters")
            plt.xlabel("Proportion of female actors")
            plt.ylabel("Number of clusters")
            plt.show()
        return [(p, 1 - p) for p in female_percentages]

    def size_distribution(self, plot=False, log=True, max_value=None):
        """
        Calculates the size distribution of the clusters.
        The size of each cluster is determined by the number of actors it contains.
        Optionally, it can plot a histogram of the cluster sizes.

        Parameters
        ----------
        plot : bool, optional
            If True, a histogram displaying the size distribution of
            clusters will be shown. Defaults to False.
        log: bool, optional
            If True, set yscale to log (Default True)
        max_value: int, optional
            If not None, limit the plot to the [0, max_value] range.
            Default to None.

        Returns
        -------
        list of int
            A list containing the sizes of the clusters, where each size represents
            the number of actors in a cluster.
        """
        sizes = [len(cluster.actor_ids) for cluster in self.clusters]
        if max_value is not None:
            sizes = list(filter(lambda x: x <= max_value, sizes))
        if plot:
            plt.hist(sizes)
            plt.title("Size distribution of clusters")
            plt.xlabel("Number of actors")
            plt.ylabel("Number of clusters")
            if log:
                plt.yscale("log")
            plt.show()
        return sizes

    def nth_genre_distribution(self, n, plot=False):
        """
        Calculates the distribution of the nth most preferred genre across the clusters.
        For each cluster, the nth most common genre is identified and counted.
        Optionally, it can plot a bar chart of the distribution.

        Parameters
        ----------
        n : int
            The rank of the genre to analyze (e.g., 1 for the most preferred genre, 2 for the second most preferred, etc.).

        plot : bool, optional
            If True, a bar chart displaying the distribution of the nth preferred genre across clusters will be shown.

        Returns
        -------
        dict
            A dictionary where keys are genres and values are the counts of clusters that have that genre as the nth most preferred,
            sorted in descending order of counts.
        """
        nth_genres = []
        index = n - 1
        for cluster in self.clusters:
            cluster_genres = list(cluster.cluster_genres().keys())
            if len(cluster_genres) > index:
                nth_genres.append(cluster_genres[index])
        nth_genres = dict(Counter(nth_genres).most_common())
        if plot:
            max_num_values = 40  # keep maximum 40 first genres for readability
            x = np.arange(min(len(nth_genres), max_num_values))
            figure = plt.figure(figsize=(10, 5))
            plt.bar(x, list(nth_genres.values())[:max_num_values])
            plt.xticks(
                x, list(nth_genres.keys())[:max_num_values], rotation=90, fontsize=8
            )
            suffix = "th"
            if n == 1:
                suffix = "st"
            elif n == 2:
                suffix = "nd"
            elif n == 3:
                suffix = "rd"
            plt.title(f"Distribution of {n}{suffix} prefered genre across clusters")
            plt.xlabel(f"{n}{suffix} prefered genre")
            plt.ylabel("Number of clusters")
            plt.show()
        return nth_genres
