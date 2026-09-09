# Scientific Systems Integration — LIMS, Empower CDS, SmartLab Scripting
### Lab system data flow modelling, Python scripting integration patterns, and GMP computer system validation documentation

## What's here

| Component | Description |
|---|---|
| `data/` | Simulated LIMS sample records and Empower CDS chromatography run exports |
| `lims_integration/lims_sample_tracker.py` | Sample chain-of-custody tracking and LIMS-style status workflow |
| `empower_cds/chromatography_data_parser.py` | Parses and validates Empower-style chromatography result exports |
| `smartlab_scripting/les_automation_example.py` | A BIOVIA SmartLab/LES-style scripted workflow step (Python) |
| `csv_documentation/` | Computer System Validation (IQ/OQ/PQ) documentation for a lab system |
| `docs/scope_note.md` | What this project does and does not demonstrate |

## LIMS sample tracking

`lims_integration/lims_sample_tracker.py` models the core LIMS data object — a sample moving through a defined status workflow (Received → In Testing → Result Entered → Reviewed → Released), with chain-of-custody logging.

Run:
```bash
python data/generate_lab_systems_data.py
python lims_integration/lims_sample_tracker.py
```

## Empower CDS data parsing

`empower_cds/chromatography_data_parser.py` parses a simulated Empower-style chromatography results export (peak area, retention time, pass/fail against specification) and flags out-of-specification results.

Run:
```bash
python empower_cds/chromatography_data_parser.py
```

## SmartLab/LES scripting example

`smartlab_scripting/les_automation_example.py` is a worked example of the kind of scripted logic a Laboratory Execution System (LES) automation step performs — sequencing a test procedure, enforcing that steps complete in order, and logging execution against the procedure definition.

Run:
```bash
python smartlab_scripting/les_automation_example.py
```

## Computer System Validation documentation

`csv_documentation/` contains an IQ/OQ/PQ validation protocol template and a worked example — the GMP documentation framework required before any lab system change goes live.

## Repo structure

```
scientific-systems-lims-integration/
├── README.md
├── data/
│   └── generate_lab_systems_data.py
├── lims_integration/
│   └── lims_sample_tracker.py
├── empower_cds/
│   └── chromatography_data_parser.py
├── smartlab_scripting/
│   └── les_automation_example.py
├── csv_documentation/
│   ├── csv_protocol_template.md
│   └── worked_example_oq_protocol.md
└── docs/
    └── scope_note.md
```
