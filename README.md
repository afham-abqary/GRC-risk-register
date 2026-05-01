# GRC Risk Register

A command-line risk register tool for tracking and managing cybersecurity
risks aligned with ISO/IEC 27001 risk management principles.

## What it does

- Add and track cybersecurity risks with full details
- Automatic risk scoring using Likelihood x Impact matrix
- Risk level classification (Low / Medium / High / Critical)
- Update risk status and mitigation plans
- Visual risk summary with breakdown by level and status
- Export full risk register to CSV for audit reporting
- Persistent storage using JSON

## How to run

git clone https://github.com/afham-abqary/grc-risk-register
cd grc-risk-register
python risk_register.py

## Risk scoring matrix

| Score | Level    |
| 1-4   | Low      |
| 5-9   | Medium   |
| 10-15 | High     |
| 16-25 | Critical |

## Example entry

Risk ID     : RISK-001
Name        : Unauthorised Access to Admin Panel
Likelihood  : 3 - Possible
Impact      : 4 - Major
Risk Score  : 12
Risk Level  : High
Treatment   : Mitigate
Status      : In Progress
