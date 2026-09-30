import tkinter as tk
from tkinter import ttk, messagebox

from src.core.calculator import CostCalculator
from src.core.projection import CostProjection
from src.core.optimizer import CostOptimizer
from src.core.comparison import InstanceComparison

from src.reports.csv_report import generate_csv
from src.reports.json_report import generate_json
from src.reports.html_report import generate_html


class Dashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("AWS Cloud Cost Estimation & Optimization")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)

        self.calculator = CostCalculator()

        self.last_costs = None

        self.setup_style()
        self.create_ui()

    # -------------------------------------------------
    # STYLE
    # -------------------------------------------------

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 22, "bold")
        )

        style.configure(
            "Heading.TLabel",
            font=("Arial", 13, "bold")
        )

        style.configure(
            "Card.TFrame",
            padding=15
        )

        style.configure(
            "TButton",
            padding=8
        )

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def create_ui(self):

        title = ttk.Label(
            self.root,
            text="AWS Cloud Cost Estimation Dashboard",
            style="Title.TLabel"
        )

        title.pack(
            pady=(20, 10)
        )

        subtitle = ttk.Label(
            self.root,
            text="Estimate • Compare • Project • Optimize"
        )

        subtitle.pack(
            pady=(0, 15)
        )

        main = ttk.Frame(
            self.root
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.create_configuration(main)
        self.create_results(main)

    # -------------------------------------------------
    # CONFIGURATION
    # -------------------------------------------------

    def create_configuration(self, parent):

        config = ttk.LabelFrame(
            parent,
            text="Infrastructure Configuration",
            padding=15
        )

        config.pack(
            fill="x",
            pady=10
        )

        # Region

        ttk.Label(
            config,
            text="AWS Region"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.region = ttk.Combobox(
            config,
            values=[
                "ap-south-1",
                "ap-southeast-1",
                "us-east-1",
                "us-west-2",
                "eu-west-1",
                "eu-north-1"
            ],
            state="readonly"
        )

        self.region.set("ap-south-1")

        self.region.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        # EC2

        ttk.Label(
            config,
            text="EC2 Instance"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.ec2_type = ttk.Combobox(
            config,
            values=[
                "t3.micro",
                "t3.small",
                "t3.medium",
                "t3.large",
                "t3.xlarge"
            ],
            state="readonly"
        )

        self.ec2_type.set("t3.micro")

        self.ec2_type.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        ttk.Label(
            config,
            text="EC2 Quantity"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.ec2_quantity = ttk.Entry(config)

        self.ec2_quantity.insert(
            0,
            "1"
        )

        self.ec2_quantity.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        # EBS

        ttk.Label(
            config,
            text="EBS Type"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.ebs_type = ttk.Combobox(
            config,
            values=["gp3", "gp2"],
            state="readonly"
        )

        self.ebs_type.set("gp3")

        self.ebs_type.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        ttk.Label(
            config,
            text="EBS Storage GB"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.ebs_storage = ttk.Entry(config)

        self.ebs_storage.insert(
            0,
            "20"
        )

        self.ebs_storage.grid(
            row=2,
            column=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        # S3

        ttk.Label(
            config,
            text="S3 Storage GB"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.s3_storage = ttk.Entry(config)

        self.s3_storage.insert(
            0,
            "50"
        )

        self.s3_storage.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        # RDS

        ttk.Label(
            config,
            text="RDS Instance"
        ).grid(
            row=3,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.rds_type = ttk.Combobox(
            config,
            values=[
                "db.t3.micro",
                "db.t3.small",
                "db.t3.medium"
            ],
            state="readonly"
        )

        self.rds_type.set(
            "db.t3.micro"
        )

        self.rds_type.grid(
            row=3,
            column=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        # RDS quantity

        ttk.Label(
            config,
            text="RDS Quantity"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.rds_quantity = ttk.Entry(config)

        self.rds_quantity.insert(
            0,
            "1"
        )

        self.rds_quantity.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        # Lambda

        ttk.Label(
            config,
            text="Lambda Requests (Million)"
        ).grid(
            row=4,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.lambda_requests = ttk.Entry(config)

        self.lambda_requests.insert(
            0,
            "1"
        )

        self.lambda_requests.grid(
            row=4,
            column=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        # Network

        ttk.Label(
            config,
            text="Data Transfer GB"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.network = ttk.Entry(config)

        self.network.insert(
            0,
            "10"
        )

        self.network.grid(
            row=5,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        # Budget

        ttk.Label(
            config,
            text="Monthly Budget ($)"
        ).grid(
            row=5,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.budget = ttk.Entry(config)

        self.budget.insert(
            0,
            "50"
        )

        self.budget.grid(
            row=5,
            column=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        for i in range(4):
            config.columnconfigure(
                i,
                weight=1
            )

        # Buttons

        button_frame = ttk.Frame(
            config
        )

        button_frame.grid(
            row=6,
            column=0,
            columnspan=4,
            pady=15
        )

        ttk.Button(
            button_frame,
            text="Calculate Cost",
            command=self.calculate
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Export Reports",
            command=self.export_reports
        ).pack(
            side="left",
            padx=5
        )

    # -------------------------------------------------
    # RESULTS
    # -------------------------------------------------

    def create_results(self, parent):

        results = ttk.LabelFrame(
            parent,
            text="Cost Analysis",
            padding=15
        )

        results.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.result_text = tk.Text(
            results,
            height=18,
            font=("Consolas", 11),
            wrap="word"
        )

        self.result_text.pack(
            fill="both",
            expand=True
        )

    # -------------------------------------------------
    # GET RESOURCES
    # -------------------------------------------------

    def get_resources(self):

        return {

            "ec2": {
                "instance_type": self.ec2_type.get(),
                "quantity": int(
                    self.ec2_quantity.get()
                )
            },

            "ebs": {
                "volume_type": self.ebs_type.get(),
                "storage_gb": float(
                    self.ebs_storage.get()
                )
            },

            "s3": {
                "storage_gb": float(
                    self.s3_storage.get()
                )
            },

            "rds": {
                "instance_type": self.rds_type.get(),
                "quantity": int(
                    self.rds_quantity.get()
                )
            },

            "lambda": {
                "requests_million": float(
                    self.lambda_requests.get()
                )
            },

            "network": {
                "data_transfer_gb": float(
                    self.network.get()
                )
            }
        }

    # -------------------------------------------------
    # CALCULATE
    # -------------------------------------------------

    def calculate(self):

        try:

            resources = self.get_resources()

            budget = float(
                self.budget.get()
            )

            costs = self.calculator.calculate(
                resources
            )

            self.last_costs = costs

            projection = CostProjection(
                costs["Total"]
            )

            optimizer = CostOptimizer(
                self.calculator
            )

            suggestions = optimizer.analyze(
                resources,
                budget
            )

            annual = projection.yearly_projection()

            self.result_text.delete(
                "1.0",
                tk.END
            )

            self.result_text.insert(
                tk.END,
                "\nAWS CLOUD COST ESTIMATION\n"
            )

            self.result_text.insert(
                tk.END,
                "=" * 55 + "\n\n"
            )

            self.result_text.insert(
                tk.END,
                f"Region          : {self.region.get()}\n\n"
            )

            for service, cost in costs.items():

                if service != "Total":

                    self.result_text.insert(
                        tk.END,
                        f"{service:<15}: ${cost:,.2f}\n"
                    )

            self.result_text.insert(
                tk.END,
                "\n"
            )

            self.result_text.insert(
                tk.END,
                f"{'MONTHLY TOTAL':<15}: ${costs['Total']:,.2f}\n"
            )

            self.result_text.insert(
                tk.END,
                f"{'YEARLY TOTAL':<15}: ${annual:,.2f}\n"
            )

            self.result_text.insert(
                tk.END,
                f"{'BUDGET':<15}: ${budget:,.2f}\n\n"
            )

            if costs["Total"] <= budget:

                self.result_text.insert(
                    tk.END,
                    "STATUS: WITHIN BUDGET\n\n"
                )

            else:

                self.result_text.insert(
                    tk.END,
                    "STATUS: BUDGET EXCEEDED\n\n"
                )

            self.result_text.insert(
                tk.END,
                "OPTIMIZATION SUGGESTIONS\n"
            )

            self.result_text.insert(
                tk.END,
                "-" * 55 + "\n"
            )

            for suggestion in suggestions:

                self.result_text.insert(
                    tk.END,
                    f"• {suggestion}\n"
                )

            self.result_text.insert(
                tk.END,
                "\n12-MONTH PROJECTION\n"
            )

            self.result_text.insert(
                tk.END,
                "-" * 55 + "\n"
            )

            for data in projection.projection_data():

                self.result_text.insert(
                    tk.END,
                    f"Month {data['month']:02d}: "
                    f"${data['cost']:,.2f}\n"
                )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # -------------------------------------------------
    # EXPORT
    # -------------------------------------------------

    def export_reports(self):

        if not self.last_costs:

            messagebox.showwarning(
                "No Data",
                "Calculate the cost before exporting."
            )

            return

        csv_file = generate_csv(
            self.last_costs
        )

        json_file = generate_json(
            self.last_costs
        )

        html_file = generate_html(
            self.last_costs
        )

        messagebox.showinfo(
            "Reports Generated",
            f"Reports created successfully.\n\n"
            f"{csv_file}\n"
            f"{json_file}\n"
            f"{html_file}"
        )

    # -------------------------------------------------
    # CLEAR
    # -------------------------------------------------

    def clear(self):

        self.result_text.delete(
            "1.0",
            tk.END
        )

        self.last_costs = None


def run():

    root = tk.Tk()

    Dashboard(root)

    root.mainloop()
