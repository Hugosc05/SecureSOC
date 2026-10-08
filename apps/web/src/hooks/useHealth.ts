import { useEffect, useState } from 'react'

import { fetchHealthState, type HealthState } from '../lib/api/health'

const POLL_MS = 15_000

/** Polls API readiness; aborts in-flight requests on unmount. */
export function useHealth(pollMs = POLL_MS): HealthState {
  const [state, setState] = useState<HealthState>({ kind: 'checking' })

  useEffect(() => {
    const controller = new AbortController()
    const tick = () => {
      void fetchHealthState(controller.signal).then((s) => {
        if (!controller.signal.aborted) setState(s)
      })
    }
    tick()
    const id = window.setInterval(tick, pollMs)
    return () => {
      controller.abort()
      window.clearInterval(id)
    }
  }, [pollMs])

  return state
}
