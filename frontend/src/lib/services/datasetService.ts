// 前端数据集服务层 - 调用 Python 后端 API

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Dataset {
  name: string;
  displayName: string;
  reference: string;
}

export interface DatasetsResponse {
  datasets: Dataset[];
}

export interface CelltypePlotResponse {
  imageUrl: string;
}

export interface GenePlotsResponse {
  gene: string;
  dataset: string;
  violinUrl: string;
  umapUrl: string;
}

// 获取所有数据集列表
export async function getDatasetNames(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/datasets`);
  if (!response.ok) {
    throw new Error("Failed to fetch datasets");
  }
  const data: DatasetsResponse = await response.json();
  return data.datasets.map((d) => d.name);
}

// 获取完整数据集列表（包含 displayName 和 reference）
export async function getDatasets(): Promise<Dataset[]> {
  const response = await fetch(`${API_BASE_URL}/api/datasets`);
  if (!response.ok) {
    throw new Error("Failed to fetch datasets");
  }
  const data: DatasetsResponse = await response.json();
  return data.datasets;
}

// 获取主细胞类型图
export async function getCelltypePlot(
  datasetName: string
): Promise<CelltypePlotResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/datasets/${datasetName}/celltype`,
    { cache: "no-store" }
  );
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error(`Dataset '${datasetName}' not found`);
    }
    throw new Error("Failed to fetch celltype plot");
  }
  return response.json();
}

// 获取基因表达图
export async function getGenePlots(
  datasetName: string,
  gene: string
): Promise<GenePlotsResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/datasets/${datasetName}/gene/${gene}`
  );
  if (!response.ok) {
    if (response.status === 404) {
      const error = await response.json();
      throw new Error(error.detail || `Gene '${gene}' not found`);
    }
    throw new Error("Failed to fetch gene plots");
  }
  return response.json();
}

// 获取完整图片 URL
export function getImageUrl(path: string): string {
  if (path.startsWith("http")) {
    return path;
  }
  return `${API_BASE_URL}${path}`;
}
