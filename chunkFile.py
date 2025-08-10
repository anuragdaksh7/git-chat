from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_file(file_path, chunk_size=800, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️ Could not read {file_path}: {e}")
        return []

    chunks = text_splitter.split_text(content)
    return [
        {
            "file_path": str(file_path),
            "start_line": None,  # Optional: track exact lines
            "end_line": None,
            "content": chunk
        }
        for chunk in chunks
    ]
