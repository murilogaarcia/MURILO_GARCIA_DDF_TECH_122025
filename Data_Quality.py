import pandas as pd
import os
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:1003@localhost:5432/postgres",
    connect_args={"options": "-c client_encoding=UTF8"},
    pool_pre_ping=True
)

dfs = {
    "fact_sales": pd.read_sql("SELECT * FROM gold.fact_sales", engine),
    "sales_offer": pd.read_sql("SELECT * FROM gold.dim_special_offer", engine),
    "product": pd.read_sql("SELECT * FROM gold.dim_product", engine),
    "customer": pd.read_sql("SELECT * FROM gold.dim_customer", engine)
}




def dq_check(
    df: pd.DataFrame,
    table_name: str,
    not_null: list[str] | None = None,
    numeric_ranges: dict[str, tuple[float | None, float | None]] | None = None,
    allowed_values: dict[str, set] | None = None,
) -> pd.DataFrame:
    """
    Retorna um dataframe de resultados de qualidade (métricas) para 1 tabela.
    - not_null: colunas que não podem ser nulas
    - numeric_ranges: {"col": (min, max)} (use None para sem limite)
    - allowed_values: {"col": {val1, val2, ...}}
    """
    not_null = not_null or []
    numeric_ranges = numeric_ranges or {}
    allowed_values = allowed_values or {}

    total_rows = len(df)
    results = []

    # Total
    results.append({
        "table": table_name,
        "check": "total_rows",
        "column": None,
        "value": total_rows,
        "pct_failed": 0.0
    })

    # Not null checks
    for col in not_null:
        if col not in df.columns:
            results.append({"table": table_name, "check": "not_null", "column": col, "value": "missing_column", "pct_failed": None})
            continue
        pct_failed = df[col].isna().mean() if total_rows else 0.0
        results.append({"table": table_name, "check": "not_null", "column": col, "value": None, "pct_failed": float(pct_failed)})

    # Range checks
    for col, (min_v, max_v) in numeric_ranges.items():
        if col not in df.columns:
            results.append({"table": table_name, "check": "range", "column": col, "value": "missing_column", "pct_failed": None})
            continue

        s = pd.to_numeric(df[col], errors="coerce")
        mask = pd.Series(False, index=df.index)
        if min_v is not None:
            mask |= (s < min_v)
        if max_v is not None:
            mask |= (s > max_v)

        pct_failed = mask.mean() if total_rows else 0.0
        results.append({
            "table": table_name,
            "check": "range",
            "column": col,
            "value": f"[{min_v},{max_v}]",
            "pct_failed": float(pct_failed)
        })

    # Allowed values checks
    for col, allowed in allowed_values.items():
        if col not in df.columns:
            results.append({"table": table_name, "check": "allowed_values", "column": col, "value": "missing_column", "pct_failed": None})
            continue

        s = df[col]
        mask = ~s.isna() & ~s.isin(allowed)
        pct_failed = mask.mean() if total_rows else 0.0
        results.append({
            "table": table_name,
            "check": "allowed_values",
            "column": col,
            "value": f"allowed={len(allowed)}",
            "pct_failed": float(pct_failed)
        })

    return pd.DataFrame(results)




def run_dq_suite(dfs: dict, rules: dict) -> pd.DataFrame:
    all_results = []
    for name, df in dfs.items():
        r = rules.get(name, {})
        all_results.append(
            dq_check(
                df=df,
                table_name=name,
                not_null=r.get("not_null", []),
                numeric_ranges=r.get("numeric_ranges", {}),
                allowed_values=r.get("allowed_values", {})
            )
        )
    return pd.concat(all_results, ignore_index=True)




dq_rules = {
    "fact_sales": {
        "not_null": ["sales_order_id", "order_date", "customer_id","product_id"],
        "numeric_ranges": {
            "unit_price": (0, None),
            "gross_revenue": (0, None),
            "net_revenue": (0, None),
            "order_qty": (0, None),
        }
    },
    "dim_special_offer": {
        "not_null": ["special_offer_id", "category", "start_date", "end_date", "offer_status"],
        "numeric_ranges": {
            "min_qty": (1, None),
            "max_qty": (0, None),
            "duration_days": (0, 1),
        }
    },
    "dim_product": {
        "not_null": ["ProductID", "Name"],
        "numeric_ranges": {
            "ListPrice": (0, None),
            "StandardCost": (0, None),
        }
    },
    "dim_customer": {
        "not_null": ["CustomerID"]
    }
}


dq_report = run_dq_suite(dfs, dq_rules)

# Ordena para leitura
dq_report = dq_report.sort_values(["table", "check", "column"], na_position="last")

# Salvar

os.makedirs("data_quality", exist_ok=True)

dq_report.to_csv("data_quality/relatorio_dq.csv", index=False)

with open("data_quality/relatorio_dq.md", "w", encoding="utf-8") as f:
    f.write(dq_report.to_markdown(index=False))

def main():
    print("Running Data Quality checks...")
    # tudo que já existe no notebook continua aqui

if __name__ == "__main__":
    main()


