// 数据集 API 路由
import { NextResponse } from 'next/server';
import { getDatasets, getDatasetNames } from '@/lib/data/datasets';

// GET /api/datasets - 获取所有数据集
export async function GET() {
  try {
    const datasets = await getDatasets();
    const names = Object.keys(datasets);
    
    return NextResponse.json({
      success: true,
      data: {
        names,
        datasets
      }
    });
  } catch (error) {
    console.error('获取数据集失败:', error);
    return NextResponse.json(
      { success: false, error: '获取数据集失败' },
      { status: 500 }
    );
  }
}
