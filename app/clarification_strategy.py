

# Strategic clarification engine
# for SHL-style consultative workflows

# Goal:
# Ask only the most relevant
# clarification question before
# generating recommendations.




# Prevents repeated clarification
# questions during multi-turn flow

def already_answered(

    conversation,

    keywords
):

    conversation_lower = (
        conversation.lower()
    )

    for keyword in keywords:

        if keyword in conversation_lower:

            return True

    return False



# Handles high-volume hiring
# for customer support/contact center

def contact_center_strategy(
    conversation
):

    conversation_lower = (
        conversation.lower()
    )

   

    # Detects customer support /
    # contact center hiring intent

    contact_center_terms = [

        "contact center",
        "call center",
        "customer support",
        "inbound calls",
        "outbound calls",
        "voice process",
        "bpo",
        "customer service agent",
        "phone support",
        "support representative"
    ]

    detected = any(

        term in conversation_lower

        for term in contact_center_terms
    )

    if not detected:

        return None


    # Determines spoken language
    # screening requirements

    if not already_answered(

        conversation,

        [
            "english",
            "spanish",
            "french",
            "german",
            "hindi"
        ]
    ):

        return (
            "Before I shape the "
            "assessment stack — "
            "what language are "
            "the customer calls in?"
        )



    # Identifies regional English
    # variant for SVAR alignment

    english_variants = [

        "us",
        "uk",
        "australian",
        "indian"
    ]

    if (

        "english"
        in conversation_lower

        and

        not already_answered(
            conversation,
            english_variants
        )
    ):

        return (
            "SVAR has multiple "
            "English variants "
            "(US, UK, Australian, "
            "Indian). Which best "
            "matches your customer "
            "base?"
        )

    return None



# Handles executive and
# leadership hiring workflows

def leadership_strategy(
    conversation
):

    conversation_lower = (
        conversation.lower()
    )

    leadership_terms = [

        "leadership",
        "director",
        "executive",
        "vp",
        "vice president",
        "ceo",
        "cto",
        "cio",
        "cxo",
        "senior leadership"
    ]

    leadership_detected = any(

        term in conversation_lower

        for term in leadership_terms
    )

    if not leadership_detected:

        return None

    

    # Clarifies leadership use case
    # before assessment recommendation

    if not already_answered(

        conversation,

        [
            "selection",
            "development",
            "succession",
            "benchmark",
            "benchmarking"
        ]
    ):

        return (
            "Is this initiative focused "
            "on executive selection, "
            "leadership development, "
            "or succession benchmarking?"
        )

    return None




# Handles technical and
# engineering hiring scenarios

def tech_strategy(
    conversation
):

    conversation_lower = (
        conversation.lower()
    )

    tech_terms = [

        "java",
        "python",
        "rust",
        "golang",
        "developer",
        "engineer",
        "backend",
        "frontend",
        "software engineer",
        "technical architect"
    ]

    tech_detected = any(

        term in conversation_lower

        for term in tech_terms
    )

    if not tech_detected:

        return None

   

    # Identifies seniority level
    # for assessment calibration

    if not already_answered(

        conversation,

        [
            "entry",
            "junior",
            "mid",
            "senior",
            "lead",
            "architect",
            "manager"
        ]
    ):

        return (
            "What level of experience "
            "are you hiring for?"
        )

    

    # Determines technical emphasis
    # within engineering role

    if not already_answered(

        conversation,

        [
            "coding",
            "architecture",
            "leadership",
            "backend",
            "frontend",
            "full stack"
        ]
    ):

        return (
            "Is the role primarily "
            "coding-focused, "
            "architecture-focused, "
            "or leadership-oriented?"
        )

    return None




# Handles sales hiring and
# sales transformation workflows

def sales_strategy(
    conversation
):

    conversation_lower = (
        conversation.lower()
    )

    sales_terms = [

        "sales",
        "business development",
        "account executive",
        "account manager",
        "inside sales",
        "sales organization",
        "sales team"
    ]

    detected = any(

        term in conversation_lower

        for term in sales_terms
    )

    if not detected:

        return None

    

    # Distinguishes enterprise
    # vs retail sales context

    if not already_answered(

        conversation,

        [
            "b2b",
            "b2c",
            "enterprise",
            "retail"
        ]
    ):

        return (
            "Is this primarily a "
            "B2B enterprise sales "
            "environment or a "
            "customer-facing retail "
            "sales role?"
        )

    return None



# Handles finance and analytical
# hiring scenarios

def finance_strategy(
    conversation
):

    conversation_lower = (
        conversation.lower()
    )

    finance_terms = [

        "financial analyst",
        "finance",
        "investment",
        "banking",
        "audit",
        "accounting",
        "treasury",
        "financial planning"
    ]

    detected = any(

        term in conversation_lower

        for term in finance_terms
    )

    if not detected:

        return None

   

    # Identifies analytical intensity
    # for cognitive assessment alignment

    if not already_answered(

        conversation,

        [
            "numerical",
            "analytical",
            "reasoning",
            "cognitive"
        ]
    ):

        return (
            "Will the role require "
            "strong numerical reasoning "
            "or analytical problem-solving?"
        )

    return None



# Executes domain-specific
# clarification routing

def generate_strategic_clarification(
    conversation
):



    result = contact_center_strategy(
        conversation
    )

    if result:

        return result


    result = leadership_strategy(
        conversation
    )

    if result:

        return result



    result = tech_strategy(
        conversation
    )

    if result:

        return result



    result = sales_strategy(
        conversation
    )

    if result:

        return result

 

    result = finance_strategy(
        conversation
    )

    if result:

        return result

    return None