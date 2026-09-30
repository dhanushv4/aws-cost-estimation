# AWS Cost Estimation Dashboard

A GUI-based AWS infrastructure cost estimation project built with Python and Tkinter.

This project allows users to define AWS EC2 infrastructure, configure EBS storage and monthly data transfer, and generate an estimated monthly and 12-month infrastructure cost report.

> **Important:** This project is a cost estimation tool. It does not connect to the AWS Billing API and does not represent an actual AWS invoice.

---

## 📌 Project Overview

Estimating cloud infrastructure cost before deployment is useful for planning and budgeting.

This project provides a simple desktop GUI where users can enter their infrastructure configuration:

- AWS Region
- EC2 instance groups
- EC2 instance type
- Number of EC2 instances
- EBS storage per instance
- Monthly data transfer
- EBS storage price

The application then calculates:

- Monthly EC2 cost
- Monthly EBS cost
- Monthly network/data-transfer cost
- Total monthly estimated cost
- Annual EC2 cost
- Annual EBS cost
- Annual network cost
- Total 12-month estimated cost

The application also generates CSV, JSON, and HTML reports.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Build a simple AWS cost estimation system.
2. Provide a GUI instead of requiring command-line input.
3. Allow users to define multiple EC2 instance groups.
4. Calculate estimated infrastructure costs.
5. Generate a 12-month cost projection.
6. Generate downloadable/local reports.
7. Keep pricing configurable without using AWS Billing APIs.
8. Demonstrate Python, GUI development, cloud concepts, and cost analysis.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Tkinter GUI       │
                    │                     │
                    │ Region              │
                    │ EC2 Groups          │
                    │ Instance Type       │
                    │ Instance Quantity    │
                    │ EBS Storage         │
                    │ Data Transfer       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Pricing Configuration│
                    │                     │
                    │ config/pricing.json │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Cost Calculator     │
                    │                     │
                    │ EC2 Cost            │
                    │ EBS Cost            │
                    │ Network Cost        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ 12-Month Projection │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │          Report Generator       │
              │                                 │
              │ CSV │ JSON │ HTML              │
              └─────────────────────────────────┘
