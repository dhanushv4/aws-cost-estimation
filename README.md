# AWS Cost Estimation Dashboard

A Python-based desktop GUI application for estimating AWS infrastructure costs before deployment.

The application provides a simple dashboard to estimate EC2, EBS, and network transfer costs using locally configured pricing data.

> **Note:** This project is a local cost estimation tool. It does not create AWS resources, use Terraform, or connect to AWS Billing APIs.

## Features

- EC2 cost estimation
- Multiple EC2 instance types
- EBS storage cost estimation
- Network transfer cost estimation
- Monthly cost calculation
- Annual cost calculation
- AWS region selection
- Cost summary dashboard
- CSV report generation
- JSON report generation
- HTML report generation
- Configurable pricing using JSON
- Dark-themed Tkinter GUI

## Architecture

```text
                         ┌───────────────────────┐
                         │         USER          │
                         │   Cloud / DevOps      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────┐
                    │     Tkinter GUI Dashboard   │
                    │                             │
                    │  • AWS Region               │
                    │  • EC2 Configuration        │
                    │  • EBS Storage              │
                    │  • Network Transfer         │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │      Pricing Configuration   │
                    │                             │
                    │     config/pricing.json     │
                    │                             │
                    │  • Instance Price            │
                    │  • vCPU                      │
                    │  • Memory                    │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Cost Calculator        │
                    │                             │
                    │  • EC2 Cost                 │
                    │  • EBS Cost                 │
                    │  • Network Cost             │
                    │  • Monthly Cost             │
                    │  • Annual Cost              │
                    └──────────────┬──────────────┘
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
                ┌─────────────────┐  ┌─────────────────┐
                │ Cost Dashboard  │  │ Report Generator│
                │                 │  │                 │
                │ Monthly Cost    │  │ CSV             │
                │ Annual Cost     │  │ JSON            │
                │ EC2 Cost        │  │ HTML            │
                │ EBS Cost        │  │                 │
                │ Network Cost    │  │                 │
                └─────────────────┘  └────────┬────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │     reports/     │
                                     │ Generated Reports │
                                     └──────────────────┘
```

## Cost Calculation

### EC2

```text
EC2 Monthly Cost
=
Number of Instances
× Hourly Price
× 730 Hours
```

### EBS

```text
EBS Monthly Cost
=
Number of Instances
× EBS GB per Instance
× EBS Price per GB
```

### Network

```text
Network Cost
=
Data Transfer GB
× Transfer Price per GB
```

### Total

```text
Monthly Total
=
EC2 Cost
+ EBS Cost
+ Network Cost
```

```text
Annual Total
=
Monthly Total × 12
```

## Supported EC2 Instances

The default configuration supports:

| Instance | vCPU | Memory |
|---|---:|---:|
| t3.micro | 2 | 1 GiB |
| t3.small | 2 | 2 GiB |
| t3.medium | 2 | 4 GiB |
| t3.large | 2 | 8 GiB |
| r6i.xlarge | 4 | 32 GiB |

Pricing is stored in:

```text
config/pricing.json
```

## Project Structure

```text
aws-cost-estimation/
│
├── app.py
│
├── config/
│   └── pricing.json
│
├── reports/
│   ├── *.csv
│   ├── *.json
│   └── *.html
│
├── architecture/
│   ├── architecture.md
│   └── architecture-diagram.png
│
├── tests/
│   └── test_calculator.py
│
├── .gitignore
├── LICENSE
└── README.md
```

## Technologies

- Python
- Tkinter
- JSON
- CSV
- HTML
- Linux / WSL
- Git
- GitHub

## Requirements

- Python 3.10+
- Tkinter
- Git

No external Python packages are required for the basic application.

## Installation

Clone the repository:

```bash
git clone git@github.com:dhanushv4/aws-cost-estimation.git
```

Go to the project:

```bash
cd aws-cost-estimation
```

Install Tkinter on Ubuntu/WSL:

```bash
sudo apt update
sudo apt install python3-tk
```

Create required directories:

```bash
mkdir -p config reports
```

Validate the pricing file:

