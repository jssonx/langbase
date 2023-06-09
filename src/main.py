import os
import tempfile
import streamlit as st
from streamlit_chat import message
from utils.langbase import Langbase

st.set_page_config(page_title="langbase", page_icon=":book:", layout="wide")


def initialize_session_state():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
        if is_openai_api_key_set():
            st.session_state["langbase"] = Langbase(st.session_state["OPENAI_API_KEY"])
        else:
            st.session_state["langbase"] = None


def update_openai_api_key():
    if (
        len(st.session_state["input_OPENAI_API_KEY"]) > 0
        and st.session_state["input_OPENAI_API_KEY"]
        != st.session_state["OPENAI_API_KEY"]
    ):
        st.session_state["OPENAI_API_KEY"] = st.session_state["input_OPENAI_API_KEY"]
        if st.session_state["langbase"] is not None:
            st.warning("Please upload files again.")
        st.session_state["messages"] = []
        st.session_state["user_input"] = ""
        st.session_state["langbase"] = Langbase(st.session_state["OPENAI_API_KEY"])


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
        query = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            answers_from_gpt = st.session_state["langbase"].ask(query)

        st.session_state["messages"].append((query, True))
        st.session_state["messages"].append((answers_from_gpt, False))


def read_and_save_file():
    st.session_state["langbase"].forget()  # to reset the knowledge base
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(
            f"Ingesting {file.name}"
        ):
            st.session_state["langbase"].ingest(file_path)
        os.remove(file_path)


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0


def get_token_nums():
    converted_messages = convert_messages(st.session_state["messages"])
    return st.session_state["langbase"].get_tokens(converted_messages)


def convert_messages(raw_messages):
    messages = []
    for msg, is_user in raw_messages:
        messages.append({"role": "user" if is_user else "assistant", "content": msg})
    return messages


def display_session_state():
    st.subheader("Session State")
    st.write("messages:", st.session_state["messages"])
    st.write("langbase:", st.session_state["langbase"])
    st.write("token_nums:", get_token_nums())

def display_titles():
    st.write(
            """
            ✨ langbase &nbsp; [![GitHub][github_badge]][github_link]
            =====================

            A LangChain-based knowledgebase QA dock.

            [github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
            [github_link]: https://github.com/jssonx/langbase
            """
        )
    

def main():
    display_titles()
    initialize_session_state()


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
        "Start here",
        key="user_input",
        disabled=not is_openai_api_key_set(),
        on_change=process_input,
    )

    st.divider()
    display_session_state()  # 添加显示会话状态的部分


if __name__ == "__main__":
    main()

# Questions:
# Who is the author of the paper "Attention is all you need"?
# What is MACK CROLANGUAGE's email address?
