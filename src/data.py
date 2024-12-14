import os
import shutil
from pathlib import Path

import pandas as pd
import wget

URL = {
    "dataset": "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz",
    "readme": "http://www.cs.cmu.edu/~ark/personas/data/README.txt",
}

ROOT_PATH = Path(__file__).absolute().resolve().parent.parent
DATA_PATH = ROOT_PATH / "data" / "cmu"
AWARD_PATH = ROOT_PATH / "data" / "awards"


def download_data(force_download=False):
    if not DATA_PATH.exists() or force_download:
        DATA_PATH.mkdir(exist_ok=True, parents=True)

        wget.download(URL["readme"], str(DATA_PATH / "README.txt"))
        wget.download(URL["dataset"], str(DATA_PATH / "MovieSummaries.tar.gz"))

        shutil.unpack_archive(str(DATA_PATH / "MovieSummaries.tar.gz"), str(DATA_PATH))
        os.remove(str(DATA_PATH / "MovieSummaries.tar.gz"))


def load_awards():
    """
    Load the movie awards dataset.
    Assumes the awards data contains 'FreebaseMovieId', 'Awards', and 'Nominations' columns.

    Args:
    - file_path (str): Path to the awards dataset.

    Returns:
    - DataFrame: Pandas DataFrame containing the awards data.
    """
    awards = pd.read_csv(AWARD_PATH / "awards_actors.tsv", sep="\t")
    return awards


def load_nominations():
    """
    Load the movie nominations dataset, assuming it has columns: 'freebase_ids' and 'nominations' (comma-separated nominations).

    Args:
    - file_path (str): Path to the nominations dataset.

    Returns:S
    - DataFrame: Pandas DataFrame containing the nominations data.
    """
    nominations = pd.read_csv(AWARD_PATH / "nominations_actors.tsv", sep="\t")
    return nominations


def load_plots():
    """Returns a pandas DataFrame containing plot summaries."""
    plots = pd.read_csv(
        DATA_PATH / "MovieSummaries" / "plot_summaries.txt",
        sep="\t",
        names=["WikipediaId", "PlotSummary"],
    )
    return plots


def load_movies():
    """Returns a pandas DataFrame containing movies metadata."""
    movies = pd.read_csv(
        DATA_PATH / "MovieSummaries" / "movie.metadata.tsv",
        sep="\t",
        names=[
            "WikipediaId",
            "FreebaseId",
            "MovieName",
            "ReleaseDate",
            "Revenue",
            "Runtime",
            "Languages",
            "Countries",
            "Genres",
        ],
    )
    return movies


def load_movies_and_plots():
    """Returns a pandas DataFrame containing movies metadata and plot summaries merged in one table."""
    movies = load_movies()
    plots = load_plots()
    movies = pd.merge(movies, plots, on="WikipediaId", how="inner")
    return movies


def load_characters():
    """Returns a pandas DataFrame containing characters metadata."""
    characters = pd.read_csv(
        DATA_PATH / "MovieSummaries" / "character.metadata.tsv",
        sep="\t",
        names=[
            "WikipediaId",
            "FreebaseId",
            "ReleaseDate",
            "CharacterName",
            "ActorDateOfBirth",
            "ActorGender",
            "ActorHeight",
            "ActorEthnicity",
            "ActorName",
            "ActorAgeAtRelease",
            "FreebaseCharacterActorMapId",
            "FreebaseCharId",
            "FreebaseActorId",
        ],
    )
    return characters
