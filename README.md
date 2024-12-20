# EPFL ADA 2024, Project-2, Team d2ptm

<p align="center"><big>
<b>Topic:</b> The impact of actors' friendships on their career
</big>
</p>

<p align="center">
  <a href="#abstract">Abstract</a> •
  <a href="#research-questions">Research Questions</a> •
  <a href="#methodology">Methodology</a> •
  <a href="#team-organization">Team Organization</a> •
  <a href="#proposed-timeline">Proposed Timeline</a> •
  <a href="#references">References</a> •
  <a href="#installation">Installation</a> •
  <a href="#project-structure">Project Structure</a>
</p>

## Datastory
Available at:
https://epfl-ada.github.io/ada-2024-project-d2ptm/

## Abstract

In today’s competitive job market, leveraging professional networks is crucial for securing top-tier positions.
But does the same apply to movie actors, where education might not play such a significant role?
To explore this, we examine whether an actor’s professional community shapes their success.
We build a graph where vertices represent actors, and edges connect those who have appeared in a movie together, **symbolizing a "friendship" between them**.
By clustering actors into communities, we investigate the role of friendships in shaping career trajectories.
Our analysis focuses on the U.S. movies but extends to films from other countries to determine if the conclusions are universal.
This study aims to reveal whether an actor’s community significantly impacts their career outcomes and how friendship patterns vary across time and countries.

## Research Questions

The topic of our research is: **does actor's friendships have and impact on his or her career?**

We will focus on the movies created in the USA.

To answer this question, we investigate the following sub-questions:

1. **Awards.** What are the chances that an actor gets an award?
   - Are awarded actors usually together in the same cluster? This means that either a cluster has many actors with awards or none.
2. **Revenue.** What is the influence of a community on the movie revenue?
   - _Deep Analysis of the top cluster_. What are the groups with the most financial success (e.g. highest average revenue / highest total revenue) and what are their characteristics?
   - _Cluster comparison analysis_. Do certain types of actor clusters (e.g., clusters featuring actors from diverse genres etc.) correlate with higher or lower revenues?
3. **Total Success.** Are the groups with the most awards (or nominations) also the groups with the highest revenue?

4. **Central Nodes.** Are there key actors (central nodes) whose presence significantly impacts the connectivity and composition of clusters?

5. **Time.** How do clusters evolve over time?
   - From which to which year has the cluster existed? Are clusters “compact” in time?
   - Do the characteristics of the leading actor group evolve over time?

While answering these questions provides a comprehensive analysis for the American movies, we want to understand how likely the same conclusions will hold for other countries.
Therefore, we will compare the clusters from the USA with the clusters from another country, e.g. India:

6. **Country-wise comparison**
   - Do the clusters have a significant distribution difference between these two countries (e.g., tend to be much smaller/bigger in size)?
   - What are the differences between top-one (revenue-wise) cluster for these countries in terms of distributions (age, genres, etc.)?

## Methods

### Datasets and pre-processing

