from dataclasses import dataclass
from typing import List


@dataclass
class RoadmapItem:
    control_id: str
    wave: int
    owner: str
    action: str
    review_trigger: str
    source_result: str


def build_roadmap(results: List[dict]) -> List[RoadmapItem]:
    roadmap = []
    for result in results:
        if result["status"] == "missed":
            wave = 1
            action = "implement and retest interruption"
        elif result["status"] == "late":
            wave = 2
            action = "improve detection and response"
        else:
            continue
        roadmap.append(RoadmapItem(
            result["control_id"], wave, result["owner"], action,
            "failed retest or material path change", result["status"]
        ))
    return sorted(roadmap, key=lambda item: (item.wave, item.control_id))


def render_roadmap(roadmap: List[RoadmapItem]) -> None:
    for item in roadmap:
        print(
            f"Wave {item.wave} | {item.control_id} | "
            f"{item.owner} | {item.action}"
        )


if __name__ == "__main__":
    validation_results = [
        {"control_id": "web-filtering", "status": "missed", "owner": "Web Platform"},
        {"control_id": "c2-detection", "status": "late", "owner": "Security Operations"},
        {"control_id": "session-revocation", "status": "passed", "owner": "Identity Team"},
    ]
    render_roadmap(build_roadmap(validation_results))
