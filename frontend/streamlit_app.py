import streamlit as st
import requests


# ==========================================
# CONFIG
# ==========================================

st.set_page_config(

    page_title=
        "SHL Assessment Agent",

    page_icon="🎯",

    layout="wide"
)


API_URL = (
    "https://manjunath3035-shl-backend.hf.space/chat"
)


# ==========================================
# TITLE
# ==========================================

st.title(
    "🎯 SHL Assessment Recommendation Agent"
)

st.caption(
    "Powered by RAG + Conversational AI | "
    "Individual Test Solutions Catalog"
)


# ==========================================
# SESSION
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# DISPLAY CHAT
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================================
# INPUT
# ==========================================

prompt = st.chat_input(
    "Describe the role "
    "you're hiring for..."
)


if prompt:

    st.session_state.messages.append(

        {

            "role":
                "user",

            "content":
                prompt
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(prompt)


    payload = {

        "messages":

            st.session_state.messages
    }


    try:

        response = requests.post(

            API_URL,

            json=payload,

            timeout=120
        )


        data = response.json()


        reply = data.get(
            "reply",
            ""
        )


        recommendations = data.get(

            "recommendations",

            []
        )


        with st.chat_message(
            "assistant"
        ):

            st.markdown(reply)


            if recommendations:

                st.subheader(
                    "📋 Recommended "
                    "Assessments"
                )


                for rec in recommendations:

                    st.markdown(

                        f"### "
                        f"{rec['name']}"
                    )


                    st.write(

                        "Type:",

                        rec.get(

                            "test_type",

                            "Assessment"
                        )
                    )


                    url = (

                        rec.get(
                            "url"
                        )

                        or

                        rec.get(
                            "link"
                        )

                        or

                        rec.get(
                            "product_url"
                        )
                    )


                    if url:

                        st.markdown(

                            f"[Open Assessment]"
                            f"({url})"
                        )


            if data.get(
                "end_of_conversation"
            ):

                st.success(
                    "✅ Conversation "
                    "complete!"
                )


        st.session_state.messages.append(

            {

                "role":
                    "assistant",

                "content":
                    reply
            }
        )


    except Exception as e:

        st.error(

            f"Backend Error: "
            f"{str(e)}"
        )