from sentence_transformers.models import StaticEmbedding
from sentence_transformers import SentenceTransformer
import os
import html

class Embedding():
    def __init__(self):
        os.environ["HF_HOME"] = "data/models/"
        static = StaticEmbedding.from_model2vec("neuml/pubmedbert-base-embeddings-8M")
        self.model = SentenceTransformer(modules=[static])
    
    def clean_text(self, text):
        text = html.unescape(text)
        text = " ".join(text.split())
        return text

    def encode(self, sentences):
        cleaned_sentences = [self.clean_text(sentence) for sentence in sentences]
        return self.model.encode(cleaned_sentences)
