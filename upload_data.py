import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv

# -----------------------------------
# 🔐 Load API key
# -----------------------------------
env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(env_path)

api_key = os.getenv("PINECONE_API_KEY")

# -----------------------------------
# 🔑 Connect to Pinecone
# -----------------------------------
print("🔄 Connecting to Pinecone...")
pc = Pinecone(api_key=api_key)
index = pc.Index("product-recommendation")

# -----------------------------------
# 📦 Load Data
# -----------------------------------
print("🔄 Loading data...")
df = pd.read_pickle("product_data.pkl")

# -----------------------------------
# 🤖 Load Model
# -----------------------------------
print("🔄 Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------
# 🧠 Create Embeddings
# -----------------------------------
print("🔄 Creating embeddings...")
product_names = df["Product Name"].astype(str).tolist()
embeddings = model.encode(product_names)

# -----------------------------------
# 📤 Upload to Pinecone
# -----------------------------------
print("🔄 Uploading to Pinecone in batches...")

vectors = []
for i, emb in enumerate(embeddings):
    vectors.append((str(i), emb.tolist()))

batch_size = 100  # 👈 important

for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    index.upsert(batch)
    print(f"✅ Uploaded batch {i} to {i + batch_size}")

print("🎉 All data uploaded successfully!")