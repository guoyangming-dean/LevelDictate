# LevelDictate - 英语听写练习系统

基于用户自有英文材料的个性化词汇抽取 + 听写练习系统

## 项目简介

本项目是一个前后端分离的英语学习 Web 应用：
- **前端**: Streamlit
- **后端**: FastAPI

核心功能：
1. 上传英文学习材料（PDF/TXT）
2. 自动解析文本并提取英文词汇
3. 根据用户选择的 CEFR 等级筛选适合的词汇
4. 生成听写练习任务
5. 自动判分并返回正确率

## 项目结构

```
LevelDictate/
├── backend/               # FastAPI 后端
│   ├── app/
│   │   ├── main.py       # FastAPI 入口
│   │   ├── routers/      # API 路由
│   │   ├── services/     # 业务逻辑
│   │   │   ├── file_parser.py       # 文件解析
│   │   │   ├── text_cleaner.py      # 文本清洗
│   │   │   ├── word_extractor.py    # 单词抽取
│   │   │   ├── level_filter.py       # 等级筛选
│   │   │   ├── dictation_service.py  # 听写服务
│   │   │   └── answer_checker.py     # 答案判定
│   │   └── models/      # 数据模型
│   │       └── schemas.py
│   ├── data/            # 词汇数据
│   │   └── cefr_words.json
│   └── requirements.txt
├── frontend/            # Streamlit 前端
│   ├── app.py          # Streamlit 入口
│   ├── api_client.py   # API 客户端
│   └── requirements.txt
├── sample_data/         # 示例数据
│   └── sample.txt
└── README.md
```

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd LevelDictate
```

### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 安装前端依赖

```bash
cd frontend
pip install -r requirements.txt
```

### 4. 启动后端

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

后端启动后访问: http://localhost:8000

### 5. 启动前端

```bash
cd frontend
streamlit run app.py
```

前端启动后访问: http://localhost:8501

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/upload` | POST | 上传文件并解析 |
| `/api/extract_words` | POST | 从文本提取词汇 |
| `/api/generate_dictation` | POST | 生成听写任务 |
| `/api/check_answer` | POST | 判分 |
| `/api/health` | GET | 健康检查 |
| `/api/cefr_levels` | GET | 获取 CEFR 等级列表 |

## 使用流程

1. **上传文件**: 在前端上传 TXT 或 PDF 文件
2. **提取词汇**: 点击按钮提取候选词汇
3. **设置等级**: 在侧边栏选择英语水平（A1-C1）
4. **生成听写**: 点击生成听写任务
5. **填写答案**: 输入单词拼写
6. **查看结果**: 提交后查看得分和正确答案

## CEFR 等级说明

| 等级 | 名称 | 说明 |
|------|------|------|
| A1 | 入门级 | 能理解并使用日常用语和最基本的句子 |
| A2 | 初级 | 能理解最常使用的句子和表达 |
| B1 | 中级 | 能理解日常工作、学习等常见场景的标准语句 |
| B2 | 中高级 | 能理解具体或抽象主题的复杂文章 |
| C1 | 高级 | 能流利自然地表达思想 |

## 技术栈

- **前端**: Streamlit, Requests
- **后端**: FastAPI, Pydantic, PyPDF2
- **数据**: 本地 JSON 文件

## 注意事项

1. 第一版仅支持可复文本的 PDF（不支持 OCR 扫描版）
2. 词汇等级筛选使用预设词表，简化实现
3. 听写判分为精确匹配（忽略大小写）

## 后续扩展

- [ ] 添加 TTS 语音播放
- [ ] 支持更多文件格式
- [ ] 添加用户登录系统
- [ ] 使用更精确的 i+1 词汇筛选
- [ ] 添加错题本功能
