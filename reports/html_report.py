import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

def get_overall(rows, key="criticality"):
    """Общий статус секции — худший из всех строк."""
    levels = {"OK": 0, "WARNING": 1, "CRITICAL": 2}
    worst = "OK"
    for r in rows:
        c = r.get(key, "OK")
        if levels.get(c, 0) > levels[worst]:
            worst = c
    return worst

def generate(sections: list[dict], output_path: str, command: str):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report.html")

    html = template.render(
        db_host=os.getenv("DB_HOST", "unknown"),
        db_name=os.getenv("DB_NAME", "unknown"),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        command=command,
        sections=sections,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nReport saved: {output_path}")