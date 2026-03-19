import faiss
import numpy as np
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

# -----------------------------------
# 🚀 Initialize FastAPI App
# -----------------------------------
app = FastAPI(title="Walmart Product Recommendation API")

# -----------------------------------
# 🌐 Enable CORS (IMPORTANT)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend (React)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# 📦 Load Data & FAISS Index
# -----------------------------------
print("🔄 Loading FAISS index...")
index = faiss.read_index("product_index.faiss")

print("🔄 Loading product data...")
df = pd.read_pickle("product_data.pkl")

# -----------------------------------
# 🧹 Clean Image URLs
# -----------------------------------
df["Product Image Url"] = (
    df["Product Image Url"]
    .astype(str)
    .str.replace('\\"', '', regex=False)
    .str.replace('"', '', regex=False)
    .str.strip()
)

# Optional: fill missing values
df.fillna({
    "Product Name": "Unknown",
    "Product Price": 0,
    "Product Rating": 0,
    "Product Image Url": ""
}, inplace=True)

# -----------------------------------
# 🤖 Load Embedding Model
# -----------------------------------
print("🔄 Loading Sentence Transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------
# 🧠 Recommendation Function
# -----------------------------------
def recommend_products(query: str, top_n: int = 5):

    # Convert query to embedding
    query_vector = model.encode([query]).astype("float32")

    # Search FAISS index
    distances, indices = index.search(query_vector, top_n)

    # Fetch products
    results = df.iloc[indices[0]]

    # Select relevant columns
    results = results[[
        "Product Name",
        "Product Price",
        "Product Rating",
        "Product Image Url"
    ]]

    return results.to_dict(orient="records")

# -----------------------------------
# 📡 API Endpoints
# -----------------------------------

# Health check
@app.get("/")
def home():
    return {"message": "🚀 API is running!"}


# Recommendation endpoint
@app.get("/recommend")
def recommend(
    query: str = Query(..., description="Search query"),
    top_n: int = Query(5, description="Number of recommendations")
):
    try:
        recommendations = recommend_products(query, top_n)

        return {
            "query": query,
            "count": len(recommendations),
            "recommendations": recommendations
        }

    except Exception as e:
        return {
            "error": str(e)
        }