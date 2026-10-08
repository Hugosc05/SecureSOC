import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { HealthIndicator } from './HealthIndicator'

function mockFetch(impl: () => Promise<Response>) {
  vi.stubGlobal('fetch', vi.fn(impl))
}

const json = (status: number, body: unknown) =>
  Promise.resolve(
    new Response(JSON.stringify(body), {
      status,
      headers: { 'Content-Type': 'application/json' },
    }),
  )

describe('HealthIndicator', () => {
  it('shows ready when the API and database are up', async () => {
    mockFetch(() => json(200, { status: 'ready', checks: { database: 'ok' } }))
    render(<HealthIndicator />)
    expect(await screen.findByText('API ready')).toBeInTheDocument()
  })

  it('shows degraded when readiness returns 503', async () => {
    mockFetch(() => json(503, { status: 'unavailable', checks: { database: 'error' } }))
    render(<HealthIndicator />)
    expect(await screen.findByText('Degraded')).toBeInTheDocument()
  })

  it('shows unreachable when the network call fails', async () => {
    mockFetch(() => Promise.reject(new TypeError('Failed to fetch')))
    render(<HealthIndicator />)
    expect(await screen.findByText('API unreachable')).toBeInTheDocument()
  })

  it('only calls the same-origin API path', async () => {
    mockFetch(() => json(200, { status: 'ready', checks: {} }))
    render(<HealthIndicator />)
    await screen.findByText('API ready')
    expect(fetch).toHaveBeenCalledWith('/api/v1/health/ready', expect.anything())
  })
})
