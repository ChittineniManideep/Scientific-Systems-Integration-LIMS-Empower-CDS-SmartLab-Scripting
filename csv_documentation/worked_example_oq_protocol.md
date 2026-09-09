# Computer System Validation Protocol — Worked Example
## LIMS Sample Status Workflow — Operational Qualification (OQ)

| Field | Value |
|---|---|
| Protocol Number | CSV-LIMS-014-OQ |
| System | LIMS |
| Validation Phase | Operational Qualification |
| Version | 1.0 |

## 1. Purpose
Verify that the LIMS sample status workflow enforces the defined state sequence and rejects invalid transitions, per the system's functional specification.

## 2. Scope
Covers the sample status workflow module only (Received → In Testing → Result Entered → Reviewed → Released/Rejected). Does not cover report generation or instrument interfacing, qualified under separate protocols.

## 3. Prerequisites
- Installation Qualification (CSV-LIMS-014-IQ) complete and approved
- Test environment provisioned with representative sample data

## 4. Test Cases

| Test ID | Description | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|
| TC-01 | Attempt to transition a sample from "Received" directly to "Released", skipping intermediate states | System rejects the transition | System rejected the transition with a sequence violation error | Pass |
| TC-02 | Complete a valid full lifecycle: Received → In Testing → Result Entered → Reviewed → Released | All transitions succeed, chain of custody logged for each | All 4 transitions completed, chain of custody shows timestamp/actor/from/to for each | Pass |
| TC-03 | Attempt to transition a "Released" sample back to any prior state | System rejects the transition (Released is terminal) | System rejected the transition | Pass |
| TC-04 | Send a sample back from "Reviewed" to "Result Entered" for retest | System allows this specific backward transition | System allowed the transition | Pass |

## 5. Deviations
None identified during this qualification run.

## 6. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Protocol Author | [Name] | | [Date] |
| QA Reviewer | [Name] | | [Date] |
| System Owner | [Name] | | [Date] |
