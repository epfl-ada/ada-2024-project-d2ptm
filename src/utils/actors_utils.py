from ..data import load_characters
from ..data import load_movies

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


def print_actor_stats(actor_id):
    """Prints some statistics about this actor.
    
    Parameters
    ----------
    actor_id : str
        Freebase actor ID
    """
    print(f"Name: {get_actor_name(actor_id)}")
    print(f"  * Played in {actor_movie_count(actor_id)} movies.")
    print(f"  * Total movie revenues: {actor_total_revenue(actor_id):16,.0f}$.")
    print(f"  * Average movie revenue: {actor_mean_revenue(actor_id):15,.0f}$.")