Our primary dataset is the CMU Movie Summary Corpus [[1]](#cmu_dataset). It contains 81741 movies with their Wikipedia-based plot summaries and Freebase-based metadata, including revenue, genre, release data, runtime, language, country of origin, and information about movie characters and corresponding actors (date of birth, age, height, ethnicity, and gender).

During data pre-processing, we discovered that only about 20% of the U.S. movies in the dataset have revenue details.
We keep only movies that are in English because they represent the majority of the U.S. movies and other languages could be considered as outliers for our analysis.

To answer the awards-related questions, we supplement this dataset with the information from Wikidata obtained via our [SPARQL scrapping algorithm](scrape_awards.py) and actors' FreebaseID from the CMU movie dataset. We scrape both the awards and the nominations. We focus on the USA-related awards.

We cleaned the data by removing NaNs and fixing date format as described in the [notebook](results.ipynb).

For the main analysis, we will focus on the USA subset of this dataset, resulting in 6694 movies and 30379 actors after cleaning the data.

### Partitioning Methodology

#### Films Selection

As already mentioned, we will focus on the U.S. part of the dataset. We will select movies that have `United States of America` in countries. If we take all the films with this property, we might end up having films whose main production country is not the U.S., but that were partially filmed in the U.S. So we additionally select only films with `English Language` in languages (though it may not exclude British movies shot in the USA, this is a good heuristic for the given dataset). Besides, we filter out films that have `NaN`s in `Revenue` or `ReleaseDate`.

#### Graph Construction

For each selected movie, we add an edge between any two actors of the movie. So the vertices in the graph are actors and there is an edge $\Leftrightarrow$ there is a movie with both of these actors.

#### Partitioning Algorithm

We use the Louvain algorithm [[2]](https://arxiv.org/pdf/0803.0476) to construct partitions. In comparative community detection studies, this algorithm is one of the top in terms of speed and quality of partitions [[3]](https://arxiv.org/pdf/0908.1062).

#### Films Corresponding to Partitions

After running the partition algorithm, we get the clusters for actors, but using only actors, we will lose the information coming from movies like revenue and genres.

To use the movie information in the actor clusters, we assign each cluster some set of movies. To do the assignment, we fix the `SELECTION_THRESHOLD` hyperparameter, then for each cluster assign all movies that have more `SELECTION_THRESHOLD`$\%$ of actors in this cluster.

We experimented with values `SELECTION_THRESHOLD` (0 or 50).

`SELECTION_THRESHOLD` $= 0$ means that each cluster will have all the movies where at least one of the actors in the cluster participated.

`SELECTION_THRESHOLD` $= 50$ means that each cluster will have all the movies that have the most part of the cast in the cluster. In contrast to the `SELECTION_THRESHOLD` $= 0$ case, we will have that each movie can belong to at most one cluster.

With the `SELECTION_THRESHOLD` $= 0$, we get more movies in clusters than for `SELECTION_THRESHOLD` $= 50$, but they can be less related to the cluster.

The determination of the right value of hyperparameter is the future direction of our work.

#### Quality Check

To check the clustering quality numerically we use `coverage` and `partition` metrics, see the [notebook](results.ipynb) for more info on them.

We also calculate some statistics and provide some assumptions for the verification of clustering quality. See the [notebook](results.ipynb) for more details.

## Team organization

Each member will focus on answering one of the above research questions:

- Research question 1: Petr Grinberg
- Research question 2: Paul Guillon
- Research question 3, 6: Maksim Vasiliev
- Research question 4: Daniil Pyatko
- Research question 5: Tymur Tytarenko

## Proposed timeline

- 15/11 - 29/11: Homework 2
- 30/11 - 13/12: Answer research questions individually
- 14/12 - 20/12: Create datastory/website together

## References

1. <a id="cmu_dataset"></a> Bamman, D., O’Connor, B., & Smith, N. A. (2013, August). Learning latent personas of film characters. In Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (pp. 352-361).
2. <a id="louvain_algorithm"></a> Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of statistical mechanics: theory and experiment, 2008(10), P10008.
3. <a id="cluster_quality_metric"></a> Fortunato, S. (2010). Community detection in graphs. Physics reports, 486(3-5), 75-174.

# Installation

Follow these steps for the installation:

0. (Optional) Create and activate new environment using [`conda`](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) or `venv` ([`+pyenv`](https://github.com/pyenv/pyenv)). Python should be `3.10+`.

   a. `conda` version:

   ```bash
   # create env
   conda create -n project_env python=PYTHON_VERSION

   # activate env
   conda activate project_env
   ```

   b. `venv` (`+pyenv`) version:

   ```bash
   # create env
   ~/.pyenv/versions/PYTHON_VERSION/bin/python3 -m venv project_env

   # alternatively, using default python version
   python3 -m venv project_env

   # activate env
   source project_env
   ```

1. Install all required packages

   ```bash
   pip install -r requirements.txt
   ```

The dataset will be downloaded in the [notebook](results.ipynb) automatically.

# Project Structure

The structure of the code is as follows:

```
.
├── data  # the dir with all the datasets
│   ├── awards # the scraped awards obtained via our script
│   │   ├── awards_actors.tsv
│   │   ├── awards_movies.tsv
│   │   ├── nominations_actors.tsv
│   │   └── nominations_movies.tsv
│   └── cmu # CMU dataset (downloaded in the notebook)
│       ├── MovieSummaries
│       │   ├── character.metadata.tsv
│       │   ├── movie.metadata.tsv
│       │   ├── name.clusters.txt
│       │   ├── plot_summaries.txt
│       │   ├── README.txt
│       │   └── tvtropes.clusters.txt
│       └── README.txt
├── README.md # this file
├── requirements.txt # required packages
├── results.ipynb # main notebook
└── src # all the code
    ├── data.py # data loading code
    ├── __init__.py
    ├── scripts # scripts
    │   ├── __init__.py
    │   └── scrape_awards.py # script for obtaining the awards dataset
    └── utils # some utils
        ├── actors.py # utils for actors' stats
        ├── graphs.py # utils for cluster stats
        ├── helpers.py # additional helpers for plotting and cleaning
        ├── __init__.py
```
