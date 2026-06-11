from pathlib import Path
from datasets import load_dataset
from src.embedding import Embedding
from src.io_vector_store import IOVectorStore

#TODO Update if new data is available

DATA_DIR = Path("data/medical_docs")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_medical_documents():
    ds = load_dataset(
        "slinusc/PubMedAbstractsSubset",
        cache_dir="data/medical_docs/cache"
    )
    return ds

def initialize_ingestion(batch_size: int = 256):
    ds = load_medical_documents()
    emb = Embedding()
    
    all_documents = [x['abstract'] for x in ds['train']]
    pm_ids = [x['PMID'] for x in ds['train']]
    
    vector_store = IOVectorStore()
    for i in range(0, len(all_documents), batch_size):
        batch_docs = all_documents[i : i + batch_size]
        batch_ids = pm_ids[i : i + batch_size]
        db_ids = range(i, i + len(batch_docs))
        batch_embeddings = emb.encode(batch_docs)
        vector_store.add_documents(db_ids, batch_ids, batch_docs, batch_embeddings)
    print("Ingestion complete!")
