# Feature spec: Offline sync, security, and data integrity

## Summary
Ensure the app remains usable without internet connectivity, safely synchronizes records when online, and protects customer and financial data across account boundaries.

## Problem statement
Tractor work often happens in places with weak or no connectivity. The app must let workers save records locally and synchronize them later without creating duplicate jobs or silently losing financial information.

## User stories
- As a field user, I want to save jobs offline so that I can continue working without signal.
- As an owner, I want sync retries and conflict warnings so that I do not lose financial records.
- As a product owner, I want secure multi-tenant data handling so that one business cannot access another business's data.

## Acceptance criteria
- [ ] Users can create and update core records while offline after initial setup.
- [ ] Records are marked pending synchronization and show last successful sync time.
- [ ] Sync retries are idempotent and do not create duplicate jobs or payments.
- [ ] Conflicting edits are surfaced rather than silently overwritten.
- [ ] Data is isolated by owner account and access is enforced server-side.
- [ ] Sensitive customer and payment data is not logged unnecessarily.
- [ ] Authentication is required for cloud-backed accounts.

## Non-goals
- Continuous raw location tracking
- Fully autonomous AI synchronization or data recovery workflows

## Constraints
- Local-only mode must clearly communicate the lack of backup.
- Payment and financial operations must preserve auditability.
- Users must understand pending sync and error states.

## Risks and assumptions
- Multi-device editing may create conflict scenarios requiring human review.
- Local storage and sync can be deferred for early pilot scenarios but must be planned for MVP readiness.

## Open questions
- Is the initial pilot local-only or cloud-backed from day one?
- Do pilot users require account recovery and export controls immediately or later?
