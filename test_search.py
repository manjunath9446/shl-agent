from app.retriever import search_assessments

query = "Java developer assessment"

results = search_assessments(query)

print("\nRESULTS:\n")

print(results)