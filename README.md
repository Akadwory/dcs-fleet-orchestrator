# DCS Fleet Orchestrator

DCS Fleet Orchestrator is an internal engineering platform for managing SMS-based troubleshooting workflows for CalAmp telematics units such as LMU2630, LMU3040, and LMU3640.

The system is being designed to replace manual troubleshooting workflows with a structured, auditable, and scalable platform that supports batch command execution, response tracking, and investigation reporting.

## Purpose

Today, troubleshooting many field units requires a repetitive manual workflow:

- export unit information from internal systems
- locate identifiers such as ESN, ICCID, and password
- manually determine the destination phone number
- send SMS diagnostic commands one unit at a time
- manually review responses
- manually summarize findings

This project aims to standardize and automate that process.

## Phase 1 Goal

Phase 1 focuses on building the operational foundation for batch SMS troubleshooting.

Core Phase 1 capabilities:

- import unit data from Excel files
- store and manage unit records
- select one or many units for investigation
- send approved SMS command templates in batch
- record outbound command activity
- store inbound replies
- display command and reply history
- generate internal troubleshooting summaries

## Target Devices

Initial support is intended for CalAmp device families including:

- LMU2630
- LMU3040
- LMU3640

## Intended Users

This system is intended for internal DCS technical teams such as:

- Field Applications Engineers
- Support Engineers
- Technical Operations Staff
- Reliability and troubleshooting personnel

## Architecture Direction

The system will be built as a modular monolith following large-company engineering practices:

- clean separation of API, services, repositories, and integrations
- centralized configuration management
- structured logging
- environment-based settings
- database-backed auditability
- clear documentation and controlled command workflows

## Initial Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker Compose
- pandas / openpyxl
- pytest

## Phase 1 Non-Goals

The following items are intentionally out of scope for Phase 1:

- direct DMCTC integration
- Outlook or email automation
- AI-based troubleshooting recommendations
- customer-facing dashboards
- predictive maintenance analytics
- firmware orchestration workflows

## Repository Status

Current status:

- repository initialized
- enterprise folder structure created
- project scope locked
- README defined

Next steps:

- environment configuration
- dependency definition
- container setup
- application bootstrap
- database foundation
- import workflow implementation

## Engineering Principles

This project is being built with the following standards:

- step-by-step implementation
- documentation before complexity
- maintainable architecture over quick scripting
- operational auditability
- scalable internal platform design
- large-company style development discipline