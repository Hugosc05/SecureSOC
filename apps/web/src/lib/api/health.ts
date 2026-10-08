import { ApiError, getJson } from './client'

export type CheckStatus = 'ok' | 'error'

export interface Readiness {
  status: 'ready' | 'unavailable'
  checks: Record<string, CheckStatus>
}

export type HealthState =
  | { kind: 'checking' }
  | { kind: 'ready'; checks: Record<string, CheckStatus> }
  | { kind: 'degraded'; checks: Record<string, CheckStatus> }
  | { kind: 'unreachable' }

function isReadiness(value: unknown): value is Readiness {
  return (
    typeof value === 'object' &&
    value !== null &&
    'status' in value &&
    'checks' in value &&
    typeof (value as { checks: unknown }).checks === 'object'
  )
}

/** Maps the readiness endpoint (200 or 503) to a UI state. Never throws. */
export async function fetchHealthState(signal?: AbortSignal): Promise<HealthState> {
  try {
    const body = await getJson<Readiness>('/api/v1/health/ready', { signal })
    return { kind: 'ready', checks: body.checks }
  } catch (err) {
    if (err instanceof ApiError && err.status === 503 && isReadiness(err.body)) {
      return { kind: 'degraded', checks: err.body.checks }
    }
    return { kind: 'unreachable' }
  }
}
