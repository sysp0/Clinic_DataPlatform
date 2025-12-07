
<div align="center">

  <h1> 📊 Clinic DataPlatform </h1>

  <p>
    <strong>A Data Engineering Platform for tracking patient KPIs, financial revenue, and doctor performance.</strong>
  </p>

<img src="./docs/images/superset.png" alt="SuperSet Dashboard" width="700">

</div>

---

<p align="center">
  <a href="https://airflow.apache.org/">
    <img src="docs/logo/AirflowLogo.jpg" alt="Apache Airflow" width="80" />
  </a>
  <a href="https://superset.apache.org/">
    <img src="docs/logo/apache-superset.png" alt="Apache Superset" width="80" />
  </a>
  <a href="https://www.docker.com/">
    <img src="docs/logo/docker-logo.png" alt="Docker" width="80" />
  </a>
  <a href="https://pandera.readthedocs.io/">
    <img src="docs/logo/pandera_logo.png" alt="Pandera" width="80" />
  </a>
  <a href="https://www.postgresql.org/">
    <img src="docs/logo/postgresql.png" alt="PostgreSQL" width="80" />
  </a>
  <a href="https://www.python.org/">
    <img src="docs/logo/python-logo.png" alt="Python" width="80" />
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="docs/logo/uv-logo.png" alt="uv" width="80" />
  </a>
</p>

---

## 📋 Executive Summary

