def get_user_configuration():

    print()
    print("=" * 60)
    print("        AWS COST ESTIMATION")
    print("=" * 60)

    region = input("Enter AWS region [ap-south-1]: ").strip()

    if not region:
        region = "ap-south-1"

    print()
    print("Available instance types:")
    print("1. t3.micro")
    print("2. t3.small")
    print("3. t3.medium")
    print("4. t3.large")
    print("5. r6i.xlarge")

    print()

    group_count = int(
        input("How many EC2 instance groups? ")
    )

    groups = []

    for i in range(group_count):

        print()
        print(f"========== EC2 GROUP {i + 1} ==========")

        name = input(
            "Group name: "
        ).strip()

        instance_type = input(
            "Instance type: "
        ).strip()

        instance_count = int(
            input("Number of instances: ")
        )

        ebs_gb = float(
            input("EBS storage per instance (GB): ")
        )

        groups.append({
            "name": name,
            "instance_type": instance_type,
            "instance_count": instance_count,
            "ebs_gb": ebs_gb
        })

    print()

    data_transfer = float(
        input("Monthly data transfer (GB): ")
    )

    return {
        "region": region,
        "groups": groups,
        "data_transfer_gb": data_transfer
    }


if __name__ == "__main__":

    config = get_user_configuration()

    print()
    print("=" * 60)
    print("CONFIGURATION RECEIVED")
    print("=" * 60)

    print(f"Region: {config['region']}")

    for group in config["groups"]:
        print()
        print(f"Group: {group['name']}")
        print(
            f"Instance Type: "
            f"{group['instance_type']}"
        )
        print(
            f"Instances: "
            f"{group['instance_count']}"
        )
        print(
            f"EBS: "
            f"{group['ebs_gb']} GB"
        )

    print()
    print(
        f"Data Transfer: "
        f"{config['data_transfer_gb']} GB/month"
    )
