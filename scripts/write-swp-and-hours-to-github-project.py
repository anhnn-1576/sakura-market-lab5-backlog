"""Ghi finalSWP và giờ ước lượng từ báo cáo sun-estimate đã validate lên GitHub Project.

Chỉ ghi cho task lá (issues[] trong payload); container không có điểm riêng.
Quy tắc giờ (estimate.md mục 3): giờ = SWP × 1,5 + 1 giờ quality gate; issue làm rõ (nhãn clarify) không cộng 1 giờ.
Dùng: python scripts/write-swp-and-hours-to-github-project.py reports/<báo-cáo>.html
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

OWNER = "anhnn-1576"
PROJECT_NUMBER = "1"
SWP_FIELD = "SWP"
HOURS_FIELD = "Estimate (h)"
HOURS_PER_SWP = 1.5
QUALITY_GATE_HOURS = 1
ROOT = Path(__file__).resolve().parent.parent
MAP_FILE = ROOT / "backlog" / "issue-number-map.json"
GH = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"


def gh(*args: str) -> str:
    result = subprocess.run([GH, *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} lỗi: {result.stderr.strip()}")
    return result.stdout


def gh_json(*args: str):
    return json.loads(gh(*args))


def hours_for(row: dict) -> float:
    gate = 0 if "clarify" in row["labels"] else QUALITY_GATE_HOURS
    return row["finalSWP"] * HOURS_PER_SWP + gate


def read_payload(report: Path) -> dict:
    html = report.read_text(encoding="utf-8")
    match = re.search(r'<script id="report-data" type="application/json">(.*?)</script>', html, re.S)
    if not match:
        raise RuntimeError("Không tìm thấy payload nhúng trong báo cáo")
    payload = json.loads(match.group(1))
    if payload["run"]["calibrationStatus"] not in {"accepted", "calibrated", "skipped"}:
        raise RuntimeError("Báo cáo chưa qua bước review / hiệu chỉnh")
    return payload


def resolve_ids() -> tuple[str, dict]:
    project = gh_json("project", "view", PROJECT_NUMBER, "--owner", OWNER, "--format", "json")
    fields = gh_json("project", "field-list", PROJECT_NUMBER, "--owner", OWNER, "--format", "json")["fields"]
    ids = {f["name"]: f["id"] for f in fields if f["name"] in (SWP_FIELD, HOURS_FIELD)}
    missing = {SWP_FIELD, HOURS_FIELD} - set(ids)
    if missing:
        raise RuntimeError(f"Project thiếu trường {', '.join(sorted(missing))}")
    return project["id"], ids


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    payload = read_payload(Path(sys.argv[1]))
    by_number = {v["number"]: v["project_item_id"] for v in json.loads(MAP_FILE.read_text(encoding="utf-8")).values()}
    project_id, field_ids = resolve_ids()

    for row in payload["issues"]:
        number = int(row["issueRef"].rsplit("#", 1)[1])
        item_id = by_number.get(number)
        if item_id is None:
            print(f"Dừng: #{number} không có trong {MAP_FILE.name}", file=sys.stderr)
            return 1
        values = {SWP_FIELD: row["finalSWP"], HOURS_FIELD: hours_for(row)}
        try:
            for name, value in values.items():
                gh("project", "item-edit", "--id", item_id, "--project-id", project_id,
                   "--field-id", field_ids[name], "--number", str(value))
        except RuntimeError as error:
            print(f"Dừng ở #{number}: {error}", file=sys.stderr)
            return 1
        print(f"#{number:>3} SWP = {values[SWP_FIELD]}, giờ = {values[HOURS_FIELD]}")
    print(f"Xong: đã ghi {len(payload['issues'])} task lá")
    return 0


if __name__ == "__main__":
    sys.exit(main())
