"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useDataset } from "@/lib/contexts/DatasetContext";
import { getCelltypePlot, getImageUrl } from "@/lib/services/datasetService";

export function LeftMainArea() {
  const { currentDataset } = useDataset();
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!currentDataset) {
      setImageUrl(null);
      return;
    }

    async function loadCelltypePlot() {
      setLoading(true);
      setError(null);
      try {
        const response = await getCelltypePlot(currentDataset!);
        const fullUrl = getImageUrl(response.imageUrl);
        setImageUrl(fullUrl);
      } catch (err) {
        setError(err instanceof Error ? err.message : "加载失败");
      } finally {
        setLoading(false);
      }
    }

    loadCelltypePlot();
  }, [currentDataset]);

  if (!currentDataset) {
    return (
      <div className="flex-1 min-w-0 h-full flex items-center justify-center bg-muted/20">
        <p className="text-muted-foreground">请选择一个数据集</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex-1 min-w-0 h-full flex items-center justify-center bg-muted/20">
        <p className="text-muted-foreground">加载中...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 min-w-0 h-full flex items-center justify-center bg-muted/20">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!imageUrl) {
    return (
      <div className="flex-1 min-w-0 h-full flex items-center justify-center bg-muted/20">
        <p className="text-muted-foreground">暂无图片</p>
      </div>
    );
  }

  return (
    <div className="flex-1 min-w-0 h-full relative">
      <Image
        src={imageUrl}
        alt={`${currentDataset} 细胞类型图`}
        fill
        className="object-contain"
        unoptimized // 后端动态生成，禁用 Next.js 图片优化
      />
    </div>
  );
}
