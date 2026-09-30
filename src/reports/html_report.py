from pathlib import Path


def generate_html(costs, filename="reports/cost-report.html"):

    Path(filename).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    rows = ""

    for service, cost in costs.items():

        rows += f"""
        <tr>
            <td>{service}</td>
            <td>${cost:,.2f}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>

<html>

<head>

<title>AWS Cost Estimation Report</title>

<style>

body {{
    font-family: Arial;
    background: #0f172a;
    color: white;
    padding: 40px;
}}

h1 {{
    color: #38bdf8;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 30px;
}}

th, td {{
    padding: 15px;
    border-bottom: 1px solid #334155;
    text-align: left;
}}

th {{
    color: #38bdf8;
}}

</style>

</head>

<body>

<h1>AWS Cost Estimation Report</h1>

<table>

<tr>
<th>Service</th>
<th>Monthly Cost</th>
</tr>

{rows}

</table>

</body>

</html>
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

    return filename
