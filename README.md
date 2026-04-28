# 🏥 Pharmaceutical Sales Data Pipeline

> Production-grade ETL pipeline processing 250K+ pharmaceutical sales records with incremental loading, data quality validation, and automated orchestration.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Pipeline Stages](#pipeline-stages)
- [Monitoring](#monitoring)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

End-to-end batch ETL pipeline that processes pharmaceutical sales data from raw CSV files into a star schema data warehouse. The pipeline implements incremental processing with checkpoint-based resume capability, ensuring no data is processed twice and failures can be recovered seamlessly.

**Key Metrics:**
- 📊 Processes ~250,000 records
- ⚡ Parquet compression: 80% size reduction vs CSV
- 🔄 Incremental loading with checkpoint tracking
- ✅ 100% idempotent operations

---

## 🏗️ Architecture
<img width="1536" height="1024" alt="architecture" src="https://github.com/user-attachments/assets/c2443120-ccae-4764-a709-169b964802e8" />


**Data Flow:**
1. **Preprocessing**: Split large CSV into monthly Parquet files
2. **Extraction**: Incremental batch processing with checkpoint
3. **Validation**: Schema, null, and range checks
4. **Transformation**: Cleaning, type conversion, business rules
5. **Modeling**: Star schema (3 dimensions + 1 fact table)
6. **Loading**: Idempotent PostgreSQL insertion

---

## ✨ Features

### **Production-Ready Concepts**

✅ **Incremental Processing**
- Checkpoint-based resume mechanism
- Processes only new data on each run
- Fault-tolerant with resume capability

✅ **Data Quality**
- Schema validation (required columns check)
- Null value detection and handling
- Range validation (quantity, price, sales)
- Duplicate removal

✅ **Idempotent Operations**
- `ON CONFLICT DO NOTHING` for safe reruns
- No duplicate data on pipeline retries
- Safe for daily scheduled runs

✅ **Orchestration**
- Apache Airflow DAG for automation
- Daily schedule with configurable retry logic
- Error handling and logging

✅ **Dimensional Modeling**
- Star schema design
- Separate dimension and fact tables
- Optimized for analytics queries

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.8+ |
| **Orchestration** | Apache Airflow 2.0+ |
| **Database** | PostgreSQL 13+ |
| **Data Processing** | Pandas, PyArrow |
| **Database ORM** | SQLAlchemy, psycopg2 |
| **File Format** | Parquet (columnar storage) |

---

## 📂 Project Structure
pharma-sales-pipeline/
│
├── 📂 airflow/
│   └── 📂 dags/
│       └── sales_pipeline_dag.py          # Airflow DAG (orchestration)
│
├── 📂 config/
│   └── config.py                         # DB config, paths, constants
│
├── 📂 data/
│   ├── 📂 raw/
│   │   └── pharma_sales_raw.csv          # Original dataset
│   │
│   ├── 📂 processed/
│   │   ├── 2017_01.parquet
│   │   ├── 2017_02.parquet
│   │   └── ...                           # Monthly partitioned data
│   │
│   └── 📂 checkpoints/
│       └── last_processed.txt            # Incremental tracking
│
├── 📂 scripts/
│   └── split_data.py                     # CSV → Parquet splitter
│
├── 📂 sql/
│   └── create_tables.sql                 # Star schema DDL
│
├── 📂 src/
│   ├── extract.py                        # Incremental extraction logic
│   ├── validate.py                       # Schema, null, range checks
│   ├── transform.py                      # Cleaning + business logic
│   ├── model.py                          # Fact & dimension creation
│   ├── load.py                           # PostgreSQL loading logic
│   └── utils.py                          # Helper functions (optional)
│
├── main.py                               # Run pipeline locally
├── requirements.txt                      # Dependencies
├── README.md                             # Documentation
├── .gitignore                            # Ignore unnecessary files
└── LICENSE                               # MIT (optional but good)
---

## 📸 Sample Output

### Airflow DAG Success
<img width="960" height="504" alt="airflow" src="https://github.com/user-attachments/assets/97e8d239-5dce-4402-bda9-b9b0c9cd09a9" />


### Database Load
- Customers: 551 rows
- Products: 240 rows
- Sales: 5183 rows
## 🚀 Setup & Installation

### **Prerequisites**
- Python 3.8+
- PostgreSQL 13+
- Apache Airflow 2.0+ (WSL on Windows or native Linux)

### **1. Clone Repository**
```bash
git clone https://github.com/Akshayj2804/pharma-sales-pipeline.git
cd pharma-sales-pipeline
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Configure Database**
Edit `config/config.py`:
```python
DB_CONFIG = {
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432,
    'database': 'pharma_sales'
}
```

### **4. Create Database Tables**
```bash
psql -U postgres -d pharma_sales -f sql/create_tables.sql
```

### **5. Prepare Data**
```bash
# Split CSV into monthly parquet files
python scripts/split_data.py
```

### **6. Test Pipeline Locally**
```bash
python main.py
```

### **7. Deploy to Airflow**
```bash
# Copy DAG to Airflow
cp airflow/dags/sales_pipeline_dag.py ~/airflow/dags/

# Start Airflow
airflow webserver --port 8080  # Terminal 1
airflow scheduler               # Terminal 2
```

Access Airflow UI: `http://localhost:8080`

---

## 💻 Usage

### **Manual Run (Testing)**
```bash
python main.py
```

### **Airflow Scheduled Run**
1. Open Airflow UI: `http://localhost:8080`
2. Enable DAG: `sales_pipeline`
3. Trigger manually or wait for daily schedule

### **Checkpoint Management**
```bash
# View current checkpoint
cat data/checkpoints/last_processed.txt

# Reset checkpoint (reprocess all)
rm data/checkpoints/last_processed.txt
```

---

## 🔄 Pipeline Stages

### **1️⃣ Extract**
- Reads checkpoint to determine next file
- Loads parquet file into DataFrame
- Returns `None` if no new files

### **2️⃣ Validate**
- **Schema validation**: Checks required columns
- **Null validation**: Detects nulls in critical fields
- **Range validation**: Removes invalid quantities/prices

### **3️⃣ Transform**
- Column name standardization (lowercase, underscores)
- Type conversions (numeric, datetime)
- Business logic (sales = price × quantity)
- Duplicate removal

### **4️⃣ Model**
- Creates 3 dimension tables (customers, products, sales_team)
- Creates 1 fact table (sales transactions)
- Ensures referential integrity

### **5️⃣ Load**
- Inserts dimensions first
- Inserts fact table with `ON CONFLICT DO NOTHING`
- Idempotent: safe to rerun

### **6️⃣ Checkpoint Update**
- Records processed file name
- Ensures next run picks up from here

---

## 📈 Monitoring

### **Airflow UI**
- DAG run status (success/failure)
- Task logs and execution time
- Retry history

### **PostgreSQL Queries**
```sql
-- Check data loaded
SELECT COUNT(*) FROM sales_fact;

-- Monthly sales summary
SELECT year, month, SUM(sales) as total_sales
FROM sales_fact
GROUP BY year, month
ORDER BY year, month;

-- Top products
SELECT product_name, SUM(sales) as revenue
FROM sales_fact
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;
```
## 📊 Business Use Case

This pipeline enables:
- Monthly sales trend analysis
- Top-performing product identification
- Customer-level revenue insights

---
### **Logs**
- Airflow logs: `~/airflow/logs/`
- Application logs: Console output during runs

---
## 🎯 Key Takeaways

- Built a production-style ETL pipeline from scratch  
- Implemented incremental and idempotent processing  
- Automated workflows using Airflow  
- Designed data models for analytical querying
  
---
## 🔮 Future Enhancements

- [ ] Add data quality metrics dashboard
- [ ] Implement email alerts on failures
- [ ] Add unit tests for each module
- [ ] Support for cloud storage (S3/GCS)
- [ ] Real-time streaming with Kafka
- [ ] Data lineage tracking
- [ ] Performance optimization with Dask
- [ ] CI/CD pipeline with GitHub Actions

---

## 👤 Author

**Akshay Jagtap**
- GitHub: [@Akshayj2804](https://github.com/Akshayj2804)
- LinkedIn: https://www.linkedin.com/in/akshay-jagtap2003/

---

## 🙏 Acknowledgments

- Apache Airflow community
- Open source Python data engineering tools

---

**⭐ If you find this project useful, please consider giving it a star!**

