import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Vicency Cosmetics Sales Dashboard",
    page_icon="💄",
    layout="wide",
)

# --- Data Loading and Cleaning ---
@st.cache_data
def load_and_clean_data(uploaded_file):
    """Loads the cosmetics dataset from an uploaded file and performs cleaning."""
    if uploaded_file is None:
        return None
    df = pd.read_csv(uploaded_file)

    # Clean column names (remove spaces and special characters)
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('($)', '', regex=False)

    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Feature Engineering for time-based analysis
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    return df

# --- Main Application ---
st.title("💄 Vicency Cosmetics Sales Dashboard")
st.markdown("Explore sales data with interactive filters and visualizations.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is None:
    st.info("Please upload a CSV file to begin analysis.")
    st.stop()

df = load_and_clean_data(uploaded_file)

if df is None:
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")

selected_countries = st.sidebar.multiselect(
    "Country",
    options=sorted(df['Country'].unique()),
    default=sorted(df['Country'].unique())
)

selected_products = st.sidebar.multiselect(
    "Product",
    options=sorted(df['Product'].unique()),
    default=sorted(df['Product'].unique())
)

selected_sales_persons = st.sidebar.multiselect(
    "Sales Person",
    options=sorted(df['Sales_Person'].unique()),
    default=sorted(df['Sales_Person'].unique())
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max(),
)

# --- Filtering Data based on selections ---
start_date, end_date = date_range
df_filtered = df[
    (df['Country'].isin(selected_countries)) &
    (df['Product'].isin(selected_products)) &
    (df['Sales_Person'].isin(selected_sales_persons)) &
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- KPI Section ---
st.header("Key Performance Indicators")
total_sales = df_filtered['Amount_'].sum()
total_boxes = df_filtered['Boxes_Shipped'].sum()
unique_products = df_filtered['Product'].nunique()
num_sales_persons = df_filtered['Sales_Person'].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Total Sales ($)", value=f"${total_sales:,.2f}")
kpi2.metric(label="Total Boxes Shipped", value=f"{total_boxes:,}")
kpi3.metric(label="Unique Products Sold", value=f"{unique_products}")
kpi4.metric(label="Active Sales Persons", value=f"{num_sales_persons}")

st.markdown("---")

# --- Charts Section ---
st.header("Visual Analysis")

col1, col2 = st.columns(2)

# Monthly Sales Trend
with col1:
    st.subheader("Monthly Sales Trend")
    monthly_sales = df_filtered.groupby('Month')['Amount_'].sum().reset_index()
    fig_monthly = px.line(
        monthly_sales,
        x='Month',
        y='Amount_',
        markers=True,
        labels={'Amount_': 'Total Sales ($)'},
        title="Total Sales Over Time"
    )
    fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Total Sales ($)")
    st.plotly_chart(fig_monthly, use_container_width=True)

# Total Sales by Country
with col2:
    st.subheader("Total Sales by Country")
    country_sales = df_filtered.groupby('Country')['Amount_'].sum().sort_values(ascending=False).reset_index()
    fig_country = px.bar(
        country_sales,
        x='Country',
        y='Amount_',
        color='Country',
        labels={'Amount_': 'Total Sales ($)'},
        title="Sales Performance Across Countries"
    )
    st.plotly_chart(fig_country, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

# Sales Person Performance
with col3:
    st.subheader("Sales Person Performance")
    person_perf = df_filtered.groupby('Sales_Person')[['Amount_', 'Boxes_Shipped']].sum().reset_index()
    
    # Using a grouped bar chart for better comparison
    fig_person = go.Figure()
    fig_person.add_trace(go.Bar(
        x=person_perf['Sales_Person'],
        y=person_perf['Amount_'],
        name='Sales Amount ($)',
        marker_color='indianred'
    ))
    fig_person.add_trace(go.Bar(
        x=person_perf['Sales_Person'],
        y=person_perf['Boxes_Shipped'],
        name='Boxes Shipped',
        marker_color='lightsalmon'
    ))
    
    fig_person.update_layout(
        barmode='group',
        title="Sales Amount vs. Boxes Shipped by Sales Person",
        xaxis_title="Sales Person",
        yaxis_title="Count / Amount"
    )
    st.plotly_chart(fig_person, use_container_width=True)

# Top Selling Products by Country
with col4:
    st.subheader("Top Selling Product by Country")
    top_products_country = df_filtered.groupby(['Country', 'Product'])['Amount_'].sum().reset_index()
    top_products_country = top_products_country.loc[top_products_country.groupby('Country')['Amount_'].idxmax()]
    
    fig_top_prod = px.bar(
        top_products_country,
        x='Country',
        y='Amount_',
        color='Product',
        hover_name='Product',
        labels={'Amount_': 'Total Sales ($)'},
        title="Most Popular Product in Each Country"
    )
    st.plotly_chart(fig_top_prod, use_container_width=True)


# --- Raw Data Section ---
st.markdown("---")
with st.expander("View Filtered Raw Data"):
    st.dataframe(df_filtered)

