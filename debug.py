import chromadb

# Connect to your persistent Chroma DB
client = chromadb.PersistentClient(path="./chroma_db")

# List all collections
collections = client.list_collections()
print("\n📂 Collections in DB:")
for col in collections:
    print(f" - {col.name}")

# Pick a collection (change name if needed)
collection_name = "codebase"
collection = client.get_collection(collection_name)

# Get total number of entries
count = collection.count()
print(f"\n📊 Collection '{collection_name}' contains {count} documents.")

# Fetch a few sample entries
print("\n🔍 Sample entries:")
results = collection.peek(limit=5)  # small preview
for i, (doc, meta) in enumerate(zip(results["documents"], results["metadatas"]), start=1):
    print(f"\n--- Document {i} ---")
    print(f"Metadata: {meta}")
    print(f"Content Preview: {doc[:200]}...")  # first 200 chars

# Optional: search test
query = "function to fetch user data"
search_results = collection.query(query_texts=[query], n_results=3)
print("\n🔎 Search results for:", query)
for doc, meta, dist in zip(
    search_results["documents"][0],
    search_results["metadatas"][0],
    search_results["distances"][0],
):
    print(f"- File: {meta.get('file_path', 'unknown')}, Distance: {dist:.4f}")
    print(f"  Snippet: {doc[:150]}...\n")
