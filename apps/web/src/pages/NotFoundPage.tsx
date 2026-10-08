import { Link } from 'react-router'

export function NotFoundPage() {
  return (
    <div className="mx-auto max-w-md py-16 text-center">
      <p className="font-mono text-sm text-faint">404</p>
      <h1 className="mt-2 text-lg font-semibold">This section does not exist yet</h1>
      <Link to="/" className="mt-4 inline-block text-sm text-accent hover:underline">
        Back to overview
      </Link>
    </div>
  )
}
