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
        setError(err instanceof Error ? err.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    }

    loadCelltypePlot();
  }, [currentDataset]);

  if (!currentDataset) {
    return (
      <div className="flex-1 min-w-0 h-full flex items-center justify-center bg-muted/20">
        <p className="text-muted-foreground">No dataset selected</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex-1 min-w-0 h-full flex items-center justify-center bg-muted/20">
        <p className="text-muted-foreground">Loading...</p>
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
        <p className="text-muted-foreground">No image</p>
      </div>
    );
  }

  return (
    <div className="flex-1 min-w-0 h-full relative">
      <Image
        src={imageUrl}
        alt={`${currentDataset} celltype plot`}
        fill
        className="object-contain"
        unoptimized // 后端动态生成，禁用 Next.js 图片优化
      />
    </div>
  );
}
