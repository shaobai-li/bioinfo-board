import Image from "next/image";

export function LeftMainArea() {
  return (
    <div className="flex-1 min-w-0 h-full relative">
      <Image
        src="/29872af2fada2ee3fa9adf014a243492.jpg"
        alt="主要区域图片"
        fill
        className="object-cover"
      />
    </div>
  );
}

