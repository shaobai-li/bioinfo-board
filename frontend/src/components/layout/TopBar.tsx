export function TopBar() {
  return (
    <header className="w-full px-4 py-4">
      {/* 左侧标题区域 */}
      <div className="flex items-center gap-4">
        {/* 颜色指示块 */}
        <div className="w-4 h-10 bg-[#ec4899]" />
        {/* 标题文本 */}
        <span className="text-3xl font-bold tracking-wide">Testis</span>
      </div>
    </header>
  );
}

