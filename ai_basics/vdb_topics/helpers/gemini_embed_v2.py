from chromadb import EmbeddingFunction, Embeddings
from chromadb.api.collection_configuration import validate_embedding_function_conflict_on_get
from google import genai


class GeminiGenAiEmbeddingFunction(EmbeddingFunction):

    def __init__(
        self,
        title: str,
        model: str,
        api_key: str,
        task_type: str = "retrieval_document"
    ) -> None:
        """
        Initialize the embedding function for Gemini Gen Ai Embedding.
        :param title: The title of the embedding.
        :param model: The model to use for the embedding.
        :param task_type: The type of task to use for the embedding.
        :param gemini_api_key: The gemini API key to use for the embedding.
        """
        self.title = title
        self.model = model
        self.task_type = task_type
        self.client = genai.Client(api_key=api_key)

    def __call__(self, docs, *args, **kwargs) -> Embeddings:
        """
        Automatically create the embedding function for Gemini Gen Ai Embedding.
        :param doc: Document to be embedded.
        :param args: Arguments passed to the embedding function.
        :param kwargs: Keyword arguments passed to the embedding function.
        :return:
        """
        try:
            vectors = []
            config = {
                "title": self.title,
                "task_type": self.task_type,
            }
            for doc in docs:
                rslt = self.client.models.embed_content(
                    contents=doc,
                    model=self.model,
                    config=config,
                )
                vectors.append(rslt.embeddings[0].values)
            return vectors
        except Exception as e:
            print(f"ERROR: Something Went Wrong with Exception: {e}")
            return [[]]
