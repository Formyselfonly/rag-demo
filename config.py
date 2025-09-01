import dotenv
import os

# 加载.env文件
dotenv.load_dotenv()

class Config():
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")  # 默认使用OpenAI的embedding模型
        self.LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")  # 默认使用GPT-3.5-turbo

config = Config()