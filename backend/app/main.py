"""
FastAPI 后端入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.routes import router

# 创建 FastAPI 应用
app = FastAPI(
    title="LevelDictate API",
    description="英语学习 - 词汇抽取与听写练习系统",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（生产环境应限制）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api", tags=["dictation"])


@app.get("/")
async def root():
    """
    根路径
    """
    return {
        "message": "Welcome to LevelDictate API",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
