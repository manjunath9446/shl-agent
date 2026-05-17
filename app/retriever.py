# ==========================================
# app/retriever.py
# ==========================================

# Lightweight retrieval layer
# optimized for stable deployment

import chromadb

from app.query_expansion import (
    expand_query_with_llm
)


# ==========================================
# CHROMADB CLIENT
# ==========================================

# Persistent vector database
# for SHL assessment catalog

client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=chromadb.Settings(
        anonymized_telemetry=False
    )
)


# ==========================================
# LIGHTWEIGHT COLLECTION SETUP
# ==========================================

# Avoids heavy SentenceTransformer
# loading during Render startup

collection = client.get_or_create_collection(
    name="shl_assessments"
)

print(
    "\nChromaDB collection ready"
)


# ==========================================
# GET COLLECTION
# ==========================================

# Returns active collection

def get_collection():

    return collection


# ==========================================
# FORMAT RESULTS
# ==========================================

# Converts raw ChromaDB output
# into structured response format

def format_results(results):

    formatted_results = []

    metadatas = (
        results.get("metadatas", [[]])[0]
    )

    documents = (
        results.get("documents", [[]])[0]
    )

    distances = (
        results.get("distances", [[]])[0]
    )

    for idx, item in enumerate(metadatas):

        formatted_results.append({

            "name":
                item.get("name", ""),

            "url":
                item.get("url", ""),

            "test_type":
                item.get(
                    "test_type",
                    "Unknown"
                ),

            "description":
                documents[idx]
                if idx < len(documents)
                else "",

            "score":
                distances[idx]
                if idx < len(distances)
                else 999
        })

    return formatted_results


# ==========================================
# FALLBACK KEYWORD RETRIEVAL
# ==========================================

# Lightweight retrieval fallback
# for deployment-safe querying

def keyword_match_score(
    query,
    text
):

    query_words = (
        query.lower().split()
    )

    text_lower = text.lower()

    score = 0

    for word in query_words:

        if word in text_lower:

            score += 1

    return score


# ==========================================
# RAW QUERY RETRIEVAL
# ==========================================

# Direct retrieval without
# semantic expansion

def retrieve_raw_query(

    query,

    n_results=10
):

    try:

        results = collection.get()

        metadatas = results.get(
            "metadatas",
            []
        )

        documents = results.get(
            "documents",
            []
        )

        ranked = []

        for idx, item in enumerate(
            metadatas
        ):

            description = (
                documents[idx]
                if idx < len(documents)
                else ""
            )

            combined_text = (
                f"{item.get('name', '')} "
                f"{description}"
            )

            score = keyword_match_score(
                query,
                combined_text
            )

            ranked.append({

                "name":
                    item.get("name", ""),

                "url":
                    item.get("url", ""),

                "test_type":
                    item.get(
                        "test_type",
                        "Unknown"
                    ),

                "description":
                    description,

                "score":
                    score
            })

        ranked = sorted(

            ranked,

            key=lambda x: x["score"],

            reverse=True
        )

        return ranked[:n_results]

    except Exception as e:

        print(
            "\nRAW QUERY ERROR:"
        )

        print(str(e))

        return []


# ==========================================
# MAIN RETRIEVAL PIPELINE
# ==========================================

# Expands recruiter intent
# and retrieves ranked candidates

def retrieve_assessments(

    query,

    n_results=15
):

    try:

        # ==================================
        # QUERY EXPANSION
        # ==================================

        # Expands hiring context
        # for stronger retrieval coverage

        expanded_query = (
            expand_query_with_llm(query)
        )

        print("\n=== QUERY EXPANSION ===")

        print(
            "ORIGINAL:",
            query
        )

        print(
            "EXPANDED:",
            expanded_query
        )

        # ==================================
        # FALLBACK RETRIEVAL
        # ==================================

        results = retrieve_raw_query(

            expanded_query,

            n_results=n_results
        )

        print(
            f"\nRetrieved "
            f"{len(results)} "
            f"candidate assessments"
        )

        return results

    except Exception as e:

        print(
            "\nRETRIEVAL ERROR:"
        )

        print(str(e))

        return []


# ==========================================
# COMPARISON RETRIEVAL
# ==========================================

# Retrieves assessments for
# side-by-side comparison workflows

def retrieve_for_comparison(

    query,

    n_results=10
):

    try:

        return retrieve_raw_query(

            query,

            n_results=n_results
        )

    except Exception as e:

        print(
            "\nCOMPARISON ERROR:"
        )

        print(str(e))

        return []


# ==========================================
# COLLECTION STATUS
# ==========================================

# Utility helper for deployment
# health verification

def collection_exists():

    try:

        count = collection.count()

        return count >= 0

    except:

        return False