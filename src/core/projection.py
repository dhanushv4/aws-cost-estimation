class CostProjection:

    def __init__(self, monthly_cost):
        self.monthly_cost = monthly_cost

    def yearly_projection(self):
        return self.monthly_cost * 12

    def monthly_projection(self):
        return [
            round(self.monthly_cost * month, 2)
            for month in range(1, 13)
        ]

    def projection_data(self):

        values = self.monthly_projection()

        return [
            {
                "month": index + 1,
                "cost": value
            }
            for index, value in enumerate(values)
        ]
