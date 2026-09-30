import csv
from pathlib import Path


def generate_csv(costs, filename="reports/cost-report.csv"):

    Path(filename).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Service",
            "Monthly Cost"
        ])

        for service, cost in costs.items():
            writer.writerow([
                service,
                round(cost, 2)
            ])

    return filename
