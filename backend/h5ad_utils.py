"""
h5ad 数据处理工具模块
"""
import numpy as np
import scanpy as sc
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.axes import Axes

matplotlib.use('Agg')  # 非交互式后端
from pathlib import Path
from typing import Optional, Tuple

from config import OUTPUTS_DIR
from data_loader import get_dataset

# 内存缓存：数据集名称 -> adata 对象
_data_cache = {}


def load_h5ad(dataset_name: str) -> sc.AnnData:
    """
    加载 h5ad 文件（带缓存）

    Args:
        dataset_name: 数据集名称

    Returns:
        sc.AnnData:  AnnData 对象

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 数据集配置不存在
    """
    # 检查缓存
    if dataset_name in _data_cache:
        return _data_cache[dataset_name]

    # 获取数据集配置
    dataset = get_dataset(dataset_name)
    if not dataset:
        raise ValueError(f"Dataset '{dataset_name}' not found in metadata")

    # 读取文件
    file_path = dataset.path
    if not Path(file_path).exists():
        raise FileNotFoundError(f"h5ad file not found: {file_path}")

    adata = sc.read(file_path)

    # 清空 uns 避免序列化问题
    adata.uns = {}

    # 提取降维坐标到 obs（方便绘图）
    if dataset.obsm in adata.obsm:
        adata.obs['RD1'] = adata.obsm[dataset.obsm][:, 0]
        adata.obs['RD2'] = adata.obsm[dataset.obsm][:, 1]

    # 设置细胞类型分类（保持原有顺序）
    if dataset.type in adata.obs:
        celltype_col = dataset.type
        lst_order = adata.obs[celltype_col].unique()
        adata.obs['celltype'] = adata.obs[celltype_col].astype('category').cat.set_categories(lst_order)

    # 存入缓存
    _data_cache[dataset_name] = adata

    return adata


def _gene_expression_values(adata: sc.AnnData, gene: str) -> np.ndarray:
    """与 scanpy 绘图一致：若存在 raw 且含该基因则取 raw 表达。"""
    if adata.raw is not None and gene in adata.raw.var_names:
        m = adata.raw[:, gene].X
    else:
        m = adata[:, gene].X
    if hasattr(m, "toarray"):
        return np.asarray(m.toarray()).ravel()
    return np.asarray(m).ravel()


def _plot_gene_embedding_umap(
    adata: sc.AnnData,
    gene: str,
    ax: Axes,
    *,
    color_map: str = "viridis",
    title: Optional[str] = None,
) -> None:
    """
    基因表达散点图；用 matplotlib.colorbar(ax=...) 把 colorbar 放在主坐标轴右侧。
    """
    expr = _gene_expression_values(adata, gene)
    x = adata.obs["RD1"].to_numpy()
    y = adata.obs["RD2"].to_numpy()
    order = np.argsort(expr)
    x, y, expr = x[order], y[order], expr[order]

    n = adata.n_obs
    pt_size = 120000.0 / max(n, 1)

    coll = ax.scatter(
        x,
        y,
        c=expr,
        cmap=color_map,
        s=pt_size,
        edgecolors="none",
        linewidths=0,
    )
    ax.set_title(title or f"{gene} Expression")
    ax.set_xlabel("RD1")
    ax.set_ylabel("RD2")

    fig = ax.figure
    fig.colorbar(coll, ax=ax, fraction=0.04, pad=0.12)


def validate_gene(adata: sc.AnnData, gene: str) -> bool:
    """
    验证基因是否存在于数据集中

    Args:
        adata: AnnData 对象
        gene: 基因名称

    Returns:
        bool: 是否存在
    """
    return gene in adata.var_names


def get_dataset_output_dir(dataset_name: str) -> Path:
    """
    获取数据集的图片输出目录

    Args:
        dataset_name: 数据集名称

    Returns:
        Path: 输出目录路径
    """
    output_dir = OUTPUTS_DIR / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_celltype_plot(dataset_name: str) -> str:
    """
    生成主细胞类型图（UMAP/t-SNE 按细胞类型着色）

    Args:
        dataset_name: 数据集名称

    Returns:
        str: 生成的图片文件名（如 'celltype.png'）
    """
    adata = load_h5ad(dataset_name)
    dataset = get_dataset(dataset_name)

    output_dir = get_dataset_output_dir(dataset_name)
    output_file = output_dir / "celltype.png"

    # 略加宽画布，左侧留给图例，避免与散点区挤在一起
    fig, ax = plt.subplots(figsize=(12, 8))

    sc.pl.scatter(
        adata,
        x='RD1',
        y='RD2',
        color='celltype',
        ax=ax,
        show=False,
        title=f"{dataset_name} - Cell Types"
    )

    # 图例放在散点图左侧：锚点取图例框的右侧中点，对齐到坐标轴左侧更负处，间距更大
    leg = ax.get_legend()
    if leg is not None:
        leg.set_loc("center right")
        leg.set_bbox_to_anchor((-0.18, 0.5), transform=ax.transAxes)

    plt.tight_layout(rect=[0.06, 0.06, 0.98, 0.94])
    plt.savefig(output_file, dpi=150, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)

    return "celltype.png"


def generate_gene_plots(dataset_name: str, gene: str) -> Tuple[str, str]:
    """
    生成基因表达图（小提琴图 + UMAP图）

    Args:
        dataset_name: 数据集名称
        gene: 基因名称

    Returns:
        Tuple[str, str]: (小提琴图文件名, UMAP图文件名)

    Raises:
        ValueError: 基因不存在
    """
    adata = load_h5ad(dataset_name)

    # 验证基因存在
    if not validate_gene(adata, gene):
        raise ValueError(f"Gene '{gene}' not found in dataset '{dataset_name}'")

    output_dir = get_dataset_output_dir(dataset_name)
    violin_file = output_dir / f"{gene}_violin.png"
    umap_file = output_dir / f"{gene}_umap.png"

    # 1. 生成小提琴图
    fig, ax = plt.subplots(figsize=(12, 6))
    sc.pl.violin(
        adata,
        [gene],
        groupby='celltype',
        ax=ax,
        show=False
    )
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(violin_file, dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 2. 生成 UMAP 图（按基因表达量着色）
    # 不用 sc.pl.scatter(ax=...)：连续色时 scanpy 的 colorbar 在自定义 ax 上常错位
    fig, ax = plt.subplots(figsize=(10, 8))
    _plot_gene_embedding_umap(
        adata, gene, ax, color_map="viridis", title=f"{gene} Expression"
    )
    plt.tight_layout()
    plt.savefig(umap_file, dpi=150, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)

    return (f"{gene}_violin.png", f"{gene}_umap.png")


def clear_cache(dataset_name: Optional[str] = None):
    """
    清除缓存（用于内存管理）

    Args:
        dataset_name: 指定数据集名称，None 则清除所有
    """
    global _data_cache
    if dataset_name:
        _data_cache.pop(dataset_name, None)
    else:
        _data_cache.clear()
