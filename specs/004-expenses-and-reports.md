# Feature spec: Expenses and business reporting

## Summary
Track operating expenses and provide report summaries that help owners understand work value, payments, outstanding balances, and estimated operating result.

## Problem statement
Owners need to know whether tractor work is profitable and whether cash inflows are keeping pace with expenses. Without clear reporting, they cannot compare cost to revenue across dates, customers, or tractors.

## User stories
- As an owner, I want to log fuel, maintenance, and driver expenses so that I can measure costs realistically.
- As a manager, I want daily and monthly reports so that I can review business performance.
- As a user, I want clearly labelled metrics so that I understand what is revenue, what is cash received, and what is an estimate.

## Acceptance criteria
- [ ] Expenses can be recorded with category, amount, date, optional tractor, optional job, and note.
- [ ] Common categories include diesel/fuel, maintenance, oil, spare parts, driver wages, and other.
- [ ] Dashboard and report screens show work value, payments received, outstanding balances, expenses, and estimated operating result.
- [ ] Cancelled jobs are excluded from completed work value.
- [ ] Planned and draft orders do not appear as completed revenue.
- [ ] Metrics are labelled consistently and the estimated operating result is clearly marked as an estimate.

## Non-goals
- Formal financial accounting or tax filing
- Payroll or HR management

## Constraints
- Expense totals must not double-count work-associated expenses in overall expense totals.
- Report filters and totals must be consistent across screens.

## Risks and assumptions
- Owners may use custom categories beyond the initial MVP list.
- Some cost entries may not be tied directly to a specific work order.

## Open questions
- Is an explicit cost allocation model needed for work-order-specific expenses?
- Should the first report view include weekly and monthly ranges only, or more advanced seasonal filters?
