import ast
import json
import os
import random
from collections import Counter, OrderedDict
from pathlib import Path
from copy import deepcopy

import community as community_louvain
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns


def set_random_seed(seed=1):
    np.random.seed(seed)
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def add_filter_metadata(f_filter):
    def f_filter_with_metadata(df, *args, **kwargs):
        args_list = list(map(str, args)) + [f"{k}={v}" for k, v in kwargs.items()]
        filter_metadata = f"{f_filter.__name__}({' '.join(args_list)})"
        if len(df.attrs) == 0:
            df.attrs = {"filter_metadata": []}
        df.attrs["filter_metadata"] = df.attrs["filter_metadata"] + [filter_metadata]
        return f_filter(df, *args, **kwargs)
    return f_filter_with_metadata


def read_json(fname):
    fname = Path(fname)
    with fname.open("rt") as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    fname = Path(fname)
    with fname.open("wt") as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


def write_communities(G, communities, fname):
    out = deepcopy(G.graph["filter_metadata"])
    out["data"] = communities
    write_json(out, fname)

def read_communities(G, fname):
    out_json = read_json(fname)
    assert out_json["movies_filter_metadata"] == G.graph["filter_metadata"]["movies_filter_metadata"], \
        f"Expected {out_json['movies_filter_metadata']}, got {G.graph['filter_metadata']['movies_filter_metadata']}"
    assert out_json["characters_filter_metadata"] == G.graph["filter_metadata"]["characters_filter_metadata"], \
        f"Expected {out_json['characters_filter_metadata']}, got {G.graph['filter_metadata']['characters_filter_metadata']}"
    return out_json["data"]



def plot_nan_distribution(df, table_name="", log_scale=False):
    df_nans = df.isnull().sum()

    if df_nans.values.max() == 0:
        print(f"There is no Nans in {table_name}")
        return None

    df_nans_sorted = pd.DataFrame(
        {"Column": df_nans.index, "MissingValues": df_nans.values}
    ).sort_values(by="MissingValues", ascending=False)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_nans_sorted, x="Column", y="MissingValues", color="skyblue")
    plt.title(f"Missing Values in {table_name} Table")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Number of Missing Values")
    if log_scale:
        plt.yscale("log")
    plt.tight_layout()
    plt.show()


@add_filter_metadata
def filter_by_country(df, country):
    df["CorrectCountry"] = df["Countries"].map(
        lambda x: country in ast.literal_eval(x).values()
    )
    df = df[df["CorrectCountry"] == True].copy()
    df = df.drop(columns=["CorrectCountry"])
    return df

def filter_by_genre(df, genre):
    df["CorrectGenre"] = df["Genres"].map(
        lambda x: genre in ast.literal_eval(x).values()
    )
    df = df[df["CorrectGenre"] == True].copy()
    df = df.drop(columns=["CorrectGenre"])
    return df

@add_filter_metadata
def drop_nans_subset(df, subset):
    return df.dropna(subset=subset).copy()


@add_filter_metadata
def drop_nans(df, column):
    return df[df[column].notnull()].copy()


def get_language_distribution(df, table_name, limit=None):
    counter = Counter()
    for i in range(df.shape[0]):
        languages = ast.literal_eval(df.iloc[i].Languages).values()
        counter.update(languages)

    counter_list = counter.most_common(limit)
    language_list, count_list = zip(*counter_list)
    plt.figure(figsize=(10, 5))
    index = np.arange(len(counter_list))
    plt.bar(index, height=count_list)
    plt.title(f"Top-{limit} Languages in the {table_name} table")
    plt.xticks(index, language_list, rotation=45, ha="right")
    plt.ylabel("Counts in log scale")
    plt.yscale("log")
    plt.xlabel("Language")
    plt.tight_layout()
    plt.show()

    ratio = count_list[0] / df.shape[0] * 100
    ratio = round(ratio, 2)
    print(f"The top-1 language is in {ratio}% of the movies")

@add_filter_metadata
def filter_by_language(df, language):
    df["CorrectLanguage"] = df["Languages"].map(
        lambda x: language in ast.literal_eval(x).values()
    )
    df = df[df["CorrectLanguage"] == True].copy()
    df = df.drop(columns=["CorrectLanguage"])
    return df

@add_filter_metadata
def fix_date(df, column):
    df[column] = pd.to_datetime(df[column], format="mixed", errors="coerce")
    return df.copy()


