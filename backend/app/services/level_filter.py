"""
等级筛选模块：根据用户英语水平筛选词汇
"""
import json
import os
from typing import List, Dict, Set, Tuple, Optional

# CEFR 等级定义
CEFR_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

# 等级对应的筛选范围（用户选择某等级时，优先给该等级到下一等级的词）
LEVEL_RANGES = {
    'A1': ['A1', 'A2'],
    'A2': ['A2', 'B1'],
    'B1': ['B1', 'B2'],
    'B2': ['B2', 'C1'],
    'C1': ['C1', 'C2'],
    'C2': ['C2'],
}


def load_cefr_words(data_dir: str = None) -> Dict[str, List[str]]:
    """
    加载 CEFR 词汇表

    Args:
        data_dir: 数据目录路径

    Returns:
        等级到词汇的映射字典
    """
    if data_dir is None:
        # 默认路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')

    cefr_file = os.path.join(data_dir, 'cefr_words.json')

    # 如果文件不存在，返回空字典
    if not os.path.exists(cefr_file):
        return {}

    try:
        with open(cefr_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def get_level_words(cefr_data: Dict[str, List[str]], levels: List[str]) -> Set[str]:
    """
    获取指定等级的词汇集合

    Args:
        cefr_data: CEFR 词汇数据
        levels: 等级列表

    Returns:
        词汇集合
    """
    words = set()
    for level in levels:
        level_key = level.upper()
        if level_key in cefr_data:
            words.update(cefr_data[level_key])
    return words


def filter_words_by_level(
    candidate_words: List[str],
    user_level: str,
    cefr_data: Optional[Dict[str, List[str]]] = None
) -> Tuple[List[str], List[str]]:
    """
    根据用户等级筛选词汇

    Args:
        candidate_words: 候选词汇列表
        user_level: 用户选择的等级 (A1/A2/B1/B2/C1)
        cefr_data: CEFR 词汇数据

    Returns:
        (推荐词汇列表, 未能分类的词汇列表)
    """
    user_level = user_level.upper()

    if user_level not in CEFR_LEVELS:
        user_level = 'A1'  # 默认

    # 如果没有 CEFR 数据，返回所有候选词
    if not cefr_data:
        return candidate_words, []

    # 获取目标等级范围
    target_levels = LEVEL_RANGES.get(user_level, ['A1', 'A2'])
    target_words = get_level_words(cefr_data, target_levels)

    # 筛选目标等级的词
    recommended = []
    unclassified = []

    for word in candidate_words:
        word_lower = word.lower()
        if word_lower in target_words:
            recommended.append(word)
        else:
            # 检查是否在更高等级
            higher_levels = [l for l in CEFR_LEVELS if l not in target_levels]
            is_higher = False
            for hl in higher_levels:
                if word_lower in get_level_words(cefr_data, [hl]):
                    # 词太难，可以跳过或标记
                    is_higher = True
                    break
            if not is_higher:
                unclassified.append(word)

    # 如果推荐词汇太少，补充一些未分类的词
    if len(recommended) < 5 and unclassified:
        recommended.extend(unclassified[:10])
        unclassified = unclassified[10:]

    return recommended, unclassified


def get_level_name(level: str) -> str:
    """
    获取等级的中文名称

    Args:
        level: CEFR 等级

    Returns:
        中文名称
    """
    level_names = {
        'A1': '入门级',
        'A2': '初级',
        'B1': '中级',
        'B2': '中高级',
        'C1': '高级',
        'C2': '精通级',
    }
    return level_names.get(level.upper(), '未知')


def get_level_description(level: str) -> str:
    """
    获取等级描述

    Args:
        level: CEFR 等级

    Returns:
        等级描述
    """
    descriptions = {
        'A1': '能理解并使用日常用语和最基本的句子',
        'A2': '能理解最身边最常使用的句子和表达',
        'B1': '能理解日常工作、学校、休闲等常见场景的标准语句',
        'B2': '能理解具体或抽象主题的复杂文章',
        'C1': '能流利自然地表达思想，无需过多寻找词汇',
        'C2': '能轻松理解几乎所有听到或读到的内容',
    }
    return descriptions.get(level.upper(), '')
