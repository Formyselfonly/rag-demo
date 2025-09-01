import chunk
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
from config import config

client=OpenAI(
    api_key=config.OPENAI_API_KEY,
)
EMBEDDING_MODEL =config.EMBEDDING_MODEL
LLM_MODEL =config.LLM_MODEL


# Qdrant配置
collection_name = "rag-demo"
qdrant_client = QdrantClient(path="./qdrant_db")

# 注册程序退出时的清理函数
import atexit
atexit.register(lambda: qdrant_client.close() if qdrant_client else None)

def embed(text: str) -> list[float]:
    result = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    
    return result.data[0].embedding

def create_db() -> None:
    chunks = chunk.get_chunks()
    
    # 创建collection（如果不存在）
    try:
        # 先获取一个embedding来确定向量维度
        sample_embedding = embed(chunks[0])
        vector_size = len(sample_embedding)
        
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        print(f"Created collection '{collection_name}' with vector size {vector_size}")
    except Exception as e:
        print(f"Collection might already exist: {e}")
    
    # 添加文档
    points = []
    for idx, c in enumerate(chunks):
        print(f"Process: {c}")
        embedding = embed(c)
        points.append(PointStruct(
            id=idx,
            vector=embedding,
            payload={"text": c}
        ))
    
    qdrant_client.upsert(
        collection_name=collection_name,
        points=points
    )

def query_db(question: str) -> list[str]:
    question_embedding = embed(question)
    result = qdrant_client.query_points(
        collection_name=collection_name,
        query=question_embedding,
        limit=5
    )
    
    documents = []
    for point in result.points:
        documents.append(point.payload["text"])
    
    return documents


def main():
    question = "李小明变成了什么?"
    
    # 检查collection是否存在，如果不存在则创建
    try:
        qdrant_client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists")
    except Exception:
        print(f"Creating collection '{collection_name}'...")
        create_db()
    
    chunks = query_db(question)
    prompt = "Please answer user's question according to context\n"
    prompt += f"Question: {question}\n"
    prompt += "Context:\n"
    for c in chunks:
        prompt += f"{c}\n"
        prompt += "-------------\n"
    
    result = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    print("The Finally Prompt is:",prompt)
    print("The Finally Response is:",result.choices[0].message.content)

if __name__ == '__main__':
    main()