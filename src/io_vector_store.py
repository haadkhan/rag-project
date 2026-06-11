import sqlite3
import sqlite_vec
from sentence_transformers import SentenceTransformer


class IOVectorStore:
    def __init__(self, vector_dimensions=256):
        self.db = sqlite3.connect("vector_store/my_vector_store.db", check_same_thread=False)
        self.db.enable_load_extension(True)
        sqlite_vec.load(self.db)
        self.db.enable_load_extension(False)
        self.vector_dimensions = vector_dimensions
        self.create_tables()
    
    def create_tables(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, pmid_val INTEGER, text TEXT)")
        self.db.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_documents USING vec0(
                id INTEGER PRIMARY KEY,
                pmid_val INTEGER,
                embedding float[{self.vector_dimensions}]
            )
        """)
        self.db.commit()
    
    def add_documents(self, document_id, pmid, document, document_embedding):
        
        for id, pmid_val, text, embedding in zip(document_id, pmid, document, document_embedding):
            cursor = self.db.execute("INSERT INTO documents (id, pmid_val, text) VALUES (?, ?, ?)", (id, pmid_val, text))
            doc_id = cursor.lastrowid
            
            self.db.execute(
                "INSERT INTO vec_documents (id, pmid_val, embedding) VALUES (?, ?, ?)",
                (doc_id, pmid_val, embedding.tobytes())
            )
        self.db.commit()
    
    def query_vector_store(self, query_vector, top_k=2) -> list:
        cursor = self.db.execute("""
            SELECT 
                documents.id,
                documents.pmid_val,
                documents.text, 
                vec_documents.distance
            FROM vec_documents
            JOIN documents ON vec_documents.id = documents.id
            WHERE embedding MATCH ? AND k = ?
            ORDER BY distance ASC
        """, (query_vector.tobytes(), top_k))
        
        return cursor.fetchall()


