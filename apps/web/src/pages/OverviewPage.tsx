import { useHealth } from '../hooks/useHealth'
import type { HealthState } from '../lib/api/health'

interface Component {
  name: string
  description: string
  phase?: number
  check?: string
}

const COMPONENTS: Component[] = [
  { name: 'API', description: 'FastAPI service' },
  { name: 'Database', description: 'PostgreSQL', check: 'database' },
  { name: 'Ingestion', description: 'Linux auth & UFW parsers', phase: 2 },
  { name: 'Detection engine', description: 'Sigma-subset rules', phase: 3 },
  { name: 'Local LLM', description: 'Ollama provider', phase: 6 },
  { name: 'Policy engine', description: 'ALLOW / DENY / REQUIRE_APPROVAL', phase: 7 },
]

type Status = { label: string; tone: string }

function statusOf(c: Component, health: HealthState): Status {
  if (c.phase !== undefined) return { label: `Phase ${c.phase}`, tone: 'text-faint' }
  if (health.kind === 'checking') return { label: 'checking', tone: 'text-muted' }
  if (health.kind === 'unreachable') return { label: 'unreachable', tone: 'text-sev-critical' }
  if (!c.check) return { label: 'online', tone: 'text-ok' }
  return health.checks[c.check] === 'ok'
    ? { label: 'online', tone: 'text-ok' }
    : { label: 'error', tone: 'text-sev-critical' }
}

export function OverviewPage() {
  const health = useHealth()

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h1 className="text-xl font-semibold tracking-tight">Overview</h1>
        <p className="mt-1 text-sm text-muted">
          Platform status. Incidents, alerts and agent activity appear here as each phase lands.
        </p>
      </div>

      <section aria-labelledby="components-h" className="rounded-lg border border-border bg-surface">
        <h2 id="components-h" className="border-b border-border px-4 py-3 text-sm font-medium">
          Components
        </h2>
        <table className="w-full text-sm">
          <thead className="sr-only">
            <tr>
              <th>Component</th>
              <th>Description</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {COMPONENTS.map((c) => {
              const s = statusOf(c, health)
              return (
                <tr key={c.name} className="border-b border-border last:border-0">
                  <td className="px-4 py-2.5 font-medium">{c.name}</td>
                  <td className="hidden px-4 py-2.5 text-muted sm:table-cell">{c.description}</td>
                  <td className={`px-4 py-2.5 text-right font-mono text-xs ${s.tone}`}>{s.label}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </section>
    </div>
  )
}
