# ==========================================
# app/retriever.py
# ==========================================

# Retrieval layer for SHL assessment catalog
# Uses ChromaDB + SentenceTransformer embeddings

import chromadb

from chromadb.utils import (
    embedding_functions
)

from app.query_expansion import (
    expand_query_with_llm
)


# ==========================================
# CHROMADB CLIENT
# ==========================================

# Persistent vector database
# for SHL assessment retrieval

client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=chromadb.Settings(
        anonymized_telemetry=False
    )
)


# ==========================================
# EMBEDDING MODEL
# ==========================================

# Lightweight embedding model
# optimized for semantic retrieval

embedding_function = (
    embedding_functions
    .SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)


# ==========================================
# COLLECTION LOADING
# ==========================================

# Loads existing collection
# or creates a new one if missing

try:

    collection = client.get_collection(

        name="shl_assessments",

        embedding_function=embedding_function
    )

    print(
        "\nLoaded existing "
        "ChromaDB collection"
    )

except Exception as e:

    print(
        "\nCollection not found."
    )

    print(
        "Creating new collection..."
    )

    collection = client.create_collection(

        name="shl_assessments",

        embedding_function=embedding_function
    )

    print(
        "\nNew ChromaDB collection "
        "created successfully"
    )


# ==========================================
# GET COLLECTION
# ==========================================

# Returns active ChromaDB collection

def get_collection():

    return collection


# ==========================================
# FORMAT RESULTS
# ==========================================

# Converts raw ChromaDB output
# into structured recommendation format

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
# RAW QUERY RETRIEVAL
# ==========================================

# Direct retrieval without
# query expansion

def retrieve_raw_query(

    query,

    n_results=10
):

    try:

        results = collection.query(

            query_texts=[query],

            n_results=n_results
        )

        return format_results(results)

    except Exception as e:

        print(
            "\nRAW QUERY ERROR:"
        )

        print(str(e))

        return []


# ==========================================
# MAIN RETRIEVAL PIPELINE
# ==========================================

# Expands hiring intent and
# retrieves broader candidate pool

def retrieve_assessments(

    query,

    n_results=15
):

    try:

        # ==================================
        # QUERY EXPANSION
        # ==================================

        # Expands recruiter intent
        # for stronger Recall@10

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
        # VECTOR RETRIEVAL
        # ==================================

        # Broad semantic retrieval
        # before recommendation filtering

        results = collection.query(

            query_texts=[
                expanded_query
            ],

            n_results=n_results
        )

        formatted = (
            format_results(results)
        )

        print(
            f"\nRetrieved "
            f"{len(formatted)} "
            f"candidate assessments"
        )

        return formatted

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

        results = collection.query(

            query_texts=[query],

            n_results=n_results
        )

        return format_results(results)

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
# and health verification

def collection_exists():

    try:

        count = collection.count()

        return count >= 0

    except:

        return False