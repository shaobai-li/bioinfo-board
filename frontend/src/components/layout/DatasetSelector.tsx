"use client";

import { useEffect, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getDatasets, Dataset } from "@/lib/services/datasetService";
import { useDataset } from "@/lib/contexts/DatasetContext";

export function DatasetSelector() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const { currentDataset, setCurrentDataset } = useDataset();

  useEffect(() => {
    async function fetchDatasets() {
      try {
        const data = await getDatasets();
        setDatasets(data);
      } catch (error) {
        console.error("获取数据集列表失败:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchDatasets();
  }, []);

  const handleSelect = (value: string) => {
    setCurrentDataset(value);
  };

  return (
    <div className="w-1/2 px-4 py-4">
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium text-foreground whitespace-nowrap">
          Dataset:
        </label>
        <Select
          disabled={loading}
          value={currentDataset || ""}
          onValueChange={handleSelect}
        >
          <SelectTrigger className="flex-1">
            <SelectValue placeholder={loading ? "Loading..." : "Select Dataset..."} />
          </SelectTrigger>
          <SelectContent>
            {datasets.map((dataset) => (
              <SelectItem key={dataset.name} value={dataset.name}>
                {dataset.displayName}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
