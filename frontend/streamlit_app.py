# ==========================================
# frontend/streamlit_app.py
# ==========================================

import streamlit as st
import requests


# ==========================================
# BACKEND API
# ==========================================

API_URL = (
    "https://shl-agent-ri7d.onrender.com/chat"
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title=(
        "SHL Assessment "
        "Recommendation Agent"
    ),

    layout="wide"
)


# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown("""

<style>

.main {
    background-color: #0b1020;
    color: white;
}

.stChatMessage {
    border-radius: 10px;
    padding: 10px;
}

</style>

""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.title(
    "🎯 SHL Assessment "
    "Recommendation Agent"
)

st.caption(
    "Powered by RAG + Conversational AI "
    "| Individual Test Solutions Catalog"
)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )


# ==========================================
# USER INPUT
# ==========================================

user_input = st.chat_input(
    "Describe the role you're hiring for..."
)


# ==========================================
# HANDLE USER MESSAGE
# ==========================================

if user_input:

    # ======================================
    # STORE USER MESSAGE
    # ======================================

    st.session_state.messages.append({

        "role": "user",

        "content": user_input
    })

    # ======================================
    # DISPLAY USER MESSAGE
    # ======================================

    with st.chat_message(
        "user"
    ):

        st.markdown(user_input)

    # ======================================
    # API REQUEST
    # ======================================

    try:

        response = requests.post(

            API_URL,

            json={

                "messages":
                    st.session_state.messages
            },

            timeout=60
        )

        # ==================================
        # DEBUG INFO
        # ==================================

        st.write(
            "Status Code:",
            response.status_code
        )

        st.write(
            "Raw Response:"
        )

        st.code(
            response.text
        )

        # ==================================
        # HANDLE BACKEND ERRORS
        # ==================================

        if response.status_code != 200:

            st.error(

                f"Backend Error:\n"
                f"{response.text}"
            )

        else:

            # ==============================
            # SAFE JSON PARSING
            # ==============================

            try:

                data = response.json()

            except Exception as json_error:

                st.error(

                    f"JSON Parse Error:\n"
                    f"{str(json_error)}"
                )

                st.stop()

            # ==============================
            # EXTRACT RESPONSE
            # ==============================

            assistant_reply = (
                data.get(
                    "reply",
                    "No response"
                )
            )

            recommendations = (
                data.get(
                    "recommendations",
                    []
                )
            )

            # ==============================
            # STORE ASSISTANT MESSAGE
            # ==============================

            st.session_state.messages.append({

                "role": "assistant",

                "content": assistant_reply
            })

            # ==============================
            # DISPLAY ASSISTANT MESSAGE
            # ==============================

            with st.chat_message(
                "assistant"
            ):

                st.markdown(
                    assistant_reply
                )

                # ==========================
                # RECOMMENDATIONS
                # ==========================

                if recommendations:

                    st.markdown(
                        "---"
                    )

                    st.subheader(
                        "📋 Recommended "
                        "Assessments"
                    )

                    for rec in recommendations:

                        with st.container():

                            st.markdown(

                                f"### "
                                f"{rec.get('name', '')}"
                            )

                            st.write(

                                f"Type: "
                                f"{rec.get('test_type', '')}"
                            )

                            st.write(

                                rec.get(
                                    "description",
                                    ""
                                )
                            )

                            url = rec.get(
                                "url",
                                ""
                            )

                            if url:

                                st.markdown(

                                    f"[Open Assessment]"
                                    f"({url})"
                                )

                            st.markdown("---")

            # ==============================
            # END OF CONVERSATION
            # ==============================

            if data.get(
                "end_of_conversation",
                False
            ):

                st.success(

                    "✅ Conversation complete!"
                )

    except Exception as e:

        st.error(

            f"API Error: {str(e)}"
        )