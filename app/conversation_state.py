

# Hybrid semantic clarification memory
# Uses semantic keyword groups instead
# of strict sentence matching.




# Detects whether conversation
# contains enough semantic indicators

def contains_keywords(
    text,
    keywords,
    threshold=1
):

    text_lower = text.lower()

    matches = 0

    for keyword in keywords:

        if keyword in text_lower:

            matches += 1

    return matches >= threshold




# Detects unresolved clarification state
# using semantic domain indicators

def detect_pending_clarification(
    conversation
):

    conversation_lower = (
        conversation.lower()
    )



    contact_center_terms = [

        "contact center",
        "call center",
        "customer support",
        "bpo",
        "voice process",
        "customer service"
    ]

    language_terms = [

        "english",
        "spanish",
        "french",
        "german",
        "hindi"
    ]

    if (

        contains_keywords(
            conversation_lower,
            contact_center_terms
        )

        and

        not contains_keywords(
            conversation_lower,
            language_terms
        )
    ):

        return {

            "type":
                "contact_center_language",

            "valid_answers":
                language_terms
        }



    english_indicators = [

        "english",
        "english speaking",
        "english support",
        "us support",
        "uk support"
    ]

    english_variants = [

        "us",
        "uk",
        "australian",
        "indian"
    ]

    if (

        contains_keywords(
            conversation_lower,
            english_indicators
        )

        and

        not contains_keywords(
            conversation_lower,
            english_variants
        )
    ):

        return {

            "type":
                "english_variant",

            "valid_answers":
                english_variants
        }



    sales_terms = [

        "sales",
        "business development",
        "account executive",
        "sales hiring",
        "sales organization"
    ]

    sales_environment_terms = [

        "b2b",
        "b2c",
        "enterprise",
        "retail"
    ]

    if (

        contains_keywords(
            conversation_lower,
            sales_terms
        )

        and

        not contains_keywords(
            conversation_lower,
            sales_environment_terms
        )
    ):

        return {

            "type":
                "sales_environment",

            "valid_answers":
                sales_environment_terms
        }



    leadership_terms = [

        "leadership",
        "executive",
        "director",
        "vp",
        "senior leadership",
        "succession"
    ]

    leadership_goal_terms = [

        "selection",
        "development",
        "benchmarking",
        "succession"
    ]

    if (

        contains_keywords(
            conversation_lower,
            leadership_terms
        )

        and

        not contains_keywords(
            conversation_lower,
            leadership_goal_terms
        )
    ):

        return {

            "type":
                "leadership_goal",

            "valid_answers":
                leadership_goal_terms
        }

    return None




# Validates whether user response
# satisfies expected clarification intent

def validate_clarification_answer(

    latest_user_message,

    pending
):

    if not pending:

        return True

    message_lower = (
        latest_user_message.lower()
    )

    valid_answers = pending[
        "valid_answers"
    ]

    return contains_keywords(

        message_lower,

        valid_answers
    )




# Re-prompts user when clarification
# response is incomplete or ambiguous

def generate_retry_question(
    pending
):

    clarification_type = pending[
        "type"
    ]


    if clarification_type == (
        "sales_environment"
    ):

        return (
            "Please specify whether "
            "the sales environment is "
            "B2B enterprise-focused "
            "or retail/customer-facing."
        )



    if clarification_type == (
        "english_variant"
    ):

        return (
            "Please specify the English "
            "variant: US, UK, "
            "Australian, or Indian."
        )



    if clarification_type == (
        "contact_center_language"
    ):

        return (
            "Please specify the primary "
            "customer interaction language "
            "(for example: English, "
            "Spanish, French)."
        )



    if clarification_type == (
        "leadership_goal"
    ):

        return (
            "Please specify whether "
            "this initiative is focused "
            "on selection, development, "
            "benchmarking, or succession."
        )

    return (
        "Could you clarify that "
        "in a little more detail?"
    )