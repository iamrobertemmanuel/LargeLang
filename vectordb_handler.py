import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from utils import load_config
import numpy as np
import json
import os

config = load_config()

class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=config["chromadb"]["chromadb_path"])
        self.collection = self.client.get_or_create_collection(
            name=config["chromadb"]["collection_name"],
            metadata={"hnsw:space": "cosine"}
        )
        
        # Configure Gemini for embeddings
        genai.configure(api_key=config["gemini"]["api_key"])
        self.model = genai.GenerativeModel('embedding-001')

    def add_texts(self, texts):
        # Generate embeddings using Gemini's embedding model
        embeddings = []
        for text in texts:
            try:
                result = self.model.generate_content(text, generation_config={'temperature': 0})
                embedding = result.prompt_feedback.safety_ratings[0].probability
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error generating embedding: {str(e)}")
                # Use a zero vector as fallback
                embeddings.append([0.0] * 768)  # Standard embedding size
        
        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=[f"doc_{i}" for i in range(len(texts))]
        )

    def similarity_search(self, query, k=4):
        # Generate query embedding
        try:
            result = self.model.generate_content(query, generation_config={'temperature': 0})
            query_embedding = result.prompt_feedback.safety_ratings[0].probability
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            query_embedding = [0.0] * 768  # Fallback to zero vector
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Return results as Document objects
        return [Document(page_content=doc) for doc in results["documents"][0]]

def load_vectordb():
    return VectorDB()

class SimpleVectorDB:
    def __init__(self, db_path="chroma_db"):
        self.db_path = db_path
        self.model = genai.GenerativeModel('embedding-001')
        os.makedirs(db_path, exist_ok=True)
        self.vectors_file = os.path.join(db_path, "vectors.json")
        self.load_db()

    def load_db(self):
        if os.path.exists(self.vectors_file):
            with open(self.vectors_file, 'r') as f:
                self.db = json.load(f)
        else:
            self.db = {"texts": [], "embeddings": []}
            self.save_db()

    def save_db(self):
        with open(self.vectors_file, 'w') as f:
            json.dump(self.db, f)

    def add_texts(self, texts):
        embeddings = []
        for text in texts:
            try:
                result = self.model.generate_content(text, generation_config={'temperature': 0})
                embedding = result.prompt_feedback.safety_ratings[0].probability
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error generating embedding: {str(e)}")
                embeddings.append([0.0] * 768)
        
        self.db["texts"].extend(texts)
        self.db["embeddings"].extend(embeddings)
        self.save_db()

    def similarity_search(self, query, k=4):
        if not self.db["texts"]:
            return []

        try:
            result = self.model.generate_content(query, generation_config={'temperature': 0})
            query_embedding = result.prompt_feedback.safety_ratings[0].probability
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            query_embedding = [0.0] * 768

        similarities = []
        for doc_embedding in self.db["embeddings"]:
            similarity = np.dot(query_embedding, doc_embedding)
            similarities.append(similarity)

        # Get indices of top k similar documents
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        # Return Document objects
        return [Document(page_content=self.db["texts"][idx]) for idx in top_k_indices]

class SimpleDocument:
    def __init__(self, page_content):
        self.page_content = page_content