import Image from "next/image";

export function TopBar() {
  return (
    <header className="w-full px-4 py-4">
      <div className="flex items-center gap-4">
        <Image
          src="/logo.png"
          alt=""
          width={256}
          height={64}
          className="h-16 w-auto object-contain -translate-y-1.5"
          priority
        />
        <span className="text-4xl font-bold tracking-wide">Leilab Public Datasets</span>
      </div>
    </header>
  );
}

