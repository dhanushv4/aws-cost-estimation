class InstanceComparison:

    def __init__(self, calculator):
        self.calculator = calculator

    def compare(self, instance_types, quantity=1):

        results = []

        for instance_type in instance_types:

            monthly = self.calculator.ec2_cost(
                instance_type,
                quantity
            )

            results.append({
                "instance": instance_type,
                "monthly": round(monthly, 2),
                "annual": round(monthly * 12, 2)
            })

        return results
