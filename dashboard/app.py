import streamlit as st
import pandas as pd
import sys
import os

# Project path setup
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.recommender import recommend
from src.budget_optimizer import recommend_by_budget
from src.deals import get_best_deals
from src.reminders import add_reminder, get_reminders
from src.user_preferences import recommend_by_category
from src.history import add_view, get_history
from src.purchase_scheduler import (
    schedule_purchase,
    get_scheduled_purchases
)
from src.analytics import get_view_statistics   

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI-Powered Personalized Shopping Assistant",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "cart" not in st.session_state:
    st.session_state.cart = []

# --------------------------------------------------
# Load Data
# --------------------------------------------------

products = pd.read_csv("data/products.csv")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Recommendations",
        "Budget Optimizer",
        "Deals",
        "Shopping Cart",
        "Checkout",
        "Reminders",
        "Purchase Scheduler",
        "Browsing History",
        "E-Commerce Integration",
        "Analytics"
    ]
)


# --------------------------------------------------
# Header
# --------------------------------------------------

if page == "Dashboard":

    st.title(
        "🛒 AI-Powered Personalized Shopping Assistant"
    )

    st.markdown("""
    This application provides:

    - AI-Based Product Recommendations
    - Budget Optimization
    - Deal Discovery
    - Smart Shopping Cart
    - Purchase Reminders
    - Product Analytics

    AI Techniques Used:

    - TF-IDF Vectorization
    - Cosine Similarity
    """)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Products",
        len(products)
    )

    col2.metric(
        "Categories",
        products["Category"].nunique()
    )

    col3.metric(
        "Average Rating",
        round(
            products["Rating"].mean(),
            2
        )
    )

# --------------------------------------------------
# Product Catalog
# --------------------------------------------------

st.divider()

if page == "Dashboard":

    st.header("📦 Product Catalog")

    st.dataframe(
        products,
        width="stretch"
    )

# --------------------------------------------------
# AI Recommendation Engine
# --------------------------------------------------

st.divider()

if page == "Recommendations":

    st.header(
        "🤖 AI Product Recommendation Engine"
    )

    selected_product = st.selectbox(
        "Select a Product",
        products["ProductName"].tolist()
    )

    add_view(selected_product)

    if st.button(
        "Generate Recommendations"
    ):

        recommendations = recommend(
            selected_product
        )

        if recommendations:

            recommendation_df = pd.DataFrame(
                {
                    "Recommended Products":
                    recommendations
                }
            )

            st.dataframe(
                recommendation_df,
                width="stretch"
            )

    # -----------------------------------
    # Personalized Recommendations
    # -----------------------------------

    st.subheader(
        "👤 Personalized Recommendations"
    )

    preferred_category = st.selectbox(
        "Select Your Favourite Category",
        products["Category"].unique(),
        key="preferred_category"
    )

    if st.button(
        "Get Personalized Suggestions"
    ):

        personalized = recommend_by_category(
            preferred_category
        )

        st.dataframe(
            personalized[
                [
                    "ProductName",
                    "Brand",
                    "Price",
                    "Rating"
                ]
            ],
            width="stretch"
        )


# --------------------------------------------------
# Budget Optimizer
# --------------------------------------------------

st.divider()

if page == "Budget Optimizer":

    st.header("💰 Budget Optimizer")

    budget = st.number_input(
        "Enter Budget (€)",
        min_value=10,
        max_value=5000,
        value=100,
        step=10
    )

    if st.button("Find Products Within Budget"):

        budget_products = recommend_by_budget(
            budget
        )

        st.success(
            f"Top Products Within €{budget}"
        )

        st.dataframe(
            budget_products[
                [
                    "ProductName",
                    "Category",
                    "Price",
                    "Rating"
                ]
            ],
            width="stretch"
        )


# --------------------------------------------------
# Deal Discovery
# --------------------------------------------------

st.divider()

if page == "Deals":

    st.header("🔥 Best Deals")

    if st.button("Show Best Deals"):

        deals = get_best_deals()

        st.dataframe(
            deals[
                [
                    "ProductName",
                    "Price",
                    "OriginalPrice",
                    "Savings"
                ]
            ],
            width="stretch"
        )


# --------------------------------------------------
# Smart Shopping Cart
# --------------------------------------------------

st.divider()

if page == "Shopping Cart":

    st.header("🛒 Shopping Cart")

    cart_product = st.selectbox(
        "Select Product to Add",
        products["ProductName"].tolist(),
        key="cart_product"
    )

    if st.button("Add To Cart"):

        st.session_state.cart.append(cart_product)

        st.success(
            f"{cart_product} added to cart."
        )

    if st.session_state.cart:

        cart_df = products[
            products["ProductName"].isin(
                st.session_state.cart
            )
        ]

        st.subheader("Current Cart")

        st.dataframe(
            cart_df[
                [
                    "ProductName",
                    "Category",
                    "Price"
                ]
            ],
            width="stretch"
        )

        total_price = cart_df["Price"].sum()

        st.metric(
            "Total Cart Value",
            f"€{total_price}"
        )


# --------------------------------------------------
# Checkout
# --------------------------------------------------

st.divider()

