import { LeftMainArea } from "@/components/left-panel/LeftMainArea";

export function LeftPanel() {
  return (
    <aside className="flex flex-col flex-1 border-[0.5px] border-foreground/60 p-4 min-h-0">
      {/* 主要区域 */}
      <div className="flex-1 mt-4 flex min-h-0">
        <LeftMainArea />
      </div>
    </aside>
  );
}

