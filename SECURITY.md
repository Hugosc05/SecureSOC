# Security Policy

SecureSOC is a research and portfolio project designed to run **locally**. It is not intended to be exposed to the Internet.

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Use GitHub's private vulnerability reporting (*Security → Report a vulnerability*) on this repository instead. Include the affected version or commit, the steps to reproduce, and the impact.

Agent-security findings are especially welcome: prompt-injection bypasses, policy-engine bypasses, and unauthorised tool execution. Every confirmed bypass becomes a regression test in the red-team suite.

## Supported versions

Only the latest commit on `main` is supported.

## Scope and rules for the lab

- Offensive tooling (Kali, scanners, brute-force tools) may only target the project's **own isolated lab VMs** on a host-only network.
- The project contains no functionality to attack third-party systems, and contributions adding it will be rejected.
- High-risk response actions (`block_ip`, `isolate_host`) are simulated by default.

## Design commitments

- No secrets in the repository. Configuration comes from `.env` (git-ignored).
- The LLM agent has no shell access, no arbitrary network egress and no ability to approve its own actions.
- Authorisation decisions are made by deterministic code, not by the model.
- The audit log is append-only and tamper-evident (from Phase 7).
