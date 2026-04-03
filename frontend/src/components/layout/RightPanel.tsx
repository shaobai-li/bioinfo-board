"use client";

import { useEffect, useState } from "react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useDataset } from "@/lib/contexts/DatasetContext";
import { getGenePlots, getImageUrl } from "@/lib/services/datasetService";

interface GenePlots {
  gene: string;
  violinUrl: string;
  umapUrl: string;
}

export function RightPanel() {
  const { currentDataset } = useDataset();
  const [geneInput, setGeneInput] = useState("");
  const [genePlots, setGenePlots] = useState<GenePlots | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 切换数据集时清空基因表达图
  useEffect(() => {
    setGenePlots(null);
    setGeneInput("");
    setError(null);
  }, [currentDataset]);

  const handleSearch = async () => {
    if (!currentDataset || !geneInput.trim()) return;

    const gene = geneInput.trim();
    setLoading(true);
    setError(null);

    try {
      const response = await getGenePlots(currentDataset, gene);
      setGenePlots({
        gene: response.gene,
        violinUrl: getImageUrl(response.violinUrl),
        umapUrl: getImageUrl(response.umapUrl),
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "查询失败");
      setGenePlots(null);
    } finally {
      setLoading(false);
    }
  };

  const tabTriggerClass = `
    rounded-none px-4 py-2 relative
    border border-transparent
    data-[state=inactive]:text-blue-500
    data-[state=active]:border-black data-[state=active]:border-b-0
    data-[state=active]:z-20
  `;

  const tabContentClass = "flex-1 border border-black mt-[-1px] overflow-hidden";

  return (
    <section className="h-full w-1/2">
      <Tabs defaultValue="overview" className="h-full flex flex-col gap-0">
        {/* TabsList */}
        <TabsList className="bg-transparent p-0 h-auto gap-0 justify-start shrink-0">
          <TabsTrigger value="overview" className={tabTriggerClass}>
            Overview
          </TabsTrigger>
          <TabsTrigger value="cell-type-expression" className={tabTriggerClass}>
            Cell Type Expression
          </TabsTrigger>
        </TabsList>

        {/* Overview 内容区域 */}
        <TabsContent value="overview" className={tabContentClass}>
          <ScrollArea className="h-full">
            <div className="p-4">
              <p className="text-muted-foreground">Overview 内容区域</p>
            </div>
          </ScrollArea>
        </TabsContent>

        {/* Cell Type Expression 内容区域 */}
        <TabsContent value="cell-type-expression" className={tabContentClass}>
          <ScrollArea className="h-full">
            <div className="p-4 space-y-4">
              {/* 基因搜索框 */}
              <div className="flex gap-2">
                <Input
                  placeholder="输入基因名称（如 KIT）"
                  value={geneInput}
                  onChange={(e) => setGeneInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  disabled={!currentDataset || loading}
                />
                <Button
                  onClick={handleSearch}
                  disabled={!currentDataset || !geneInput.trim() || loading}
                >
                  {loading ? "查询中..." : "查询"}
                </Button>
              </div>

              {/* 错误提示 */}
              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded">
                  <p className="text-red-600 text-sm">{error}</p>
                </div>
              )}

              {/* 未选择数据集提示 */}
              {!currentDataset && (
                <p className="text-muted-foreground text-sm">
                  请先选择一个数据集
                </p>
              )}

              {/* 基因表达图 */}
              {genePlots && (
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium mb-2">
                      {genePlots.gene} 小提琴图
                    </p>
                    <img
                      src={genePlots.violinUrl}
                      alt={`${genePlots.gene} violin plot`}
                      className="w-full h-auto object-contain"
                    />
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-2">
                      {genePlots.gene} UMAP 图
                    </p>
                    <img
                      src={genePlots.umapUrl}
                      alt={`${genePlots.gene} UMAP`}
                      className="w-full h-auto object-contain"
                    />
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
        </TabsContent>
      </Tabs>
    </section>
  );
}
