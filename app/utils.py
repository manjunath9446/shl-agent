

import os
import requests

from dotenv import load_dotenv



load_dotenv()



GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)

MODEL_NAME = (
    "llama-3.3-70b-versatile"
)



def call_llm(
    messages,
    max_tokens=300,
    temperature=0.2
):

    headers = {

        "Authorization":
            f"Bearer {GROQ_API_KEY}",

        "Content-Type":
            "application/json"
    }

    payload = {

        "model": MODEL_NAME,

        "messages": messages,

        "temperature": temperature,

        "max_tokens": max_tokens
    }

    response = requests.post(

        GROQ_URL,

        headers=headers,

        json=payload,

        timeout=60
    )

 

    if response.status_code != 200:

        print("\n=== GROQ ERROR ===")

        print(response.status_code)

        print(response.text)

    response.raise_for_status()

    data = response.json()

    return (

        data["choices"][0]
        ["message"]["content"]
        .strip()
    )




def contains_professional_context(
    query
):

    professional_terms = [

        # TECH

        "java",
        "python",
        "developer",
        "engineer",
        "backend",
        "frontend",
        "full stack",
        "software",
        "cloud",
        "devops",

        # BUSINESS

        "sales",
        "support",
        "operations",
        "finance",
        "analyst",
        "consultant",

        # LEADERSHIP

        "leadership",
        "manager",
        "director",
        "executive",
        "vp",
        "vice president",
        "cxo",
        "ceo",
        "cto",
        "cio",

        # HR / HIRING

        "hiring",
        "recruitment",
        "assessment",
        "candidate",
        "benchmarking",
        "talent",
        "selection",

        # SHL STYLE

        "succession",
        "psychometric",
        "behavioral",
        "personality",
        "executive hiring"
    ]

    query_lower = query.lower()

    for term in professional_terms:

        if term in query_lower:

            return True

    return False




def is_assessment_related(
    query
):

   

    # This prevents over-rejection
    # of short professional queries
    # like:
    #
    # "java"
    # "leadership"
    # "developers"
    # "backend hiring"
    #
    # which SHOULD continue
    # into clarification flow.
    

    if contains_professional_context(
        query
    ):

        print(
            "\n=== PROFESSIONAL CONTEXT DETECTED ==="
        )

        return True

   

    messages = [

        {
            "role": "system",

            "content": """
You are an enterprise hiring
and assessment intent classifier.

Determine whether the user
is discussing:

- hiring
- recruitment
- candidate evaluation
- leadership hiring
- talent assessment
- psychometric testing
- workforce evaluation
- employee development
- executive assessment
- skills testing
- organizational capability
- leadership development
- succession planning

Return ONLY:

YES
or
NO
"""
        },

        {
            "role": "user",

            "content": query
        }
    ]

    try:

        result = call_llm(

            messages,

            max_tokens=5,

            temperature=0
        )

        print("\n=== INTENT CHECK ===")

        print("QUERY:", query)

        print("RESULT:", result)

        return "YES" in result.upper()

    except Exception as e:

        print(
            "\nIntent classification failed:",
            e
        )

        return False




def parse_recommendations_from_response(

    reply,

    candidates
):

    selected = []

    lower_reply = reply.lower()



    opq_requested = (

        "opq" in lower_reply

        or

        "occupational personality questionnaire"
        in lower_reply
    )


    for candidate in candidates:

        candidate_name = (
            candidate["name"].lower()
        )

        if candidate_name in lower_reply:

            selected.append({

                "name":
                    candidate["name"],

                "url":
                    candidate["url"],

                "test_type":
                    candidate.get(
                        "test_type",
                        "Unknown"
                    )
            })



    if opq_requested:

        existing_names = set([

            s["name"]

            for s in selected
        ])

        for candidate in candidates:

            candidate_name = (
                candidate["name"].lower()
            )

            if (

                "opq" in candidate_name

                and

                candidate["name"]
                not in existing_names
            ):

                selected.append({

                    "name":
                        candidate["name"],

                    "url":
                        candidate["url"],

                    "test_type":
                        candidate.get(
                            "test_type",
                            "Unknown"
                        )
                })



    existing_names = set([

        s["name"]

        for s in selected
    ])

    for candidate in candidates:

        if candidate["name"] not in existing_names:

            selected.append({

                "name":
                    candidate["name"],

                "url":
                    candidate["url"],

                "test_type":
                    candidate.get(
                        "test_type",
                        "Unknown"
                    )
            })

        if len(selected) >= 10:

            break

    return selected