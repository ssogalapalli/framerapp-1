# Feature spec: Payments, advances, and customer ledger

## Summary
Provide a transparent ledger of work charges, received payments, advances, and outstanding balances for each customer and work order.

## Problem statement
Without a consistent payment lifecycle, customers may be overcharged, underpaid, or misrepresented in their balance. The ledger must support partial payments, advances, reversals, and accurate outstanding amounts.

## User stories
- As an owner, I want to record payments against a work order so that I can track what has been received.
- As an owner, I want to support customer advances so that prepaid amounts do not get confused with completed work.
- As a reviewer, I want a customer ledger so that I can reconcile balances and spot disputes quickly.

## Acceptance criteria
- [ ] A payment can be recorded with amount, date, method, reference, and optional note.
- [ ] A payment can be allocated to one or more work orders or stored as an unallocated advance.
- [ ] The app prevents negative payment values and over-allocation beyond amounts due or paid.
- [ ] Customer balances are calculated from charges, valid payments, advances, and reversals without double counting.
- [ ] Reversed or corrected payments remain auditable instead of being silently deleted.
- [ ] The customer ledger displays work history, allocated payments, and current balance clearly.

## Non-goals
- Direct online payment gateway processing
- Automatic debt collection or legal enforcement

## Constraints
- All payment corrections must use an auditable reversal or correction flow.
- Unallocated advances must be visible separately from outstanding debt.
- The same payment cannot be counted twice across totals.

## Risks and assumptions
- Some businesses will record cash payments with minimal references.
- Payment allocations may need manual editing in cases of partial settlements.

## Open questions
- Should the MVP support unallocated advances from the start or only allocated payments?
- Is there a required bank or UPI reference format for the pilot?
