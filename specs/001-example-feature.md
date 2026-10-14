# Feature spec: Customer and tractor management

## Summary
Allow tractor owners to set up their business profile, manage customers and tractors, and configure activity defaults before capturing jobs, payments, and expenses.

## Problem statement
Owners need a reliable way to maintain a list of customers, tractors, and activity rate defaults without relying on paper records or inconsistent spreadsheets.

## User stories
- As a tractor owner, I want to add and update customer details so that I can track each person's work and balance.
- As a tractor owner, I want to manage multiple tractors so that each job is tied to the correct equipment.
- As a business owner, I want configurable activity names and rates so that pricing remains consistent and accurate over time.

## Acceptance criteria
- [ ] The owner can create, edit, search, and deactivate customers.
- [ ] The owner can manage multiple tractors with display name, registration number, and active status.
- [ ] Activity names, units, and default rates can be configured per owner.
- [ ] Historical work records preserve the rate used at time of creation even if defaults change later.
- [ ] Invalid customer or tractor data is rejected with clear validation.

## Non-goals
- Driver/operator role management in the first milestone
- Multi-owner or marketplace functionality
- GPS-based fleet tracking

## Constraints
- Data must be scoped to the owner account.
- Default rates and units must be configurable for local market needs.
- Customer records must accommodate missing phone or address fields.

## Risks and assumptions
- Some customers may share names or villages, so duplicate warnings are useful but not blocking.
- The MVP focuses on owner-only workflow and can expand later for operator accounts.

## Open questions
- Which Indian languages are required for the first pilot?
- Are customer advances required in the first release or can they be deferred?
