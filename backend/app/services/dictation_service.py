"""
听写服务模块：生成听写任务
"""
import random
from typing import List
from ..models.schemas import DictationItem


def generate_dictation_task(
    words: List[str],
    question_count: int = 10
) -> List[DictationItem]:
    """
    生成听写任务

    Args:
        words: 推荐词汇列表
        question_count: 题目数量

    Returns:
        听写题目列表
    """
    if not words:
        return []

    # 随机选择词汇
    selected_words = random.sample(
        words,
        min(question_count, len(words))
    )

    # 生成听写题目
    dictation_items = []
    for word in selected_words:
        # TODO: 第一版只使用原形，后续可以加入词形变换
        display_word = word

        dictation_items.append(
            DictationItem(
                word=word.lower(),
                display_word=display_word
            )
        )

    return dictation_items


def shuffle_dictation(items: List[DictationItem]) -> List[DictationItem]:
    """
    打乱听写题目顺序

    Args:
        items: 听写题目列表

    Returns:
        打乱后的题目列表
    """
    shuffled = items.copy()
    random.shuffle(shuffled)
    return shuffled
