import streamlit as st
import pandas as pd
import plotly.express as px
import os

from data import (
    TRENDS,
    INVENTORY,
    PRICING,
    WHOLESALERS,
    get_forecast_data,
    get_sales_history,
    CATEGORIES,
)

st.set_page_config(page_title="Trendora", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "inventory" not in st.session_state:
    st.session_state.inventory = INVENTORY.copy()


def logo():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("Assets/images/logos/image.png", width=280)
        except Exception:
            pass


def landing_page():
    logo()

    st.markdown("<h1 style='text-align:center;color:#D4AF37;'>Trendora</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Your Smart Fashion Business Partner</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Trends. Inventory. Growth.</p>", unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login as Small Business Owner", use_container_width=True):
            if email == "" or password == "":
                st.error("Please enter email and password.")
            else:
                st.session_state.logged_in = True
                st.session_state.page = "Dashboard"
                st.rerun()


def sidebar():
    st.sidebar.title("Trendora")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Trends", "Inventory", "Pricing", "Forecast", "Wholesalers", "Profile"]
    )

    st.session_state.page = menu

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()


def dashboard():
    st.title("Owner Dashboard")

    inventory_df = pd.DataFrame(st.session_state.inventory)
    trends_df = pd.DataFrame(TRENDS)

    total_products = len(inventory_df)
    reorder_now = len(inventory_df[inventory_df["status"] == "REORDER NOW"])
    dead_stock = len(inventory_df[inventory_df["status"] == "DEAD STOCK"])
    avg_heat = int(trends_df["heat"].mean())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Products", total_products)
    c2.metric("Reorder Alerts", reorder_now)
    c3.metric("Dead Stock", dead_stock)
    c4.metric("Avg Trend Heat", avg_heat)

    st.divider()

    st.subheader("Trending This Week")
    cols = st.columns(4)

    for i, trend in enumerate(TRENDS[:4]):
        with cols[i]:
            st.success(f"{trend['name']}\n\nHeat: {trend['heat']} | {trend['direction']}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Inventory Status")
        status_count = inventory_df["status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]
        fig = px.pie(status_count, values="Count", names="Status", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Trend Heat by Category")
        fig = px.bar(trends_df, x="name", y="heat", color="urgency")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Smart Alerts")

    for item in st.session_state.inventory:
        if item["status"] == "REORDER NOW":
            st.warning(f"{item['name']} needs reorder. Quantity left: {item['qty']}")

        if item["status"] == "DEAD STOCK":
            st.error(f"{item['name']} is dead stock. Consider clearance sale.")


def trends_page():
    st.title("Fashion Trends")

    category = st.selectbox("Filter Category", CATEGORIES)

    filtered = TRENDS

    if category != "All":
        filtered = [t for t in TRENDS if t["category"] == category]

    for trend in filtered:
        st.markdown("---")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(trend["name"])
            st.write(trend["description"])
            st.write(f"Category: {trend['category']}")
            st.write(f"City: {trend['city']}")
            st.write(f"Tags: {', '.join(trend['tags'])}")

        with col2:
            st.metric("Heat", trend["heat"])
            st.write(trend["direction"])
            st.write(f"Change: {trend['change']}")
            st.write(f"Urgency: {trend['urgency']}")


def inventory_page():
    st.title("Inventory Management")

    st.subheader("Add New Product")

    product_name = st.text_input("Product Name")

    category = st.selectbox(
        "Category",
        ["Tops", "Bottoms", "Dresses", "Sets", "Outerwear", "Jewellery", "Footwear"]
    )

    qty = st.number_input("Quantity", min_value=0, step=1)
    reorder_point = st.number_input("Reorder Point", min_value=0, step=1)
    cost = st.number_input("Cost Price", min_value=0)
    selling_price = st.number_input("Selling Price", min_value=0)

    image = st.file_uploader(
        "Upload Product Image",
        type=["png", "jpg", "jpeg"]
    )

    if st.button("Add Product", use_container_width=True):
        image_path = ""

        if image is not None:
            os.makedirs("Uploads", exist_ok=True)

            image_path = os.path.join(
                "Uploads",
                f"{len(st.session_state.inventory) + 1}_{image.name}"
            )

            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

        status = "HEALTHY"

        if qty == 0:
            status = "OUT OF STOCK"
        elif qty <= reorder_point:
            status = "REORDER NOW"

        new_product = {
            "sku": f"SKU-{len(st.session_state.inventory) + 1}",
            "name": product_name,
            "qty": qty,
            "reorder_point": reorder_point,
            "cost": cost,
            "selling_price": selling_price,
            "days_of_stock": 0,
            "velocity": "Medium",
            "status": status,
            "category": category,
            "trend_alignment": 50,
            "image_path": image_path
        }

        if product_name == "":
            st.error("Please enter product name.")
        else:
            st.session_state.inventory.append(new_product)
            st.success("Product added successfully.")
            st.rerun()

    st.divider()

    st.subheader("Current Inventory")

    search = st.text_input("Search Inventory")

    filter_status = st.selectbox(
        "Filter Status",
        ["All", "REORDER NOW", "HEALTHY", "OVERSTOCK", "DEAD STOCK", "OUT OF STOCK"]
    )

    inventory = st.session_state.inventory

    for index, item in enumerate(inventory):
        if search.lower() not in item["name"].lower():
            continue

        if filter_status != "All" and item["status"] != filter_status:
            continue

        st.markdown("---")

        col1, col2 = st.columns([1, 4])

        with col1:
            if item.get("image_path", "") and os.path.exists(item["image_path"]):
                st.image(item["image_path"], width=140)
            else:
                st.write("No Image")

        with col2:
            st.subheader(item["name"])
            st.write(f"SKU: {item['sku']}")
            st.write(f"Category: {item['category']}")
            st.write(f"Quantity: {item['qty']}")
            st.write(f"Selling Price: ₹{item['selling_price']}")
            st.write(f"Status: {item['status']}")

            if item["qty"] == 0:
                st.error("Out of Stock")
            elif item["qty"] <= item["reorder_point"]:
                st.warning("Low Stock")
            else:
                st.success("In Stock")

            if st.button(f"Edit {item['sku']}", key=f"edit_{index}"):
                st.session_state[f"edit_{index}"] = True

            if st.session_state.get(f"edit_{index}", False):
                new_qty = st.number_input(
                    "Update Quantity",
                    min_value=0,
                    value=int(item["qty"]),
                    key=f"qty_{index}"
                )

                new_price = st.number_input(
                    "Update Selling Price",
                    min_value=0,
                    value=int(item["selling_price"]),
                    key=f"price_{index}"
                )

                if st.button("Save Changes", key=f"save_{index}"):
                    st.session_state.inventory[index]["qty"] = new_qty
                    st.session_state.inventory[index]["selling_price"] = new_price

                    if new_qty == 0:
                        st.session_state.inventory[index]["status"] = "OUT OF STOCK"
                    elif new_qty <= item["reorder_point"]:
                        st.session_state.inventory[index]["status"] = "REORDER NOW"
                    else:
                        st.session_state.inventory[index]["status"] = "HEALTHY"

                    st.session_state[f"edit_{index}"] = False
                    st.success("Updated successfully.")
                    st.rerun()

            if st.button(f"Delete {item['sku']}", key=f"delete_{index}"):
                st.session_state.inventory.pop(index)
                st.success("Deleted successfully.")
                st.rerun()


def pricing_page():
    st.title("Pricing Recommendations")

    df = pd.DataFrame(PRICING)

    st.dataframe(df, use_container_width=True)

    st.divider()

    fig = px.bar(
        df,
        x="product",
        y=["your_price", "market_avg", "suggested"],
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    for item in PRICING:
        if "Price UP" in item["opportunity"]:
            st.success(f"{item['product']}: Suggested price ₹{item['suggested']}")
        elif "Reduce" in item["opportunity"]:
            st.warning(f"{item['product']}: Reduce price to ₹{item['suggested']}")
        else:
            st.error(f"{item['product']}: Clearance recommended at ₹{item['suggested']}")


def forecast_page():
    st.title("Demand Forecast")

    forecast = get_forecast_data()
    df = pd.DataFrame(forecast)

    st.dataframe(df, use_container_width=True)

    fig = px.line(
        df,
        x="weeks",
        y=df.columns[1:],
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    sales = get_sales_history()

    st.subheader("Sales History")

    fig2 = px.line(
        sales,
        x="date",
        y="revenue",
        markers=True
    )

    st.plotly_chart(fig2, use_container_width=True)


def wholesalers_page():
    st.title("Verified Wholesalers")

    for wholesaler in WHOLESALERS:
        st.markdown("---")

        st.subheader(wholesaler["name"])
        st.write(f"City: {wholesaler['city']}")
        st.write(f"Rating: {wholesaler['rating']}")
        st.write(f"Years in Business: {wholesaler['years']}")
        st.write(f"Speciality: {wholesaler['speciality']}")
        st.write(f"Minimum Order Value: ₹{wholesaler['min_order_value']}")
        st.write(f"Tags: {', '.join(wholesaler['tags'])}")

        with st.expander("View Products"):
            for product in wholesaler["products"]:
                st.write(f"Product: {product['name']}")
                st.write(f"MOQ: {product['moq']}")
                st.write(f"Price per Unit: ₹{product['price_per_unit']}")
                st.write(f"Fabric: {product['fabric']}")
                st.write(f"Lead Days: {product['lead_days']}")
                st.write("---")


def profile_page():
    st.title("Business Owner Profile")

    st.write("Owner Name: Small Business Owner")
    st.write("Business Name: Trendora Fashion Store")
    st.write("Location: Hyderabad")
    st.write("Category: Apparel")
    st.write("Contact: owner@trendora.com")

    st.divider()

    st.subheader("Business Summary")

    st.info("""
This dashboard helps business owners track fashion trends,
manage inventory, check demand forecast, compare pricing,
and connect with verified wholesalers.
""")


if not st.session_state.logged_in:
    landing_page()

else:
    sidebar()

    if st.session_state.page == "Dashboard":
        dashboard()

    elif st.session_state.page == "Trends":
        trends_page()

    elif st.session_state.page == "Inventory":
        inventory_page()

    elif st.session_state.page == "Pricing":
        pricing_page()

    elif st.session_state.page == "Forecast":
        forecast_page()

    elif st.session_state.page == "Wholesalers":
        wholesalers_page()

    elif st.session_state.page == "Profile":
        profile_page()