import pickle
import time
from collections import defaultdict

import pandas as pd
from SPARQLWrapper import JSON, SPARQLExceptions, SPARQLWrapper
from tqdm import tqdm

from src.data import load_characters, load_movies


def awards_str_query(freebaseids_query):
    """
    Creates query to scrape awards
    """
    query = f"""
    SELECT ?s ?sLabel ?freebaseID ?awardLabel ?awardDate
    WHERE {{
    
    VALUES ?freebaseID {{ 
        {freebaseids_query}
    }}
    
    ?s wdt:P646 ?freebaseID .
    ?s wdt:P166 ?award .
    OPTIONAL {{ ?s p:P166 ?awardStatement .
               ?awardStatement ps:P166 ?award ;
                              pq:P585 ?awardDate . }}

    # Subquery to retrieve award labels
    ?award rdfs:label ?awardLabel .
    FILTER(LANG(?awardLabel) = "en")
    
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
    }}
    """
    return query


def nominations_str_query(freebaseids_query):
    """
    Creates query to scrape nominations
    """
    query = f"""
    SELECT ?s ?sLabel ?freebaseID ?nominationLabel ?nominationDate
    WHERE {{
    
    VALUES ?freebaseID {{ 
        {freebaseids_query}
    }}
    
    ?s wdt:P646 ?freebaseID .
    ?s wdt:P1411 ?nomination .
    OPTIONAL {{ ?s p:P1411 ?nominationStatement .
               ?nominationStatement ps:P1411 ?nomination ;
                              pq:P585 ?nominationDate . }}

    # Subquery to retrieve award labels
    ?nomination rdfs:label ?nominationLabel .
    FILTER(LANG(?nominationLabel) = "en")
    
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
    }}
    """
    return query


def make_query(query):
    """
    Send query to DB
    """
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return True, results
    except SPARQLExceptions.SPARQLWrapperException:
        print("stopped because timeout!")
        time.sleep(2 * 60)
        return False, None


def query_awards(freebaseids, query_f, label_name, query_dict):
    """
    Full pipeline for scraping and processing.
    """
    # if verbose:
    #    print(f'Couldn\'t find in cache, querying for {freebaseid}')
    time.sleep(0)

    freebaseids_query = " ".join(f'"{id}"' for id in freebaseids)
    freebase_id_set = set(freebaseids)
    removing_set = set()

    query = query_f(freebaseids_query)

    stopped = False
    results = None
    while not stopped:
        stopped, results = make_query(query)

    for ans_dict in results["results"]["bindings"]:
        name = ans_dict["freebaseID"]["value"]
        awards = ans_dict[label_name]["value"]
        query_dict[name].append(awards)
        removing_set.add(name)
    if len(results["results"]["bindings"]) > 300:
        length = len(results["results"]["bindings"])
        print(f"sleeping!: {length}")
        time.sleep(30)
    for name in freebase_id_set - removing_set:
        query_dict[name] = []


if __name__ == "__main__":

    name = "movies"

    if name == "movies":

        movies = load_movies()
        ids = movies.FreebaseId.unique()
    elif name == "actors":
        characters = load_characters()
        ids = characters.FreebaseActorId.unique()

    cache = defaultdict(list)

    k = 200
    w = (len(ids) + k - 1) // k
    for i in tqdm(range(w)):
        # if i % 50 == 0 and i != 0:
        #    time.sleep(30)
        # if i % 200 == 0 and i != 0:
        #    time.sleep(9 * 60)
        cur_ids = ids[i * k : (i + 1) * k]
        query_awards(cur_ids, nominations_str_query, "nominationLabel", cache)
        i += 1

    with open(f"nominations_{name}.pkl", "wb") as f:
        pickle.dump(cache, f)

    to_pandas_dict = defaultdict(dict)

    for i, (key, val) in enumerate(cache.items()):
        merged_val = ",".join(val)
        to_pandas_dict["freebase_ids"][i] = key
        to_pandas_dict["nominations"][i] = merged_val

    ds = pd.DataFrame.from_dict(to_pandas_dict)

    ds.to_csv(f"nominations_{name}.tsv", sep="\t")
