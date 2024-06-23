from typing import Dict, List, Optional

from pinecone_text.sparse import BM25Encoder
from pyvi.ViTokenizer import tokenize
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from app.schemas import Document


class QdrantVectorStore:
    def __init__(
        self,
        host_url: Optional[str] = None,
        collection_name: Optional[str] = None,
        model_name: Optional[str] = None,
        is_segmented: Optional[bool] = None,
        bm25_parameter_path: Optional[str] = None,
        top_k: Optional[int] = None,
    ):
        self.client = QdrantClient(url=host_url)
        self.model = SentenceTransformer(model_name_or_path=model_name)
        self.collection_name = collection_name
        self.is_segmented = is_segmented
        self.bm25_encoder = BM25Encoder.default().load(bm25_parameter_path)
        self.top_k = top_k

        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "text-dense": models.VectorParams(
                        size=self.model.get_sentence_embedding_dimension(),  # OpenAI Embeddings
                        distance=models.Distance.COSINE,
                    )
                },
                sparse_vectors_config={
                    "text-sparse": models.SparseVectorParams(
                        index=models.SparseIndexParams(
                            on_disk=False,
                        )
                    )
                },
            )

    def add_vector(self, index: Optional[int], document: Optional[Document]):

        return

    def hybrid_search(self, search_query: Optional[str]):

        sparse_embedding = self.bm25_encoder.encode_queries(search_query)
        dense_embedding = self.model.encode(tokenize(search_query))

        dense_result, sparse_result = self.client.search_batch(
            collection_name="medical-qa",
            requests=[
                models.SearchRequest(
                    vector=models.NamedVector(
                        name="text-dense",
                        vector=dense_embedding,
                    ),
                    limit=10,
                    with_payload=True,
                ),
                models.SearchRequest(
                    vector=models.NamedSparseVector(
                        name="text-sparse",
                        vector=models.SparseVector(
                            indices=sparse_embedding["indices"],
                            values=sparse_embedding["values"],
                        ),
                    ),
                    limit=10,
                    with_payload=True,
                ),
            ],
        )

        total_result = dense_result + sparse_result

        rank_fusion_scores = self.rank_fusion(dense_search_result=dense_result, sparse_search_result=sparse_result)
        rank_list = list(self.ranking(rank_fusion_scores=rank_fusion_scores).keys())
        retrieved_documents = self.mapping_document(rank_list=rank_list, total_result=total_result)
        return retrieved_documents

    def rank_fusion(
        self, dense_search_result: List[models.PointStruct], sparse_search_result: List[models.PointStruct]
    ):

        rank_fusion_scores = {}

        for index, dense_result in enumerate(dense_search_result):

            if dense_result.id not in rank_fusion_scores:
                rank_fusion_scores[dense_result.id] = (len(dense_search_result) - index) / len(dense_search_result)

        for index, sparse_result in enumerate(sparse_search_result):
            if sparse_result.id not in rank_fusion_scores:
                rank_fusion_scores[sparse_result.id] = (len(sparse_search_result) - index) / len(sparse_search_result)

            else:
                rank_fusion_scores[sparse_result.id] += (len(sparse_search_result) - index) / len(sparse_search_result)

        return rank_fusion_scores

    def ranking(self, rank_fusion_scores: Dict[int, float]):
        sorted_fusion_score = dict(sorted(rank_fusion_scores.items(), key=lambda item: item[1], reverse=True))
        return sorted_fusion_score

    def mapping_document(self, rank_list: Dict[int, float], total_result: List[models.PointStruct]):
        retrieved_documents = []

        for rank in rank_list[: self.top_k]:

            for point in total_result:
                if point.id == rank:
                    retrieved_documents.append(point.payload["content"])

        return retrieved_documents
