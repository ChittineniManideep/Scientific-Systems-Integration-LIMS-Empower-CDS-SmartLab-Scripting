"""
LIMS-style sample status workflow and chain-of-custody tracking — the
core LIMS data model: a sample moves through a defined sequence of
statuses, each transition logged with actor and timestamp.
"""
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import pandas as pd


class SampleStatus(str, Enum):
    RECEIVED = "Received"
    IN_TESTING = "In Testing"
    RESULT_ENTERED = "Result Entered"
    REVIEWED = "Reviewed"
    RELEASED = "Released"
    REJECTED = "Rejected"


VALID_TRANSITIONS = {
    SampleStatus.RECEIVED: {SampleStatus.IN_TESTING, SampleStatus.REJECTED},
    SampleStatus.IN_TESTING: {SampleStatus.RESULT_ENTERED, SampleStatus.REJECTED},
    SampleStatus.RESULT_ENTERED: {SampleStatus.REVIEWED, SampleStatus.IN_TESTING},
    SampleStatus.REVIEWED: {SampleStatus.RELEASED, SampleStatus.RESULT_ENTERED},
    SampleStatus.RELEASED: set(),
    SampleStatus.REJECTED: set(),
}


class InvalidSampleTransitionError(Exception):
    pass


@dataclass
class Sample:
    sample_id: str
    test_type: str
    status: SampleStatus = SampleStatus.RECEIVED
    chain_of_custody: list = field(default_factory=list)

    def transition(self, new_status: SampleStatus, actor: str, note: str = ""):
        if new_status not in VALID_TRANSITIONS[self.status]:
            raise InvalidSampleTransitionError(
                f"{self.sample_id}: cannot move from {self.status.value} to {new_status.value}"
            )
        self.chain_of_custody.append({
            "timestamp": datetime.now().isoformat(), "from": self.status.value,
            "to": new_status.value, "actor": actor, "note": note,
        })
        self.status = new_status


if __name__ == "__main__":
    samples_df = pd.read_csv("data/lims_samples.csv")

    import random
    random.seed(17)
    results = []
    for _, row in samples_df.head(30).iterrows():
        s = Sample(sample_id=row.sample_id, test_type=row.test_type)
        s.transition(SampleStatus.IN_TESTING, actor="Lab.Analyst", note="Testing started")

        if random.random() < 0.85:
            s.transition(SampleStatus.RESULT_ENTERED, actor="Lab.Analyst", note="Results entered")
            if random.random() < 0.1:
                s.transition(SampleStatus.IN_TESTING, actor="QC.Reviewer", note="Sent back — result outside expected range, retest required")
                s.transition(SampleStatus.RESULT_ENTERED, actor="Lab.Analyst", note="Retest results entered")
            s.transition(SampleStatus.REVIEWED, actor="QC.Reviewer", note="Reviewed and approved")
            s.transition(SampleStatus.RELEASED, actor="QA.Release", note="Released")
        else:
            s.transition(SampleStatus.REJECTED, actor="Lab.Analyst", note="Sample integrity compromised")

        results.append({
            "sample_id": s.sample_id, "test_type": s.test_type, "final_status": s.status.value,
            "transitions": len(s.chain_of_custody),
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv("lims_integration/sample_lifecycle_results.csv", index=False)
    print(results_df.final_status.value_counts())

    s0 = Sample(sample_id=samples_df.sample_id.iloc[0], test_type=samples_df.test_type.iloc[0])
    s0.transition(SampleStatus.IN_TESTING, actor="Lab.Analyst")
    s0.transition(SampleStatus.RESULT_ENTERED, actor="Lab.Analyst")
    s0.transition(SampleStatus.REVIEWED, actor="QC.Reviewer")
    s0.transition(SampleStatus.RELEASED, actor="QA.Release")
    print(f"\nExample chain of custody for {s0.sample_id}:")
    for event in s0.chain_of_custody:
        print(f"  {event['timestamp']} | {event['from']} -> {event['to']} | {event['actor']} | {event['note']}")