if page == "Checkout":

    st.header("💳 Checkout")

    if st.session_state.cart:

        cart_df = products[
            products["ProductName"].isin(
                st.session_state.cart
            )
        ]

        total_price = cart_df["Price"].sum()

        st.subheader("Order Summary")

        st.dataframe(
            cart_df[
                [
                    "ProductName",
                    "Price"
                ]
            ],
            width="stretch"
        )

        st.metric(
            "Total Amount",
            f"€{total_price}"
        )

        payment_method = st.selectbox(
            "Select Payment Method",
            [
                "Credit Card",
                "Debit Card",
                "PayPal",
                "Bank Transfer"
            ]
        )

        if st.button("Place Order"):

            st.success(
                f"Payment Successful via {payment_method}"
            )

            st.balloons()

    else:

        st.warning(
            "Your cart is empty."
        )


# --------------------------------------------------
# Purchase Reminders
# --------------------------------------------------

st.divider()

if page == "Reminders":

    st.header("📅 Purchase Reminders")

    reminder_product = st.selectbox(
        "Select Product",
        products["ProductName"].tolist(),
        key="reminder_product"
    )

    reminder_date = st.date_input(
        "Select Reminder Date"
    )

    if st.button("Save Reminder"):

        add_reminder(
            reminder_product,
            str(reminder_date)
        )

        st.success(
            "Reminder Saved Successfully."
        )

    st.subheader("Saved Reminders")

    reminders = get_reminders()

    if reminders:

        reminder_df = pd.DataFrame(
            reminders,
            columns=[
                "ID",
                "Product",
                "Reminder Date"
            ]
        )

        st.dataframe(
            reminder_df,
            width="stretch"
        )


# --------------------------------------------------
# Purchase Scheduling
# --------------------------------------------------

st.divider()

if page == "Purchase Scheduler":

    st.header("🛍 Purchase Scheduler")

    purchase_product = st.selectbox(
        "Select Product To Purchase Later",
        products["ProductName"].tolist(),
        key="purchase_product"
    )

    purchase_date = st.date_input(
        "Select Purchase Date",
        key="purchase_date"
    )

    if st.button("Schedule Purchase"):

        schedule_purchase(
            purchase_product,
            str(purchase_date)
        )

        st.success(
            "Purchase Scheduled Successfully."
        )

    st.subheader("Upcoming Purchases")

    scheduled = get_scheduled_purchases()

    if scheduled:

        scheduled_df = pd.DataFrame(
            scheduled,
            columns=[
                "ID",
                "Product",
                "Purchase Date"
            ]
        )

        st.dataframe(
            scheduled_df,
            width="stretch"
        )

    else:

        st.info(
            "No scheduled purchases."
        )


# --------------------------------------------------
# E-Commerce Integration
# --------------------------------------------------

st.divider()

if page == "E-Commerce Integration":

    st.header("🛍 E-Commerce Integration")

    selected_product = st.selectbox(
        "Select Product",
        products["ProductName"].tolist(),
        key="ecommerce_product"
    )

    product_data = products[
        products["ProductName"] == selected_product
    ].iloc[0]

    st.subheader(product_data["ProductName"])

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Brand:** {product_data['Brand']}"
        )

        st.write(
            f"**Category:** {product_data['Category']}"
        )

        st.write(
            f"**Rating:** ⭐ {product_data['Rating']}"
        )

    with col2:

        st.write(
            f"**Price:** €{product_data['Price']}"
        )

        st.write(
            f"**Retailer:** {product_data['Retailer']}"
        )

    st.write(
        f"**Description:** {product_data['Description']}"
    )

    st.link_button(
        f"Visit {product_data['Retailer']}",
        product_data["ProductURL"]
    )

    st.success(
        "Users can move directly from recommendation to retailer website."
    )


# --------------------------------------------------
# Analytics Dashboard
# --------------------------------------------------

st.divider()

if page == "Analytics":

    st.header("📈 Analytics Dashboard")

    # -----------------------------
    # Product Analytics
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Products by Category")

        category_counts = (
            products["Category"]
            .value_counts()
        )

        st.bar_chart(category_counts)

    with col2:

        st.subheader("Average Price by Category")

        avg_price = (
            products
            .groupby("Category")["Price"]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(avg_price)

    # -----------------------------
    # Shopping Pattern Analytics
    # -----------------------------

    st.divider()

    st.subheader("🛍 Shopping Pattern Analytics")

    history_df = get_view_statistics()

    if not history_df.empty:

        product_counts = (
            history_df["product_name"]
            .value_counts()
        )

        st.subheader("Most Viewed Products")

        st.bar_chart(product_counts)

        st.success(
            f"Top Viewed Product: {product_counts.index[0]}"
        )

        st.metric(
            "Total Product Views",
            len(history_df)
        )

        st.metric(
            "Unique Products Viewed",
            history_df["product_name"].nunique()
        )

    else:

        st.info(
            "Not enough browsing data yet."
        )


# --------------------------------------------------
# Browsing History
# --------------------------------------------------

st.divider()

if page == "Browsing History":

    st.header("🕒 Browsing History")

    history = get_history()

    if history:

        history_df = pd.DataFrame(
            history,
            columns=[
                "Product",
                "Viewed At"
            ]
        )

        st.dataframe(
            history_df,
            width="stretch"
        )

    else:

        st.info(
            "No browsing history available."
        )

