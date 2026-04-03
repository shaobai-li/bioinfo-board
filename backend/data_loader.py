"""
数据集加载模块
"""
import json
from typing import Dict, List, Optional
from pathlib import Path

from config import METADATA_FILE, DATA_ROOT
from models import Dataset, DatasetListItem


def resolve_data_path(relative_path: str) -> str:
    """
    将相对路径转换为绝对路径

    Args:
        relative_path: 相对于 DATA_ROOT 的路径

    Returns:
        str: 绝对路径
    """
    # 如果已经是绝对路径，直接返回
    if Path(relative_path).is_absolute():
        return relative_path

    # 拼接为绝对路径
    absolute_path = DATA_ROOT / relative_path
    return str(absolute_path.resolve())


def load_metadata() -> Dict[str, Dataset]:
    """
    加载 metadata.json，返回数据集字典
    将相对路径转换为绝对路径

    Returns:
        Dict[str, Dataset]: {数据集名称: Dataset对象}
    """
    if not Path(METADATA_FILE).exists():
        return {}

    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = {}
    for name, config in data.items():
        # 如果没有 displayName，使用 name 作为默认值
        if 'displayName' not in config:
            config['displayName'] = name

        # 将相对路径转换为绝对路径
        if 'path' in config:
            config['path'] = resolve_data_path(config['path'])

        result[name] = Dataset(**config)

    return result


def get_dataset_list() -> List[DatasetListItem]:
    """
    获取数据集列表（用于 /api/datasets 接口）

    Returns:
        List[DatasetListItem]: 数据集列表
    """
    metadata = load_metadata()
    return [
        DatasetListItem(
            name=name,
            displayName=dataset.displayName or name,
            reference=dataset.reference
        )
        for name, dataset in metadata.items()
    ]


def get_dataset(name: str) -> Optional[Dataset]:
    """
    根据名称获取单个数据集

    Args:
        name: 数据集名称

    Returns:
        Optional[Dataset]: Dataset对象，不存在则返回 None
    """
    metadata = load_metadata()
    return metadata.get(name)


def dataset_exists(name: str) -> bool:
    """
    检查数据集是否存在

    Args:
        name: 数据集名称

    Returns:
        bool: 是否存在
    """
    metadata = load_metadata()
    return name in metadata
