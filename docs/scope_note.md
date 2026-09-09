# Scope Note

## What this demonstrates
- The core LIMS data model (sample status workflow, chain of custody) and its enforcement logic — vendor-agnostic, but structurally identical to what any LIMS platform implements underneath its UI
- Scripted parsing/validation of chromatography-style results against specification limits, including the GMP rule that one failing peak fails the whole sample
- The step-sequencing and enforcement pattern behind LES scripting (BIOVIA SmartLab or equivalent) — a generic Python implementation, not BIOVIA's specific scripting API
- GMP Computer System Validation documentation structure (IQ/OQ/PQ), with a worked OQ example

## What this does not demonstrate, and is not trying to
- **Hands-on BIOVIA SmartLab, Empower, or a specific commercial LIMS platform.** The data model and logic transfer; the platform-specific configuration, scripting syntax, and UI experience would be learned on the job, as the role's own listing anticipates ("training provided").
- **Analytical chemistry or biology domain knowledge.** Chromatography terminology (peak area, retention time) is used correctly as data fields, not as evidence of understanding the underlying chemistry.
- **IT helpdesk/L2 support experience or ITIL certification.** This project shows the systems being supported, not ticketing/escalation practice.
