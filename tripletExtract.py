from rdflib import Graph, Namespace, URIRef, RDF, RDFS, OWL

# Namespaces
NELL = Namespace("http://nell-995.org/")
g = Graph()
g.bind("nell", NELL)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)

# Define a generic entity class
g.add((NELL.Entity, RDF.type, OWL.Class))

# Helper function for URI cleaning
def clean_uri(text):
    return text.replace("concept:", "").replace(":", "_").replace("/", "_")

path = "kb_env_rl.txt"
i=0
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            subject, obj, relation = parts  # predicate = 3rd column
            s = URIRef(f"{NELL}{clean_uri(subject)}")
            p = URIRef(f"{NELL}{clean_uri(relation)}")
            o = URIRef(f"{NELL}{clean_uri(obj)}")

            # Add the triple itself
            g.add((s, p, o))

            # Add class and property semantics
            g.add((p, RDF.type, OWL.ObjectProperty))
            g.add((s, RDF.type, NELL.Entity))
            g.add((o, RDF.type, NELL.Entity))
            i+=1
            if i >=5000:
                break
print(f"✅ Created OWL ontology with {len(g)} triples")

# Serialize as OWL RDF/XML
g.serialize("nell995.owl", format="xml")
print("✅ Saved as nell995.owl (open in Protégé)")
