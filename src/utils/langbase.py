import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyMuPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from pprint import pprint
from utils.cal_tokens import get_num_tokens_from_messages

from supabase import Client, create_client
from langchain.vectorstores import SupabaseVectorStore


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class Langbase:
    def __init__(self, openai_api_key=None, vectorstore_type="chroma") -> None:
        self.vectorstore_type = vectorstore_type
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.supabase_client = Client(supabase_url, supabase_key)
        self.embeddings = OpenAIEmbeddings(client=None, openai_api_key=openai_api_key)
        self.persist_directory = "./data/vectorstore"
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", input_key="human_input"
        )
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "human_input", "context"],
            template="""You are a great expert.
                context: {context}
                chat_history: {chat_history}
                Human: {human_input}
                Expert:""",
        )
        self.llm = ChatOpenAI(
            client=None,
            model_name="gpt-3.5-turbo",
            temperature=0.9,
            openai_api_key=openai_api_key,
        )
        if self.vectorstore_type == "chroma":
            if self.vectorstore_exists_chroma() == True:
                self.db = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                ).as_retriever()
                self.chain = load_qa_chain(
                    self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt
                )
                pprint("Vectorstore exists.")
            else:
                self.db = None
                self.chain = None
        elif self.vectorstore_type == "supabase":
            if self.vectorstore_exists_supabase() == True:
                self.db = SupabaseVectorStore(
                    embedding=self.embeddings,
                    client=self.supabase_client,
                    table_name="documents",
                ).as_retriever()
                self.chain = load_qa_chain(
                    self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt
                )
                pprint("Vectorstore exists.")
            else:
                self.db = None
                self.chain = None

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Please, add a document."
        elif self.db is None:
            response = "Please, ingest a document first."
        else:
            docs = self.db.get_relevant_documents(question)
            response = self.chain.run(input_documents=docs, human_input=question)
        return response

    def ingest(self, file_path: str) -> None:
        pdf_loader = PyMuPDFLoader(file_path)
        loaded_documents = pdf_loader.load()
        split_documents = self.text_splitter.split_documents(loaded_documents)
        if self.vectorstore_type == "chroma":
            self.db = Chroma.from_documents(
                documents=split_documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
            ).as_retriever()
        elif self.vectorstore_type == "supabase":
            self.db = SupabaseVectorStore.from_documents(
                documents=split_documents,
                embedding=self.embeddings,
                client=self.supabase,
                table_name="documents",
            ).as_retriever()
        self.chain = load_qa_chain(
            self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt
        )

    def get_tokens(self, messages) -> int:
        return get_num_tokens_from_messages(messages)

    def vectorstore_exists_chroma(self) -> bool:
        if os.path.exists(self.persist_directory):
            return len(os.listdir(self.persist_directory)) > 0
        return False

    def vectorstore_exists_supabase(self) -> bool:
        response = self.supabase_client.table("documents").select("id").execute()
        return len(response.data) > 0

    def forget(self) -> None:
        self.db = None
        self.chain = None