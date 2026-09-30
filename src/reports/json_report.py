import json
from pathlib import Path


def generate_json(costs, filename="reports/cost-report.json"):

    Path(filename).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(filename, "w", encoding="utf-8") as file:

        json.dump(
            costs,
            file,
            indent=4
        )

    return filename
