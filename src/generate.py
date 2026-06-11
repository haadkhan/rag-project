from openai import OpenAI

class llm_caller():
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:11434/v1", api_key="unused")
        self.history = []

    def generate(self, user_question, retrieved_documents):
        # 1. Format the retrieved document chunks into a single string
        context_str = "\n\n".join([f"Source {i+1}:\n{doc}" for i, doc in enumerate(retrieved_documents)])
        
        # 2. Build a structured prompt combining context and question
        rag_prompt = f"""Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, say that you don't know.

CONTEXT:
{context_str}

QUESTION:
{user_question}"""
        cleaned_prompt = rag_prompt.strip()
        self.history.append({"role": "user", "content": cleaned_prompt})
        
        response = self.client.chat.completions.create(
            model="apple-foundationmodel",
            messages=self.history
        )
        
        # Initialize an empty string to accumulate the complete response for history
        assistant_response = response.choices[0].message.content
        
        # Append the full compiled message to history only AFTER the stream ends
        self.history.append({"role": "assistant", "content": assistant_response})
        return assistant_response