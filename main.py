from src.ingest import initialize_ingestion
import os

if __name__ == "__main__":
    if "my_vector_store" not in os.listdir("vector_store"):
        initialize_ingestion()
    else:
        print("Vector store already exists")

    # Run the chat interface
    import subprocess
    subprocess.run(["streamlit", "run", "chat_interface.py"])