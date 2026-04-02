"use client";

import { useEffect, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getDatasetNames } from "@/lib/services/datasetService";

export function DatasetSelector() {
  const [datasetNames, setDatasetNames] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDatasets() {
      try {
        const names = await getDatasetNames();
        setDatasetNames(names);
      } catch (error) {
        console.error("获取数据集列表失败:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchDatasets();
  }, []);

  return (
    <div className="w-1/2 px-4 py-4">
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium text-foreground whitespace-nowrap">
          Dataset:
        </label>
        <Select disabled={loading}>
          <SelectTrigger className="flex-1">
            <SelectValue placeholder={loading ? "加载中..." : "选择数据集..."} />
          </SelectTrigger>
          <SelectContent>
            {datasetNames.map((name) => (
              <SelectItem key={name} value={name}>
                {name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
