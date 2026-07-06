import streamlit as st
from router import handle_query

st.set_page_config(
    page_title="E-commerce Support Agent",
    page_icon="🛍️",
    layout="centered"
)

st.title("🛍️ E-commerce Support Agent")

st.caption(
    "Ask about orders, shipping, returns, payments and support."
)

question = st.text_input(
    "Ask your question",
    placeholder="Example: Can I return ORD1004?"
)

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            answer = handle_query(question)

        st.markdown(answer)
    