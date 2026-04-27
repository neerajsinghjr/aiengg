from chromadb import EmbeddingFunction, Embeddings
import google.generativeai as genai


class GeminiEmbeddingFunction(EmbeddingFunction):

    def __init__(
        self,
        title: str,
        model: str,
        gemini_api_key: str,
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
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)

    def __call__(self, doc, *args, **kwargs) -> Embeddings:
        """
        Automatically create the embedding function for Gemini Gen Ai Embedding.
        :param doc: Document to be embedded.
        :param args: Arguments passed to the embedding function.
        :param kwargs: Keyword arguments passed to the embedding function.
        :return:
        """
        try:
            rslt = genai.embed_content(
                content=doc,
                model=self.model,
                title=self.title,
                task_type=self.task_type,
            )
            return rslt.get("embedding", [[]])
        except Exception as e:
            print(f"ERROR: Something Went Wrong with Exception: {e}")
            return [[]]
