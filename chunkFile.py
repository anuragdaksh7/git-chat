from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_file(file_path, chunk_size=500, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"⚠️ Could not read {file_path}: {e}")
        return []

    content = "".join(lines)
    chunks = text_splitter.split_text(content)

    results = []
    for chunk in chunks:
        # Find where chunk starts in the original file
        chunk_start_char = content.find(chunk)
        start_line = content[:chunk_start_char].count("\n") + 1
        end_line = start_line + chunk.count("\n")

        results.append({
            "file_path": str(file_path),
            "start_line": start_line,
            "end_line": end_line,
            "content": chunk
        })

    return results
