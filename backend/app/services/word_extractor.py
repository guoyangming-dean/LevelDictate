"""
单词抽取模块：从文本中提取英文单词
"""
import re
from typing import List, Set


# 常见停用词（需要过滤的词）
STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
    'at', 'from', 'by', 'on', 'off', 'for', 'in', 'out', 'over', 'to',
    'into', 'with', 'about', 'against', 'between', 'through', 'during',
    'before', 'after', 'above', 'below', 'up', 'down', 'of', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'will', 'would', 'could', 'should',
    'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
    'it', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose',
    'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also',
    'now', 'here', 'there', 'any', 'much', 'as', 'him', 'her', 'its',
    'our', 'your', 'their', 'my', 'his', 'hers', 'ours', 'yours', 'theirs',
    'me', 'us', 'them', 'myself', 'yourself', 'himself', 'herself',
    'itself', 'ourselves', 'yourselves', 'themselves',
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
    'mr', 'mrs', 'ms', 'dr', 'prof', 'sir', 'madam', 'lady', 'lord',
    'etc', 'eg', 'ie', 'vs', 'via',
    'nbsp', 'amp', 'quot', 'apos', 'lt', 'gt',
}

# 常见缩写词
ABBREVIATIONS = {
    "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
    "i've", "you've", "he's", "she's", "we've", "they've",
    "i'll", "you'll", "he'll", "she'll", "we'll", "they'll",
    "i'd", "you'd", "he'd", "she'd", "we'd", "they'd",
    "don't", "doesn't", "didn't", "won't", "wouldn't", "can't", "couldn't",
    "shouldn't", "mightn't", "mustn't", "ain't", "isn't", "aren't", "wasn't", "weren't",
    "let's", "that's", "who's", "what's", "here's", "there's", "who've",
    "mr", "mrs", "ms", "dr", "prof", "st", "ave", "blvd", "co", "ltd",
    "inc", "corp", "govt", "dept", "esp", "etc", "ft", "min", "sec",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
    "mon", "tue", "wed", "thu", "fri", "sat", "sun",
}


def extract_words(text: str) -> List[str]:
    """
    从文本中提取英文单词

    Args:
        text: 输入文本

    Returns:
        单词列表（已转小写，去重）
    """
    # 使用正则提取单词（只保留纯字母的单词）
    words = re.findall(r'[a-zA-Z]+', text)

    # 转换为小写
    words = [w.lower() for w in words]

    # 过滤
    words = filter_valid_words(words)

    # 去重并保持顺序
    unique_words = list(dict.fromkeys(words))

    return unique_words


def filter_valid_words(words: List[str]) -> List[str]:
    """
    过滤无效单词

    Args:
        words: 单词列表

    Returns:
        过滤后的单词列表
    """
    valid_words = []

    for word in words:
        # 过滤长度小于2的词
        if len(word) < 2:
            continue

        # 过滤纯数字
        if word.isdigit():
            continue

        # 过滤停用词
        if word in STOPWORDS:
            continue

        # 过滤常见缩写
        if word in ABBREVIATIONS:
            continue

        # 过滤超长词（可能是错误提取）
        if len(word) > 20:
            continue

        valid_words.append(word)

    return valid_words


def get_word_frequency(text: str) -> dict:
    """
    统计单词频率

    Args:
        text: 输入文本

    Returns:
        单词频率字典
    """
    words = extract_words(text)
    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) + 1

    return freq
