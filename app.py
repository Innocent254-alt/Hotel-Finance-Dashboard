import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Title
st.set_page_config(page_title="Hospitality Financial Insights", layout="wide")
st.title("🏨 Interactive AP/AR & Revenue Performance Dashboard")
st.markdown("Designed by an AI-Augmented Financial Analyst")

# 2. Mock Dataset Function (With Complete Data Arrays)
@st.cache_data
def load_data():
    data = {
        'Department': ['Rooms', 'F&B', 'Spa', 'Rooms', 'F&B', 'Events', 'Rooms', 'Events'],
        'Client_Type': ['Corporate', 'Transient', 'Transient', 'Group', 'Corporate', 'Group', 'Transient', 'Corporate'],
        'Invoice_Amount': [12500.00, 450.50, 210.00, 8900.00, 1200.00, 15000.00, 3400.00, 6200.00],
        'Days_Outstanding':,
        'Status': ['Current', '31-60 Days', 'Current', '61-90 Days', '91+ Days', 'Current', 'Current', '91+ Days']
    }
    return pd.DataFrame(data)

# Call the function to load the spreadsheet data
df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Analytics View")
selected_dept = st.sidebar.multiselect(
    "Select Department(s):",
    options=df['Department'].unique(),
    default=df['Department'].unique()
)

selected_client = st.sidebar.selectbox(
    "Select Client Type:",
    options=['All'] + list(df['Client_Type'].unique())
)

# Apply filters based on sidebar inputs
filtered_df = df[df['Department'].isin(selected_dept)]
if selected_client != 'All':
    filtered_df = filtered_df[filtered_df['Client_Type'] == selected_client]

# 4. Key Financial Metrics (KPI Cards)
total_ar = filtered_df['Invoice_Amount'].sum()
avg_days = filtered_df['Days_Outstanding'].mean()
severe_risk = filtered_df[filtered_df['Status'] == '91+ Days']['Invoice_Amount'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Accounts Receivable", f"${total_ar:,.2f}")
col2.metric("Avg. Days Outstanding", f"{avg_days:.1f} Days")
col3.metric("Severe Collection Risk (91+ Days)",
            f"${severe_risk:,.2f}", delta="-High Risk", delta_color="inverse")

st.markdown("---")

# 5. Dynamic Interactive Visualizations
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue Allocation by Department")
    fig_pie = px.pie(filtered_df, values='Invoice_Amount', names='Department', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader("AR Aging Risk Breakdown")
    fig_bar = px.bar(filtered_df, x='Status', y='Invoice_Amount', color='Department',
                     title="Outstanding Balances by Aging Bucket",
                     labels={'Invoice_Amount': 'Outstanding Balance ($)', 'Status': 'Aging Category'})
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. Raw Data Inspection Toggle
if st.checkbox("Show Raw Ledger Sheet"):
    st.dataframe(filtered_df)
