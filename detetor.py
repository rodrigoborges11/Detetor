from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import numpy as num

_url = "https://query.wikidata.org/sparql"

query = """SELECT ?car ?carLabel ?manufacturer ?manufacturerLabel
WHERE {
  ?car wdt:P31 wd:Q1420.          # instâncias de automóvel
  ?car wdt:P176 ?manufacturer.     # fabricante
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 300
"""

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(_url, query)


data = []
for r in results["results"]["bindings"]:
    car = r["carLabel"]["value"]
    manufacturer = r.get("manufacturerLabel", {}).get("value", "Unknown")
    data.append((car, "manufacturer", manufacturer))


df = pd.DataFrame(data, columns=["head", "relation", "tail"])
df.to_csv("wikidata_car_triples.csv", index=False)
print("CSV saved!")


