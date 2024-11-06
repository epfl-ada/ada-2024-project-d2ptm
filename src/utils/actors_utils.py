from ..data import load_characters
from ..data import load_movies
from collections import Counter
import ast

def get_actor_name(actor_id):
    """Gets actor name.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    str
        actor name corresponding to actor ID
    """
    characters = load_characters()
    return characters[characters["FreebaseActorId"] == actor_id].iloc[0]["ActorName"]

def get_actor_movie_ids(actor_id):
    """Gets ids from all the movies that the actor played in.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    list
        a list of all movie ids that the actor played in
    """
    characters = load_characters()
    return characters[characters["FreebaseActorId"] == actor_id]["WikipediaId"].to_list()


def get_actor_movies(actor_id):
    """Gets all the movies that the actor played in.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    DataFrame
        a DataFrame containing metadata of all movies that the actor played in
    """
    movie_ids = get_actor_movie_ids(actor_id)
    movies = load_movies()
    return movies[movies["WikipediaId"].isin(movie_ids)]


def get_actor_movie_names(actor_id):
    """Gets names of all the movies that the actor played in.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    list
        a list of all movie names that the actor played in
    """
    return get_actor_movies(actor_id)["MovieName"].to_list()


def actor_mean_revenue(actor_id):
    """Gets mean revenue of all the movies that the actor played in.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    float64
        average revenue of the movies that the actor played in
    """
    return get_actor_movies(actor_id)["Revenue"].mean()


def actor_total_revenue(actor_id):
    """Gets total revenue of all the movies that the actor played in.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    float64
        total revenue of the movies that the actor played in
    """
    return get_actor_movies(actor_id)["Revenue"].sum()


def actor_movie_count(actor_id):
    """Gets number of movies that the actor played in.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    int
        number of movies that the actor played in
    """
    return get_actor_movies(actor_id).shape[0]


def actor_genre_counts(actor_id):
    """Counts the number of times an actor played in each genre.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID

    Returns
    -------
    Counter
        dict like object where keys are genres and values are counts
    """
    return get_actor_movies(actor_id)["Genres"].apply(lambda genres: Counter(list(ast.literal_eval(genres).values()))).sum()


def actor_prefered_genres(actor_id, n):
    """Gets the most common genres for an actor.
    
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
    return actor_genre_counts(actor_id).most_common(n)


def print_actor_stats(actor_id):
    """Prints some statistics about this actor.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID
    """
    fav_genre, fav_genre_count = actor_prefered_genres(actor_id, 1)[0]
    print(f"Name: {get_actor_name(actor_id)}")
    print(f"  * Played in {actor_movie_count(actor_id)} movies.")
    print(f"  * Favourite genre: {fav_genre} ({fav_genre_count} movies).")
    print(f"  * Total movie revenues: {actor_total_revenue(actor_id):16,.0f}$.")
    print(f"  * Average movie revenue: {actor_mean_revenue(actor_id):15,.0f}$.")