// 前端数据集服务层
// 封装数据集相关的 API 调用

export interface Dataset {
  path: string;
  type: string;
  obsm: string;
  layers: string;
  reference: string;
}

export interface DatasetsResponse {
  success: boolean;
  data?: {
    names: string[];
    datasets: { [key: string]: Dataset };
  };
  error?: string;
}

// 获取所有数据集
export async function getDatasets(): Promise<DatasetsResponse> {
  const response = await fetch('/api/datasets');
  return response.json();
}

// 获取数据集名称列表
export async function getDatasetNames(): Promise<string[]> {
  const result = await getDatasets();
  if (result.success && result.data) {
    return result.data.names;
  }
  return [];
}
