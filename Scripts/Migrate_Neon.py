import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

#Exportando dados do Postgres local para Neon (Postgres na nuvem)

# PostgreSQL local
LOCAL = create_engine(
    "postgresql+psycopg2://postgres:1003@localhost:5432/postgres",
    connect_args={"options": "-c client_encoding=UTF8"}
)

# Neon
NEON = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_nfH6NG4WUKZl@ep-flat-tooth-ah0q78nc-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

tables = [
    "fact_sales",
    "dim_customer",
    "dim_product",
    "dim_date",
    "dim_special_offer"
]

# Garante schema
with NEON.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))


for t in tables:
    print(f"Migrating {t}")
    df = pd.read_sql(f"SELECT * FROM gold.{t}", LOCAL)
    df.to_sql(t, NEON, schema="gold", if_exists="replace", index=False)

print("Migration to Neon completed successfully")

