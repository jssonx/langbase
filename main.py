import os
import tempfile
import streamlit as st
from streamlit_chat import message
from langbase import Langbase

st.set_page_config(page_title="langbase", page_icon=":book:", layout="wide")


def initialize_session_state():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
        if is_openai_api_key_set():
            st.session_state["conversation"] = Langbase(
                st.session_state["OPENAI_API_KEY"]
            )
        else:
            st.session_state["conversation"] = None


def update_openai_api_key():
    if (
        len(st.session_state["input_OPENAI_API_KEY"]) > 0
        and st.session_state["input_OPENAI_API_KEY"]
        != st.session_state["OPENAI_API_KEY"]
    ):
        st.session_state["OPENAI_API_KEY"] = st.session_state["input_OPENAI_API_KEY"]
        if st.session_state["conversation"] is not None:
            st.warning("Please upload files again.")
        st.session_state["messages"] = []
        st.session_state["user_input"] = ""
        st.session_state["conversation"] = Langbase(st.session_state["OPENAI_API_KEY"])


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if (
        st.session_state["user_input"]
        and len(st.session_state["user_input"].strip()) > 0
    ):
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            query_text = st.session_state["conversation"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((query_text, False))


def read_and_save_file():
    st.session_state["conversation"].forget()  # to reset the knowledge base
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(
            f"Ingesting {file.name}"
        ):
            st.session_state["conversation"].ingest(file_path)
        os.remove(file_path)


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0


def main():
    initialize_session_state()

    st.header("ChatPDF")

    if st.text_input(
        "OpenAI API Key",
        value=st.session_state["OPENAI_API_KEY"],
        key="input_OPENAI_API_KEY",
        type="password",
    ):
        update_openai_api_key()

    st.subheader("Upload files")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
        disabled=not is_openai_api_key_set(),
    )

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input(
        "Message",
        key="user_input",
        disabled=not is_openai_api_key_set(),
        on_change=process_input,
    )

    st.divider()


if __name__ == "__main__":
    main()

# Who is the author of the paper "Attention is all you need"?
# Give me a program that say hello world in C++.
# What is MACK CROLANGUAGE's email address?