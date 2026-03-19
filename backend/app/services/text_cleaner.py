"""
文本清洗模块：清理和规范化文本
"""
import re
from typing import List


def remove_special_characters(text: str) -> str:
    """
    移除特殊字符，保留基本标点

    Args:
        text: 原始文本

    Returns:
        清理后的文本
    """
    # 保留字母、数字、空格、常见标点
    # 移除控制字符和特殊符号
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
    return text


def normalize_whitespace(text: str) -> str:
    """
    规范化空白字符

    Args:
        text: 原始文本

    Returns:
        规范化后的文本
    """
    # 将多个空格合并为一个
    text = re.sub(r'[ \t]+', ' ', text)
    # 将多个换行合并为两个
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 去除行首行尾空白
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    return text


def remove_numbers_as_words(text: str) -> str:
    """
    移除纯数字（但保留数字在单词中的情况）

    Args:
        text: 原始文本

    Returns:
        处理后的文本
    """
    # 移除独立存在的数字
    text = re.sub(r'\b\d+\b', '', text)
    return text


def clean_text(text: str) -> str:
    """
    完整文本清洗流程

    Args:
        text: 原始文本

    Returns:
        清洗后的文本
    """
    text = remove_special_characters(text)
    text = normalize_whitespace(text)
    text = remove_numbers_as_words(text)
    return text


def split_into_sentences(text: str) -> List[str]:
    """
    将文本分割成句子

    Args:
        text: 文本

    Returns:
        句子列表
    """
    # 按常见句末标点分割
    sentences = re.split(r'[.!?]+', text)
    # 过滤空句子
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences
