import fire
import rdflib
import pandas as pd
from functools import lru_cache
import json


def get_expressions(namespace):
    namespace = check_if_namespace(namespace)
    df = download_data(namespace)
    new_melted_unique = process(df, namespace)
    save(df, new_melted_unique)


def check_if_namespace(namespace):
    if namespace[:7] == 'http://':
        return namespace
    elif ',' in namespace:
        potential_namespaces = namespace.split(',')
        for potential_namespace in potential_namespaces:
            if potential_namespace[:7] == 'http://':
                return potential_namespace
    else:
        raise Exception


@lru_cache(20)
def download_data(namespace: str) -> pd.DataFrame:
    g = rdflib.Graph()
    g.load(namespace)
    df = pd.DataFrame(
        [(s, p, o) for s, p, o in g],
        columns=['subject', 'predicate', 'object']
    )
    return df


def process(df, namespace):
    melted = df.melt()
    new_melted = melted[melted['value'].str.startswith(
        namespace)].drop_duplicates()
    new_melted_unique = new_melted.groupby('value').agg(lambda x: ', '.join(x))
    return new_melted_unique


def save(df, new_melted_unique):
    df.to_csv('/tmp/namespace.csv', header=None)
    new_melted_unique.to_csv('/tmp/namespace_unique.csv', header=None)


def get_all_namespaces():
    all_vocabs_raw = json.load(open('all_vocabs.json', 'r'))
    vocabs_res = all_vocabs_raw['results']['bindings']
    vocabs_relevant = [{
        'uri': vocab['vocabURI']['value'],
        'prefix': vocab['vocabPrefix']['value']
    } for vocab in vocabs_res]
    vocabs = pd.DataFrame(vocabs_relevant)
    vocabs = vocabs.set_index('prefix')
    vocabs.to_csv('/tmp/vocabs.csv')


if __name__ == "__main__":
    # namespace = 'http://dbpedia.org/ontology/'
    fire.Fire(get_expressions)
