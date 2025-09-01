#!/usr/bin/env python3
"""
演示 OpenAI Embeddings API 响应结构
"""
import os
from openai import OpenAI

# 设置API密钥（示例）
client = OpenAI(api_key="your_api_key_here")

def demonstrate_embedding_response():
    """演示embedding响应的数据结构"""
    
    print("=== 单个文本的情况 ===")
    single_text = "KerryZheng变成了什么？"
    
    result_single = client.embeddings.create(
        model="text-embedding-3-small",
        input=single_text  # 传入单个字符串
    )
    
    print(f"输入文本: {single_text}")
    print(f"result.data 的长度: {len(result_single.data)}")
    print(f"result.data[0].index: {result_single.data[0].index}")
    print(f"result.data[0].embedding 的维度: {len(result_single.data[0].embedding)}")
    print(f"前5个向量值: {result_single.data[0].embedding[:5]}")
    
    print("\n=== 多个文本的情况 ===")
    multiple_texts = [
        "KerryZheng变成了什么？",
        "史莱姆是怎么评价美食的？",
        "故事中最好吃的菜是什么？"
    ]
    
    result_multiple = client.embeddings.create(
        model="text-embedding-3-small",
        input=multiple_texts  # 传入文本列表
    )
    
    print(f"输入文本数量: {len(multiple_texts)}")
    print(f"result.data 的长度: {len(result_multiple.data)}")
    
    for i, text in enumerate(multiple_texts):
        print(f"文本 {i}: {text}")
        print(f"  对应 result.data[{i}].index: {result_multiple.data[i].index}")
        print(f"  向量维度: {len(result_multiple.data[i].embedding)}")
        print(f"  前3个值: {result_multiple.data[i].embedding[:3]}")
    
    print("\n=== 为什么使用 data[0] ===")
    print("因为我们的 embed() 函数每次只处理一个文本:")
    print("- input 参数是单个字符串，不是列表")
    print("- 所以 result.data 只有一个元素")  
    print("- data[0] 就是我们需要的那个（也是唯一的）embedding")
    print("- .embedding 提取实际的向量数据")

def our_embed_function(text: str) -> list[float]:
    """我们项目中的 embed 函数"""
    result = client.embeddings.create(
        model="text-embedding-3-small",
        input=text  # 单个文本
    )
    
    # 详细解释每一步
    print(f"1. 输入文本: {text}")
    print(f"2. result.data 长度: {len(result.data)}")
    print(f"3. result.data[0] 是第一个（唯一的）embedding对象")
    print(f"4. result.data[0].embedding 是实际的向量，长度: {len(result.data[0].embedding)}")
    
    return result.data[0].embedding

if __name__ == "__main__":
    # 注意：这个脚本需要真实的API密钥才能运行
    print("这个示例展示了为什么我们使用 result.data[0].embedding")
    print("如果要运行，请设置真实的 OPENAI_API_KEY")
    
    # demonstrate_embedding_response()
    # our_embed_function("测试文本")
