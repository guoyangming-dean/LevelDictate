"""
文件解析模块：处理 txt 和 pdf 文件
"""
import io
import re
from typing import Tuple, Optional


def parse_txt_file(file_content: bytes) -> Tuple[bool, str, str]:
    """
    解析 TXT 文件

    Args:
        file_content: 文件字节内容

    Returns:
        (success, text_preview, full_text)
    """
    try:
        # 尝试 UTF-8 编码，失败则尝试其他编码
        try:
            text = file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = file_content.decode('latin-1')
            except UnicodeDecodeError:
                text = file_content.decode('gbk', errors='ignore')

        # 去除多余空白
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # 生成预览（前500字符）
        preview = text[:500] + "..." if len(text) > 500 else text

        return True, preview, text

    except Exception as e:
        return False, "", f"解析TXT文件失败: {str(e)}"


def parse_pdf_file(file_content: bytes) -> Tuple[bool, str, str]:
    """
    解析 PDF 文件（提取可复制文本）

    注意：第一版不支持 OCR 扫描版 PDF

    Args:
        file_content: 文件字节内容

    Returns:
        (success, text_preview, full_text)
    """
    try:
        # 使用 PyPDF2 提取文本
        from PyPDF2 import PdfReader

        reader = PdfReader(io.BytesIO(file_content))
        text_parts = []

        for page in reader.pages:
            try:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            except Exception:
                continue

        if not text_parts:
            return False, "", "PDF文件中未找到可提取的文本（可能是扫描版图片）"

        full_text = "\n".join(text_parts)

        # 清理文本
        full_text = re.sub(r'\r\n', '\n', full_text)
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)

        # 生成预览
        preview = full_text[:500] + "..." if len(full_text) > 500 else full_text

        return True, preview, full_text

    except ImportError:
        return False, "", "请安装 PyPDF2: pip install PyPDF2"
    except Exception as e:
        return False, "", f"解析PDF文件失败: {str(e)}"


def parse_file(file_content: bytes, filename: str) -> Tuple[bool, str, str]:
    """
    根据文件类型选择合适的解析方法

    Args:
        file_content: 文件字节内容
        filename: 文件名

    Returns:
        (success, text_preview, full_text)
    """
    file_ext = filename.lower().split('.')[-1]

    if file_ext == 'txt':
        return parse_txt_file(file_content)
    elif file_ext == 'pdf':
        return parse_pdf_file(file_content)
    else:
        return False, "", f"不支持的文件类型: {file_ext}，仅支持 txt 和 pdf"
