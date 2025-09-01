import streamlit as st
import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.getcwd())

# 导入我们的RAG模块
from embed import query_db, qdrant_client, collection_name, create_db
from openai import OpenAI
from config import config

# 配置页面
st.set_page_config(
    page_title="llm+rag+qdrant+streamlit ChatBot Demo",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化OpenAI客户端
@st.cache_resource
def init_openai_client():
    return OpenAI(api_key=config.OPENAI_API_KEY)

client = init_openai_client()

# 初始化数据库
@st.cache_resource
def init_database():
    try:
        qdrant_client.get_collection(collection_name)
        st.success("✅ 数据库已就绪")
        return True
    except Exception:
        st.info("🔄 正在初始化数据库...")
        try:
            create_db()
            st.success("✅ 数据库创建成功")
            return True
        except Exception as e:
            st.error(f"❌ 数据库初始化失败: {e}")
            return False

# RAG查询函数
def get_rag_response(question: str) -> str:
    try:
        # 获取相关文档
        chunks = query_db(question)
        
        # 构建提示词
        prompt = f"""你是一个专业的AI助手，请根据提供的上下文信息来回答用户的问题。

问题: {question}

相关信息:
"""
        for i, chunk in enumerate(chunks, 1):
            prompt += f"\n--- 信息片段 {i} ---\n{chunk}\n"
        
        prompt += "\n请基于以上信息回答问题。如果信息不足以回答问题，请诚实地说明。"
        
        # 调用OpenAI API
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是一个友好、专业的AI助手，擅长根据提供的信息回答问题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"抱歉，处理您的问题时出现了错误: {str(e)}"

# 主应用
def main():
    # 标题和描述
    st.title("🍽️ 史莱姆美食评论家 ChatBot")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("📋 应用信息")
        st.markdown("""
        **功能特点:**
        - 🤖 基于RAG的智能问答
        - 🔍 向量数据库检索
        - 💬 实时对话体验
        - 📚 史莱姆美食故事知识库
        """)
        
        st.header("🛠️ 系统状态")
        db_status = init_database()
        
        if db_status:
            st.success("🟢 系统正常运行")
        else:
            st.error("🔴 系统初始化失败")
            st.stop()
        
        st.header("📊 使用统计")
        if "message_count" not in st.session_state:
            st.session_state.message_count = 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("对话次数", st.session_state.message_count)
        with col2:
            total_messages = len(st.session_state.get("messages", []))
            st.metric("总消息数", total_messages)
        
        # 示例问题
        st.header("💡 示例问题")
        example_questions = [
            "KerryZheng变成了什么？",
            "史莱姆是怎么评价美食的？",
            "故事中最好吃的菜是什么？",
            "KerryZheng之前是做什么工作的？",
            "史莱姆的身体会有什么变化？"
        ]
        
        for question in example_questions:
            if st.button(f"❓ {question}", key=f"example_{question}", use_container_width=True):
                # 模拟用户输入
                st.session_state.user_question = question
                st.rerun()
        
        st.markdown("---")
        
        # 清空聊天历史按钮
        if st.button("🗑️ 清空聊天记录", type="secondary"):
            st.session_state.messages = []
            st.session_state.message_count = 0
            st.rerun()
    
    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "你好！我是史莱姆美食评论家的AI助手 🍽️✨\n\n你可以问我关于KerryZheng的史莱姆冒险故事的任何问题！比如：\n- KerryZheng变成了什么？\n- 史莱姆是怎么评价美食的？\n- 故事中最好吃的菜是什么？",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
        ]
    
    # 显示聊天历史
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(f"⏰ {message['timestamp']}")
    
    # 处理示例问题
    if "user_question" in st.session_state:
        prompt = st.session_state.user_question
        del st.session_state.user_question
    else:
        prompt = None
    
    # 用户输入
    if not prompt:
        prompt = st.chat_input("请输入您的问题...")
    
    if prompt:
        # 添加用户消息
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"⏰ {timestamp}")
        
        # 生成并显示AI回复
        with st.chat_message("assistant"):
            with st.spinner("🤔 正在思考..."):
                response = get_rag_response(prompt)
            
            st.markdown(response)
            response_timestamp = datetime.now().strftime("%H:%M:%S")
            st.caption(f"⏰ {response_timestamp}")
            
            # 添加AI消息到历史
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "timestamp": response_timestamp
            })
            
            # 更新统计
            st.session_state.message_count += 1

if __name__ == "__main__":
    main()
