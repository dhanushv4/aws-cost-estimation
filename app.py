import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime
import json
import csv
import subprocess
import sys
import os

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config" / "pricing.json"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

DEFAULT_PRICES = {
    "t3.micro": {
        "vcpus": 2,
        "memory_gib": 1,
        "hourly_price": 0.0104
    },
    "t3.small": {
        "vcpus": 2,
        "memory_gib": 2,
        "hourly_price": 0.0208
    },
    "t3.medium": {
        "vcpus": 2,
        "memory_gib": 4,
        "hourly_price": 0.0416
    },
    "t3.large": {
        "vcpus": 2,
        "memory_gib": 8,
        "hourly_price": 0.0832
    },
    "r6i.xlarge": {
        "vcpus": 4,
        "memory_gib": 32,
        "hourly_price": 0.252
    }
}

if CONFIG_FILE.exists():
    try:
        PRICES = json.loads(CONFIG_FILE.read_text())
    except Exception:
        PRICES = DEFAULT_PRICES
else:
    PRICES = DEFAULT_PRICES
    CONFIG_FILE.write_text(
        json.dumps(PRICES, indent=4)
    )

MONTHLY_HOURS = 730
DEFAULT_EBS_PRICE = 0.10
DEFAULT_TRANSFER_PRICE = 0.09


