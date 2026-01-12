import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="RetailFlow | GLP Dashboard", layout="wide")

# --- Title and Header ---
st.title("🚀 RetailFlow: Operations & Tech Suite")
st.markdown("""
*Developed as a decision-support tool for Retail Operations and Supply Chain management.*
""")

# --- Data Loading ---
@st.cache_data
def load_data():
    t = pd.read_csv('transactions.csv', parse_dates=['timestamp'])
    p = pd.read_csv('products.csv')
    i = pd.read_csv('inventory.csv')
    return t, p, i

df_t, df_p, df_i = load_data()

# --- Section 1: Operational KPIs ---
st.header("📦 Inventory & Supply Chain")
col1, col2, col3 = st.columns(3)

# Merge data for logic
merged_ops = pd.merge(df_i, df_p, on='product_id')
# Logic: If stock is less than 3x Lead Time consumption (Simple safety stock logic)
merged_ops['reorder_status'] = merged_ops.apply(
    lambda x: "🚨 URGENT REORDER" if x['current_stock'] < 20 else "✅ OK", axis=1
)

with col1:
    st.metric("Low Stock Items", len(merged_ops[merged_ops['reorder_status'] == "🚨 URGENT REORDER"]))
with col2:
    total_rev = (df_t.merge(df_p, on='product_id')['quantity'] * df_t.merge(df_p, on='product_id')['unit_price']).sum()
    st.metric("Total Revenue", f"₹{total_rev:,.0f}")
with col3:
    st.metric("Active Customers", df_t['customer_id'].nunique())

st.dataframe(merged_ops[['product_name', 'current_stock', 'lead_time_days', 'reorder_status']], width='stretch')
# --- Section 2: Cohort Analysis (Business Analytics Requirement) ---
st.header("📈 Customer Retention (Cohort Analysis)")

# Prepare Cohorts
df_t['cohort_month'] = df_t.groupby('customer_id')['timestamp'].transform('min').dt.to_period('M')
df_t['order_month'] = df_t['timestamp'].dt.to_period('M')

cohort_data = df_t.groupby(['cohort_month', 'order_month']).agg(n_customers=('customer_id', 'nunique')).reset_index()
cohort_data['period_number'] = (cohort_data.order_month - cohort_data.cohort_month).apply(lambda x: x.n)

# Pivot table for heatmap
pivot = cohort_data.pivot_table(index='cohort_month', columns='period_number', values='n_customers')
retention_matrix = pivot.divide(pivot.iloc[:, 0], axis=0)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(retention_matrix, annot=True, fmt='.0%', cmap='YlGnBu', ax=ax)
plt.title('Monthly Retention Rate %')
st.pyplot(fig)

# --- Section 3: Tech Focus (SQL Logic Simulation) ---
st.header("💻 Backend Logic: Optimized Queries")
with st.expander("View SQL logic for Inventory Restocking"):
    st.code("""
    SELECT p.product_name, i.current_stock
    FROM products p
    JOIN inventory i ON p.product_id = i.product_id
    WHERE i.current_stock < (p.lead_time_days * 5) -- Logic for safety stock
    ORDER BY i.current_stock ASC;
    """, language='sql')