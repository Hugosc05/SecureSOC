import { NavLink, Outlet } from 'react-router'

import { HealthIndicator } from '../components/HealthIndicator'
import { NAV_ITEMS } from './navigation'

export function AppShell() {
  return (
    <div className="flex h-full min-h-screen">
      <aside className="hidden w-60 shrink-0 flex-col border-r border-border bg-surface md:flex">
        <div className="flex h-14 items-center gap-2.5 border-b border-border px-5">
          <img src="/favicon.svg" alt="" className="h-6 w-6" />
          <span className="text-[15px] font-semibold tracking-tight">SecureSOC</span>
        </div>

        <nav aria-label="Main" className="flex-1 space-y-0.5 p-3">
          {NAV_ITEMS.map((item) =>
            item.phase === undefined ? (
              <NavLink
                key={item.to}
                to={item.to}
                end
                className={({ isActive }) =>
                  `flex items-center rounded-md px-3 py-2 text-sm transition-colors ${
                    isActive
                      ? 'bg-accent-soft text-text'
                      : 'text-muted hover:bg-surface-2 hover:text-text'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ) : (
              <span
                key={item.to}
                aria-disabled="true"
                title={`Available from phase ${item.phase}`}
                className="flex cursor-not-allowed items-center justify-between rounded-md px-3 py-2 text-sm text-faint"
              >
                {item.label}
                <span className="font-mono text-[10px] uppercase tracking-wider">P{item.phase}</span>
              </span>
            ),
          )}
        </nav>

        <p className="border-t border-border px-5 py-3 font-mono text-[11px] text-faint">
          local · €0 · v0.1.0
        </p>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 items-center justify-between border-b border-border bg-surface/60 px-4 md:px-6">
          <span className="text-sm font-semibold md:hidden">SecureSOC</span>
          <span className="hidden text-sm text-muted md:inline">Local Security Operations</span>
          <HealthIndicator />
        </header>
        <main className="flex-1 p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
