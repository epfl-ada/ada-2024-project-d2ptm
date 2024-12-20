from src.utils.helpers import filter_by_genre
from src.utils.helpers import filter_by_country, filter_by_genre, drop_nans, fix_date, filter_by_language, merge_movies_and_actors
from src.data import load_movies, load_characters
from src.awards.helpers import get_linreg_q3


import matplotlib.pyplot as plt
import numpy as np


countries_langue = {
    'English': ('United States of America', 'English Language'),
    'French' : ('France', 'French Language'),
    'German': ('Germany', 'German Language'),
    'Spanish': ('Spain', 'Spanish Language'),
    'Chinese': ('Italy', 'Italian Language'),
    'Japanise': ('Japan', 'Japanese Language'),
    'Hindi': ('India', 'Hindi Language')  
}


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

    ax = plt.gca()
    ax.scatter(total_drama_num_actors, total_drama_revenues, alpha=0.7, marker='o', label='drama', color="orange")
    ax.scatter(total_comedie_num_actors, total_comedie_revenues, alpha=0.7, marker='+', label='horror', color="blue")


    predicted_revenue = get_linreg_q3(total_drama_num_actors, total_drama_revenues)
    sorted_idx = np.argsort(total_drama_num_actors)

    ax.plot(np.array(total_drama_num_actors)[sorted_idx], predicted_revenue[sorted_idx], color="orange", label="Linear Regression Line Drama")

    predicted_revenue = get_linreg_q3(total_comedie_num_actors, total_comedie_revenues)
    sorted_idx = np.argsort(total_comedie_num_actors)

    ax.plot(np.array(total_comedie_num_actors)[sorted_idx], predicted_revenue[sorted_idx], color="blue", label="Linear Regression Line Comedy")


    plt.title("Total Number of Actors vs. Average Revenue (by Cluster)")
    plt.xlabel("Total Number of Actors")
    plt.ylabel("Average Revenue per Film (in billions)")
    plt.xscale("log")
    plt.grid(True)
    plt.legend()
    plt.show()


def get_len_of_language(movies, country, language):
    countryMovies = filter_by_country(movies, country=country)
    countryMovies = drop_nans(countryMovies, column="Revenue")
    countryMovies = filter_by_language(countryMovies, language=language)
    return len(countryMovies)


def draw_movies_for_language(movies):
    storage = {}
    for key in countries_langue:
        country, langue = countries_langue[key]
        len_of_countries = get_len_of_language(movies, country, langue)
        storage[key] = len_of_countries
    names = list(storage)
    vals = [storage[key] for key in storage]
    sorted_ind = np.argsort(vals)
    sorted_vals = [vals[ind] for ind in reversed(sorted_ind)]
    sorted_names = [names[ind] for ind in reversed(sorted_ind)]

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_names, sorted_vals, alpha=0.7, color="orange")
    plt.title("Total number of movies with revenue vs language")
    plt.xlabel("Languages of the movies")
    plt.ylabel("Total number of movies with revenue")
    plt.yscale("log")
    plt.grid(True)
    plt.show()