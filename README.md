# RAG Project

A Simple Retrieval-Augmented Generation (RAG) system for querying medical literature using vector embeddings and a local LLM.

## Features

- **Vector-based document retrieval**: Uses SQLite with sqlite-vec for efficient similarity search
- **Medical document ingestion**: Loads PubMed abstracts from HuggingFace datasets
- **Chat interface**: Streamlit-based UI for natural language queries
- **Local LLM integration**: Uses Apple foundation model

AI assistant Devin helped build the project using the free "swe-1.6 slow" model.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. The project uses Apple's Foundation Model. I set it up using opensource package [apfel](https://github.com/sgoedecke/apfel). Starting a local server is done using following
```bash
apfel server
```

## Setup

### Initial Data Ingestion

The dataset used is from pubmed abstracts from [huggingface](https://huggingface.co/datasets/slinusc/PubMedAbstractsSubset) and placed in data directory. 


```bash
python main.py
```

This will:
- Download the PubMed abstracts dataset
- Generate embeddings using sentence-transformers
- Store documents and embeddings in the vector database
- Launch the Streamlit chat interface

### Manual Ingestion

If you need to re-ingest data, delete the `vector_store/` directory and run:

```bash
python main.py
```

## Usage

### Starting the Chat Interface

Run the main script:
```bash
python main.py
```

Or directly launch Streamlit:
```bash
streamlit run chat_interface.py
```

### Using the Chat Interface

1. Open your browser to the URL shown in the terminal (typically `http://localhost:8501`)
2. Enter your medical question in the chat input
3. The system will:
   - Retrieve relevant documents from the vector store
   - Augment your query with context from the retrieved documents
   - Generate an answer using the LLM

## Project Structure

```
rag-project/
├── chat_interface.py      # Streamlit chat UI
├── main.py                # Entry point for ingestion and app launch
├── requirements.txt       # Python dependencies
├── src/
│   ├── ingest.py          # Data ingestion from HuggingFace
│   ├── embedding.py       # Text embedding generation
│   ├── io_vector_store.py # SQLite vector database operations
│   ├── rag.py             # RAG orchestration logic
│   └── generate.py        # LLM interaction
├── data/                  # Data storage (datasets, models cache)
└── vector_store/          # SQLite vector database
```

## Configuration

- **Embedding model**: Uses `neuml/pubmedbert-base-embeddings-8M` via sentence-transformers
- **Vector dimensions**: 256
- **Top-k retrieval**: Returns top 2 most relevant documents
- **LLM endpoint**: Configured in `src/generate.py` (default: `http://localhost:11434/v1`)

## Dependencies

- streamlit
- openai
- sentence-transformers
- datasets
- sqlite-vec

## Notes

- The vector store is created in `vector_store/my_vector_store.db`
- The system maintains conversation history within the chat session
