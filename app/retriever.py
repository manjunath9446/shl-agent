# ==========================================
# app/retriever.py
# ==========================================

# Lightweight JSON-based retrieval layer
# optimized for stable cloud deployment

import json
import os

from app.query_expansion import (
    expand_query_with_llm
)


# ==========================================
# LOAD ASSESSMENT CATALOG
# ==========================================

# Loads SHL assessment catalog
# from local JSON file

CATALOG_PATH = (
    "data/shl_product_catalog.json"
)

assessment_catalog = []


def load_catalog():

    global assessment_catalog

    if not os.path.exists(
        CATALOG_PATH
    ):

        print(
            "\nCatalog file not found"
        )

        assessment_catalog = []

        return

    with open(

        CATALOG_PATH,

        "r",

        encoding="utf-8"

    ) as f:

        assessment_catalog = (
            json.load(f)
        )

    print(
        f"\nLoaded "
        f"{len(assessment_catalog)} "
        f"assessments from catalog"
    )


# Load catalog during startup

load_catalog()


# ==========================================
# GET COLLECTION
# ==========================================

# Compatibility helper for API

def get_collection():

    class DummyCollection:

        def count(self):

            return len(
                assessment_catalog
            )

    return DummyCollection()


# ==========================================
# KEYWORD MATCH SCORE
# ==========================================

# Lightweight semantic scoring
# using keyword overlap

def keyword_match_score(

    query,

    text
):

    query_words = (

        query.lower()
        .replace(",", " ")
        .split()
    )

    text_lower = text.lower()

    score = 0

    for word in query_words:

        if word in text_lower:

            score += 1

    return score


# ==========================================
# FORMAT ASSESSMENT
# ==========================================

# Standardizes assessment response

def format_assessment(
    item,
    score
):

    return {

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
            item.get(
                "description",
                ""
            ),

        "score":
            score
    }


# ==========================================
# RAW QUERY RETRIEVAL
# ==========================================

# Direct retrieval without
# query expansion

def retrieve_raw_query(

    query,

    n_results=10
):

    ranked = []

    for item in assessment_catalog:

        combined_text = (

            f"{item.get('name', '')} "

            f"{item.get('description', '')} "

            f"{item.get('test_type', '')}"
        )

        score = keyword_match_score(

            query,

            combined_text
        )

        ranked.append(

            format_assessment(
                item,
                score
            )
        )

    ranked = sorted(

        ranked,

        key=lambda x: x["score"],

        reverse=True
    )

    return ranked[:n_results]


# ==========================================
# MAIN RETRIEVAL PIPELINE
# ==========================================

# Expands recruiter intent
# before retrieval

def retrieve_assessments(

    query,

    n_results=15
):

    try:

        # ==================================
        # QUERY EXPANSION
        # ==================================

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
        # RETRIEVAL
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
# comparison workflows

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

# Health check helper

def collection_exists():

    return len(
        assessment_catalog
    ) > 0