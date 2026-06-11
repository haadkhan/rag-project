from src.io_vector_store import IOVectorStore
from src.embedding import Embedding

class RAG:
    def __init__(self):
        self.io_vector_store = IOVectorStore()
        self.embedding = Embedding()

    
    def retrieve_and_augment(self, query: str):
        query_embedding = self.embedding.encode([query])[0]
        results = self.io_vector_store.query_vector_store(query_embedding, top_k=2)
        #0 is doc_id, 1 is PMID, 2 is text, 3 is distance
        relevant_docs = [x[2] for x in results]
        return relevant_docs
