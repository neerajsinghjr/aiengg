import asyncio
import chromadb


VDB_DIR = "./vdb"
TEST_COLLN = "test_colln"
TEST_COLLN_001 = "test_colln_001"
TEST_COLLN_002 = "test_colln_002"


def chroma_in_memory_client():
    """Chroma client with In-Memory vector collection but goes out of scope when program terminates."""
    client = chromadb.Client()

    # creating collection;;
    colln = client.get_or_create_collection("test_colln_001")

    # adding data to collection;;
    colln.add(
        ids=["id1", "id2"],
        documents=[
            "This is a test record for first collection",
            "Hello World, my first collection is live now...",
        ],
    )

    # querying a record;;
    rslt = colln.query(query_texts="Hello World, Neeraj this side ...")
    print(f" Chroma In-Memory Results: {rslt}")
    """
    {
        'ids': [['id2', 'id1']], 
        'embeddings': None, 
        'documents': [[
            'Hello World, my first collection is live now...', 
            'This is a test record for first collection'
        ]], 
        'uris': None, 
        'included': ['metadatas', 'documents', 'distances'], 
        'data': None, 
        'metadatas': [[None, None]], 
        'distances': [[1.4304147958755493, 1.907928228378296]]
    }
    """


def chroma_persisent_client():
    """Persistent clients are those where database stays intact even after the program terminates."""
    client = chromadb.PersistentClient(VDB_DIR)
    colln = client.get_or_create_collection(TEST_COLLN_002)
    colln.add(
        ids=["id1", "id2"],
        documents=[
            "This is a test record for first collection",
            "Hello World, my first collection is live now...",
        ],
    )
    rslt = colln.query(query_texts="Hello World, Neeraj this side ...")
    print(f"Chroma Persistent Client: {rslt}")


def chroma_http_server_client():
    """ Chroma Http Server is a http server.
        First run:
            $chrome run --path ai_basics/vdb_topics/vdb
    """
    client = chromadb.HttpClient(host="localhost", port=8000)
    colln = client.get_or_create_collection("test_colln_002")
    rslt = colln.query(query_texts="Hello World, Neeraj this side ...")
    print(f"Chroma Http Server Client: {rslt}")


async def chroma_async_http_server_client():
    """ Chroma Async Http Server is an Asynchronous http server.
        First run:
            $chrome run --path ai_basics/vdb_topics/vdb
        """
    client = await chromadb.AsyncHttpClient(host="localhost", port=8000)
    colln = await client.get_or_create_collection("test_colln_002")
    rslt = await colln.query(query_texts="Hello World, Neeraj this side ...")
    print(f"Chroma Async Http Server Client: {rslt}")


if __name__ == "__main__":
    # chroma_in_memory_client()
    # chroma_persisent_client()
    # chroma_http_server_client()
    asyncio.run(chroma_async_http_server_client())
