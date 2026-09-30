import json
from pathlib import Path
from datetime import datetime


class AWSCostCalculator:

    def __init__(self, config_path):
        self.config_path = Path(config_path)

        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.project = self.config["project"]
        self.instance = self.config["instance"]
        self.storage = self.config["storage"]
        self.network = self.config["network"]
        self.additional = self.config["additional"]

    def calculate_ec2_monthly_cost(self, hours):
        return (
            self.instance["hourly_price"]
            * self.instance["number_of_instances"]
            * hours
        )

    def calculate_ebs_monthly_cost(self):
        return (
            self.storage["ebs_gb_per_instance"]
            * self.instance["number_of_instances"]
            * self.storage["ebs_price_per_gb_month"]
        )

    def calculate_network_monthly_cost(self):
        return (
            self.network["data_transfer_gb_per_month"]
            * self.network["data_transfer_price_per_gb"]
        )

    def calculate_additional_monthly_cost(self):
        return (
            self.additional["elastic_ip_monthly"]
            + self.additional["cloudwatch_monthly"]
        )

    def calculate_monthly_cost(self, hours):
        ec2 = self.calculate_ec2_monthly_cost(hours)
        ebs = self.calculate_ebs_monthly_cost()
        network = self.calculate_network_monthly_cost()
        additional = self.calculate_additional_monthly_cost()

        total = ec2 + ebs + network + additional

        return {
            "ec2": round(ec2, 2),
            "ebs": round(ebs, 2),
            "network": round(network, 2),
            "additional": round(additional, 2),
            "total": round(total, 2)
        }

    def generate_yearly_report(self):
        monthly_reports = []

        year = datetime.now().year

        for month in range(1, 13):

            # Approximate monthly hours.
            # For a simple estimation model we use 730 hours/month.
            hours = 730

            costs = self.calculate_monthly_cost(hours)

            monthly_reports.append({
                "month": f"{year}-{month:02d}",
                "hours": hours,
                **costs
            })

        annual_ec2 = sum(item["ec2"] for item in monthly_reports)
        annual_ebs = sum(item["ebs"] for item in monthly_reports)
        annual_network = sum(item["network"] for item in monthly_reports)
        annual_additional = sum(
            item["additional"] for item in monthly_reports
        )

        annual_total = (
            annual_ec2
            + annual_ebs
            + annual_network
            + annual_additional
        )

        return {
            "generated_at": datetime.now().isoformat(),
            "project": self.project,
            "instance": self.instance,
            "storage": self.storage,
            "network": self.network,
            "monthly_reports": monthly_reports,
            "annual_summary": {
                "ec2": round(annual_ec2, 2),
                "ebs": round(annual_ebs, 2),
                "network": round(annual_network, 2),
                "additional": round(annual_additional, 2),
                "total": round(annual_total, 2),
                "monthly_average": round(annual_total / 12, 2)
            }
        }
