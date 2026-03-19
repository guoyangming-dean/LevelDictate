"""
API 路由定义
"""
import os
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from ..models.schemas import (
    UploadResponse,
    ExtractWordsRequest,
    ExtractWordsResponse,
    DictationRequest,
    DictationResponse,
    DictationItem,
    AnswerCheckRequest,
    AnswerCheckResponse,
    ErrorResponse
)
from ..services.file_parser import parse_file
from ..services.text_cleaner import clean_text
from ..services.word_extractor import extract_words
from ..services.level_filter import filter_words_by_level, load_cefr_words
from ..services.dictation_service import generate_dictation_task, shuffle_dictation
from ..services.answer_checker import check_answers


router = APIRouter()

# 加载 CEFR 词汇数据
CEFR_DATA = None


def get_cefr_data():
    """获取 CEFR 词汇数据（延迟加载）"""
    global CEFR_DATA
    if CEFR_DATA is None:
        CEFR_DATA = load_cefr_words()
    return CEFR_DATA


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件并解析文本

    Args:
        file: 上传的文件

    Returns:
        解析结果和文本预览
    """
    try:
        # 读取文件内容
        content = await file.read()

        # 解析文件
        success, preview, full_text = parse_file(content, file.filename)

        if not success:
            return UploadResponse(
                success=False,
                text_preview="",
                full_text="",
                message=full_text  # 错误信息
            )

        # 清洗文本
        cleaned_text = clean_text(full_text)

        return UploadResponse(
            success=True,
            text_preview=preview,
            full_text=cleaned_text,
            message="文件解析成功"
        )

    except Exception as e:
        return UploadResponse(
            success=False,
            text_preview="",
            full_text="",
            message=f"处理文件时出错: {str(e)}"
        )


@router.post("/extract_words", response_model=ExtractWordsResponse)
async def extract_candidate_words(request: ExtractWordsRequest):
    """
    从文本中提取候选单词

    Args:
        request: 包含文本的请求

    Returns:
        候选词汇列表
    """
    try:
        text = request.text

        if not text or len(text.strip()) == 0:
            return ExtractWordsResponse(
                success=False,
                candidate_words=[],
                total_count=0
            )

        # 清洗文本
        cleaned_text = clean_text(text)

        # 提取单词
        words = extract_words(cleaned_text)

        return ExtractWordsResponse(
            success=True,
            candidate_words=words,
            total_count=len(words)
        )

    except Exception as e:
        return ExtractWordsResponse(
            success=False,
            candidate_words=[],
            total_count=0
        )


@router.post("/generate_dictation", response_model=DictationResponse)
async def generate_dictation(request: DictationRequest):
    """
    生成听写任务

    Args:
        request: 听写请求

    Returns:
        听写任务和推荐词汇
    """
    try:
        candidate_words = request.candidate_words
        user_level = request.user_level
        question_count = request.question_count

        # 验证题目数量
        if question_count not in [10, 20, 30]:
            question_count = 10

        # 验证用户等级
        valid_levels = ['A1', 'A2', 'B1', 'B2', 'C1']
        if user_level not in valid_levels:
            user_level = 'A1'

        if not candidate_words:
            return DictationResponse(
                success=False,
                recommended_words=[],
                dictation_items=[],
                user_level=user_level,
                question_count=question_count
            )

        # 获取 CEFR 数据
        cefr_data = get_cefr_data()

        # 根据等级筛选词汇
        recommended, _ = filter_words_by_level(
            candidate_words,
            user_level,
            cefr_data
        )

        # 如果推荐词汇不够，从候选词中补充
        if len(recommended) < question_count:
            remaining = [w for w in candidate_words if w not in recommended]
            recommended.extend(remaining[:question_count - len(recommended)])

        # 生成听写任务
        dictation_items = generate_dictation_task(
            recommended,
            question_count
        )

        # 打乱顺序
        dictation_items = shuffle_dictation(dictation_items)

        return DictationResponse(
            success=True,
            recommended_words=recommended,
            dictation_items=dictation_items,
            user_level=user_level,
            question_count=len(dictation_items)
        )

    except Exception as e:
        return DictationResponse(
            success=False,
            recommended_words=[],
            dictation_items=[],
            user_level=request.user_level,
            question_count=request.question_count
        )


@router.post("/check_answer", response_model=AnswerCheckResponse)
async def check_dictation_answer(request: AnswerCheckRequest):
    """
    判定听写答案

    Args:
        request: 答案检查请求

    Returns:
        判分结果
    """
    try:
        dictation_items = request.dictation_items
        user_answers = request.user_answers

        if not dictation_items:
            return AnswerCheckResponse(
                success=False,
                results=[],
                correct_count=0,
                total_count=0,
                accuracy=0.0
            )

        # 判分
        result = check_answers(dictation_items, user_answers)

        return result

    except Exception as e:
        return AnswerCheckResponse(
            success=False,
            results=[],
            correct_count=0,
            total_count=0,
            accuracy=0.0
        )


@router.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "ok", "message": "Backend is running"}


@router.get("/cefr_levels")
async def get_cefr_levels():
    """
    获取支持的 CEFR 等级列表
    """
    return {
        "levels": [
            {"code": "A1", "name": "入门级", "description": "能理解并使用日常用语和最基本的句子"},
            {"code": "A2", "name": "初级", "description": "能理解最身边最常使用的句子和表达"},
            {"code": "B1", "name": "中级", "description": "能理解日常工作、学校、休闲等常见场景的标准语句"},
            {"code": "B2", "name": "中高级", "description": "能理解具体或抽象主题的复杂文章"},
            {"code": "C1", "name": "高级", "description": "能流利自然地表达思想，无需过多寻找词汇"},
        ]
    }
