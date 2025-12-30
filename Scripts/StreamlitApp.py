import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px


DB_URL = "postgresql+psycopg2://postgres:1003@localhost:5432/postgres" \
""

engine = create_engine(
    DB_URL,
    connect_args={"options": "-c client_encoding=UTF8"},
    pool_pre_ping=True,
)

try:
    with engine.connect() as conn:
        db = conn.execute(text("SELECT current_database();")).fetchone()[0]
        st.success(f"Conectado no banco: {db}")
except Exception as e:
    st.error(f"Falha ao conectar: {repr(e)}")
    st.stop()

query = """
SELECT *
FROM gold.vw_sales_daily_category
"""
df = pd.read_sql(query, engine)

# Garantir tipo datetime
df["date_day"] = pd.to_datetime(df["date_day"])

st.sidebar.title("Filtros")

min_date = df["date_day"].min().date()
max_date = df["date_day"].max().date()

# Filtro de período
date_range = st.sidebar.date_input(
    "Período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filtro de categoria
categories = st.sidebar.multiselect(
    "Categoria",
    options=sorted(df["category_name"].unique()),
    default=sorted(df["category_name"].unique())
)

# Converter filtros para Timestamp
start_date = pd.to_datetime(date_range[0])
end_date   = pd.to_datetime(date_range[1])

# Aplicar filtros
df_f = df[
    (df["date_day"] >= start_date) &
    (df["date_day"] <= end_date) &
    (df["category_name"].isin(categories))
]

'''Streamlit App -> Filtros'''

st.sidebar.title("Filtros")

min_date = df["date_day"].min()
max_date = df["date_day"].max()

date_range = st.sidebar.date_input(
    "Período",
    [min_date, max_date]
)

categories = st.sidebar.multiselect(
    "Categoria",
    df["category_name"].unique(),
    default=df["category_name"].unique()
)

df_f = df[
    (df["date_day"] >= pd.to_datetime(date_range[0])) &
    (df["date_day"] <= pd.to_datetime(date_range[1])) &
    (df["category_name"].isin(categories))
]

st.metric("Receita líquida", f"${df_f['net_revenue'].sum():,.2f}")
st.metric("Categorias", df_f["category_name"].nunique())

bar = (
    df_f.groupby("category_name")["net_revenue"]
    .sum()
    .reset_index()
)

fig = px.bar(bar, x="category_name", y="net_revenue", title="Receita por categoria")
st.plotly_chart(fig, use_container_width=True)


'''Receita ao longo do tempo e Top 10 produtos'''
df_f = df_f.copy()
st.subheader("Receita ao longo do tempo (mensal)")

df_f["month"] = df_f["date_day"].dt.to_period("M").dt.to_timestamp()

ts = (
    df_f.groupby("month", as_index=False)["net_revenue"]
        .sum()
        .sort_values("month")
)

fig_line = px.line(ts, x="month", y="net_revenue", title="Receita líquida por mês")
st.plotly_chart(fig_line, use_container_width=True)


st.subheader("Top 10 produtos por receita líquida")
top = pd.read_sql("""
SELECT p.product_name, SUM(f.net_revenue) AS revenue
FROM gold.fact_sales f
JOIN gold.dim_product p ON f.product_id = p.product_id
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10
""", engine)

st.dataframe(top)

