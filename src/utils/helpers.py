import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from collections import Counter
import numpy as np

def plot_nan_distribution(df, table_name=""):
    df_nans = df.isnull().sum()

    if df_nans.values.max() == 0:
        print(f"There is no Nans in {table_name}")
        return None

    df_nans_sorted = pd.DataFrame({
            'Column': df_nans.index,
            'MissingValues': df_nans.values
    }).sort_values(by='MissingValues', ascending=False)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_nans_sorted, x='Column', y='MissingValues', color='skyblue')
    plt.title(f"Missing Values in {table_name} Table")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Number of Missing Values")
    plt.tight_layout()
    plt.show()


def filter_by_country(df, country):
    df["CorrectCountry"] = df["Countries"].map(lambda x: country in ast.literal_eval(x).values())
    df = df[df["CorrectCountry"] == True].copy()
    df = df.drop(columns=["CorrectCountry"])
    return df

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
    plt.xticks(index, language_list, rotation=45, ha='right')
    plt.ylabel("Counts in log scale")
    plt.yscale("log")
    plt.xlabel("Language")
    plt.tight_layout()
    plt.show()

    ratio = count_list[0] / df.shape[0] * 100
    ratio = round(ratio, 2)
    print(f"The top-1 language is in {ratio}% of the movies") 


def filter_by_language(df, language):
    df["CorrectLanguage"] = df["Languages"].map(lambda x: language in ast.literal_eval(x).values())
    df = df[df["CorrectLanguage"] == True].copy()
    df = df.drop(columns=["CorrectLanguage"])
    return df


def fix_date(df, column):
    df[column] = pd.to_datetime(df[column], format="mixed", errors='coerce')
    return df.copy()


def plot_decade_distribution(df, table_name):
    df['Year'] = df['ReleaseDate'].dt.year
    df['Decade'] = ((df['Year'] // 10) * 10).astype(int)

    df_decade = df.groupby('Decade').size()

    plt.figure(figsize=(8,5))
    df_decade.sort_values(ascending=True).plot(kind='barh', color='yellow')
    plt.title(f'Number of {table_name} by Decade', fontsize=16)
    plt.xlabel('Total number', fontsize=12)
    plt.ylabel('Decade', fontsize=12)

    plt.tight_layout()
    plt.show()



def plot_revenue_distribution(df, table_name):
    plt.figure(figsize=(8,5))
    sns.boxplot(data=df, x='Revenue')
    plt.title(f'Box Office Revenue Distribution for {table_name} Table')
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
    plt.xticks(index, language_list, rotation=45, ha='right')
    plt.ylabel("Counts in log scale")
    plt.yscale("log")
    plt.xlabel("Genre")
    plt.tight_layout()
    plt.show()


def merge_movies_and_actors(movies, characters):
    return pd.merge(movies, characters, on="WikipediaId", how="inner")