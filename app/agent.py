
from app.models import (
    ChatResponse
)

from app.utils import (

    is_assessment_related,

    call_llm,

    parse_recommendations_from_response
)

from app.retriever import (

    retrieve_assessments,

    retrieve_for_comparison
)

from app.query_expansion import (
    expand_query_with_llm
)

from app.clarification_strategy import (
    generate_strategic_clarification
)

from app.conversation_state import (

    detect_pending_clarification,

    validate_clarification_answer,

    generate_retry_question
)

from app.recommendation_state import (

    update_recommendation_state,

    get_recommendation_state,

    detect_replacement_target
)

from app.consultation_mode_router import (

    detect_consultation_mode,

    ADVISORY,

    REFINEMENT,

    COMPARISON,

    RECOMMENDATION
)


# CONFIG
# Controls conversation limits
# for SHL evaluation constraints

MAX_USER_TURNS = 4

FINAL_RECOMMENDATION_COUNT = 10


# BUILD CONVERSATION
# Converts chat history into
# a single conversational context


def build_conversation(
    messages
):

    return "\n".join([

        f"{m.role}: {m.content}"

        for m in messages
    ])


# COUNT USER TURNS
# Prevents excessive clarification loops
# and enforces recommendation flow


def count_user_turns(
    messages
):

    return len([

        m for m in messages

        if m.role == "user"
    ])


# HALLUCINATION FILTER
# Prevents hallucinated assessments
# by validating against retrieved catalog data

def validate_recommendations(
    recommendations,
    retrieved_candidates
):

    candidate_names = {

        c["name"]

        for c in retrieved_candidates
    }

    candidate_urls = {

        c["url"]

        for c in retrieved_candidates
    }

    validated = []

    for rec in recommendations:

        if (

            rec.get("name") in candidate_names

            and

            rec.get("url") in candidate_urls
        ):

            validated.append(rec)

    return validated


# REFINEMENT FLOW
# Refines existing recommendation stack
# without regenerating from scratch



def handle_refinement_query(
    latest_query
):

    state = get_recommendation_state()

    current_stack = state[
        "current_stack"
    ]

    if not current_stack:

        return ChatResponse(

            reply=(
                "I don't currently have "
                "an assessment strategy "
                "to refine."
            ),

            recommendations=[],

            end_of_conversation=False
        )

    target = detect_replacement_target(

        latest_query,

        current_stack
    )

    stack_context = "\n\n".join([

        f"""
Assessment:
{a['name']}

Type:
{a['test_type']}
"""

        for a in current_stack
    ])

    messages = [

        {
            "role": "system",

            "content": """
You are an SHL assessment consultant.

The user wants to refine
an EXISTING assessment stack.

IMPORTANT:
- modify only requested areas
- preserve strong layers
- do NOT regenerate from scratch
- stay consultative
"""
        },

        {
            "role": "user",

            "content": f"""
Current Stack:
{stack_context}

Refinement Request:
{latest_query}

Target:
{target['name'] if target else 'Unknown'}
"""
        }
    ]

    reply = call_llm(

        messages,

        max_tokens=500,

        temperature=0.2
    )

    updated_stack = current_stack.copy()


    if (

        target

        and

        "opq" in target["name"].lower()
    ):

        updated_stack = [

            a for a in updated_stack

            if a["name"] != target["name"]
        ]

    update_recommendation_state(

        recommendations=updated_stack,

        domain=state["domain"],

        strategy=reply
    )

    return ChatResponse(

        reply=reply,

        recommendations=updated_stack,

        end_of_conversation=False
    )


# ADVISORY FLOW
# Handles HR strategy discussions
# without triggering random recommendations

def handle_advisory_query(
    latest_query
):

    state = get_recommendation_state()

    current_stack = state[
        "current_stack"
    ]

    stack_context = "\n\n".join([

        f"""
Assessment:
{a['name']}

Type:
{a['test_type']}
"""

        for a in current_stack
    ])

    messages = [

        {
            "role": "system",

            "content": """
You are an SHL hiring consultant.

The user is asking an HR
strategy or advisory question.

IMPORTANT:
- DO NOT regenerate assessments
- DO NOT recommend random tests
- continue current consultation
- answer strategically
"""
        },

        {
            "role": "user",

            "content": f"""
Current Stack:
{stack_context}

HR Advisory Question:
{latest_query}
"""
        }
    ]

    reply = call_llm(

        messages,

        max_tokens=400,

        temperature=0.2
    )

    return ChatResponse(

        reply=reply,

        recommendations=current_stack,

        end_of_conversation=False
    )


# COMPARISON FLOW
# Compares assessments using
# retrieved catalog context


