"""
后端配置文件
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent

# 数据根目录（从环境变量读取，默认为项目下的 data 目录）
DATA_ROOT = Path(os.getenv("DATA_ROOT", BASE_DIR / "data"))

# 数据目录配置
METADATA_FILE = DATA_ROOT / "metadata.json"

# 图片输出目录（仍在 backend 下）
OUTPUTS_DIR = BASE_DIR / "outputs"

# 确保目录存在
OUTPUTS_DIR.mkdir(exist_ok=True)
DATA_ROOT.mkdir(parents=True, exist_ok=True)

# FastAPI 配置
APP_HOST = "0.0.0.0"
APP_PORT = 8000

# CORS 配置（允许前端访问）
CORS_ORIGINS = [
    "http://localhost:3000",  # Next.js 开发服务器
    "http://127.0.0.1:3000",
]

# 允许任意 IPv4 地址通过 3000 端口访问（例如公网/局域网 IP）
CORS_ORIGIN_REGEX = r"^https?://(\d{1,3}\.){3}\d{1,3}:3000$"