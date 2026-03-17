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
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"]
    )
    return conn

conn = get_connection()
st.success("✅ Connected to Snowflake Successfully!")

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
