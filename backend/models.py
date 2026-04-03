"""
Pydantic 数据模型
"""
from pydantic import BaseModel
from typing import Dict, List, Optional


class Dataset(BaseModel):
    """数据集模型"""
    path: str
    type: str
    obsm: str
    layers: str
    reference: str
    # 可选的显示名称（如果没有，使用 key）
    displayName: Optional[str] = None


class DatasetListItem(BaseModel):
    """数据集列表项（返回给前端）"""
    name: str
    displayName: str
    reference: str


class DatasetListResponse(BaseModel):
    """数据集列表响应"""
    datasets: List[DatasetListItem]


class CelltypePlotResponse(BaseModel):
    """细胞类型图响应"""
    imageUrl: str


class GenePlotsResponse(BaseModel):
    """基因表达图响应"""
    gene: str
    dataset: str
    violinUrl: str
    umapUrl: str


class ErrorResponse(BaseModel):
    """错误响应"""
    error: str
