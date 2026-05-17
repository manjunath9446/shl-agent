
from app.utils import call_llm


def expand_query_with_llm(query):

    messages = [

        {
            "role": "system",
            "content": """
You improve hiring and assessment queries
for semantic retrieval.

Expand the query using:
- related skills
- job role terminology
- assessment terminology
- hiring terminology

Keep expansion concise.

Return ONLY the expanded query.
"""
        },

        {
            "role": "user",
            "content": query
        }
    ]

    try:

        expanded = call_llm(

            messages,

            max_tokens=80,

            temperature=0.2
        )

        return expanded

    except Exception as e:

        print(
            "LLM query expansion failed:",
            e
        )

        return query