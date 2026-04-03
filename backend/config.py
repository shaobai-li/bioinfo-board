"""
后端配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent

# 数据目录
DATA_DIR = BASE_DIR / "data"
METADATA_FILE = DATA_DIR / "metadata.json"

# 图片输出目录
OUTPUTS_DIR = BASE_DIR / "outputs"

# 确保输出目录存在
OUTPUTS_DIR.mkdir(exist_ok=True)

# FastAPI 配置
APP_HOST = "0.0.0.0"
APP_PORT = 8000

# CORS 配置（允许前端访问）
CORS_ORIGINS = [
    "http://localhost:3000",  # Next.js 开发服务器
    "http://127.0.0.1:3000",
]
