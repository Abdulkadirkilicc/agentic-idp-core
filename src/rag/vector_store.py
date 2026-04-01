import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_data")

from langchain_core.embeddings import Embeddings

class DummyEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

class VectorStoreManager:
    def __init__(self):
        # We use a dummy key if nothing is set just to allow it to initialize
        api_key = os.environ.get("OPENAI_API_KEY", "dummy-key")
        if api_key == "dummy-key":
            self.embeddings = DummyEmbeddings()
        else:
            self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.vector_store = Chroma(
            collection_name="idp_knowledge_base",
            embedding_function=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )

    def add_documents(self, docs):
        """
        Adds a list of LangChain Document objects to the vector store.
        """
        if not docs:
            return
        self.vector_store.add_documents(docs)
        self.vector_store.persist()

    def get_retriever(self, search_kwargs={"k": 3}):
        """
        Returns a document retriever using similarity search.
        """
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)

vector_store_manager = VectorStoreManager()