```bash
python3 -m json.tool config/pricing.json
```

## Run

Start the application:

```bash
python3 app.py
```

The **AWS Cost Estimation Dashboard** will open.

## How to Use

### 1. Select Region

Example:

```text
ap-south-1
```

### 2. Enter Network Transfer

Example:

```text
100 GB/month
```

### 3. Configure EBS

Example:

```text
20 GB per instance
```

### 4. Add EC2 Instance

Example:

```text
Instance Type: t3.medium
Quantity: 2
EBS: 20 GB
```

Click:

```text
Add Group
```

### 5. Calculate

Click:

```text
Calculate
```

The dashboard displays:

- Monthly EC2 cost
- Monthly EBS cost
- Monthly network cost
- Total monthly cost
- Annual cost

### 6. Generate Reports

Click:

```text
Calculate & Generate Report
```

Reports are stored in:

```text
reports/
```

## Reports

The application generates:

### CSV

Useful for Excel and data analysis.

### JSON

Useful for automation and future integrations.

### HTML

Useful for browser viewing and project demonstrations.

Example:

```text
reports/
├── cost_report_20260930_190500.csv
├── cost_report_20260930_190500.json
└── cost_report_20260930_190500.html
```

## Example

Configuration:

```text
Region:
ap-south-1

EC2:
2 × t3.medium

EBS:
20 GB per instance

Network:
100 GB/month
```

Example calculation:

```text
EC2:
2 × $0.0416 × 730
= $60.736/month

EBS:
2 × 20 × $0.10
= $4.00/month

Network:
100 × $0.09
= $9.00/month

Estimated Monthly Total:
$73.736

Estimated Annual Total:
$884.832
```

These values are based on the pricing configured in `config/pricing.json`.

## AWS and Terraform

This project does not require:

- AWS account
- AWS credentials
- AWS CLI
- Terraform
- EC2 deployment
- AWS Billing API

The application runs completely locally.

The project uses AWS infrastructure concepts for cost estimation and planning.

## Troubleshooting

### Tkinter Error

If you see:

```text
ModuleNotFoundError: No module named 'tkinter'
```

Run:

```bash
sudo apt update
sudo apt install python3-tk
```

### Pricing Error

If you see:

```text
KeyError: 't3.medium'
```

check:

```text
config/pricing.json
```

Make sure `t3.medium` exists.

Example:

```json
"t3.medium": {
  "vcpus": 2,
  "memory_gib": 4,
  "hourly_price": 0.0416
}
```

### Validate JSON

Run:

```bash
python3 -m json.tool config/pricing.json
```

## Git Commands

Check changes:

```bash
git status
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Upgrade AWS cost estimation dashboard"
```

Push:

```bash
git push origin main
```

## Future Improvements

- S3 cost estimation
- RDS cost estimation
- Lambda cost estimation
- CloudFront estimation
- NAT Gateway estimation
- Monthly cost charts
- 12-month projection
- Budget alerts
- Cost optimization recommendations
- EC2 instance comparison
- JSON infrastructure import
- AWS Pricing API integration
- Automated tests
- GitHub Actions CI/CD
- Docker support
- Web-based dashboard

## Disclaimer

This application provides estimated costs based on locally configured pricing values.

Actual AWS charges can vary based on:

- AWS region
- Usage
- Operating system
- Storage
- Data transfer
- Discounts
- Free Tier
- Savings Plans
- Reserved Instances
- Taxes
- Current AWS pricing

Always verify current AWS pricing before deploying production infrastructure.

## Author

**Dhanush V**

MCA Graduate | Cloud & DevOps

GitHub:

```text
https://github.com/dhanushv4
```

## Project Goal

The goal of this project is to provide a simple local tool for Cloud and DevOps engineers to estimate infrastructure costs before deployment.

```text
PLAN
  ↓
CONFIGURE
  ↓
ESTIMATE
  ↓
ANALYZE
  ↓
GENERATE REPORT
  ↓
OPTIMIZE
```

---

⭐ **AWS Cost Estimation Dashboard — Python + Tkinter + Cloud/DevOps**
