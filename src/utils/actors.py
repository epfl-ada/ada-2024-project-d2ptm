import ast
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from ..data import load_characters, load_movies
from ..utils.helpers import merge_movies_and_actors


class ActorStats:
    """
    Gives access to various functions about actors.
    """

    def __init__(self, characters, movies):
        """
        Creates an ActorStats object.

        Parameters
        ----------
        characters: pd.DataFrame
            Pre-processed table with characters metadata
        movies: pd.DataFrame
            Pre-processed table with movies metadata
        """
        self.characters = characters
        self.movies = movies

    def actor_name(self, actor_id):
        """
        Gets actor name.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        str
            actor name corresponding to actor ID
        """
        return self.characters[self.characters["FreebaseActorId"] == actor_id].iloc[0][
            "ActorName"
        ]

    def actor_movie_ids(self, actor_id):
        """
        Gets ids from all the movies that the actor played in.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        list
            a list of all movie ids that the actor played in
        """
        return (
            self.characters[self.characters["FreebaseActorId"] == actor_id][
                "WikipediaId"
            ]
            .dropna()
            .to_list()
        )

    def actor_movies(self, actor_id):
        """
        Gets all the movies that the actor played in.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        DataFrame
            a DataFrame containing metadata of all movies that the actor played in
        """
        movie_ids = self.actor_movie_ids(actor_id)
        return self.movies[self.movies["WikipediaId"].isin(movie_ids)]

    def actor_movie_names(self, actor_id):
        """
        Gets names of all the movies that the actor played in.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        list
            a list of all movie names that the actor played in
        """
        return self.actor_movies(actor_id)["MovieName"].dropna().to_list()

    def actor_mean_revenue(self, actor_id):
        """
        Gets mean revenue of all the movies that the actor played in.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        float64
            average revenue of the movies that the actor played in
        """
        return self.actor_movies(actor_id)["Revenue"].mean()

    def actor_total_revenue(self, actor_id):
        """
        Gets total revenue of all the movies that the actor played in.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        float64
            total revenue of the movies that the actor played in
        """
        return self.actor_movies(actor_id)["Revenue"].sum()

    def actor_movie_count(self, actor_id):
        """
        Gets number of movies that the actor played in.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        int
            number of movies that the actor played in
        """
        return self.actor_movies(actor_id).shape[0]

    def actor_genre_counts(self, actor_id):
        """
        Counts the number of times an actor played in each genre.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID

        Returns
        -------
        Counter
            dict like object where keys are genres and values are counts
        """
        return (
            self.actor_movies(actor_id)["Genres"]
            .apply(lambda genres: Counter(list(ast.literal_eval(genres).values())))
            .sum()
        )

    def actor_prefered_genres(self, actor_id, n):
        """
        Gets the most common genres for an actor.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID
        n: int
            Top n values to return

        Returns
        -------
        list
            list of name-count pairs
        """
        return self.actor_genre_counts(actor_id).most_common(n)

    def print_actor_stats(self, actor_id):
        """
        Prints some statistics about this actor.

        Parameters
        ----------
        actor_id : str
            Freebase actor ID
        """
        fav_genre, fav_genre_count = self.actor_prefered_genres(actor_id, 1)[0]
        print(f"Name: {self.actor_name(actor_id)}")
        print(f"  * Played in {self.actor_movie_count(actor_id)} movies.")
        print(f"  * Favourite genre: {fav_genre} ({fav_genre_count} movies).")
        print(
            f"  * Total movie revenues: {self.actor_total_revenue(actor_id):16,.0f}$."
        )
        print(
            f"  * Average movie revenue: {self.actor_mean_revenue(actor_id):15,.0f}$."
        )