🔗 **[داستان حل مسئله و تصمیمات طراحی](https://github.com/sysp0/Clinic_DataPlatform/blob/main/docs/Clinic_Design_Decisions.md)**

---

## 🚀 درباره پروژه

پلتفرمی برای پاسخ به سوالات کلیدی کلینیک:
- درآمد امروز چقدر بود؟
- کدام پزشک بیشترین پذیرش را دارد؟
- وضعیت مطالبات بیمه چطور است؟

ابزار **Apache Airflow** هر ساعت داده‌ها را از دیتابیس مبدا می‌خواند، با **Pandera** اعتبارسنجی می‌کند و در Warehouse جایگزین  می‌کند (**SCD Type 1**).

---

## 🏗 معماری

```

┌─────────────┐     ┌──────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Source DB  │────▶│ Python + Pandera │────▶│  PostgreSQL  │────▶│  Superset   │
│   (MSSQL)   │     │   ETL Pipeline   │     │     DWH      │     │  Dashboard  │
└─────────────┘     └──────────────────┘     └──────────────┘     └─────────────┘
                             ▲
                             │ Hourly Trigger
                    ┌────────┴────────┐
                    │ Apache Airflow  │
                    └─────────────────┘
```

| لایه          | تکنولوژی                | وظیفه                        |
| ------------- | ----------------------- | ---------------------------- |
| Orchestration | Airflow                 | زمان‌بندی و اجرای خودکار ETL |
| Processing    | Python, Pandas, Pandera | استخراج، اعتبارسنجی، تبدیل   |
| Storage       | PostgreSQL              | ذخیره‌سازی Star Schema       |
| Visualization | Superset                | داشبورد و KPI                |

---

## 🛠 راه‌اندازی

```bash
chmod +x setup.sh superset/setup.sh && ./setup.sh
```

تنها با یک دستور تمامی نیازمندی های پروژه راه اندازی میشود. 

و میتوانیم از محیط AirFlow روند ETL رو اجرا کنیم.

زمانی که خروجی زیر ظاهر شد یعنی عملیات با موفقیت انجام شده است:

```
==================================
         SERVICES READY
==================================

AirFlow:
  URL: http://localhost:8080
  User: admin
  Pass: run {"admin": "G2WzwBbTUa7xv2DF"}

Superset:
  URL: http://localhost:8088
  User: admin
  Pass: secret

==================================
```

---

## 📊 دسترسی به سرویس‌ها

| سرویس    | آدرس                  | یوزر / پسورد        |
| -------- | --------------------- | ------------------- |
| Superset | http://localhost:8088 | admin / secret      |
| Airflow  | http://localhost:8080 | airflow / `docker exec -it bi_airflow cat simple_auth_manager_passwords.json.generated` |

---

## 🗄 ساختار دیتابیس (Star Schema)

```
                    ┌──────────────────┐
                    │  Fact_Reception  │
                    ├──────────────────┤
                    │ FactID (PK)      │
                    │ DoctorID (FK)    │──────┐
                    │ PatientID (FK)   │──────┼──────┐
                    │ ServiceID (FK)   │──────┼──────┼──────┐
                    │ InsuranceID (FK) │──────┼──────┼──────┼──────┐
                    │ ReceptionDate    │      │      │      │      │
                    │ TotalAmount      │      │      │      │      │
                    │ PatientShare     │      │      │      │      │
                    │ InsuranceShare   │      │      │      │      │
                    │ DiscountAmount   │      │      │      │      │
                    └──────────────────┘      │      │      │      │
                              │               │      │      │      │
         ┌────────────────────┘               │      │      │      │
         ▼                                    ▼      │      │      │
┌─────────────────┐                 ┌─────────────────┐     │      │
│   Dim_Doctor    │                 │   Dim_Patient   │     │      │
├─────────────────┤                 ├─────────────────┤     │      │
│ DoctorID (PK)   │                 │ PatientID (PK)  │     │      │
│ DoctorName      │                 │ FullName        │     │      │
│ Specialty       │                 │ Gender          │     │      │
└─────────────────┘                 └─────────────────┘     │      │
                                                            │      │
                    ┌───────────────────────────────────────┘      │
                    ▼                                              ▼
          ┌─────────────────┐                           ┌─────────────────┐
          │   Dim_Service   │                           │  Dim_Insurance  │
          ├─────────────────┤                           ├─────────────────┤
          │ ServiceID (PK)  │                           │ InsuranceID(PK) │
          │ ServiceName     │                           │ InsuranceName   │
          │ ServiceGroup    │                           └─────────────────┘
          └─────────────────┘
```

---

## 📁 ساختار پروژه

```
Clinic_DataPlatform/
├── dags/                    # Airflow DAGs
│   └── clinic_etl.py
├── src/
│   ├── db.py                # Database connections
│   ├── extract.py           # Data extraction
│   ├── transform.py         # Data transformation
│   ├── load.py              # Data loading
│   └── models/
│       ├── source.py        # Pandera schemas (Source)
│       └── warehouse.py     # SQLAlchemy models (DWH)
├── docs/
│   ├── superset.png
│   └── Clinic_Design_Decisions.md
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📈 نمونه KPIهای داشبورد

| KPI               | مقدار نمونه           |
| ----------------- | --------------------- |
| کل پذیرش‌ها       | 442,178               |
| تعداد پزشکان فعال | 88 از 145             |
| درآمد کل          | 19 میلیارد ریال       |
| سهم نقدی          | 61%                   |
| سهم بیمه          | 39%                   |
| نرخ تخفیف         | 10.9%                 |
| پزشک پرکار        | مهدی عبدی (56K پذیرش) |

---

## 🔄 جریان ETL

```
┌────────────────────────────────────────────────────────────────────┐
│                         EXTRACT                                    │
├────────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Doctor  │  │ Patient │  │ Service │  │Insurance│  │Reception│   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │            │            │            │            │        │
│       └────────────┴────────────┴────────────┴────────────┘        │
│                                 │                                  │
│                                 ▼                                  │
│                    ┌───────────────────────┐                       │
│                    │   Pandera Validation  │                       │
│                    │   (Schema Checking)   │                       │
│                    └───────────┬───────────┘                       │
└────────────────────────────────┼───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                         TRANSFORM                                  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   • Join Doctor + DoctorGroup → Dim_Doctor                         │
│   • Join Patient + Gender → Dim_Patient                            │
│   • Join Service + ServiceGroup → Dim_Service                      │
│   • InsuranceType → Dim_Insurance                                  │
│   • Header + Detail → Fact_Reception                               │
│                                                                    │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                           LOAD                                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │                  PostgreSQL Warehouse                   │      │
│   ├─────────────────────────────────────────────────────────┤      │
│   │  TRUNCATE → INSERT (SCD Type 1 - Full Refresh)          │      │
│   └─────────────────────────────────────────────────────────┘      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ تنظیمات محیطی (.env)

```env
ACCEPT_EULA=Y
SA_PASSWORD=Passw0rd
MSSQL_PID=Developer
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=airflow_db
SOURCE_CONN_STRING=mssql+pymssql://SA:Passw0rd@127.0.0.1:1433/ClinicDB

# Airflow
AIRFLOW_UID=1000
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://admin:admin@postgres:5432/airflow_db
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__API__SECRET_KEY=your-secret-key-here
AIRFLOW__WEBSERVER__SECRET_KEY=your-secret-key-here

# Auto DB Migration & User Creation
_AIRFLOW_DB_MIGRATE=true

WAREHOUSE_CONN_STRING=postgresql+psycopg2://admin:admin@127.0.0.1:5432/warehouse_db
TALISMAN_ENABLED=False


# Superset
SUPERSET_SECRET_KEY=your-superset-secret-key-change-this
SUPERSET_ADMIN_USERNAME=admin
SUPERSET_ADMIN_PASSWORD=admin123
SUPERSET_ADMIN_EMAIL=admin@example.com
SUPERSET_ADMIN_FIRSTNAME=Admin
SUPERSET_ADMIN_LASTNAME=User
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://admin:admin@postgres:5432/superset_db
```

---

## 🔍 اعتبارسنجی داده (Data Validation)

با استفاده از **Pandera**، داده‌ها قبل از ورود به Warehouse بررسی می‌شوند:

| جدول | قوانین اعتبارسنجی |
|------|-------------------|
| Patient | `PatientPK` یکتا، `NationalCode` غیرتهی |
| Doctor | `DoctorPK` یکتا |
| Reception Header | `PatientPK` حتماً باید مقدار داشته باشد |
| Reception Detail | `ServiceCode` معتبر، مبالغ غیرمنفی |



```python

# Pandera Schema
class PatientReceptionHeader(pa.DataFrameModel):
    PatientReceptionHeaderPK: Series[int] = pa.Field(unique=True)
    PatientPK: Series[int] = pa.Field()  # NOT NULL
    DoctorPK: Series[int] = pa.Field(nullable=True)
    ReceptionDate: Series[pd.Timestamp] = pa.Field(nullable=True)
```

---

## 📌 نکات مهم

> توضیح **SCD Type 1:** در هر اجرای ETL، تمام داده‌های Warehouse پاک و با داده جدید جایگزین می‌شود. اگر نیاز به نگهداری تاریخچه دارید، باید به SCD Type 2 مهاجرت کنید.

> توضیح **Airflow DAG:** به صورت پیش‌فرض هر ساعت اجرا می‌شود. برای تغییر، `schedule` را در فایل DAG ویرایش کنید.

## 📷 Screenshots

### Superset
![SuperSet1](./docs/images/SuperSet1.png)

![SuperSet2](./docs/images/SuperSet2.png)

![SuperSet3](./docs/images/SuperSet3.png)

![SuperSet4](./docs/images/SuperSet4.png)

### MS SQL (Raw Data)
![MSSQL](./docs/images/MSSQL.png)

### AirFlow
![AirFlow1](./docs/images/AirFlow1.png)

![AirFlow2](./docs/images/AirFlow2.png)

![AirFlow3](./docs/images/AirFlow3.png)
