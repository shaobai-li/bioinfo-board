"""
FastAPI 主入口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

from config import APP_HOST, APP_PORT, CORS_ORIGINS, OUTPUTS_DIR

app = FastAPI(
    title="Bioinfo Board API",
    description="生信数据可视化后端 API",
    version="1.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """根路径 - 健康检查"""
    return {"message": "Bioinfo Board API is running"}


@app.get("/api/datasets")
def get_datasets():
    """获取数据集列表"""
    # TODO: 读取 metadata.json 返回数据集列表
    pass


@app.get("/api/datasets/{name}/celltype")
def get_celltype_plot(name: str):
    """获取主细胞类型图"""
    # TODO: 生成或返回主细胞类型图
    pass


@app.get("/api/datasets/{name}/gene/{gene}")
def get_gene_plots(name: str, gene: str):
    """获取基因表达图（小提琴图 + UMAP图）"""
    # TODO: 生成基因表达图
    pass


@app.get("/api/images/{dataset}/{filename}")
def get_image(dataset: str, filename: str):
    """代理访问图片文件"""
    # TODO: 返回图片文件
    pass


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
