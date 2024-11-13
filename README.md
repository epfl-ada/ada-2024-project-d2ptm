# EPFL ADA 2024, Project-2, Team d2ptm

<p align="center"><big>
<b>Topic:</b> The impact of actors' collaborations on their career
</big>
</p>

<p align="center">
  <a href="#abstract">Abstract</a> •
  <a href="#research-questions">Research Questions</a> •
  <a href="#methodology">Methodology</a> •
  <a href="#proposed-timeline">Proposed Timeline</a> •
  <a href="#team-organization">Team Organization</a> •
  <a href="#references">References</a>
</p>

## Abstract

In the modern era of publicly available high-quality education and a consequent large number of professionals, getting a position in a top-tier company becomes more and more complicated. One way to improve your job search is to enrich your community and find "friends" in the companies that could refer you for a position. However, we wonder if this problem exists in the movie actors' profession, for which, the top-tier education might not be such an important factor to get an offer. We want to investigate whether the actor’s community defines his or her future and success in the profession. To do this, we define the graph of actors' collaborations: vertices are actors and an edge depends on the existence of a mutual movie for the corresponding actors. Then, we split the vertices into clusters, a.k.a. communities, and analyze them to answer different questions regarding the impact of the collaborations on actors’ success. While the main experiments are conducted on Hollywood subset of movies, we also compare clusters from different countries to see whether the conclusions still hold.

## Research Questions

The topic of our research is: **does actor's collaborations have and impact on his or her career?**

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

While answering these questions provides a comprehensive analysis for the USA movies, we want to understand how likely the same conclusions will hold for other countries. Therefore, we will compare the clusters from the USA with the clusters from another country, e.g. India:

- Do the clusters have a significant distribution difference between these two countries (e.g., tend to be much smaller/bigger in size)
- What are the differences between top-one (revenue-wise) cluster for these countries in terms of distributions (age, genres, etc.).

## Methodology

### Datasets and pre-processing

Our primary dataset is the CMU movie datasets [add reference]. TODO add description.

To answer the awards-related questions, we supplement this dataset with the following ones:

- Academy Awards: TODO
- Golden Globe Awards: TODO
- Emmy Awards: TODO

TODO_ADD_CLEANING_PROCESS_DESCRIPTION

For the main analysis, we will focus on the USA subset of this datasets, resulting in TODO_ADD_NUMBER movies and TODO actors after cleaning the data.

### Methodology

TODO

## Proposed timeline

TODO, mb merge with team organization.

## Team organization

The full list of authors and the assigned tasks for the Project-3 are presented below:

- TODO

## References

1. TODO_ADD_DATASETS_AND_ALGORITHMS_PAPERS