class Cluster(ActorStats):
    """
    A cluster contains a list of actors and offers various functions to
    compute and plot specific statistics about it.
    """

    def __init__(self, characters, movies, actor_ids):
        """
        Creates a cluster given a list of Freebase actor IDs (as strings).
        """
        super().__init__(characters, movies)
        self.actor_ids = actor_ids
        self.movies_and_actors = merge_movies_and_actors(
            self.movies, characters[characters["FreebaseActorId"].isin(actor_ids)]
        )

    def __str__(self):
        """
        Returns a string representation of the actor IDs in this object.

        Returns
        -------
        str
            A string listing the actor IDs associated with this object.
        """
        return str(self.actor_ids)

    def cluster_mean_revenue(self):
        """
        Gets mean revenue generated by the actors in the cluster.

        Returns
        -------
        float64
            The mean revenue for the specified cluster.
        """
        return self.movies_and_actors.groupby("FreebaseActorId").Revenue.mean().mean()

    def cluster_median_revenue(self):
        """
        Gets median revenue generated by the actors in the cluster.

        Returns
        -------
        float64
            The median revenue for the specified cluster.
        """
        return self.movies_and_actors.groupby("FreebaseActorId").Revenue.median().median()

    def cluster_movies(self):
        """
        Gets all the movies where at least one actor of the cluster played in.

        Returns
        -------
        DataFrame
            a DataFrame containing metadata of all movies that the group of actors played in.
        """
        movie_ids = self.movies_and_actors["WikipediaId"].unique()
        return self.movies[self.movies["WikipediaId"].isin(movie_ids)]

    def cluster_actors(self):
        """
        Gets all the actor names in the cluster.

        Returns
        -------
        list
            a list of all the actor names in the cluster.
        """
        return sorted(list(self.movies_and_actors["ActorName"].unique()))

    def cluster_total_revenue(self):
        """
        Gets total revenue generated by a cluster.
        Each movie is only counted once even if several actors from the
        group played in the same movie.

        Returns
        -------
        float64
            The total revenue for the specified cluster.
        """
        return self.cluster_movies()["Revenue"].sum()

    def cluster_genders(self, plot=False, title="Gender proportions in this actor group"):
        """
        Calculates the percentage of female and male actors in the cluster.
        Optionally, it can plot a pie chart of the gender distribution in the cluster.

        Parameters
        ----------
            plot : bool, optional
                If True, a pie chart displaying the gender distribution is shown. Defaults to False.
            title : str, optional
                Title of the pie chart. Defaults to 'Gender proportions in this actor group'.

        Returns
        -------
            tuple: A tuple containing two float values:
                - female_percent (float): The percentage of female actors in the cluster.
                - male_percent (float): The percentage of male actors in the cluster.
        """
        # Only keep one movie per actor
        actors = self.characters[
            self.characters["FreebaseActorId"].isin(self.actor_ids)
        ].drop_duplicates(subset="FreebaseActorId")
        female_count = actors[actors["ActorGender"] == "F"].shape[0]
        male_count = actors[actors["ActorGender"] == "M"].shape[0]
        total = female_count + male_count
        if total > 0:  # may occur if there are Nans for this data
            female_percent = female_count / total
            male_percent = male_count / total
        else:
            female_percent = -1
            male_percent = -1
        if plot:
            plt.pie(
                [female_percent, male_percent],
                labels=["Female", "Male"],
                autopct="%1.1f%%",
            )
            plt.title(title)
            plt.show()
        return female_percent, male_percent

    def cluster_ages(self, plot=False, title="Age at release distribution in this actor group"):
        """
        Gets the ages of actors at the time of release for a cluster, for each of their roles.
        Optionally, it can plot a histogram of the age distribution across the cluster.

        Parameters
        ----------
        plot : bool, optional
            If True, a histogram displaying the age distribution at release will be shown. Defaults to False.
        title : str, optional
            Title of the histogram. Defaults to 'Age at release distribution in this actor group'.
        
        Returns
        -------
        list of float
            A list containing the ages of the actors at the time of release, for each of their roles.
        """
        roles = self.characters[self.characters["FreebaseActorId"].isin(self.actor_ids)]
        # Keep only positive and non NaN values
        ages = (
            roles[roles["ActorAgeAtRelease"] > 0]["ActorAgeAtRelease"]
            .dropna()
            .to_list()
        )
        if plot:
            plt.hist(ages)
            plt.title(title)
            plt.xlabel("Age at release")
            plt.ylabel("Count")
            plt.show()
        return ages

    def cluster_genres(self, plot=False):
        """
        Gets the genre distribution for movies within a specified cluster.
        Optionally, it can plot a bar chart of the genre distribution across the cluster.

        Parameters
        ----------
        plot : bool, optional
            If True, a bar chart displaying the genre distribution will be shown. Defaults to False.

        Returns
        -------
        dict
            A dictionary where keys are genres and values are the counts of movies within the cluster for each genre.
        """
        genres = (
            self.cluster_movies()["Genres"]
            .apply(lambda genres: Counter(list(ast.literal_eval(genres).values())))
            .sum()
        )
        # Sort by genres by count
        genres = {p[0]:p[1] for p in sorted(genres.items(), key=lambda pair: pair[1], reverse=True)}
        if plot:
            num_values = min(len(genres), 20)  # keep only 20 first genres for readability
            y = np.arange(num_values)
            figure = plt.figure(figsize=(10, 5))
            plt.barh(y, list(genres.values())[:num_values][::-1])
            plt.yticks(y, list(genres.keys())[:num_values][::-1], fontsize=8)
            plt.title("Genre distribution in this actor group")
            plt.xlabel("Movie count")
            plt.ylabel("Genre")
            plt.show()
        return genres

    def compare_genders_with(self, cluster2, titles, colors=["#FF2E63", "#08D9D6"]):
        """
        Compares the gender distributions of two clusters by displaying side-by-side pie charts.
    
        Parameters
        ----------
        cluster2 : object
            The second cluster to compare with the current cluster.
        titles : list of str
            A list of titles for the pie charts. The first title corresponds to the 
            current cluster, and the second title corresponds to the second cluster.
        colors : list of str, optional
            A list of two hexadecimal color codes used to represent the gender categories 
            in the pie charts. Defaults to ["#FF2E63" (Female), "#08D9D6" (Male)].
    
        Returns
        -------
        None
            Displays the pie charts but does not return any data.
        """
        cluster1 = self
        cluster1_males, cluster1_females = cluster1.cluster_genders()
        cluster2_males, cluster2_females = cluster2.cluster_genders()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        ax1.pie([cluster1_males, cluster1_females], colors=colors,
                labels=["Female", "Male"], autopct="%1.1f%%")
        ax1.set_xlabel(titles[0])
        ax2.pie([cluster2_males, cluster2_females], colors=colors,
                labels=["Female", "Male"], autopct="%1.1f%%")
        ax2.set_xlabel(titles[1])
        plt.show()

    def compare_ages_with(self, cluster2, labels, colors=["#FF2E63", "#08D9D6"]):
        """
        Compares the age distributions of two clusters by displaying overlapping histograms.
    
        Parameters
        ----------
        cluster2 : object
            The second cluster to compare with the current cluster.
        labels : list of str
            A list of labels for the histograms. The first label corresponds to the 
            current cluster, and the second label corresponds to the second cluster.
        colors : list of str, optional
            A list of two hexadecimal color codes used to represent the clusters in the histograms. 
            Defaults to ["#FF2E63", "#08D9D6"].
    
        Returns
        -------
        None
            Displays the histograms but does not return any data.
        """
        cluster1 = self
        cluster1_ages = cluster1.cluster_ages()
        cluster2_ages = cluster2.cluster_ages()
        plt.hist(cluster1_ages, alpha=0.5, label=labels[0], color=colors[0], density=True)
        plt.hist(cluster2_ages, alpha=0.5, label=labels[1], color=colors[1], density=True)
        plt.xlabel('Age')
        plt.ylabel('Normalized Frequency')
        plt.title('Age at release distribution')
        plt.legend()
        plt.show()