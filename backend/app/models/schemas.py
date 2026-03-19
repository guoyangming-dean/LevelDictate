"""
Pydantic 数据模型定义
"""
from typing import List, Optional
from pydantic import BaseModel


class UploadResponse(BaseModel):
    """文件上传响应"""
    success: bool
    text_preview: str
    full_text: str
    message: str = ""


class ExtractWordsRequest(BaseModel):
    """提取单词请求"""
    text: str


class ExtractWordsResponse(BaseModel):
    """提取单词响应"""
    success: bool
    candidate_words: List[str]
    total_count: int


class DictationRequest(BaseModel):
    """听写请求"""
    candidate_words: List[str]
    user_level: str  # A1, A2, B1, B2, C1
    question_count: int  # 10, 20, 30


class DictationItem(BaseModel):
    """听写题目"""
    word: str
    display_word: str  # 用于显示的单词（可以是原形或变形）


class DictationResponse(BaseModel):
    """听写响应"""
    success: bool
    recommended_words: List[str]
    dictation_items: List[DictationItem]
    user_level: str
    question_count: int


class AnswerCheckRequest(BaseModel):
    """答案检查请求"""
    dictation_items: List[DictationItem]
    user_answers: List[str]


class AnswerResult(BaseModel):
    """单个答案结果"""
    word: str
    user_answer: str
    is_correct: bool
    correct_answer: str


class AnswerCheckResponse(BaseModel):
    """答案检查响应"""
    success: bool
    results: List[AnswerResult]
    correct_count: int
    total_count: int
    accuracy: float


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    error: str
    detail: Optional[str] = None
