

# Determines what type of
# consultation turn this is.

# Prevents:
# random assessment regeneration
# during HR advisory discussions.



RECOMMENDATION = "recommendation"

REFINEMENT = "refinement"

COMPARISON = "comparison"

ADVISORY = "advisory"

CLARIFICATION = "clarification"




def is_advisory_query(
    query
):

    advisory_terms = [

        "salary",
        "compensation",
        "package",
        "candidate experience",
        "drop off",
        "drop-off",
        "assessment fatigue",
        "time to hire",
        "benchmarking",
        "industry standard",
        "best practice",
        "hiring funnel",
        "selection process",
        "assessment duration",
        "candidate complaints",
        "recruitment strategy",
        "volume hiring",
        "hiring scale",
        "cost",
        "roi"
    ]

    query_lower = query.lower()

    return any(

        term in query_lower

        for term in advisory_terms
    )




def is_comparison_query(
    query
):

    comparison_terms = [

        "compare",
        "difference",
        "vs",
        "versus",
        "better than"
    ]

    query_lower = query.lower()

    return any(

        term in query_lower

        for term in comparison_terms
    )



def is_refinement_query(
    query
):

    refinement_terms = [

        "replace",
        "remove",
        "instead",
        "shorter",
        "longer",
        "alternative",
        "swap",
        "change",
        "keep",
        "exclude",
        "include",
        "add qpd",
        "add spoken english"
    ]

    query_lower = query.lower()

    return any(

        term in query_lower

        for term in refinement_terms
    )



def detect_consultation_mode(
    latest_query
):

    if is_advisory_query(
        latest_query
    ):

        return ADVISORY

    if is_refinement_query(
        latest_query
    ):

        return REFINEMENT

    if is_comparison_query(
        latest_query
    ):

        return COMPARISON

    return RECOMMENDATION