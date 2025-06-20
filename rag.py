import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

class ProductRAG:
    def __init__(self, catalog_path='product_catalog.csv'):
        self.catalog = pd.read_csv(catalog_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.model.encode(self.catalog['description'].tolist(), show_progress_bar=False)

    def retrieve(self, query, top_k=2):
        query_emb = self.model.encode([query])
        sims = cosine_similarity(query_emb, self.embeddings)[0]
        top_indices = sims.argsort()[-top_k:][::-1]
        return self.catalog.iloc[top_indices]

    def answer_query(self, query):
        retrieved = self.retrieve(query)
        context = "\n".join([
            f"{row['name']}: {row['description']} (Price: ${row['price']})" for _, row in retrieved.iterrows()
        ])
        prompt = f"You are a helpful product assistant. Use the following product info to answer the question.\n\n{context}\n\nQuestion: {query}\nAnswer:"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()