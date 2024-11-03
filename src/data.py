import os
import shutil
from pathlib import Path

import wget

URL = {
    "dataset": "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz",
    "readme": "http://www.cs.cmu.edu/~ark/personas/data/README.txt",
}

ROOT_PATH = Path(__file__).absolute().resolve().parent.parent
DATA_PATH = ROOT_PATH / "data" / "cmu"


def download_data(force_download=False):
    if not DATA_PATH.exists() or force_download:
        DATA_PATH.mkdir(exist_ok=True, parents=True)

        wget.download(URL["readme"], str(DATA_PATH / "README.txt"))
        wget.download(URL["dataset"], str(DATA_PATH / "MovieSummaries.tar.gz"))

        shutil.unpack_archive(str(DATA_PATH / "MovieSummaries.tar.gz"), str(DATA_PATH))
        os.remove(str(DATA_PATH / "MovieSummaries.tar.gz"))
