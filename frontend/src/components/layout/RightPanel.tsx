import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";

export function RightPanel() {
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

        {/* 内容区域 */}
        <TabsContent value="overview" className={tabContentClass}>
          <ScrollArea className="h-full">
            <div className="p-4">
              <p className="text-muted-foreground">Overview 内容区域</p>
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="cell-type-expression" className={tabContentClass}>
          <ScrollArea className="h-full">
            <div className="p-4 space-y-4">
              <img 
                src="/d8cf328b2647165b3df8c84f9e62f664.jpg" 
                alt="Cell Type Expression 1" 
                className="w-full h-auto object-contain"
              />
              <img 
                src="/fcb6c7197a8fb87fe0830609254761f2.jpg" 
                alt="Cell Type Expression 2" 
                className="w-full h-auto object-contain"
              />
            </div>
          </ScrollArea>
        </TabsContent>

      </Tabs>
    </section>
  );
}
