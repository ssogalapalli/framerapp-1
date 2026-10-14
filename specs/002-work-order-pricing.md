# Feature spec: Work order and pricing calculations

## Summary
Allow owners to record tractor jobs, capture multiple work items, and calculate totals reliably using quantity, unit, rate, charges, and discounts.

## Problem statement
Jobs are often tracked informally and can produce billing disputes when quantity, rate, or discounts are not recorded consistently. The app must calculate totals exactly once and retain the agreed rate used when the job was created.

## User stories
- As an owner, I want to create a work order for a customer so that I can record the job and associated items.
- As a user, I want pricing to be calculated automatically so that I do not make arithmetic mistakes.
- As a reviewer, I want historical rate snapshots so that old jobs remain correct even if the default rate changes.

## Acceptance criteria
- [ ] A work order can include one or more work items for a customer and optional tractor.
- [ ] Each work item stores activity, quantity, unit, agreed rate, extra charges, discount, and line total.
- [ ] The app calculates `line_total = (quantity × agreed_rate) + extra_charges − discount`.
- [ ] The work order total is the sum of all included line totals.
- [ ] Negative quantity, negative charges, and invalid discounts are rejected.
- [ ] Historical job rates are preserved even after the default activity rate changes.
- [ ] Cancelled jobs remain in history but are excluded from completed work value.

## Non-goals
- Live GPS-tracked job monitoring
- Automated invoicing or tax calculations
- Public job marketplace

## Constraints
- The app must use a single documented rounding convention.
- The system must reject values that clearly violate financial rules.
- Draft and planned jobs must not be treated as completed revenue.

## Risks and assumptions
- Some work orders may include mixed units or custom rates.
- Users need a clear status model to distinguish planned, in progress, completed, and cancelled.

## Open questions
- Should custom activities need approval or just allow free-form names?
- Are discounts expected to be limited to per-line amounts only in the MVP?
