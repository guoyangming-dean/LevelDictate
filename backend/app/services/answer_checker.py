"""
答案判定模块：判分和结果返回
"""
from typing import List
from ..models.schemas import (
    DictationItem,
    AnswerResult,
    AnswerCheckResponse
)


def check_answers(
    dictation_items: List[DictationItem],
    user_answers: List[str]
) -> AnswerCheckResponse:
    """
    判定用户答案

    Args:
        dictation_items: 听写题目列表
        user_answers: 用户答案列表

    Returns:
        判分结果
    """
    results = []
    correct_count = 0

    # 确保答案数量与题目数量一致
    min_len = min(len(dictation_items), len(user_answers))

    for i in range(min_len):
        item = dictation_items[i]
        user_answer = user_answers[i].strip().lower() if user_answers[i] else ""
        correct_answer = item.word.lower()

        # 判断是否正确（精确匹配）
        is_correct = user_answer == correct_answer

        if is_correct:
            correct_count += 1

        results.append(
            AnswerResult(
                word=item.word,
                user_answer=user_answer,
                is_correct=is_correct,
                correct_answer=correct_answer
            )
        )

    # 处理未作答的题目
    if len(dictation_items) > len(user_answers):
        for i in range(len(user_answers), len(dictation_items)):
            item = dictation_items[i]
            results.append(
                AnswerResult(
                    word=item.word,
                    user_answer="",
                    is_correct=False,
                    correct_answer=item.word.lower()
                )
            )

    total_count = len(dictation_items)
    accuracy = round(correct_count / total_count * 100, 1) if total_count > 0 else 0.0

    return AnswerCheckResponse(
        success=True,
        results=results,
        correct_count=correct_count,
        total_count=total_count,
        accuracy=accuracy
    )


def normalize_answer(answer: str) -> str:
    """
    规范化用户答案（去除多余空白，转小写）

    Args:
        answer: 用户答案

    Returns:
        规范化后的答案
    """
    return answer.strip().lower()
