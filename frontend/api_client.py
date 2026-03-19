"""
API 客户端：封装调用 FastAPI 后端的请求逻辑
"""
import requests
from typing import Optional, List, Dict, Any


# 后端 API 地址
API_BASE_URL = "http://localhost:8000/api"


def upload_file(file_path: str) -> Dict[str, Any]:
    """
    上传文件并解析文本

    Args:
        file_path: 文件路径

    Returns:
        API 响应结果
    """
    url = f"{API_BASE_URL}/upload"

    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        response = requests.post(url, files=files)

    return response.json()


def upload_file_content(file_content: bytes, filename: str) -> Dict[str, Any]:
    """
    上传文件内容并解析文本

    Args:
        file_content: 文件字节内容
        filename: 文件名

    Returns:
        API 响应结果
    """
    url = f"{API_BASE_URL}/upload"

    files = {'file': (filename, file_content)}
    response = requests.post(url, files=files)

    return response.json()


def extract_words(text: str) -> Dict[str, Any]:
    """
    从文本中提取候选单词

    Args:
        text: 文本内容

    Returns:
        API 响应结果
    """
    url = f"{API_BASE_URL}/extract_words"

    payload = {"text": text}
    response = requests.post(url, json=payload)

    return response.json()


def generate_dictation(
    candidate_words: List[str],
    user_level: str,
    question_count: int
) -> Dict[str, Any]:
    """
    生成听写任务

    Args:
        candidate_words: 候选词汇列表
        user_level: 用户等级 (A1/A2/B1/B2/C1)
        question_count: 题目数量 (10/20/30)

    Returns:
        API 响应结果
    """
    url = f"{API_BASE_URL}/generate_dictation"

    payload = {
        "candidate_words": candidate_words,
        "user_level": user_level,
        "question_count": question_count
    }
    response = requests.post(url, json=payload)

    return response.json()


def check_answer(
    dictation_items: List[Dict[str, str]],
    user_answers: List[str]
) -> Dict[str, Any]:
    """
    判定听写答案

    Args:
        dictation_items: 听写题目列表
        user_answers: 用户答案列表

    Returns:
        API 响应结果
    """
    url = f"{API_BASE_URL}/check_answer"

    payload = {
        "dictation_items": dictation_items,
        "user_answers": user_answers
    }
    response = requests.post(url, json=payload)

    return response.json()


def get_cefr_levels() -> Dict[str, Any]:
    """
    获取 CEFR 等级列表

    Returns:
        API 响应结果
    """
    url = f"{API_BASE_URL}/cefr_levels"
    response = requests.get(url)

    return response.json()


def health_check() -> Dict[str, Any]:
    """
    健康检查

    Returns:
        API 响应结果
    """
    url = f"{API_BASE_URL}/health"
    response = requests.get(url)

    return response.json()
