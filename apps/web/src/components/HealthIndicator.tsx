import { useHealth } from '../hooks/useHealth'
import type { HealthState } from '../lib/api/health'

const VIEW: Record<HealthState['kind'], { label: string; dot: string }> = {
  checking: { label: 'Checking…', dot: 'bg-faint' },
  ready: { label: 'API ready', dot: 'bg-ok' },
  degraded: { label: 'Degraded', dot: 'bg-sev-medium' },
  unreachable: { label: 'API unreachable', dot: 'bg-sev-critical' },
}

export function HealthIndicator() {
  const state = useHealth()
  const view = VIEW[state.kind]
  const detail =
    state.kind === 'ready' || state.kind === 'degraded'
      ? Object.entries(state.checks)
          .map(([name, s]) => `${name}: ${s}`)
          .join(', ')
      : undefined

  return (
    <div
      role="status"
      aria-live="polite"
      title={detail}
      className="flex items-center gap-2 rounded-full border border-border bg-surface px-3 py-1 text-xs text-muted"
    >
      <span aria-hidden="true" className={`h-2 w-2 rounded-full ${view.dot}`} />
      {view.label}
    </div>
  )
}
