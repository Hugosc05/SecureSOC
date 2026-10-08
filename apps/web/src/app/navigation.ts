/**
 * Sidebar entries. Sections that do not exist yet are listed with the phase that
 * builds them, so the UI is honest about what works today.
 */
export interface NavItem {
  label: string
  to: string
  /** Roadmap phase that implements it; undefined = available now. */
  phase?: number
}

export const NAV_ITEMS: NavItem[] = [
  { label: 'Overview', to: '/' },
  { label: 'Incidents', to: '/incidents', phase: 4 },
  { label: 'Alerts', to: '/alerts', phase: 3 },
  { label: 'Events', to: '/events', phase: 2 },
  { label: 'Agent runs', to: '/agent', phase: 6 },
  { label: 'Approvals', to: '/approvals', phase: 8 },
  { label: 'Security', to: '/security', phase: 9 },
]
