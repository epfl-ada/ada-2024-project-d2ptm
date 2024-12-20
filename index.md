---
layout: article
title: The Impact of Actors' Connections on Their Career
header:
  theme: dark
  background: "linear-gradient(135deg, rgb(0, 0, 0), rgb(0, 0, 0))"
article_header:
  type: overlay
  theme: dark
  background_color: "#123"
  background_image: false
---

In today’s competitive job market, leveraging professional networks is crucial for securing top-tier positions. But does the same apply to movie actors, where education might not play such a significant role? To explore this, we examine whether an actor’s professional community shapes their success. We build a graph where vertices represent actors, and edges connect those who have appeared in a movie together, **symbolizing a "friendship" between them**. By clustering actors into communities, we investigate the role of friendships in shaping career trajectories. Our analysis focuses on the U.S. movies but extends to films from other countries to determine if the conclusions are universal. This study aims to reveal whether an actor’s community significantly impacts their career outcomes and how friendship patterns vary across time and countries.

---

# Starting our investigation

As in any research, we need some data to do analysis and base our conclusions on. For this study, we utilize [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/) that includes 81741 movies with their Wikipedia-based plot summaries and Freebase-based metadata, including revenue, genre, release data, runtime, language, country of origin, and information about movie characters and corresponding actors (date of birth, age, height, ethnicity, and gender).

The traditional career path of an actor can be different in different countries. To begin with, let's focus on the USA movies and their actors. By conducting analysis on a certain region, we ensure that the in-depth concepts and flows of actors' career are kept, hence, providing comprehensive analysis and meaningful conclusions. After filtering, we obtain 6923 movies to work on.

Before going into actors' analysis, let's look how our data is distributed.

ADD PLOTS About movies.

# Creating a Graph

Now that we have a full view on our data, we can connect it with the information about the actors. We want to investigate the impact of actors' connections and community on their career. How can we create a computational model for that?

Let's say that two actors are "friends" if they have a mutual movie. Then, we obtain a classical interpretation of a graph data and can use it as our computational model: vertices are defined by unique actor names and edges connect actors if they are friends (i.e., participated in the same movie).

TODO

## How can we ensure that our clustering is meaningful?

TODO add about verification

# Research Questions

## TODO

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
