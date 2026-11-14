import streamlit as st
import pandas as pd

menu = {
    "cupcake": 3.75,
    "cookie": 2.00,
    "muffin": 2.75,
    "scone": 3.25,
    "brownie": 3.00,
}

sample_sales = {
    "cupcake": 18,
    "cookie": 30,
    "muffin": 12,
    "scone": 10,
    "brownie": 15,
}


def apply_discount(subtotal):
    """Apply a 10% discount when the original subtotal is at least $50.00."""
    if subtotal >= 50.00:
        return round(subtotal * 0.90, 2)
    return subtotal


def shipping_fee(subtotal):
    """Return free delivery for subtotals of at least $35.00; otherwise $5.99."""
    if subtotal >= 35.00:
        return 0.0
    return 5.99


st.sidebar.header("Order Options")
customer_name = st.sidebar.text_input("Customer name or nickname", value="")
product = st.sidebar.selectbox("Product", options=list(menu.keys()))
quantity = st.sidebar.number_input(
    "Quantity", min_value=1, max_value=30, value=1, step=1
)
fulfillment = st.sidebar.selectbox("Fulfillment", options=["Pickup", "Delivery"])
show_chart = st.sidebar.checkbox("Show sample sales chart", value=True)

st.title("🥖 Bright Bakery Order Calculator")
st.markdown(
    "Calculate your bakery quote, review the menu, and inspect sample sales data below."
)

unit_price = menu[product]
subtotal = unit_price * quantity
discounted_subtotal = apply_discount(subtotal)
discount_amount = round(subtotal - discounted_subtotal, 2)

if fulfillment == "Pickup":
    delivery_fee = 0.0
else:
    delivery_fee = shipping_fee(subtotal)

total = discounted_subtotal + delivery_fee

st.subheader("Current Quote")
col1, col2 = st.columns(2)

with col1:
    st.write("**Selected Product:**", product.capitalize())
    st.write("**Quantity:**", quantity)
    st.write("**Unit Price:**", f"${unit_price:.2f}")
    st.write("**Fulfillment Method:**", fulfillment)

with col2:
    st.write("**Original Subtotal:**", f"${subtotal:.2f}")
    st.write("**Discount Amount:**", f"${discount_amount:.2f}")
    st.write("**Delivery Fee:**", f"${delivery_fee:.2f}")
    st.metric(label="Final Total", value=f"${total:.2f}")

st.divider()
st.subheader("Bakery Menu")
menu_df = pd.DataFrame(
    {
        "Product": [p.capitalize() for p in menu.keys()],
        "Price ($)": [f"${price:.2f}" for price in menu.values()],
    }
)
st.dataframe(menu_df, hide_index=True, use_container_width=True)

st.subheader("Sample Sales")
st.caption("Fictional practice sales data for display purposes.")
if show_chart:
    sales_df = pd.DataFrame(
        {
            "Product": [p.capitalize() for p in sample_sales.keys()],
            "Units sold": list(sample_sales.values()),
        }
    ).set_index("Product")
    st.bar_chart(sales_df, sort=False)

st.divider()
if st.button("Check quote"):
    cleaned_name = customer_name.strip()
    if not cleaned_name:
        st.warning(
            "Please enter a customer name or nickname before checking your quote."
        )
    else:
        st.success(
            f"Thank you, {cleaned_name}! Your quote has been reviewed. "
            "Note: This practice app does not save orders or take payments."
        )
