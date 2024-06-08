from typing import Optional

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from app.schemas import Document


class QdrantVectorStore:
    def __init__(
        self, host_url: Optional[str] = None, collection_name: Optional[str] = None, model_name: Optional[str] = None
    ):
        self.client = QdrantClient(url=host_url)
        self.model = SentenceTransformer(model_name_or_path=model_name)
        self.collection_name = collection_name
        """
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=self.model.get_sentence_embedding_dimension(), distance=models.Distance.COSINE
            ),
        )
        """

    def add_vector(self, index: Optional[int], document: Optional[Document]):
        self.client.upload_points(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=index,
                    vector=self.model.encode("\n".join([document.title, document.description])),
                    payload=document.model_dump(),
                )
            ],
        )

    def similarity_search(self, query: Optional[str], top_k: Optional[int]):
        retrieved_documents = self.client.search(
            collection_name=self.collection_name, query_vector=self.model.encode(query), limit=top_k
        )

        return retrieved_documents
