import os
import chromadb
from sentence_transformers import SentenceTransformer
from cloneRepo import clone_repo, list_code_files
from chunkFile import chunk_file
from urllib.parse import urlparse

def get_repo_name(repo_url):
    path = urlparse(repo_url).path
    return path.rstrip("/").split("/")[-1].replace(".git", "")

def index_codebase(repo_url, branch="main"):
    # Temp folder for repo
    repo_name = get_repo_name(repo_url)
    repo_dir = f"./repos/{repo_name}"  # unique folder per repo
    os.makedirs("./repos", exist_ok=True)

    # Step 1: Clone
    clone_repo(repo_url, repo_dir)

    # Step 2: Prepare Chroma
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="codebase")

    # Step 3: Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 4: Process files
    for file_path in list_code_files(repo_dir):
        chunks = chunk_file(file_path)
        for idx, chunk in enumerate(chunks):
            embedding = model.encode(chunk["content"]).tolist()
            doc_id = f"{file_path}-{idx}"
            collection.add(
              ids=[doc_id],
              embeddings=[embedding],
              metadatas=[{
                  "file_path": str(chunk.get("file_path", "")),
                  "start_line": int(chunk.get("start_line") or -1),
                  "end_line": int(chunk.get("end_line") or -1)
              }],
              documents=[chunk["content"] or ""]
            )
    print("✅ Indexing complete")
