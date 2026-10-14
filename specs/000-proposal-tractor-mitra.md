# Proposal: Tractor Mitra MVP

## Summary
Propose an offline-first mobile app for tractor owners to record work orders, customer balances, payments, and operating expenses with simple local-language-friendly workflows.

## Problem
Tractor owners currently rely on paper ledgers, informal memory, and scattered notes to track jobs, charges, balances, and costs. This leads to missed work, incorrect bills, unpaid balances, and poor visibility into profitability.

## Proposed solution
Build a mobile-first business utility that allows owners to:
- manage customers and tractors
- create work orders with multiple activities and pricing
- record payments and customer advances
- log expenses
- review balances and business summaries
- operate offline and sync later when connectivity is restored

## Scope
### In scope for MVP
- owner profile setup
- customer management
- tractor management
- activity types and default pricing
- work order entry with items and totals
- partial payment tracking and balance ledger
- expense logging and summary reports
- offline-first local storage and sync retry
- basic authentication and owner-level data isolation

### Out of scope for MVP
- live GPS tracking
- public marketplace or booking platform
- tax filing or audited accounting statements
- online payment processing
- AI-based automation

## Goals
- reduce billing errors and missed customer follow-up
- make daily work records easier to keep in the field
- provide confidence in outstanding balances and profitability
- support low-connectivity and low-end Android device usage

## Non-functional priorities
- offline-first reliability
- data integrity for payments and financial totals
- clear validation and audit traceability
- local-language-friendly and accessible UI
- secure owner-scoped data boundaries

## Proposed milestone sequence
1. Foundation and configuration
2. Customer, tractor, and activity setup
3. Work order and pricing
4. Payment ledger and expense tracking
5. Reports and sync readiness

## Acceptance signal
The proposal is accepted when the project team agrees on the MVP scope, the required data model is realistic, and the next draft spec can be implemented in traceable feature-sized slices.
