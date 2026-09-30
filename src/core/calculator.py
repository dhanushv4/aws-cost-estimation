import json
from pathlib import Path


class CostCalculator:

    HOURS_PER_MONTH = 730

    def __init__(self):
        pricing_file = Path(__file__).resolve().parents[2] / "config" / "pricing.json"

        with open(pricing_file, "r", encoding="utf-8") as file:
            self.pricing = json.load(file)

    def ec2_cost(self, instance_type, quantity):
        hourly = self.pricing["ec2"].get(instance_type, 0)
        return hourly * self.HOURS_PER_MONTH * quantity

    def ebs_cost(self, volume_type, storage_gb):
        price_per_gb = self.pricing["ebs"].get(volume_type, 0)
        return price_per_gb * storage_gb

    def s3_cost(self, storage_gb):
        price_per_gb = self.pricing["s3"]["standard"]
        return price_per_gb * storage_gb

    def rds_cost(self, instance_type, quantity):
        hourly = self.pricing["rds"].get(instance_type, 0)
        return hourly * self.HOURS_PER_MONTH * quantity

    def lambda_cost(self, requests_million):
        price = self.pricing["lambda"]["per_million_requests"]
        return requests_million * price

    def network_cost(self, data_transfer_gb):
        price = self.pricing["network"]["data_transfer_per_gb"]
        return data_transfer_gb * price

    def calculate(self, resources):

        result = {
            "EC2": 0,
            "EBS": 0,
            "S3": 0,
            "RDS": 0,
            "Lambda": 0,
            "Network": 0
        }

        result["EC2"] = self.ec2_cost(
            resources["ec2"]["instance_type"],
            resources["ec2"]["quantity"]
        )

        result["EBS"] = self.ebs_cost(
            resources["ebs"]["volume_type"],
            resources["ebs"]["storage_gb"]
        )

        result["S3"] = self.s3_cost(
            resources["s3"]["storage_gb"]
        )

        result["RDS"] = self.rds_cost(
            resources["rds"]["instance_type"],
            resources["rds"]["quantity"]
        )

        result["Lambda"] = self.lambda_cost(
            resources["lambda"]["requests_million"]
        )

        result["Network"] = self.network_cost(
            resources["network"]["data_transfer_gb"]
        )

        result["Total"] = sum(result.values())

        return result
