"""Ghi finalSWP từ báo cáo sun-estimate đã validate vào trường SWP trên GitHub Project.

Chỉ ghi cho task lá (issues[] trong payload); container không có điểm riêng.
Dùng: python scripts/write-swp-to-github-project.py reports/<báo-cáo>.html
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

OWNER = "anhnn-1576"
PROJECT_NUMBER = "1"
FIELD_NAME = "SWP"
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


def read_payload(report: Path) -> dict:
    html = report.read_text(encoding="utf-8")
    match = re.search(r'<script id="report-data" type="application/json">(.*?)</script>', html, re.S)
    if not match:
        raise RuntimeError("Không tìm thấy payload nhúng trong báo cáo")
    payload = json.loads(match.group(1))
    if payload["run"]["calibrationStatus"] not in {"accepted", "calibrated", "skipped"}:
        raise RuntimeError("Báo cáo chưa qua bước review / hiệu chỉnh")
    return payload


def resolve_ids() -> tuple[str, str]:
    project = gh_json("project", "view", PROJECT_NUMBER, "--owner", OWNER, "--format", "json")
    fields = gh_json("project", "field-list", PROJECT_NUMBER, "--owner", OWNER, "--format", "json")["fields"]
    field = next((f for f in fields if f["name"] == FIELD_NAME), None)
    if field is None:
        raise RuntimeError(f"Project không có trường {FIELD_NAME}")
    return project["id"], field["id"]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    payload = read_payload(Path(sys.argv[1]))
    by_number = {v["number"]: v["project_item_id"] for v in json.loads(MAP_FILE.read_text(encoding="utf-8")).values()}
    project_id, field_id = resolve_ids()

    for row in payload["issues"]:
        number = int(row["issueRef"].rsplit("#", 1)[1])
        item_id = by_number.get(number)
        if item_id is None:
            print(f"Dừng: #{number} không có trong {MAP_FILE.name}", file=sys.stderr)
            return 1
        try:
            gh("project", "item-edit", "--id", item_id, "--project-id", project_id,
                    "--field-id", field_id, "--number", str(row["finalSWP"]))
        except RuntimeError as error:
            print(f"Dừng ở #{number}: {error}", file=sys.stderr)
            return 1
        print(f"#{number:>3} SWP = {row['finalSWP']}")
    print(f"Xong: đã ghi {len(payload['issues'])} task lá")
    return 0


if __name__ == "__main__":
    sys.exit(main())
