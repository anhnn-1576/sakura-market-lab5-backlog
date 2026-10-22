"""Đẩy backlog/backlog-items.json lên GitHub: tạo issue, nối sub-issue, thêm vào Project.

Chạy lặp được: mục đã có trong backlog/issue-number-map.json thì bỏ qua.
Dùng: python scripts/push-backlog-to-github-project.py
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

OWNER = "anhnn-1576"
REPO = f"{OWNER}/sakura-market-lab5-backlog"
PROJECT_NUMBER = "1"
ROOT = Path(__file__).resolve().parent.parent
ITEMS_FILE = ROOT / "backlog" / "backlog-items.json"
MAP_FILE = ROOT / "backlog" / "issue-number-map.json"
GH = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"

LABEL_COLORS = {
    "epic": "5319e7",
    "clarify": "fbca04",
    "constraint:完納奨励金": "d93f0b",
    "layer:db": "0e8a16",
    "layer:api": "1d76db",
    "layer:ui": "c5def5",
    "layer:test": "bfd4f2",
    "layer:infra": "006b75",
}


def gh(*args: str) -> str:
    result = subprocess.run([GH, *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} lỗi: {result.stderr.strip()}")
    return result.stdout.strip()


def labels_of(item: dict) -> list[str]:
    labels = list(item.get("labels", []))
    if item["level"] == "epic":
        labels.append("epic")
    return labels


def build_body(item: dict, issue_map: dict) -> str:
    lines = [f"**Mã backlog:** `{item['key']}`", f"**Spec / căn cứ:** {item.get('spec', '—')}"]
    parent = item.get("parent")
    if parent:
        lines.append(f"**Cha:** #{issue_map[parent]['number']} (`{parent}`)")
    lines += ["", item.get("desc", "").replace("\nXong khi:", "\n\n**Xong khi:**")]
    lines += ["", "---", "Nguồn: [`backlog/backlog-items.json`](../blob/main/backlog/backlog-items.json) · "
              "Tiền đề: [`PREMISE.md`](../blob/main/PREMISE.md) · Nguyên tắc chia: [`task-breakdown.md`](../blob/main/task-breakdown.md)"]
    return "\n".join(lines)


def ensure_labels(items: list[dict]) -> None:
    used = {label for item in items for label in labels_of(item)}
    for label in sorted(used):
        gh("label", "create", label, "--repo", REPO, "--color", LABEL_COLORS.get(label, "ededed"), "--force")


def save_map(issue_map: dict) -> None:
    MAP_FILE.write_text(json.dumps(issue_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def push_item(item: dict, issue_map: dict) -> None:
    args = ["issue", "create", "--repo", REPO, "--title", f"[{item['key']}] {item['title']}",
            "--body", build_body(item, issue_map)]
    for label in labels_of(item):
        args += ["--label", label]
    url = gh(*args).splitlines()[-1]
    number = int(url.rstrip("/").split("/")[-1])
    issue_id = int(gh("api", f"repos/{REPO}/issues/{number}", "--jq", ".id"))

    # Thêm vào Project trước khi nối sub-issue: workflow "auto-add sub-issues" của Project
    # sẽ tự thêm issue con, khiến item-add sau đó báo "already exists".
    item_id = gh("project", "item-add", PROJECT_NUMBER, "--owner", OWNER, "--url", url, "--format", "json", "--jq", ".id")
    parent = item.get("parent")
    if parent:
        gh("api", "-X", "POST", f"repos/{REPO}/issues/{issue_map[parent]['number']}/sub_issues",
           "-F", f"sub_issue_id={issue_id}")

    issue_map[item["key"]] = {"number": number, "id": issue_id, "project_item_id": item_id, "url": url}
    save_map(issue_map)
    print(f"{item['key']:>7} → #{number}")


def main() -> int:
    items = json.loads(ITEMS_FILE.read_text(encoding="utf-8"))["items"]
    issue_map = json.loads(MAP_FILE.read_text(encoding="utf-8")) if MAP_FILE.exists() else {}
    ensure_labels(items)
    for item in items:
        if item["key"] in issue_map:
            continue
        try:
            push_item(item, issue_map)
        except RuntimeError as error:
            print(f"Dừng ở {item['key']}: {error}", file=sys.stderr)
            return 1
        time.sleep(1)  # tránh giới hạn tốc độ tạo nội dung của GitHub
    print(f"Xong: {len(issue_map)}/{len(items)} mục đã có trên GitHub")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("GH_PROMPT_DISABLED", "1")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
