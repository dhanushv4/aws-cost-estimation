from pathlib import Path

from calculator import AWSCostCalculator
from report import ReportGenerator


def print_header():
    print()
    print("=" * 65)
    print("              AWS COST ESTIMATION SYSTEM")
    print("=" * 65)
    print()


def print_configuration(calculator):

    project = calculator.project
    instance = calculator.instance
    storage = calculator.storage
    network = calculator.network

    print("PROJECT CONFIGURATION")
    print("-" * 65)

    print(f"Region              : {project['region_name']}")
    print(f"Region Code         : {project['region']}")

    print()
    print("EC2 CONFIGURATION")
    print("-" * 65)

    print(f"Instance Type       : {instance['instance_type']}")
    print(f"vCPU                : {instance['vcpus']}")
    print(f"Memory              : {instance['memory_gib']} GiB")
    print(
        f"Number of VMs      : "
        f"{instance['number_of_instances']}"
    )
    print(
        f"Hourly Price       : "
        f"${instance['hourly_price']}"
    )

    print()
    print("STORAGE CONFIGURATION")
    print("-" * 65)

    print(
        f"EBS per VM          : "
        f"{storage['ebs_gb_per_instance']} GB"
    )

    print(
        f"EBS price           : "
        f"${storage['ebs_price_per_gb_month']}/GB/month"
    )

    print()
    print("NETWORK CONFIGURATION")
    print("-" * 65)

    print(
        f"Data Transfer       : "
        f"{network['data_transfer_gb_per_month']} GB/month"
    )

    print(
        f"Transfer price      : "
        f"${network['data_transfer_price_per_gb']}/GB"
    )

    print()


def print_monthly_report(report):

    print("12-MONTH COST REPORT")
    print("-" * 65)

    print(
        f"{'Month':<12}"
        f"{'EC2':>12}"
        f"{'EBS':>12}"
        f"{'Network':>12}"
        f"{'Total':>12}"
    )

    print("-" * 65)

    for row in report["monthly_reports"]:

        print(
            f"{row['month']:<12}"
            f"${row['ec2']:>10.2f}"
            f"${row['ebs']:>10.2f}"
            f"${row['network']:>10.2f}"
            f"${row['total']:>10.2f}"
        )

    print("-" * 65)


def print_annual_summary(report):

    summary = report["annual_summary"]

    print()
    print("ANNUAL SUMMARY")
    print("=" * 65)

    print(f"EC2 Cost           : ${summary['ec2']:,.2f}")
    print(f"EBS Cost           : ${summary['ebs']:,.2f}")
    print(f"Network Cost       : ${summary['network']:,.2f}")
    print(
        f"Additional Cost    : "
        f"${summary['additional']:,.2f}"
    )

    print("-" * 65)

    print(
        f"TOTAL ANNUAL COST  : "
        f"${summary['total']:,.2f}"
    )

    print(
        f"MONTHLY AVERAGE    : "
        f"${summary['monthly_average']:,.2f}"
    )

    print("=" * 65)


def main():

    print_header()

    project_root = Path(__file__).resolve().parent.parent

    config_file = project_root / "config" / "pricing.json"

    calculator = AWSCostCalculator(config_file)

    print_configuration(calculator)

    report = calculator.generate_yearly_report()

    print_monthly_report(report)

    print_annual_summary(report)

    report_generator = ReportGenerator(
        project_root / "reports"
    )

    csv_file = report_generator.generate_csv(report)
    json_file = report_generator.generate_json(report)
    txt_file = report_generator.generate_text_summary(report)

    print()
    print("REPORT FILES CREATED")
    print("-" * 65)

    print(f"CSV  : {csv_file}")
    print(f"JSON : {json_file}")
    print(f"TEXT : {txt_file}")

    print()
    print("Cost estimation completed successfully.")
    print()


if __name__ == "__main__":
    main()
