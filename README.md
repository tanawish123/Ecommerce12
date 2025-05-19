
# E-commerce Inventory & Sales API

This project is a FastAPI-based backend service for managing products, sales, and inventory in an e-commerce context. It supports operations like retrieving sales data, analyzing revenue, managing inventory levels, and tracking inventory changes over time.

---

## Features

- CRUD operations on products and sales
- Revenue summary and comparison reports
- Inventory management with stock updates and change tracking
- Low stock alerts
- Filter and aggregate sales data by date, category, and product

---

## Tech Stack

- Python 3.9+
- FastAPI
- MySQL (via aiomysql)
- Pydantic for data validation
- Uvicorn for ASGI server

---

## Getting Started

### Prerequisites

- Python 3.9 or higher installed
- MySQL server installed and running
- Git (optional, for cloning repo)

---


### 2. Setup MySQL Database

1. Create a MySQL database and user for the project (optional example):

```sql
CREATE DATABASE ecommerce_db;
CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;

### 2. Setup for project
1. clone it
git clone https://github.com/your-repo.git
cd your-repo

2.create virtual environment
python3 -m venv venv
source venv/bin/activate
