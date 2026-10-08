/**
 * Minimal typed HTTP client. Same-origin only: the API is always reached via
 * /api (Vite proxy in dev, nginx in Docker), so no credentials or tokens ever
 * go to another origin.
 */
export class ApiError extends Error {
  readonly status: number
  readonly body: unknown

  constructor(status: number, body: unknown) {
    super(`API request failed with status ${status}`)
    this.name = 'ApiError'
    this.status = status
    this.body = body
  }
}

export async function getJson<T>(path: string, init?: { signal?: AbortSignal }): Promise<T> {
  if (!path.startsWith('/api/')) throw new Error(`Refusing non-API path: ${path}`)
  const res = await fetch(path, {
    method: 'GET',
    headers: { Accept: 'application/json' },
    credentials: 'same-origin',
    signal: init?.signal,
  })
  const body: unknown = await res.json().catch(() => null)
  if (!res.ok) throw new ApiError(res.status, body)
  return body as T
}