def plot_decade_distribution(df, table_name):
    df["Year"] = df["ReleaseDate"].dt.year
    df["Decade"] = ((df["Year"] // 10) * 10).astype(int)

    df_decade = df.groupby("Decade").size()

    plt.figure(figsize=(8, 5))
    df_decade.plot(kind="barh", color="yellow")
    plt.title(f"Number of {table_name} by Decade", fontsize=16)
    plt.xlabel("Total number", fontsize=12)
    plt.ylabel("Decade", fontsize=12)

    plt.tight_layout()
    plt.show()


def plot_revenue_distribution(df, table_name):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="Revenue")
    plt.title(f"Box Office Revenue Distribution for {table_name} Table")
    plt.xlabel("Revenue")
    plt.xscale("log")
    plt.show()


def plot_top_genres(df, table_name, limit=None):
    counter = Counter()
    for i in range(df.shape[0]):
        genres = ast.literal_eval(df.iloc[i].Genres).values()
        counter.update(genres)

    counter_list = counter.most_common(limit)
    language_list, count_list = zip(*counter_list)
    plt.figure(figsize=(10, 5))
    index = np.arange(len(counter_list))
    plt.bar(index, height=count_list)
    plt.title(f"Top-{limit} Genre in the {table_name} table")
    plt.xticks(index, language_list, rotation=45, ha="right")
    plt.ylabel("Counts in log scale")
    plt.yscale("log")
    plt.xlabel("Genre")
    plt.tight_layout()
    plt.show()


def merge_movies_and_actors(movies, characters):
    res = pd.merge(
        movies, characters, on="WikipediaId", how="inner", suffixes=("", "_duplicate")
    )
    res = res[list(set(movies.columns.tolist() + characters.columns.tolist()))]
    res.attrs["movies_filter_metadata"] = movies.attrs.get("filter_metadata", [])
    res.attrs["characters_filter_metadata"] = characters.attrs.get("filter_metadata", [])
    return res.copy()


def create_graph_from_data(movies_and_characters):
    G = nx.Graph()
    for movie_actors in movies_and_characters.groupby("FreebaseId")[
        "FreebaseActorId"
    ].unique():
        for actor_l in movie_actors:
            for actor_r in movie_actors:
                if (
                    actor_l is not np.nan
                    and actor_r is not np.nan
                    and actor_l < actor_r
                ):
                    G.add_edge(actor_l, actor_r)
            G.add_node(actor_l)  # to add nodes without friends
    G.graph["filter_metadata"] = movies_and_characters.attrs
    return G


def get_connected_components(G):
    return nx.connected_components(G)


def get_communities(G, seed=1):
    # Detect communities
    partition = community_louvain.best_partition(G, random_state=seed)

    communities = {}
    for node, comm_id in partition.items():
        communities.setdefault(comm_id, []).append(node)
    communities = communities.values()

    return list(communities)


def calculate_partition_quality(
    G, communities, movies, characters_movies, take_film_fraction
):
    actor_cnt_in_film = characters_movies.groupby("FreebaseId")[
        "FreebaseActorId"
    ].count()

    df_partition_top_movie_info = None
    dict_parition_info = {
        "PartitionIndex": [],
        "Size": [],
        "Ethnicity": [],
        "NaN Ethnicity Percent": [],
    }
    communities_srt = sorted(list(communities), key=lambda x: len(x), reverse=True)
    coverage, performance = nx.community.partition_quality(G, communities_srt)
    print(f"The performance (partition quality) metric is {performance}")
    print(f"The coverage (partition quality) metric is {coverage}")

    for parition_index, community in enumerate(communities_srt):
        community = list(community)
        dict_parition_info["PartitionIndex"].append(parition_index)
        dict_parition_info["Size"].append(len(community))

        popular_film_candidates = (
            characters_movies[characters_movies["FreebaseActorId"].isin(community)]
            .groupby("FreebaseId")
            .count()["FreebaseActorId"]
        )
        popular_film_fraction = (
            popular_film_candidates
            / actor_cnt_in_film.loc[popular_film_candidates.index]
        )
        popular_film_fraction = popular_film_fraction.sort_values(ascending=False)

        # print(f'For partition {parition_index}, size {len(community)} taking fraction {(popular_film_fraction > TAKE_FILM_FRACTION).sum() / popular_film_fraction.shape[0]}')

        popular_film_data = movies[
            movies["FreebaseId"].isin(
                popular_film_fraction[
                    (popular_film_fraction > take_film_fraction)
                ].index
            )
        ]

        popular_film_data_copy = popular_film_data.copy()
        popular_film_data_copy["PartitionIndex"] = parition_index
        if df_partition_top_movie_info is None:
            df_partition_top_movie_info = popular_film_data_copy
        else:
            df_partition_top_movie_info = pd.concat(
                [df_partition_top_movie_info, popular_film_data_copy], ignore_index=True
            )
    df_partition_top_movie_info = df_partition_top_movie_info.sort_values(
        by="PartitionIndex"
    )
    return df_partition_top_movie_info


def plot_partition_year_std_distribution(df):
    plt.figure(figsize=(8, 4))
    stds = []
    for partition_index, partition in df.groupby("PartitionIndex"):
        std = partition["Year"].std()
        stds.append(std)
    plt.hist(
        stds,
        bins=15,
    )
    plt.title("Histogram of stds for the partitions and corresponding movie years")
    plt.ylabel("Count")
    plt.xlabel("Standard Deviation of the movie release year")
    plt.show()
