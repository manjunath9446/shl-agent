# frontend/streamlit_app.py

import streamlit as st
import requests
import pandas as pd



API_URL = "https://shl-agent-ri7d.onrender.com/chat"

st.set_page_config(
    page_title="SHL Assessment Recommendation Agent",
    layout="wide"
)



st.markdown("""
<style>

.main {
    background-color: #0b1020;
    color: white;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

.assessment-card {
    padding: 15px;
    border: 1px solid #2d3748;
    border-radius: 12px;
    margin-bottom: 12px;
    background-color: #111827;
}

.small-text {
    color: #9ca3af;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)



st.title(
    "🎯 SHL Assessment Recommendation Agent"
)

st.caption(
    "Powered by RAG + Conversational AI | Individual Test Solutions Catalog"
)



if "messages" not in st.session_state:

    st.session_state.messages = []

if "all_recommendations" not in st.session_state:

    st.session_state.all_recommendations = []



with st.sidebar:

    st.markdown("## ℹ️ Assessment Types")

    st.markdown("""
A → Ability

K → Knowledge

P → Personality

S → Simulation
""")

    st.markdown("---")

    if st.session_state.all_recommendations:

        st.markdown(
            "## 📋 All Recommended Assessments"
        )

        df = pd.DataFrame(
            st.session_state.all_recommendations
        )

        if "url" in df.columns:

            df = df.drop(columns=["url"])

        st.dataframe(
            df,
            use_container_width=True
        )



for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        

        if msg.get("recommendations"):

            st.markdown("---")

            st.markdown(
                "## 📋 Recommended Assessments"
            )

            cols = st.columns(2)

            for idx, rec in enumerate(
                msg["recommendations"]
            ):

                with cols[idx % 2]:

                    with st.container():

                        st.markdown(
                            f"""
<div class="assessment-card">

### {rec['name']}

<p class="small-text">
Type: {rec['test_type']}
</p>

</div>
""",
                            unsafe_allow_html=True
                        )

                        st.link_button(
                            "View on SHL →",
                            rec["url"],
                            use_container_width=True
                        )



prompt = st.chat_input(
    "Describe the role you're hiring for..."
)



if prompt:

    

    st.session_state.messages.append({

        "role": "user",

        "content": prompt
    })

    

    payload = {

        "messages": [

            {
                "role": m["role"],

                "content": m["content"]
            }

            for m in st.session_state.messages
        ]
    }

    

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=120
        )

        data = response.json()

        assistant_message = {

            "role": "assistant",

            "content": data["reply"],

            "recommendations":
                data.get(
                    "recommendations",
                    []
                )
        }

        st.session_state.messages.append(
            assistant_message
        )

        

        for rec in data.get(
            "recommendations",
            []
        ):

            if rec not in (
                st.session_state
                .all_recommendations
            ):

                st.session_state[
                    "all_recommendations"
                ].append(rec)

        st.rerun()

    except Exception as e:

        st.error(
            f"API Error: {str(e)}"
        )



if st.session_state.messages:

    last_msg = (
        st.session_state.messages[-1]
    )

    if (
        last_msg["role"] == "assistant"
        and
        last_msg.get("recommendations")
    ):

        st.success(
            "✅ Conversation complete! "
            "Start a new session to get "
            "more recommendations."
        )

        if st.button(
            "Start New Conversation"
        ):

            st.session_state.messages = []

            st.session_state[
                "all_recommendations"
            ] = []

            st.rerun()