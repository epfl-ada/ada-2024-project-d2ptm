from src.utils.helpers import filter_by_genre
from src.utils.helpers import filter_by_country, filter_by_genre, drop_nans, fix_date, filter_by_language, merge_movies_and_actors
from src.data import load_movies, load_characters

import matplotlib.pyplot as plt


def get_dataset_by_genre(genre):
    movies = load_movies()
    characters = load_characters()


    us_movies = filter_by_country(movies, country="United States of America")
    print("Number of US movies:", us_movies.shape[0])

    us_movies = drop_nans(us_movies, column="Revenue")
    us_movies = drop_nans(us_movies, column="ReleaseDate")
    us_movies = fix_date(us_movies, column="ReleaseDate")
    us_movies = filter_by_genre(us_movies, genre=genre)
    print("Number of US movies after dropping Nans:", us_movies.shape[0])
    us_movies = filter_by_language(us_movies, language="English Language")

    characters = drop_nans(characters, column="FreebaseActorId")

    us_characters_movies = merge_movies_and_actors(us_movies, characters)
    return us_characters_movies


def filter_name_by_dict(ds, storage):
    col = ds['MovieName'].apply(lambda x: x not in storage)
    return ds[col]


def draw_drama_vs_horror_by_revenue(total_drama_num_actors, total_drama_revenues, total_comedie_num_actors, total_comedie_revenues):
    plt.figure(figsize=(10, 6))
    plt.scatter(total_drama_num_actors, total_drama_revenues, alpha=0.7, marker='o', label='drama')
    plt.scatter(total_comedie_num_actors, total_comedie_revenues, alpha=0.7, marker='+', label='horror')

    plt.title("Total Number of Actors vs. Average Revenue (by Cluster)")
    plt.xlabel("Total Number of Actors")
    plt.ylabel("Average Revenue per Film (in billions)")
    plt.xscale("log")
    plt.grid(True)
    plt.legend()
    plt.show()