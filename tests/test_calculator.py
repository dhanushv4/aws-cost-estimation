from src.core.calculator import CostCalculator


def test_ec2_cost():

    calculator = CostCalculator()

    cost = calculator.ec2_cost(
        "t3.micro",
        1
    )

    assert cost > 0


def test_ebs_cost():

    calculator = CostCalculator()

    cost = calculator.ebs_cost(
        "gp3",
        20
    )

    assert cost == 1.6


def test_total_cost():

    calculator = CostCalculator()

    resources = {

        "ec2": {
            "instance_type": "t3.micro",
            "quantity": 1
        },

        "ebs": {
            "volume_type": "gp3",
            "storage_gb": 20
        },

        "s3": {
            "storage_gb": 10
        },

        "rds": {
            "instance_type": "db.t3.micro",
            "quantity": 1
        },

        "lambda": {
            "requests_million": 1
        },

        "network": {
            "data_transfer_gb": 5
        }
    }

    result = calculator.calculate(resources)

    assert result["Total"] > 0
