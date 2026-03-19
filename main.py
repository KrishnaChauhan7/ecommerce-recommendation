import os
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "Backend.env")
load_dotenv(dotenv_path=env_path)
# -----------------------------------
# 🚀 Initialize FastAPI App
# -----------------------------------
app = FastAPI(title="Walmart Product Recommendation API")

# -----------------------------------
# 🌐 Enable CORS
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# 🔑 Pinecone Setup
# -----------------------------------
print("🔄 Connecting to Pinecone...")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("product-recommendation")  # your index name


# -----------------------------------
# 📦 Load Product Data (optional but useful)
# -----------------------------------
print("🔄 Loading product data...")
df = pd.read_pickle("product_data.pkl")

# Clean image URLs
df["Product Image Url"] = (
    df["Product Image Url"]
    .astype(str)
    .str.replace('\\"', '', regex=False)
    .str.replace('"', '', regex=False)
    .str.strip()
)

df.fillna({
    "Product Name": "Unknown",
    "Product Price": 0,
    "Product Rating": 0,
    "Product Image Url": ""
}, inplace=True)

# -----------------------------------
# 🤖 Load Model
# -----------------------------------
print("🔄 Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------
# 🧠 Recommendation Function (PINECONE)
# -----------------------------------
def recommend_products(query: str, top_n: int = 8):

    # Convert query → embedding
    query_vector = model.encode(query).tolist()

    # Query Pinecone (only need IDs)
    results = index.query(
        vector=query_vector,
        top_k=top_n,
        include_metadata=False
    )

    recommendations = []

    for match in results["matches"]:
        idx = int(match["id"])  # 👈 KEY CHANGE

        product = df.iloc[idx]  # 👈 fetch from dataframe

        recommendations.append({
            "Product Name": product["Product Name"],
            "Product Price": product["Product Price"],
            "Product Rating": product["Product Rating"],
            "Product Image Url": product["Product Image Url"],
            "score": match["score"]
        })

    return recommendations

# -----------------------------------
# 📡 API Endpoints
# -----------------------------------

@app.get("/")
def home():
    return {"message": "🚀 API is running with Pinecone!"}


@app.get("/recommend")
def recommend(
    query: str = Query(...),
    top_n: int = Query(5)
):
    try:
        recommendations = recommend_products(query, top_n)

        return {
            "query": query,
            "count": len(recommendations),
            "recommendations": recommendations
        }

    except Exception as e:
        return {"error": str(e)}