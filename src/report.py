import csv
import json
from pathlib import Path


class ReportGenerator:

    def __init__(self, output_directory="reports"):
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate_csv(self, report):

        output_file = self.output_directory / "aws-12-month-billing-report.csv"

        rows = report["monthly_reports"]

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Month",
                "Hours",
                "EC2 Cost",
                "EBS Cost",
                "Network Cost",
                "Additional Cost",
                "Total Cost"
            ])

            for row in rows:

                writer.writerow([
                    row["month"],
                    row["hours"],
                    f'{row["ec2"]:.2f}',
                    f'{row["ebs"]:.2f}',
                    f'{row["network"]:.2f}',
                    f'{row["additional"]:.2f}',
                    f'{row["total"]:.2f}'
                ])

            summary = report["annual_summary"]

            writer.writerow([])

            writer.writerow([
                "ANNUAL TOTAL",
                "",
                f'{summary["ec2"]:.2f}',
                f'{summary["ebs"]:.2f}',
                f'{summary["network"]:.2f}',
                f'{summary["additional"]:.2f}',
                f'{summary["total"]:.2f}'
            ])

            writer.writerow([
                "MONTHLY AVERAGE",
                "",
                "",
                "",
                "",
                "",
                f'{summary["monthly_average"]:.2f}'
            ])

        return output_file

    def generate_json(self, report):

        output_file = self.output_directory / "aws-12-month-billing-report.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return output_file

    def generate_text_summary(self, report):

        output_file = self.output_directory / "aws-billing-summary.txt"

        summary = report["annual_summary"]
        instance = report["instance"]
        project = report["project"]

        content = f"""
AWS COST ESTIMATION REPORT
==========================

Project
-------
{project["name"]}

Region
------
{project["region_name"]}
Region Code: {project["region"]}

EC2 Configuration
-----------------
Instance Type       : {instance["instance_type"]}
vCPU                : {instance["vcpus"]}
Memory              : {instance["memory_gib"]} GiB
Number of Instances : {instance["number_of_instances"]}
Hourly Price        : ${instance["hourly_price"]}

Annual Cost
-----------
EC2 Cost            : ${summary["ec2"]:.2f}
EBS Cost            : ${summary["ebs"]:.2f}
Network Cost        : ${summary["network"]:.2f}
Additional Cost     : ${summary["additional"]:.2f}
--------------------------------
TOTAL ANNUAL COST   : ${summary["total"]:.2f}

Monthly Average
---------------
${summary["monthly_average"]:.2f}

NOTE
----
This is an estimated cost generated using a local pricing model.
It is NOT an actual AWS billing statement.
"""

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content.strip())

        return output_file
