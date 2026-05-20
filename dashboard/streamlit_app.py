
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import numpy as np
import json
import requests

from datetime import datetime
from sklearn.linear_model import LinearRegression
from streamlit_autorefresh import st_autorefresh

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales & Inventory Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# AUTO REFRESH
# =========================================================

st_autorefresh(
    interval=60000,
    key="dashboard_refresh"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DARK MODE
# =========================================================

dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:

    st.markdown("""
    <style>

    .stApp {
        background-color: #0E1117;
        color: white;
    }

    div[data-testid="metric-container"] {
        background-color: #1E1E1E;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

# =========================================================
# USER DATABASE
# =========================================================

USER_FILE = "users.json"

# =========================================================
# LOAD USERS
# =========================================================

def load_users():

    try:

        with open(USER_FILE, "r") as file:

            return json.load(file)

    except:

        return {"users": []}

# =========================================================
# SAVE USERS
# =========================================================

def save_users(data):

    with open(USER_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )

users_data = load_users()

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "current_user" not in st.session_state:

    st.session_state.current_user = ""

if "page" not in st.session_state:

    st.session_state.page = "home"

# =========================================================
# HOME PAGE
# =========================================================

if not st.session_state.logged_in:

    st.title("📊 Sales & Inventory Dashboard")

    st.markdown("---")

    st.subheader(
        "Enterprise Business Intelligence Platform"
    )

    st.write(
        """
        Analyze sales, inventory,
        forecasting, customer trends,
        and AI insights in real-time.
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            st.session_state.page = "login"

    with col2:

        if st.button(
            "📝 Register",
            use_container_width=True
        ):

            st.session_state.page = "register"

    # =====================================================
    # REGISTER PAGE
    # =====================================================

    if st.session_state.page == "register":

        st.markdown("---")

        st.header("📝 Create Account")

        new_name = st.text_input(
            "Full Name"
        )

        new_username = st.text_input(
            "Create Username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
            "Register Account"
        ):

            if (
                new_name == ""
                or
                new_username == ""
                or
                new_password == ""
            ):

                st.error(
                    "All Fields Are Required"
                )

            elif (
                new_password
                !=
                confirm_password
            ):

                st.error(
                    "Passwords Do Not Match"
                )

            else:

                username_exists = False

                for user in users_data["users"]:

                    if (
                        user["username"].lower()
                        ==
                        new_username.lower()
                    ):

                        username_exists = True
                        break

                if username_exists:

                    st.error(
                        "Username Already Exists"
                    )

                else:

                    users_data["users"].append({

                        "name": new_name,

                        "username": new_username,

                        "password": new_password

                    })

                    save_users(users_data)

                    st.success(
                        "Registration Successful"
                    )

                    st.info(
                        "Now Login To Continue"
                    )

        if st.button(
            "⬅ Back To Login"
        ):

            st.session_state.page = "login"

    # =====================================================
    # LOGIN PAGE
    # =====================================================

    elif st.session_state.page == "login":

        st.markdown("---")

        st.header("🔐 Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login To Dashboard"
        ):

            login_success = False

            for user in users_data["users"]:

                if (
                    user["username"] == username
                    and
                    user["password"] == password
                ):

                    login_success = True

                    st.session_state.logged_in = True

                    st.session_state.current_user = (
                        user["name"]
                    )

                    break

            if login_success:

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    st.stop()

# =========================================================
# LOGOUT
# =========================================================

st.sidebar.success(
    f"Welcome {st.session_state.current_user}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.session_state.current_user = ""

    st.rerun()

# =========================================================
# FETCH LIVE API DATA
# =========================================================

url = "https://dummyjson.com/products"

response = requests.get(url)

api_data = response.json()

products = api_data["products"]

# =========================================================
# SALES DATA
# =========================================================

sales_data = []

for i, product in enumerate(products):

    random_month = np.random.randint(1, 13)

    random_day = np.random.randint(1, 28)

    random_date = datetime(
        2025,
        random_month,
        random_day
    )

    sales_data.append({

        "Order_ID": i + 1001,

        "Order_Date": random_date,

        "Customer": f"Customer_{i+1}",

        "Product": product["title"],

        "Category": product["category"],

        "Quantity": np.random.randint(1, 10),

        "Price": product["price"],

        "Region": np.random.choice([
            "North",
            "South",
            "East",
            "West"
        ])

    })

sales_df = pd.DataFrame(
    sales_data
)

# =========================================================
# INVENTORY DATA
# =========================================================

inventory_data = []

for product in products:

    inventory_data.append({

        "Product": product["title"],

        "Category": product["category"],

        "Stock_Quantity": np.random.randint(
            5,
            100
        ),

        "Reorder_Level": np.random.randint(
            10,
            30
        ),

        "Warehouse": np.random.choice([
            "Mumbai",
            "Delhi",
            "Bangalore",
            "Pune"
        ]),

        "Supplier": np.random.choice([
            "Amazon Supplier",
            "Flipkart Supplier",
            "Reliance Supplier"
        ])

    })

inventory_df = pd.DataFrame(
    inventory_data
)

# =========================================================
# DATA PROCESSING
# =========================================================

sales_df["Order_Date"] = pd.to_datetime(
    sales_df["Order_Date"]
)

sales_df["Total_Amount"] = (
    sales_df["Quantity"] *
    sales_df["Price"]
)

sales_df["Cost_Price"] = (
    sales_df["Price"] * 0.7
)

sales_df["Profit"] = (
    sales_df["Price"] -
    sales_df["Cost_Price"]
) * sales_df["Quantity"]

# =========================================================
# SQL DATABASE
# =========================================================

conn = sqlite3.connect(
    "sales_inventory.db"
)

sales_df.to_sql(
    "sales_data",
    conn,
    if_exists="replace",
    index=False
)

# =========================================================
# FILTERS
# =========================================================

# =========================================================
# FILTERS
# =========================================================

st.sidebar.title("📌 Dashboard Filters")

# =========================================================
# REGION FILTER
# =========================================================

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sales_df["Region"].unique(),
    default=sales_df["Region"].unique()
)

# =========================================================
# CATEGORY FILTER
# =========================================================

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=sales_df["Category"].unique(),
    default=sales_df["Category"].unique()
)

# =========================================================
# PRODUCT FILTER
# =========================================================

selected_product = st.sidebar.multiselect(
    "Select Product",
    options=sales_df["Product"].unique(),
    default=sales_df["Product"].unique()
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = sales_df[
    (sales_df["Region"].isin(selected_region)) &
    (sales_df["Category"].isin(selected_category)) &
    (sales_df["Product"].isin(selected_product))
]
# =========================================================
# HEADER
# =========================================================

st.title("📈 Sales & Inventory Dashboard")

st.markdown(
    f"""
    ### Live Business Insights  
    {datetime.now().strftime('%d %B %Y %H:%M:%S')}
    """
)

st.markdown("---")

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df[
    "Total_Amount"
].sum()

total_orders = filtered_df[
    "Order_ID"
].nunique()

total_profit = filtered_df[
    "Profit"
].sum()

top_product = (
    filtered_df.groupby("Product")[
        "Total_Amount"
    ]
    .sum()
    .idxmax()
)

# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "🛒 Orders",
    total_orders
)

col3.metric(
    "💵 Profit",
    f"₹{total_profit:,.0f}"
)

col4.metric(
    "🏆 Top Product",
    top_product
)

st.markdown("---")

# =========================================================
# PRODUCT SALES CHART
# =========================================================

col5, col6 = st.columns(2)

with col5:

    product_sales = (
        filtered_df.groupby("Product")[
            "Total_Amount"
        ]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        product_sales,
        x="Product",
        y="Total_Amount",
        title="Product Sales"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col6:

    region_sales = (
        filtered_df.groupby("Region")[
            "Total_Amount"
        ]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        region_sales,
        names="Region",
        values="Total_Amount",
        hole=0.4,
        title="Region Sales"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================================================
# MONTHLY SALES TREND
# =========================================================

st.subheader("📅 Monthly Sales Trend")

filtered_df["Month"] = (
    filtered_df["Order_Date"]
    .dt.month_name()
)

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly_sales = (

    filtered_df.groupby("Month")[
        "Total_Amount"
    ]
    .sum()
    .reindex(month_order)
    .reset_index()

)

monthly_sales = monthly_sales.dropna()

fig3 = px.line(

    monthly_sales,

    x="Month",

    y="Total_Amount",

    markers=True,

    title="Monthly Revenue Trend"

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================================================
# FORECASTING
# =========================================================

st.subheader("📈 Sales Forecast")

monthly_sales["Month_Number"] = np.arange(
    len(monthly_sales)
)

X = monthly_sales[["Month_Number"]]
y = monthly_sales["Total_Amount"]

model = LinearRegression()

model.fit(X, y)

future = np.array([
    [len(monthly_sales)]
])

forecast = model.predict(future)

st.metric(
    "Next Month Forecast",
    f"₹{forecast[0]:,.0f}"
)

# =========================================================
# INVENTORY STATUS
# =========================================================

st.subheader("📦 Live Inventory")

inventory_df["Status"] = inventory_df.apply(

    lambda x:

    "Low Stock"

    if x["Stock_Quantity"] <= x["Reorder_Level"]

    else "Available",

    axis=1
)

st.dataframe(
    inventory_df,
    use_container_width=True
)

# =========================================================
# INVENTORY CHART
# =========================================================

inventory_chart = px.bar(

    inventory_df,

    x="Product",

    y="Stock_Quantity",

    color="Status",

    title="Inventory Stock Levels"

)

st.plotly_chart(
    inventory_chart,
    use_container_width=True
)

# =========================================================
# PDF REPORT
# =========================================================

pdf_file = "sales_dashboard_report.pdf"

doc = SimpleDocTemplate(
    pdf_file,
    pagesize=letter
)

styles = getSampleStyleSheet()

elements = []

title = Paragraph(
    "Sales Dashboard Report",
    styles["Title"]
)

elements.append(title)
elements.append(Spacer(1, 20))

data = [
    ["Metric", "Value"],
    ["Total Sales", f"₹{total_sales:,.0f}"],
    ["Total Orders", str(total_orders)],
    ["Total Profit", f"₹{total_profit:,.0f}"],
    ["Top Product", top_product]
]

table = Table(
    data,
    colWidths=[250, 250]
)

table.setStyle(TableStyle([

    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

    ("ALIGN", (0, 0), (-1, -1), "CENTER"),

    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

    ("GRID", (0, 0), (-1, -1), 1, colors.black)

]))

elements.append(table)

doc.build(elements)

with open(pdf_file, "rb") as pdf:

    pdf_data = pdf.read()

st.download_button(

    label="📄 Download PDF Report",

    data=pdf_data,

    file_name="sales_dashboard_report.pdf",

    mime="application/pdf",

    use_container_width=True

)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Developed using Python by Bhavna"
)

