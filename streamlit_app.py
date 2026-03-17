import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

# ---------------- PAGE ----------------
st.set_page_config(page_title="Bank Churn Dashboard", layout="wide")
st.title("🏦 Bank Customer Churn Analytics")

# ---------------- CONNECTION ----------------
@st.cache_resource
def get_connection():
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )
    return conn

conn = get_connection()
st.success("✅ Connected to Snowflake")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data(query):
    return pd.read_sql(query, conn)

df = load_data("""
SELECT *
FROM BANK_DB.GOLD.VW_CHURN_SUMMARY
""")

# ---------------- KPI ----------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Segments", df["GEOGRAPHY"].nunique())
col2.metric("Total Customers", int(df["TOTAL_CUSTOMERS"].sum()))
col3.metric("Total Churned", int(df["CHURNED"].sum()))

st.markdown("---")

# ---------------- CHURN BY COUNTRY ----------------
fig1 = px.bar(
    df,
    x="GEOGRAPHY",
    y="CHURN_RATE",
    color="GENDER",
    barmode="group",
    title="Churn Rate by Geography & Gender"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CUSTOMER DISTRIBUTION ----------------
fig2 = px.pie(
    df,
    names="GEOGRAPHY",
    values="TOTAL_CUSTOMERS",
    title="Customer Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- TABLE ----------------
st.subheader("📋 Data Preview")
st.dataframe(df, use_container_width=True)
