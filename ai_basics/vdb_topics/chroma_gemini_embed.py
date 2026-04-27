import os
import chromadb
from dotenv import load_dotenv, find_dotenv
from helpers.gemini_embed_v2 import GeminiGenAiEmbeddingFunction

env = os.environ
load_dotenv(find_dotenv())


def get_client(vdb_path: str):
    """Generate chroma db with persistent mode"""
    return chromadb.PersistentClient(path=vdb_path)


def get_gemini_embed_encoder():
    from helpers.gemini_embed import GeminiEmbeddingFunction
    """(~Obsolete) Initialize gemini embedding encoder for the app"""
    return GeminiEmbeddingFunction(
        model=env.get("GEMINI_EMBED_MODEL"),
        title=env.get("GEMINI_EMBED_TITLE"),
        gemini_api_key=env.get("GEMINI_API_KEY"),
    )


def get_gemini_embed_encoder_v2():
    """Initialize gemini embedding encoder for the app"""
    return GeminiGenAiEmbeddingFunction(
        api_key=env.get("GEMINI_API_KEY"),
        model=env.get("GEMINI_EMBED_MODEL"),
        title=env.get("GEMINI_EMBED_TITLE"),
    )


def main():
    """Main function"""
    client = get_client(vdb_path=env.get("VECTOR_DB_PATH"))
    colln = client.get_or_create_collection(
        name=env.get("VECTOR_DB_COLLN"),
        embedding_function=get_gemini_embed_encoder_v2(),
    )
    colln.add(
        documents=["Gemini 2.5 Flash is highly efficient.", "ChromaDB is a vector database."],
        ids=["id1", "id2"]
    )
    results = colln.query(
        query_texts=["How efficient is Gemini?"],
        n_results=1
    )
    print(f"Query Result: {results}")


if __name__ == "__main__":
    main()