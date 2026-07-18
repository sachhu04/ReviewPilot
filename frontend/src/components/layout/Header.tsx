import { Bell, Search, User } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Header() {
  return (
    <header className="flex h-16 shrink-0 items-center gap-x-4 border-b bg-card/50 px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <form className="relative flex flex-1" action="#" method="GET">
          <label htmlFor="search-field" className="sr-only">
            Search
          </label>
          <Search
            className="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-muted-foreground"
            aria-hidden="true"
          />
          <input
            id="search-field"
            className="block h-full w-full border-0 bg-transparent py-0 pl-8 pr-0 text-foreground focus:ring-0 sm:text-sm"
            placeholder="Search reviews, PRs, issues..."
            type="search"
            name="search"
          />
        </form>
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" aria-hidden="true" />
          </Button>
          <div className="hidden lg:block lg:h-6 lg:w-px lg:bg-border" aria-hidden="true" />
          <Button variant="ghost" size="icon">
            <User className="h-5 w-5" aria-hidden="true" />
          </Button>
        </div>
      </div>
    </header>
  );
}
