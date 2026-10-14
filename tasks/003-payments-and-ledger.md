# Implementation plan: Payments, advances, and customer ledger

## Objective
Implement a ledger-driven payment flow so balances remain accurate and auditable.

## Scope
- In scope
  - Payment recording and allocation
  - Advance tracking and visible balance separation
  - Customer ledger and statement support
  - Reversal/correction handling
- Out of scope
  - Online payment processing
  - Automated collections workflow

## Tasks
1. Define Payment and PaymentAllocation entities and lifecycle states.
2. Add validation rules for non-negative amounts and safe allocations.
3. Implement balance calculation logic for work charges, payments, credits, and reversals.
4. Build customer ledger queries and statement formatting.
5. Add regression tests for partial payments, advances, and audit-safe corrections.

## Dependencies
- WorkOrder and balance model
- Reporting layer
- AuditEvent structure

## Validation
- Verify partial payment and outstanding calculation
- Validate advance tracking is separate from debt
- Confirm a corrected payment is auditable and not double-counted
