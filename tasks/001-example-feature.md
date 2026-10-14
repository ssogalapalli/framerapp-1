# Implementation plan: Customer and tractor management

## Objective
Enable a tractor owner to set up the business context and maintain customer, tractor, and activity metadata needed for job tracking.

## Scope
- In scope
  - Business profile configuration
  - Customer CRUD and search
  - Tractor CRUD and active/inactive states
  - Activity/rate configuration and historical rate snapshotting
- Out of scope
  - Operator roles and cloud sync
  - GPS or fleet telemetry

## Tasks
1. Define data models for OwnerAccount, Customer, Tractor, ActivityType, and Rate.
2. Implement repository and validation logic for create, update, search, and deactivate flows.
3. Add tests for duplicate warnings, required-field validation, and historical rate immutability.
4. Wire UI or API endpoints to expose the management screens.
5. Run targeted validation and verify acceptance criteria.

## Dependencies
- Core app domain layer
- Persistent storage abstraction
- Localization configuration for currency and units

## Validation
- Run unit tests for customer and tractor management
- Validate rate-history behavior with a regression test
- Verify empty states and validation messages in the UI or API layer