class AWSCostEstimator:

    def __init__(self, root):

        self.root = root
        self.root.title("AWS Cost Estimation Dashboard")
        self.root.geometry("1200x760")
        self.root.minsize(1050, 700)

        self.groups = []

        self.setup_style()
        self.create_interface()

    # -------------------------------------------------
    # STYLE
    # -------------------------------------------------

    def setup_style(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "TFrame",
            background="#0b1220"
        )

        style.configure(
            "Card.TFrame",
            background="#111c2e"
        )

        style.configure(
            "TLabel",
            background="#0b1220",
            foreground="#e5edf7",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Card.TLabel",
            background="#111c2e",
            foreground="#e5edf7"
        )

        style.configure(
            "Title.TLabel",
            background="#0b1220",
            foreground="#67e8f9",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Sub.TLabel",
            background="#0b1220",
            foreground="#94a3b8",
            font=("Segoe UI", 10)
        )

        style.configure(
            "TButton",
            padding=10,
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Accent.TButton",
            background="#0891b2",
            foreground="white"
        )

        style.configure(
            "Treeview",
            background="#0f1a2b",
            fieldbackground="#0f1a2b",
            foreground="#e5edf7",
            rowheight=32
        )

        style.configure(
            "Treeview.Heading",
            background="#17243a",
            foreground="#67e8f9",
            font=("Segoe UI", 10, "bold")
        )

    # -------------------------------------------------
    # MAIN INTERFACE
    # -------------------------------------------------

    def create_interface(self):

        self.root.configure(
            background="#0b1220"
        )

        # HEADER

        header = ttk.Frame(self.root)

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        ttk.Label(
            header,
            text="AWS Cost Estimation",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="AWS infrastructure cost projection • Local pricing model",
            style="Sub.TLabel"
        ).pack(anchor="w")

        # GLOBAL CONFIGURATION

        config = ttk.Frame(self.root)

        config.pack(
            fill="x",
            padx=30,
            pady=10
        )

        # REGION

        region_card = ttk.Frame(
            config,
            style="Card.TFrame",
            padding=18
        )

        region_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        ttk.Label(
            region_card,
            text="AWS REGION",
            style="Card.TLabel"
        ).pack(anchor="w")

        self.region = ttk.Combobox(
            region_card,
            values=[
                "ap-south-1",
                "ap-south-2",
                "ap-southeast-1",
                "us-east-1",
                "us-west-2",
                "eu-west-1"
            ],
            state="readonly"
        )

        self.region.set("ap-south-1")

        self.region.pack(
            fill="x",
            pady=(8, 0)
        )

        # TRANSFER

        transfer_card = ttk.Frame(
            config,
            style="Card.TFrame",
            padding=18
        )

        transfer_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )

        ttk.Label(
            transfer_card,
            text="DATA TRANSFER GB / MONTH",
            style="Card.TLabel"
        ).pack(anchor="w")

        self.transfer = ttk.Entry(
            transfer_card
        )

        self.transfer.insert(
            0,
            "100"
        )

        self.transfer.pack(
            fill="x",
            pady=(8, 0)
        )

        # EBS

        ebs_card = ttk.Frame(
            config,
            style="Card.TFrame",
            padding=18
        )

        ebs_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(8, 0)
        )

        ttk.Label(
            ebs_card,
            text="EBS PRICE / GB / MONTH",
            style="Card.TLabel"
        ).pack(anchor="w")

        self.ebs_price = ttk.Entry(
            ebs_card
        )

        self.ebs_price.insert(
            0,
            str(DEFAULT_EBS_PRICE)
        )

        self.ebs_price.pack(
            fill="x",
            pady=(8, 0)
        )

        # MAIN AREA

        main = ttk.Frame(self.root)

        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        # LEFT

        left = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=18
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        ttk.Label(
            left,
            text="EC2 INSTANCE GROUPS",
            style="Card.TLabel",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        ttk.Label(
            left,
            text="Create any number of server groups.",
            style="Card.TLabel"
        ).pack(anchor="w", pady=(4, 15))

        # FORM

        form = ttk.Frame(
            left,
            style="Card.TFrame"
        )

        form.pack(fill="x")

        ttk.Label(
            form,
            text="Group Name",
            style="Card.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.group_name = ttk.Entry(
            form
        )

        self.group_name.insert(
            0,
            "Web Server"
        )

        self.group_name.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10
        )

        ttk.Label(
            form,
            text="Instance Type",
            style="Card.TLabel"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.instance_type = ttk.Combobox(
            form,
            values=list(PRICES.keys()),
            state="readonly"
        )

        self.instance_type.set(
            "t3.medium"
        )

        self.instance_type.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10
        )

        ttk.Label(
            form,
            text="Number of Instances",
            style="Card.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.instance_count = ttk.Entry(
            form
        )

        self.instance_count.insert(
            0,
            "2"
        )

        self.instance_count.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10
        )

        ttk.Label(
            form,
            text="EBS GB / Instance",
            style="Card.TLabel"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.ebs_storage = ttk.Entry(
            form
        )

        self.ebs_storage.insert(
            0,
            "30"
        )

        self.ebs_storage.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10
        )

        form.columnconfigure(
            1,
            weight=1
        )

        # BUTTONS

        buttons = ttk.Frame(
            left,
            style="Card.TFrame"
        )

        buttons.pack(
            fill="x",
            pady=15
        )

        ttk.Button(
            buttons,
            text="+ Add Group",
            style="Accent.TButton",
            command=self.add_group
        ).pack(
            side="left"
        )

        ttk.Button(
            buttons,
            text="Remove Selected",
            command=self.remove_group
        ).pack(
            side="left",
            padx=8
        )

        ttk.Button(
            buttons,
            text="Clear",
            command=self.clear_groups
        ).pack(
            side="left"
        )

        # TABLE

        self.table = ttk.Treeview(
            left,
            columns=(
                "group",
                "type",
                "qty",
                "cpu",
                "ram",
                "ebs"
            ),
            show="headings"
        )

        columns = {
            "group": "Group",
            "type": "Instance Type",
            "qty": "Qty",
            "cpu": "vCPU",
            "ram": "RAM GiB",
            "ebs": "EBS GB"
        }

        for key, title in columns.items():

            self.table.heading(
                key,
                text=title
            )

            self.table.column(
                key,
                width=90,
                anchor="center"
            )

        self.table.column(
            "group",
            width=140,
            anchor="w"
        )

        self.table.pack(
            fill="both",
            expand=True
        )

        # RIGHT

        right = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=18
        )

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        ttk.Label(
            right,
            text="COST SUMMARY",
            style="Card.TLabel",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        self.monthly_label = self.create_kpi(
            right,
            "MONTHLY ESTIMATE"
        )

        self.annual_label = self.create_kpi(
            right,
            "12-MONTH ESTIMATE"
        )

        self.ec2_label = self.create_kpi(
            right,
            "ANNUAL EC2"
        )

        self.ebs_label = self.create_kpi(
            right,
            "ANNUAL EBS"
        )

        self.network_label = self.create_kpi(
            right,
            "ANNUAL NETWORK"
        )

        ttk.Button(
            right,
            text="Calculate & Generate Report",
            style="Accent.TButton",
            command=self.calculate
        ).pack(
            fill="x",
            pady=(15, 8)
        )

        ttk.Button(
            right,
            text="Open Reports Folder",
            command=self.open_reports
        ).pack(
            fill="x"
        )

        # OUTPUT

        output_frame = ttk.Frame(
            self.root,
            style="Card.TFrame",
            padding=15
        )

        output_frame.pack(
            fill="both",
            padx=30,
            pady=(0, 25)
        )

        ttk.Label(
            output_frame,
            text="REPORT PREVIEW",
            style="Card.TLabel",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        self.output = tk.Text(
            output_frame,
            height=8,
            background="#0f1a2b",
            foreground="#dbeafe",
            insertbackground="white",
            relief="flat",
            font=("Consolas", 10)
        )

        self.output.pack(
            fill="both",
            expand=True,
            pady=(8, 0)
        )

    # -------------------------------------------------
    # KPI
    # -------------------------------------------------

    def create_kpi(
        self,
        parent,
        title
    ):

        frame = ttk.Frame(
            parent,
            style="Card.TFrame",
            padding=10
        )

        frame.pack(
            fill="x",
            pady=4
        )

        ttk.Label(
            frame,
            text=title,
            style="Card.TLabel"
        ).pack(
            anchor="w"
        )

        value = ttk.Label(
            frame,
            text="$0.00",
            style="Card.TLabel",
            font=("Segoe UI", 16, "bold")
        )

        value.pack(
            anchor="w"
        )

        return value

    # -------------------------------------------------
    # ADD GROUP
    # -------------------------------------------------

    def add_group(self):

        try:

            name = self.group_name.get().strip()

            if not name:
                name = f"Group {len(self.groups) + 1}"

            instance_type = self.instance_type.get()

            count = int(
                self.instance_count.get()
            )

            ebs = float(
                self.ebs_storage.get()
            )

            if count <= 0:
                raise ValueError

            if ebs < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Enter valid instance count and EBS values."
            )

            return

        price = PRICES[
            instance_type
        ]

        group = {
            "name": name,
            "instance_type": instance_type,
            "instances": count,
            "ebs_gb": ebs,
            "vcpus": price["vcpus"],
            "memory_gib": price["memory_gib"],
            "hourly_price": price["hourly_price"]
        }

        self.groups.append(
            group
        )

        self.table.insert(
            "",
            "end",
            values=(
                name,
                instance_type,
                count,
                price["vcpus"],
                price["memory_gib"],
                ebs
            )
        )

        self.group_name.delete(
            0,
            "end"
        )

        self.group_name.insert(
            0,
            f"Group {len(self.groups) + 1}"
        )

    # -------------------------------------------------
    # REMOVE
    # -------------------------------------------------

    def remove_group(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Remove",
                "Select a group first."
            )

            return

        indexes = [
            self.table.index(item)
            for item in selected
        ]

        for index in sorted(
            indexes,
            reverse=True
        ):

            self.groups.pop(
                index
            )

        for item in selected:

            self.table.delete(
                item
            )

    # -------------------------------------------------
    # CLEAR
    # -------------------------------------------------

    def clear_groups(self):

        self.groups.clear()

        for item in self.table.get_children():

            self.table.delete(
                item
            )

    # -------------------------------------------------
    # CALCULATE
    # -------------------------------------------------

    def calculate(self):

        if not self.groups:

            messagebox.showerror(
                "No EC2 Groups",
                "Add at least one EC2 group."
            )

            return

        try:

            transfer = float(
                self.transfer.get()
            )

            ebs_price = float(
                self.ebs_price.get()
            )

            if transfer < 0:
                raise ValueError

            if ebs_price < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Enter valid network and EBS values."
            )

            return

        ec2_monthly = 0
        ebs_monthly = 0

        for group in self.groups:

            ec2_monthly += (
                group["instances"]
                * group["hourly_price"]
                * MONTHLY_HOURS
            )

            ebs_monthly += (
                group["instances"]
                * group["ebs_gb"]
                * ebs_price
            )

        network_monthly = (
            transfer
            * DEFAULT_TRANSFER_PRICE
        )

        total_monthly = (
            ec2_monthly
            + ebs_monthly
            + network_monthly
        )

        annual_ec2 = ec2_monthly * 12
        annual_ebs = ebs_monthly * 12
        annual_network = network_monthly * 12
        annual_total = total_monthly * 12

        self.monthly_label.config(
            text=f"${total_monthly:,.2f}"
        )

        self.annual_label.config(
            text=f"${annual_total:,.2f}"
        )

        self.ec2_label.config(
            text=f"${annual_ec2:,.2f}"
        )

        self.ebs_label.config(
            text=f"${annual_ebs:,.2f}"
        )

        self.network_label.config(
            text=f"${annual_network:,.2f}"
        )

        self.generate_reports(
            ec2_monthly,
            ebs_monthly,
            network_monthly,
            total_monthly,
            annual_total
        )

    # -------------------------------------------------
    # REPORT GENERATION
    # -------------------------------------------------

    def generate_reports(
        self,
        ec2_monthly,
        ebs_monthly,
        network_monthly,
        monthly_total,
        annual_total
    ):

        now = datetime.now()

        timestamp = now.strftime(
            "%Y%m%d_%H%M%S"
        )

        csv_file = (
            REPORT_DIR
            / f"billing_{timestamp}.csv"
        )

        json_file = (
            REPORT_DIR
            / f"billing_{timestamp}.json"
        )

        html_file = (
            REPORT_DIR
            / f"billing_{timestamp}.html"
        )

        monthly_rows = []

        for month in range(1, 13):

            monthly_rows.append(
                {
                    "month":
                   
     f"{now.year}-{month:02d}",

                    "ec2":
                        round(ec2_monthly, 2),

                    "ebs":
                        round(ebs_monthly, 2),

                    "network":
                        round(network_monthly, 2),

                    "total":
                        round(monthly_total, 2)
                }
            )

        report = {

            "generated_at":
                now.isoformat(),

            "region":
                self.region.get(),

            "pricing_model":
                "Local configurable pricing model",

            "groups":
                self.groups,

            "monthly":
                monthly_rows,

            "annual":
                {
                    "ec2":
                        round(
                            ec2_monthly * 12,
                            2
                        ),

                    "ebs":
                        round(
                            ebs_monthly * 12,
                            2
                        ),

                    "network":
                        round(
                            network_monthly * 12,
                            2
                        ),

                    "total":
                        round(
                            annual_total,
                            2
                        )
                }
        }

        # JSON

        json_file.write_text(
            json.dumps(
                report,
                indent=4
            ),
            encoding="utf-8"
        )

        # CSV

        with open(
            csv_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow(
                [
                    "Month",
                    "EC2",
                    "EBS",
                    "Network",
                    "Total"
                ]
            )

            for row in monthly_rows:

                writer.writerow(
                    [
                        row["month"],
                        row["ec2"],
                        row["ebs"],
                        row["network"],
                        row["total"]
                    ]
                )

            writer.writerow([])

            writer.writerow(
                [
                    "ANNUAL TOTAL",
                    ec2_monthly * 12,
                    ebs_monthly * 12,
                    network_monthly * 12,
                    annual_total
                ]
            )

        # HTML

        rows_html = ""

        for row in monthly_rows:

            rows_html += f"""
            <tr>
                <td>{row['month']}</td>
                <td>${row['ec2']:,.2f}</td>
                <td>${row['ebs']:,.2f}</td>
                <td>${row['network']:,.2f}</td>
                <td>${row['total']:,.2f}</td>
            </tr>
            """

        html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>AWS Cost Report</title>

<style>

body {{
    font-family: Arial;
    background: #0b1220;
    color: #e5edf7;
    padding: 40px;
}}

.container {{
    max-width: 1000px;
    margin: auto;
    background: #111c2e;
    padding: 30px;
    border-radius: 15px;
}}

h1 {{
    color: #67e8f9;
}}

.total {{
    font-size: 30px;
    color: #67e8f9;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 25px;
}}

th,
td {{
    padding: 12px;
    border-bottom: 1px solid #26364f;
    text-align: right;
}}

th:first-child,
td:first-child {{
    text-align: left;
}}

th {{
    color: #67e8f9;
}}

.note {{
    margin-top: 30px;
    color: #94a3b8;
}}

</style>

</head>

<body>

<div class="container">

<h1>AWS 12-Month Cost Estimation</h1>

<p>
Region: {self.region.get()}
</p>

<p>
Generated:
{now.strftime("%Y-%m-%d %H:%M:%S")}
</p>

<p class="total">

Annual Estimate:
${annual_total:,.2f}

</p>

<table>

<tr>

<th>Month</th>

<th>EC2</th>

<th>EBS</th>

<th>Network</th>

<th>Total</th>

</tr>

{rows_html}

</table>

<p class="note">

This is an estimated infrastructure cost
generated from a local pricing model.
It is not an actual AWS billing statement.

</p>

</div>

</body>

</html>
"""

        html_file.write_text(
            html,
            encoding="utf-8"
        )

        # PREVIEW

        self.output.delete(
            "1.0",
            "end"
        )

        self.output.insert(
            "end",
            "AWS COST ESTIMATION REPORT\n"
        )

        self.output.insert(
            "end",
            "=" * 65
            + "\n\n"
        )

        self.output.insert(
            "end",
            f"Region       : {self.region.get()}\n"
        )

        self.output.insert(
            "end",
            f"EC2 Groups   : {len(self.groups)}\n\n"
        )

        for group in self.groups:

            annual = (
                group["instances"]
                * group["hourly_price"]
                * MONTHLY_HOURS
                * 12
            )

            self.output.insert(
                "end",
                f"{group['name']:<20}"
                f"{group['instance_type']:<15}"
                f"Qty {group['instances']:<3}"
                f"Annual EC2 ${annual:,.2f}\n"
            )

        self.output.insert(
            "end",
            "\n"
            + "-" * 65
            + "\n"
        )

        self.output.insert(
            "end",
            f"Annual EC2      : "
            f"${ec2_monthly * 12:,.2f}\n"
        )

        self.output.insert(
            "end",
            f"Annual EBS      : "
            f"${ebs_monthly * 12:,.2f}\n"
        )

        self.output.insert(
            "end",
            f"Annual Network  : "
            f"${network_monthly * 12:,.2f}\n"
        )

        self.output.insert(
            "end",
            f"TOTAL ANNUAL    : "
            f"${annual_total:,.2f}\n"
        )

        self.output.insert(
            "end",
            "\nReports generated:\n"
        )

        self.output.insert(
            "end",
            f"{csv_file.name}\n"
        )

        self.output.insert(
            "end",
            f"{json_file.name}\n"
        )

        self.output.insert(
            "end",
            f"{html_file.name}\n"
        )

        messagebox.showinfo(
            "Report Generated",
            "12-month billing reports generated successfully."
        )

    # -------------------------------------------------
    # OPEN REPORTS
    # -------------------------------------------------

    def open_reports(self):

        try:

            if sys.platform.startswith("win"):

                os.startfile(
                    REPORT_DIR
                )

            elif sys.platform == "darwin":

                subprocess.run(
                    [
                        "open",
                        str(REPORT_DIR)
                    ]
                )

            else:

                subprocess.run(
                    [
                        "xdg-open",
                        str(REPORT_DIR)
                    ]
                )

        except Exception:

            messagebox.showinfo(
                "Reports Folder",
                str(REPORT_DIR)
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = AWSCostEstimator(
        root
    )

    root.mainloop()
