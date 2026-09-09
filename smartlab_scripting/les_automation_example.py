"""
A worked example of Laboratory Execution System (LES)-style scripted
procedure automation — the kind of logic BIOVIA SmartLab/LES scripting
enforces: a test procedure is broken into ordered steps, each step must
be electronically signed off before the next unlocks, and any deviation
from the defined sequence is blocked and logged, not just discouraged.

This is a generic Python implementation of the LES enforcement pattern,
not a claim of BIOVIA SmartLab platform-specific scripting syntax — the
underlying step-sequencing and electronic-signoff logic transfers
directly, the platform-specific scripting API would need to be learned
on the job.
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProcedureStep:
    step_number: int
    description: str
    requires_signoff: bool = True
    completed: bool = False
    completed_by: str = None
    completed_at: str = None
    deviation_note: str = None


class SequenceViolationError(Exception):
    pass


@dataclass
class LESProcedure:
    procedure_id: str
    title: str
    steps: list

    def complete_step(self, step_number: int, actor: str, deviation_note: str = None):
        step = next((s for s in self.steps if s.step_number == step_number), None)
        if step is None:
            raise ValueError(f"No step {step_number} in procedure {self.procedure_id}")

        prior_steps = [s for s in self.steps if s.step_number < step_number]
        incomplete_prior = [s for s in prior_steps if not s.completed]
        if incomplete_prior:
            raise SequenceViolationError(
                f"Cannot complete step {step_number} — step(s) "
                f"{[s.step_number for s in incomplete_prior]} not yet complete"
            )

        step.completed = True
        step.completed_by = actor
        step.completed_at = datetime.now().isoformat()
        step.deviation_note = deviation_note

    def is_complete(self) -> bool:
        return all(s.completed for s in self.steps)

    def summary(self):
        return [
            {"step": s.step_number, "description": s.description, "completed": s.completed,
             "by": s.completed_by, "deviation": s.deviation_note}
            for s in self.steps
        ]


if __name__ == "__main__":
    procedure = LESProcedure(
        procedure_id="LES-HPLC-STD-014",
        title="HPLC System Suitability & Sample Run Sequence",
        steps=[
            ProcedureStep(1, "Verify column temperature at set point"),
            ProcedureStep(2, "Run system suitability standard"),
            ProcedureStep(3, "Confirm system suitability within acceptance criteria"),
            ProcedureStep(4, "Load sample sequence"),
            ProcedureStep(5, "Execute sample run"),
            ProcedureStep(6, "Review and release results"),
        ],
    )

    procedure.complete_step(1, actor="Lab.Analyst")
    procedure.complete_step(2, actor="Lab.Analyst")
    procedure.complete_step(3, actor="Lab.Analyst", deviation_note="System suitability RSD 1.8%, within 2.0% acceptance limit")
    procedure.complete_step(4, actor="Lab.Analyst")
    procedure.complete_step(5, actor="Lab.Analyst")
    procedure.complete_step(6, actor="QC.Reviewer")

    print(f"Procedure {procedure.procedure_id} complete: {procedure.is_complete()}")
    for s in procedure.summary():
        print(f"  Step {s['step']}: {s['description']} — {'DONE' if s['completed'] else 'PENDING'} ({s['by']})")

    procedure2 = LESProcedure(
        procedure_id="LES-HPLC-STD-015",
        title="HPLC Run — Out of Sequence Attempt",
        steps=[ProcedureStep(1, "Verify column temperature"), ProcedureStep(2, "Run standard")],
    )
    try:
        procedure2.complete_step(2, actor="Lab.Analyst")
    except SequenceViolationError as e:
        print(f"\nCorrectly blocked out-of-sequence execution: {e}")
