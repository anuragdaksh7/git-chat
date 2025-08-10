import chromadb
from tabulate import tabulate  # pip install tabulate

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="codebase")

query = "show me cron jobs"
results = collection.query(
    query_texts=[query],
    n_results=3
)

print(f"\n🔍 Search results for: {query}\n")
if not results["ids"][0]:
    print("⚠️ No matching results found.")
else:
    rows = []
    for doc_id, meta, dist, doc in zip(
        results["ids"][0],
        results["metadatas"][0],
        results["distances"][0],
        results["documents"][0]
    ):
        rows.append([
            doc_id,
            meta.get("file_path", "unknown"),
            f"{meta.get('start_line', '?')}–{meta.get('end_line', '?')}",
            f"{dist:.4f}",
            doc[:80].replace("\n", " ") + "..."  # preview snippet
        ])

    print(tabulate(
        rows,
        headers=["ID", "File", "Lines", "Distance", "Snippet"],
        tablefmt="fancy_grid"
    ))
