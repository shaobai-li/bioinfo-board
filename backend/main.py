"""
FastAPI 主入口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from pathlib import Path

from config import APP_HOST, APP_PORT, CORS_ORIGINS, OUTPUTS_DIR
from data_loader import get_dataset_list, dataset_exists
from models import (
    DatasetListResponse,
    CelltypePlotResponse,
    GenePlotsResponse,
    ErrorResponse
)
from h5ad_utils import generate_celltype_plot, generate_gene_plots

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


@app.get("/api/datasets", response_model=DatasetListResponse)
def get_datasets():
    """获取数据集列表"""
    datasets = get_dataset_list()
    return DatasetListResponse(datasets=datasets)


@app.get("/api/datasets/{name}/celltype", response_model=CelltypePlotResponse)
def get_celltype_plot_endpoint(name: str):
    """
    获取主细胞类型图

    - 如果图片已存在，直接返回 URL
    - 如果不存在，生成图片后返回 URL
    """
    # 检查数据集是否存在
    if not dataset_exists(name):
        raise HTTPException(status_code=404, detail=f"Dataset '{name}' not found")

    # 检查图片是否已存在
    output_dir = OUTPUTS_DIR / name
    image_file = output_dir / "celltype.png"

    if not image_file.exists():
        # 生成图片
        try:
            generate_celltype_plot(name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate plot: {str(e)}")

    # 用文件 mtime 作为 query，避免浏览器长期缓存旧 PNG（改图后 URL 会变）
    v = int(image_file.stat().st_mtime)
    return CelltypePlotResponse(imageUrl=f"/api/images/{name}/celltype.png?v={v}")


@app.get("/api/datasets/{name}/gene/{gene}", response_model=GenePlotsResponse)
def get_gene_plots_endpoint(name: str, gene: str):
    """
    获取基因表达图（小提琴图 + UMAP图）

    - 验证基因是否存在于数据集中
    - 生成或返回小提琴图和 UMAP 图
    """
    # 检查数据集是否存在
    if not dataset_exists(name):
        raise HTTPException(status_code=404, detail=f"Dataset '{name}' not found")

    # 生成图片
    try:
        violin_file, umap_file = generate_gene_plots(name, gene)
    except ValueError as e:
        # 基因不存在
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plots: {str(e)}")

    return GenePlotsResponse(
        gene=gene,
        dataset=name,
        violinUrl=f"/api/images/{name}/{violin_file}",
        umapUrl=f"/api/images/{name}/{umap_file}"
    )


@app.get("/api/images/{dataset}/{filename}")
def get_image(dataset: str, filename: str):
    """
    代理访问图片文件

    - 从 outputs/{dataset}/{filename} 读取图片
    - 返回图片文件流
    """
    # 安全检查：防止路径遍历攻击
    if ".." in dataset or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid path")

    image_path = OUTPUTS_DIR / dataset / filename

    # 检查文件是否存在
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Image not found: {filename}")

    # 检查是否是文件
    if not image_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    return FileResponse(
        image_path,
        media_type="image/png",
        headers={"Cache-Control": "no-cache, must-revalidate"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
