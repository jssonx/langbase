import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFium2Loader
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class PDFQuery:
    def __init__(self, openai_api_key=None) -> None:
        OPENAI_API_KEY = openai_api_key
        self.embeddings = OpenAIEmbeddings(client=None, openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.llm = ChatOpenAI(client=None, model_name="gpt-3.5-turbo", temperature=0.9, openai_api_key=openai_api_key)
        self.chain = None
        self.db = None

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Please, add a document."
        elif self.db is None:
            response = "Please, ingest a document first."
        else:
            docs = self.db.get_relevant_documents(question)
            response = self.chain.run(input_documents=docs, question=question)
        return response

    def ingest(self, file_path: str) -> None:
        loader = PyPDFium2Loader(file_path)
        documents = loader.load()
        splitted_documents = self.text_splitter.split_documents(documents)
        self.db = Chroma.from_documents(splitted_documents, self.embeddings).as_retriever()
        self.chain = load_qa_chain(self.llm, chain_type="stuff")

    def forget(self) -> None:
        self.db = None
        self.chain = None