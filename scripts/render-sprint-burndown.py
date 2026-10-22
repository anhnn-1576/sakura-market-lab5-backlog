"""Vẽ burndown (giờ còn lại) của một sprint từ backlog/sprint-plan.json ra SVG và in bảng Markdown.

Giờ chỉ "cháy" khi task lá chuyển Done (doneOn). Task In Review / In Progress vẫn tính là còn lại.
Dùng: python scripts/render-sprint-burndown.py "Sprint 1" reports/burndown-sprint-1.svg
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_FILE = ROOT / "backlog" / "sprint-plan.json"
W, H, PAD = 720, 360, 56


def series(plan: dict, sprint_name: str) -> tuple[list[str], float, list[float], list[float]]:
    sprint = next(s for s in plan["sprints"] if s["name"] == sprint_name)
    days = sprint["workingDays"]
    leaves = [l for l in plan["leaves"] if l["iteration"] == sprint_name]
    total = sum(l["hours"] for l in leaves)
    actual = [total - sum(l["hours"] for l in leaves if l["doneOn"] and l["doneOn"] <= day) for day in days]
    ideal = [total - total * i / (len(days) - 1) for i in range(len(days))]
    return days, total, ideal, actual


def to_svg(days: list[str], total: float, ideal: list[float], actual: list[float], title: str) -> str:
    def x(i: int) -> float:
        return PAD + i * (W - 2 * PAD) / (len(days) - 1)

    def y(v: float) -> float:
        return H - PAD - v * (H - 2 * PAD) / total

    def path(values: list[float]) -> str:
        return " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))

    grid = "".join(
        f'<line x1="{PAD}" y1="{y(v):.1f}" x2="{W - PAD}" y2="{y(v):.1f}" stroke="#e5e7eb"/>'
        f'<text x="{PAD - 8}" y="{y(v) + 4:.1f}" text-anchor="end" font-size="11" fill="#6b7280">{v:.0f}</text>'
        for v in (total * k / 4 for k in range(5)))
    labels = "".join(
        f'<text x="{x(i):.1f}" y="{H - PAD + 18}" text-anchor="middle" font-size="11" fill="#6b7280">{d[8:]}/{d[5:7]}</text>'
        for i, d in enumerate(days))
    dots = "".join(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3" fill="#dc2626"/>' for i, v in enumerate(actual))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif">
<rect width="{W}" height="{H}" fill="#ffffff"/>
<text x="{PAD}" y="28" font-size="15" font-weight="bold" fill="#111827">{title}: giờ còn lại (tổng cam kết {total:g} h)</text>
{grid}{labels}
<polyline points="{path(ideal)}" fill="none" stroke="#9ca3af" stroke-width="2" stroke-dasharray="6 4"/>
<polyline points="{path(actual)}" fill="none" stroke="#dc2626" stroke-width="2.5"/>{dots}
<text x="{W - PAD}" y="48" text-anchor="end" font-size="12" fill="#9ca3af">- - - Kế hoạch (đều mỗi ngày)</text>
<text x="{W - PAD}" y="64" text-anchor="end" font-size="12" fill="#dc2626">━ Thực tế (giờ của task đã Done)</text>
</svg>
"""


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    plan = json.loads(PLAN_FILE.read_text(encoding="utf-8"))
    days, total, ideal, actual = series(plan, sys.argv[1])
    Path(sys.argv[2]).write_text(to_svg(days, total, ideal, actual, sys.argv[1]), encoding="utf-8")
    print("| Ngày | Kế hoạch còn lại (h) | Thực tế còn lại (h) | Lệch (h) |\n|---|---:|---:|---:|")
    for day, i, a in zip(days, ideal, actual):
        print(f"| {day[8:]}/{day[5:7]} | {i:.1f} | {a:.1f} | {a - i:+.1f} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
