"""Áp backlog/sprint-plan.json lên GitHub Project: Iteration, Phụ trách (giả định), Status.

Task lá lấy trực tiếp từ file kế hoạch. Container (epic, issue cha) chỉ nhận Status suy ra từ con:
Done khi mọi task lá bên dưới Done, In Progress khi có task lá đã bắt đầu, còn lại Todo.
Dùng: python scripts/apply-sprint-plan-to-github-project.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

OWNER = "anhnn-1576"
PROJECT_NUMBER = "1"
ROOT = Path(__file__).resolve().parent.parent
PLAN_FILE = ROOT / "backlog" / "sprint-plan.json"
MAP_FILE = ROOT / "backlog" / "issue-number-map.json"
ITEMS_FILE = ROOT / "backlog" / "backlog-items.json"
GH = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"


def gh(*args: str) -> str:
    result = subprocess.run([GH, *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} lỗi: {result.stderr.strip()}")
    return result.stdout


def load_fields() -> tuple[str, dict]:
    project_id = json.loads(gh("project", "view", PROJECT_NUMBER, "--owner", OWNER, "--format", "json"))["id"]
    fields = {f["name"]: f for f in json.loads(
        gh("project", "field-list", PROJECT_NUMBER, "--owner", OWNER, "--format", "json"))["fields"]}
    iteration = fields["Iteration"]
    query = '{node(id:"%s"){... on ProjectV2IterationField{configuration{iterations{id title}}}}}' % iteration["id"]
    iterations = json.loads(gh("api", "graphql", "-f", f"query={query}"))["data"]["node"]["configuration"]["iterations"]
    return project_id, {
        "status": (fields["Status"]["id"], {o["name"]: o["id"] for o in fields["Status"]["options"]}),
        "owner": (fields["Phụ trách (giả định)"]["id"],
                  {o["name"]: o["id"] for o in fields["Phụ trách (giả định)"]["options"]}),
        "iteration": (iteration["id"], {i["title"]: i["id"] for i in iterations}),
    }


def parent_statuses(leaves: list[dict]) -> dict[str, str]:
    items = {i["key"]: i for i in json.loads(ITEMS_FILE.read_text(encoding="utf-8"))["items"]}
    by_parent: dict[str, list[str]] = {}
    for leaf in leaves:
        key = items[leaf["key"]].get("parent")
        while key:
            by_parent.setdefault(key, []).append(leaf["status"])
            key = items[key].get("parent")
    result = {}
    for key, statuses in by_parent.items():
        if all(s == "Done" for s in statuses):
            result[key] = "Done"
        elif any(s != "Todo" for s in statuses):
            result[key] = "In Progress"
        else:
            result[key] = "Todo"
    return result


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    plan = json.loads(PLAN_FILE.read_text(encoding="utf-8"))
    issue_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    project_id, fields = load_fields()

    def set_option(item_id: str, field: str, value: str) -> None:
        field_id, options = fields[field]
        flag = "--iteration-id" if field == "iteration" else "--single-select-option-id"
        gh("project", "item-edit", "--id", item_id, "--project-id", project_id,
           "--field-id", field_id, flag, options[value])

    try:
        for leaf in plan["leaves"]:
            item_id = issue_map[leaf["key"]]["project_item_id"]
            set_option(item_id, "iteration", leaf["iteration"])
            set_option(item_id, "owner", leaf["owner"])
            set_option(item_id, "status", leaf["status"])
            print(f"#{leaf['number']:>3} {leaf['iteration']} · {leaf['owner']} · {leaf['status']}")
        for key, status in sorted(parent_statuses(plan["leaves"]).items()):
            set_option(issue_map[key]["project_item_id"], "status", status)
            print(f"#{issue_map[key]['number']:>3} (container {key}) · {status}")
    except (RuntimeError, KeyError) as error:
        print(f"Dừng: {error}", file=sys.stderr)
        return 1
    print("Xong")
    return 0


if __name__ == "__main__":
    sys.exit(main())
