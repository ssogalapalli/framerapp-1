# Implementation plan: Work order and pricing calculations

## Objective
Enable work order capture with reliable pricing logic and preserved historical rate metadata.

## Scope
- In scope
  - Create and edit work orders with multiple items
  - Calculate line totals and order totals
  - Preserve historical agreed rates
  - Support status transitions and cancelled-order exclusion
- Out of scope
  - Real-time GPS tracking
  - PDF invoice generation

## Tasks
1. Model WorkOrder and WorkItem with required fields and status values.
2. Implement pricing rules and validation for quantity, rates, extra charges, and discounts.
3. Add database-level and domain-level tests for calculation correctness and invalid inputs.
4. Preserve rate snapshots and prevent historical mutation.
5. Exclude cancelled or draft work from completed revenue calculations.

## Dependencies
- Customer and activity/rate models
- Domain validation library or centralized rules
- Reporting aggregation layer

## Validation
- Run pricing unit tests
- Verify cancelled-order reports omit completed work value
- Check validation messages for invalid financial values
