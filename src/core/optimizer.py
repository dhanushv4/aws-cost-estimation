class CostOptimizer:

    def __init__(self, calculator):
        self.calculator = calculator

    def analyze(self, resources, budget):

        costs = self.calculator.calculate(resources)

        suggestions = []

        total = costs["Total"]

        if total > budget:
            suggestions.append(
                f"Estimated monthly cost is ${total:.2f}, "
                f"which is above your ${budget:.2f} budget."
            )

        if costs["EC2"] > total * 0.60:
            suggestions.append(
                "EC2 is the largest cost component. "
                "Consider reviewing instance sizes and quantities."
            )

        if costs["EBS"] > 20:
            suggestions.append(
                "EBS cost is relatively high. "
                "Review unused or oversized volumes."
            )

        if costs["S3"] > 20:
            suggestions.append(
                "S3 storage cost is relatively high. "
                "Review storage usage and lifecycle policies."
            )

        if not suggestions:
            suggestions.append(
                "No major optimization suggestions based on "
                "the current estimation."
            )

        return suggestions
