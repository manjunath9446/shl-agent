

# Lightweight recommendation memory
# for consultative refinement.

# Tracks:
# - current recommendation stack
# - hiring domain
# - consultation strategy
# - refinement intent



recommendation_memory = {

    "current_stack": [],

    "domain": None,

    "strategy": None
}



def update_recommendation_state(

    recommendations,

    domain,

    strategy
):

    recommendation_memory[
        "current_stack"
    ] = recommendations

    recommendation_memory[
        "domain"
    ] = domain

    recommendation_memory[
        "strategy"
    ] = strategy




def get_recommendation_state():

    return recommendation_memory




def is_refinement_query(
    query
):

    refinement_terms = [

        "replace",
        "remove",
        "instead",
        "shorter",
        "longer",
        "too long",
        "too difficult",
        "another option",
        "alternative",
        "swap",
        "change",
        "keep",
        "exclude",
        "include"
    ]

    query_lower = query.lower()

    return any(

        term in query_lower

        for term in refinement_terms
    )




def detect_replacement_target(
    query,
    current_stack
):

    query_lower = query.lower()

    for assessment in current_stack:

        assessment_name = (
            assessment["name"]
            .lower()
        )

        if assessment_name in query_lower:

            return assessment



        if (

            "opq" in query_lower

            and

            "opq" in assessment_name
        ):

            return assessment

    return None