def handle_comparison_query(
    latest_query
):

    candidates = retrieve_for_comparison(

        latest_query,

        n_results=10
    )

    context = "\n\n".join([

        f"""
Assessment:
{c['name']}

Type:
{c['test_type']}

Description:
{c['description']}
"""

        for c in candidates
    ])

    messages = [

        {
            "role": "system",

            "content": """
You are an SHL consultant.

Compare assessments clearly.

Focus on:
- use case
- candidate experience
- hiring fit
- differences
"""
        },

        {
            "role": "user",

            "content": f"""
Query:
{latest_query}

Assessment Data:
{context}
"""
        }
    ]

    reply = call_llm(

        messages,

        max_tokens=500,

        temperature=0.2
    )

    recommendations = (

        parse_recommendations_from_response(

            reply,

            candidates
        )
    )

    recommendations = validate_recommendations(

        recommendations,

        candidates
    )

    return ChatResponse(

        reply=reply,

        recommendations=recommendations[:10],

        end_of_conversation=False
    )


# RECOMMENDATION FLOW
# Main recommendation pipeline:
# clarification → retrieval → recommendation


def handle_recommendation_query(
    full_conversation,
    force_recommend=False
):

    
    # STRATEGIC CLARIFICATION
    # Asks targeted clarification questions
# to improve retrieval precision

    if not force_recommend:

        strategic_question = (

            generate_strategic_clarification(
                full_conversation
            )
        )

        if strategic_question:

            return ChatResponse(

                reply=strategic_question,

                recommendations=[],

                end_of_conversation=False
            )

    
    # QUERY EXPANSION
    # Expands hiring intent semantically
# for better Recall@10 retrieval

    expanded_query = (
        expand_query_with_llm(
            full_conversation
        )
    )

    print("\n=== QUERY EXPANSION ===")

    print(expanded_query)



    candidates = retrieve_assessments(

        expanded_query,

        n_results=20
    )

    if not candidates:

        return ChatResponse(

            reply=(
                "I couldn't find suitable "
                "SHL assessments for this "
                "hiring scenario."
            ),

            recommendations=[],

            end_of_conversation=True
        )



    context = "\n\n".join([

        f"""
Assessment:
{c['name']}

Type:
{c['test_type']}

Description:
{c['description']}

URL:
{c['url']}
"""

        for c in candidates
    ])

    messages = [

        {
            "role": "system",

            "content": """
You are an SHL assessment consultant.

Recommend ONLY assessments
from retrieved catalog data.

IMPORTANT:
- never hallucinate
- use ONLY provided assessments
- explain why each assessment fits
- stay concise and consultative
"""
        },

        {
            "role": "user",

            "content": f"""
Hiring Context:
{full_conversation}

Retrieved Assessments:
{context}
"""
        }
    ]

    reply = call_llm(

        messages,

        max_tokens=700,

        temperature=0.2
    )

    recommendations = (

        parse_recommendations_from_response(

            reply,

            candidates
        )
    )

    # HALLUCINATION FILTER
# Ensures only catalog-backed
# assessments are returned
    recommendations = validate_recommendations(

        recommendations,

        candidates
    )


    if not recommendations:

        recommendations = candidates[:5]



    recommendations = recommendations[
        :FINAL_RECOMMENDATION_COUNT
    ]

  

    update_recommendation_state(

        recommendations=recommendations,

        domain=full_conversation,

        strategy=reply
    )

    return ChatResponse(

        reply=reply,

        recommendations=recommendations,

        end_of_conversation=True
    )



def run_agent(
    request
):

    full_conversation = (
        build_conversation(
            request.messages
        )
    )

    latest_query = (
        request.messages[-1].content
    )

   

    user_turns = count_user_turns(
        request.messages
    )

    print("\n=== USER TURNS ===")

    print(user_turns)

    force_recommend = (

        user_turns >= MAX_USER_TURNS
    )

    

    pending = (
        detect_pending_clarification(
            full_conversation
        )
    )

    if pending and not force_recommend:

        valid = (
            validate_clarification_answer(

                latest_query,

                pending
            )
        )

        if not valid:

            retry_question = (
                generate_retry_question(
                    pending
                )
            )

            return ChatResponse(

                reply=retry_question,

                recommendations=[],

                end_of_conversation=False
            )

 

    if not is_assessment_related(
        full_conversation
    ):

        return ChatResponse(

            reply=(
                "I'm specialized in "
                "SHL assessment "
                "recommendations and "
                "hiring strategy."
            ),

            recommendations=[],

            end_of_conversation=False
        )

    # CONSULTATION MODE

    mode = detect_consultation_mode(
        latest_query
    )

    print("\n=== CONSULTATION MODE ===")

    print(mode)

    # ADVISORY
    

    if mode == ADVISORY:

        return handle_advisory_query(
            latest_query
        )

 

    if mode == REFINEMENT:

        return handle_refinement_query(
            latest_query
        )

   

    if mode == COMPARISON:

        return handle_comparison_query(
            latest_query
        )

    # RECOMMENDATION\
    # Executes final assessment
# recommendation workflow 

    return handle_recommendation_query(

        full_conversation,

        force_recommend=force_recommend
    )