# Implementation plan: Expenses and business reporting

## Objective
Capture operating expense records and expose consistent business summaries for the selected period.

## Scope
- In scope
  - Expense capture and editing
  - Daily and period summaries
  - Customer, tractor, and activity breakdowns
  - Estimated operating result reporting
- Out of scope
  - Formal accounting package integration
  - Tax or statutory compliance reporting

## Tasks
1. Model Expense and reporting dimensions.
2. Implement expense validation and category rules.
3. Build dashboard and report aggregation logic.
4. Add filters for date range, customer, tractor, and activity.
5. Test consistent metric definitions and exclusion rules for cancelled jobs.

## Dependencies
- WorkOrder and payment totals
- Date-range reporting utilities
- UI reporting components or API serialization

## Validation
- Confirm expense totals reflect recorded valid data
- Verify cancelled jobs are excluded from revenue metrics
- Check dashboard and report screens use the same metric definitions
