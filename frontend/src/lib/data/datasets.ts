// 数据集 JSON 文件操作
import fs from 'fs';
import path from 'path';

const dataDirectory = path.join(process.cwd(), 'data');
const metadataFilePath = path.join(dataDirectory, 'metadata.json');

export interface Dataset {
  path: string;
  type: string;
  obsm: string;
  layers: string;
  reference: string;
}

export interface MetadataMap {
  [key: string]: Dataset;
}

// 获取所有数据集
export async function getDatasets(): Promise<MetadataMap> {
  try {
    const fileContents = fs.readFileSync(metadataFilePath, 'utf8');
    return JSON.parse(fileContents);
  } catch (error) {
    console.error('读取数据集失败:', error);
    return {};
  }
}

// 获取数据集名称列表
export async function getDatasetNames(): Promise<string[]> {
  const datasets = await getDatasets();
  return Object.keys(datasets);
}

// 根据名称获取单个数据集
export async function getDatasetByName(name: string): Promise<Dataset | null> {
  const datasets = await getDatasets();
  return datasets[name] || null;
}
