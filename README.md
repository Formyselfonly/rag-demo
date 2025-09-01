# 🚀 RAG系统入门教程 - KerryZheng史莱姆美食评论家

## 📺 视频教程
> 本项目配套B站视频教程，跟着视频Code Along学习RAG基础原理！
>
> 

[郑同学是我](https://space.bilibili.com/364838313?spm_id_from=333.1007.0.0)

## 🎯 项目简介

这是一个**RAG（Retrieval-Augmented Generation）系统**的入门教学项目。通过一个有趣的"史莱姆美食评论家"故事，你将学会：

- 📚 **文档分块处理**：如何将长文档切分成合适的片段
- 🔍 **向量嵌入**：使用OpenAI的Embedding模型将文本转换为向量
- 🗄️ **向量数据库**：使用Qdrant存储和检索相似文档
- 🤖 **智能问答**：结合检索到的上下文生成准确回答
- 💬 **Web界面**：使用Streamlit创建友好的聊天界面

(以下两张图片来自LangChain官方)

![](img/rag1.png)

![](/img/rag2.png)

## 🏗️ 技术架构

```
用户问题 → Embedding → 向量检索 → 相关文档 → LLM生成 → 回答
    ↓           ↓          ↓          ↓         ↓        ↓
  Streamlit   OpenAI    Qdrant    chunk.py   GPT-4o   Web UI
```

## 📁 项目结构

```
rag-demo/
├── 📄 README.md              # 本教程文档
├── 🎬 codealong.py           # 跟练文件（视频教学用）
├── 📝 data.md                # 史莱姆故事数据
├── ⚙️ config.py              # 配置管理
├── 🔪 chunk.py               # 文档分块处理
├── 🧠 embed.py               # 核心RAG逻辑
├── 💬 app.py                 # Streamlit聊天界面
├── 🚀 run_app.py             # 应用启动脚本
├── 📊 .streamlit/config.toml # UI配置
└── 🗄️ qdrant_db/             # 向量数据库存储
```

## 🛠️ 环境准备

### 1. Python环境
```bash
# 确保Python版本 >= 3.8
python --version
```

### 2. 安装依赖
```bash
pip install openai qdrant-client streamlit python-dotenv
```

### 3. 配置API密钥
创建`.env`文件：
```env
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# 模型配置
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
```

## 📖 分步教程

### 第一步：理解数据结构
打开`data.md`查看我们的史莱姆故事：
```markdown
# 关于一只史莱姆意外成为美食评论家这件事(KerryZheng异世界冒险)

## 第一章：意外转生
KerryZheng，一个天赋异禀的程序员...
```

### 第二步：文档分块 (`chunk.py`)
```python
def get_chunks() -> list[str]:
    content = read_data()
    chunks = content.split('\n\n')  # 按空行分割
    
    result = []
    header = ""
    for c in chunks:
        if c.startswith("#"):        # 识别标题
            header += f"{c}\n"
        else:
            result.append(f"{header}{c}")  # 组合标题+内容
            header = ""
    return result
```

**核心思想**：将长文档分成有意义的小块，每块包含章节标题+内容。

### 第三步：向量嵌入 (`embed.py`)
```python
def embed(text: str, store: bool) -> list[float]:
    result = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return result.data[0].embedding
```

**核心思想**：将文本转换为1536维的向量，相似文本的向量距离更近。

### 第四步：向量数据库存储
```python
def create_db() -> None:
    chunks = chunk.get_chunks()
    
    # 创建collection
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )
    
    # 存储向量
    points = []
    for idx, c in enumerate(chunks):
        embedding = embed(c, store=True)
        points.append(PointStruct(
            id=idx,
            vector=embedding,
            payload={"text": c}
        ))
    
    qdrant_client.upsert(collection_name=collection_name, points=points)
```

### 第五步：相似性检索
```python
def query_db(question: str) -> list[str]:
    question_embedding = embed(question, store=False)
    result = qdrant_client.query_points(
        collection_name=collection_name,
        query=question_embedding,
        limit=5
    )
    
    documents = []
    for point in result.points:
        documents.append(point.payload["text"])
    
    return documents
```

**核心思想**：用问题的向量去匹配最相似的文档片段。

### 第六步：RAG生成回答
```python
def get_rag_response(question: str) -> str:
    # 1. 检索相关文档
    chunks = query_db(question)
    
    # 2. 构建提示词
    prompt = f"""你是一个专业的AI助手，请根据提供的上下文信息来回答用户的问题。

问题: {question}

相关信息:
"""
    for i, chunk in enumerate(chunks, 1):
        prompt += f"\n--- 信息片段 {i} ---\n{chunk}\n"
    
    # 3. LLM生成回答
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content
```

## 🎮 Code Along 实践

### 跟着视频一起编程！

1. **打开`codealong.py`**
2. **跟着视频逐步实现**：
   - 导入必要库
   - 创建embedding函数
   - 实现向量存储
   - 构建检索逻辑
   - 完成RAG问答

### 测试你的代码
```python
# 测试文档分块
python chunk.py

# 测试完整RAG系统
python embed.py

# 启动Web界面
streamlit run app.py
```

## 🌟 运行完整应用

### 方法1：命令行启动
```bash
streamlit run app.py
```

### 方法2：使用启动脚本
```bash
python run_app.py
```

### 访问应用
- 打开浏览器访问：`http://localhost:8501`
- 开始与KerryZheng的史莱姆故事对话！

## 💡 示例问题

试试这些问题来测试你的RAG系统：

- 🤔 "KerryZheng变成了什么？"
- 🍽️ "史莱姆是怎么评价美食的？"
- 🎮 "KerryZheng之前在干什么？"
- 🌈 "史莱姆的身体会有什么变化？"
- ⭐ "故事中最好吃的菜是什么？"

## 🔧 核心概念解析

### RAG的工作原理
1. **检索（Retrieval）**：从知识库中找到相关信息
2. **增强（Augmented）**：将检索到的信息加入到提示词中
3. **生成（Generation）**：基于增强后的提示词生成回答

### 为什么使用RAG？
- ✅ **时效性**：可以使用最新的领域知识
- ✅ **准确性**：基于具体文档生成回答，减少幻觉
- ✅ **可控性**：知道回答的来源，便于验证
- ✅ **成本效益**：无需重新训练大模型

### 向量相似性
- 使用**余弦相似度**衡量文本相似性
- 相似文本在向量空间中距离更近
- OpenAI的embedding模型训练了丰富的语义理解

## 📚 扩展学习

### 进阶优化方向
1. **分块策略优化**：
   - 滑动窗口分块
   - 语义分割
   - 重叠分块

2. **检索优化**：
   - 混合检索（向量+关键词）
   - 重排序模型
   - 多路召回

3. **生成优化**：
   - 提示词工程
   - 思维链推理
   - 多轮对话上下文

### 相关技术栈
- **向量数据库**：Pinecone, Chroma, Weaviate
- **框架**：LangChain, LlamaIndex
- **模型**：OpenAI, Anthropic, 本地模型

## 🐛 常见问题

### Q: 端口8501被占用？
A: 
```bash
# 查看占用进程
netstat -ano | findstr 8501
# 杀死进程或使用其他端口
streamlit run app.py --server.port 8502
```

### Q: OpenAI API调用失败？
A: 检查：
- `.env`文件中的API密钥是否正确
- 账户是否有足够余额
- 网络连接是否正常

### Q: 向量数据库错误？
A: 删除`qdrant_db`文件夹重新创建：
```bash
rm -rf qdrant_db  # Linux/Mac
rmdir /s qdrant_db  # Windows
```

## 👨‍💻 关于作者

**KerryZheng** - AI工程师 & 技术教育者
- 🎥 B站视频教程制作者
- 🚀 专注于AI实战项目教学
- 📧 欢迎交流学习心得

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🎉 结语

通过这个项目，你已经掌握了RAG系统的核心原理！

记住，RAG不仅仅是技术实现，更是：
- 📖 **知识管理**的新方式
- 🤖 **人机协作**的新模式  
- 🚀 **AI应用**的新范式

继续探索，在AI的世界里创造更多可能！

---

⭐ **如果这个项目对你有帮助，请给个Star支持一下！**

🔗 **相关链接**：
- [B站视频教程](#) 
- [GitHub仓库](#)
- [技术交流群](#)
