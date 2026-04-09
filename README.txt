# 🚀 LogiMigrate: Supply Chain Data Migration Platform

## 📌 Overview

LogiMigrate is an end-to-end data migration and analytics platform that simulates a real-world enterprise scenario of transforming legacy warehouse and logistics data into a modern, structured, and scalable system.

The project covers the complete pipeline from data preprocessing and schema design to backend API development and deployment using Docker and Kubernetes, along with analytics integration using Power BI.

---

## 🎯 Problem Statement

Legacy systems often store operational data in unstructured or inefficient formats, making it difficult to:

* Analyze business performance
* Maintain data consistency
* Scale applications
* Generate real-time insights

This project demonstrates how such legacy data can be:

* Cleaned and transformed
* Normalized into relational schema
* Exposed via APIs
* Deployed in a production-like environment

---

## 🏗️ System Architecture

```
Raw Data (CSV)
        ↓
Data Processing (Pandas)
        ↓
PostgreSQL (Relational Database)
        ↓
Flask API (Backend Services)
        ↓
Docker (Containerization)
        ↓
Kubernetes (Orchestration)
        ↓
Power BI (Analytics Dashboard)
```

---

## 🛠️ Tech Stack

* **Languages:** Python, SQL
* **Data Processing:** Pandas
* **Database:** PostgreSQL
* **Backend:** Flask, SQLAlchemy
* **Containerization:** Docker, Docker Compose
* **Orchestration:** Kubernetes
* **Visualization:** Power BI

---

## 🗃️ Data Model

The dataset is transformed into a normalized relational schema with the following tables:

* **products** → item details and pricing
* **warehouses** → storage and location information
* **inventory** → stock levels and operational metrics
* **demand** → demand patterns and forecasts
* **operations** → fulfillment and performance metrics

This design ensures:

* Reduced redundancy
* Better data consistency
* Scalable system design

---

## 🔌 API Endpoints

The Flask API exposes key operational insights:

* `GET /` → Health check
* `GET /summary` → Row counts of all tables
* `GET /inventory/low-stock/count` → Number of low stock items
* `GET /operations/summary` → Operational performance summary

---

## 🐳 Docker Setup

To run the application using Docker:

```bash
docker compose up --build
```

This will:

* Start PostgreSQL container
* Start Flask API container
* Automatically connect both services

---

## ☸️ Kubernetes Deployment

To deploy the application in Kubernetes:

```bash
kubectl apply -f kubernetes/
```

Then verify:

```bash
kubectl get pods -n logimigrate
kubectl get services -n logimigrate
```

---

## 📊 Power BI Dashboard

The project integrates with Power BI to generate business insights such as:

* Low stock detection
* Order fulfillment performance
* Demand forecasting trends
* Inventory distribution by category

---

## 🔄 Data Loading

To load processed data into PostgreSQL:

```bash
python load_data.py
```

For Kubernetes deployment, ensure port-forwarding is active before running the script.

---

## 🧠 Key Learnings

* Designing normalized relational schemas (1NF, 2NF, 3NF concepts)
* Handling data dependencies and foreign key constraints
* Building REST APIs for data-driven applications
* Understanding container networking (localhost vs service name)
* Deploying applications using Docker and Kubernetes
* Managing real-world data migration workflows

---

## 🚀 Future Improvements

* Add authentication and authorization for APIs
* Integrate Redis for caching
* Automate ETL pipelines
* Deploy on cloud platforms (AWS/Azure)
* Add real-time streaming data processing

---

## 👩‍💻 Author

**Gayathridevi T**
Master of Data Science, RMIT University
Former AI/ML Engineer at Accenture

---

## 📬 Connect

* LinkedIn: *https://www.linkedin.com/in/gayathri-devi-thotappa-4892a8137?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BW9LU9KCHRZOthcBt7C%2BhVA%3D%3D*
* GitHub: *https://github.com/gayathri19-tech*

---
