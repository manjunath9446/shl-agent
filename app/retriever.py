# app/retriever.py

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

client = chromadb.PersistentClient(

    path="./chroma_db",

    settings=chromadb.Settings(
        anonymized_telemetry=False
    )
)

embedding_function = (

    embedding_functions
    .SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

collection = client.get_collection(

    name="shl_assessments",

    embedding_function=embedding_function
)

# ==========================================
# GET COLLECTION
# ==========================================

def get_collection():

    return collection

# ==========================================
# DOMAIN KEYWORD EXTRACTION
# ==========================================

def extract_domain_keywords(query):

    query_lower = query.lower()

    keywords = []

    important_terms = [

        "java",
        "python",
        "rust",
        "golang",
        "linux",
        "network",
        "networking",
        "cloud",
        "aws",
        "azure",
        "frontend",
        "backend",
        "full stack",
        "leadership",
        "executive",
        "manager",
        "sales",
        "support",
        "embedded",
        "vlsi",
        "devops",
        "ai",
        "machine learning",
        "data science",
        "security",
        "cybersecurity"
    ]

    for term in important_terms:

        if term in query_lower:

            keywords.append(term)

    return keywords

# ==========================================
# KEYWORD ALIGNMENT SCORE
# ==========================================

def keyword_alignment_score(

    assessment,

    keywords
):

    text = (

        assessment["name"]
        + " "
        + assessment["description"]

    ).lower()

    score = 0

    for keyword in keywords:

        if keyword in text:

            score += 1

    return score

# ==========================================
# FORMAT RESULTS
# ==========================================

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
# REMOVE IRRELEVANT RESULTS
# ==========================================

def filter_irrelevant_results(

    query,

    results
):

    query_lower = query.lower()

    filtered = []

    # ======================================
    # RUST FILTERING
    # ======================================

    if "rust" in query_lower:

        blocked_terms = [

            "java",
            "c#",
            "jee",
            "spring"
        ]

        for r in results:

            text = (
                r["name"] + " " +
                r["description"]
            ).lower()

            blocked = False

            for term in blocked_terms:

                if term in text:

                    blocked = True
                    break

            if not blocked:

                filtered.append(r)

        return filtered

    return results

# ==========================================
# RERANK RESULTS
# ==========================================

def rerank_results(

    query,

    results
):

    keywords = extract_domain_keywords(
        query
    )

    reranked = []

    for result in results:

        semantic_score = (
            1 / (
                result["score"] + 0.0001
            )
        )

        keyword_score = (
            keyword_alignment_score(
                result,
                keywords
            )
        )

        final_score = (

            semantic_score * 0.7

            +

            keyword_score * 0.3
        )

        result["final_score"] = final_score

        reranked.append(result)

    reranked.sort(

        key=lambda x: x["final_score"],

        reverse=True
    )

    return reranked

# ==========================================
# MAIN RETRIEVAL
# ==========================================

def retrieve_assessments(

    query,

    n_results=12
):

    # ======================================
    # QUERY EXPANSION
    # ======================================

    expanded_query = (
        expand_query_with_llm(query)
    )

    print("\n=== QUERY EXPANSION ===")

    print("ORIGINAL:", query)

    print("EXPANDED:", expanded_query)

    # ======================================
    # RETRIEVAL
    # ======================================

    results = collection.query(

        query_texts=[expanded_query],

        n_results=n_results
    )

    formatted = format_results(
        results
    )

    # ======================================
    # FILTERING
    # ======================================

    filtered = filter_irrelevant_results(

        query,

        formatted
    )

    # ======================================
    # RERANKING
    # ======================================

    reranked = rerank_results(

        query,

        filtered
    )

    print("\n=== FINAL RANKED RESULTS ===")

    for r in reranked[:5]:

        print(
            r["name"],
            " | SCORE:",
            r["final_score"]
        )



    return reranked[:5]

# COMPARISON RETRIEVAL

def retrieve_for_comparison(

    query,

    n_results=10
):

    results = collection.query(

        query_texts=[query],

        n_results=n_results
    )

    return format_results(results)
# RAW QUERY RETRIEVAL


def retrieve_raw_query(

    query,

    n_results=5
):

    results = collection.query(

        query_texts=[query],

        n_results=n_results
    )

    return format_results(results)