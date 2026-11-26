import streamlit as st


MENU = {
    "Pizza": 8.50,
    "Burger": 6.00,
    "Juice": 2.50,
    "Salad": 5.00,
    "Pasta": 7.50,
}

DISCOUNT_CODE = "SAVE10"
DISCOUNT_RATE = 0.10
FREE_DELIVERY_MINIMUM = 25.00
DELIVERY_FEE = 3.50


def item_cost(item, quantity):
    if item not in MENU or quantity < 0:
        raise ValueError("Invalid item or quantity")

    return MENU[item] * quantity


def subtotal(order):
    return round(
        sum(item_cost(item, quantity) for item, quantity in order.items()),
        2,
    )


def discount_amount(amount, code):
    if code.strip().upper() == DISCOUNT_CODE:
        return round(amount * DISCOUNT_RATE, 2)

    return 0.0


def delivery_fee(amount, delivery):
    if not delivery or amount >= FREE_DELIVERY_MINIMUM:
        return 0.0

    return DELIVERY_FEE


def order_total(order, code, delivery):
    base = subtotal(order)
    discount = discount_amount(base, code)
    fee = delivery_fee(base, delivery)

    return round(base - discount + fee, 2)


def receipt(order, code, delivery):
    base = subtotal(order)
    discount = discount_amount(base, code)
    fee = delivery_fee(base, delivery)

    return {
        "Subtotal": base,
        "Discount": discount,
        "Delivery": fee,
        "Total": round(base - discount + fee, 2),
    }


st.set_page_config(page_title="Food Ordering System", page_icon="🍕")

st.title("🍽️ Online Food Ordering System")
st.write("Choose your food, set quantities, and checkout.")

customer = st.text_input("Customer name")

st.subheader("Menu")
order = {}

for item, price in MENU.items():
    quantity = st.number_input(
        f"{item} — £{price:.2f}",
        min_value=0,
        value=0,
        step=1,
    )

    if quantity:
        order[item] = int(quantity)

if order:
    st.subheader("Your order")

    order_rows = [
        {
            "Item": item,
            "Quantity": quantity,
            "Price": f"£{item_cost(item, quantity):.2f}",
        }
        for item, quantity in order.items()
    ]

    st.table(order_rows)

st.subheader("Checkout")

code = st.text_input("Discount code", placeholder="Try SAVE10")
delivery = st.checkbox("Delivery required")

if st.button("Place order", type="primary", use_container_width=True):
    if not customer.strip():
        st.error("Please enter a customer name.")
    elif not order:
        st.error("Please choose at least one item.")
    else:
        st.success(f"Order confirmed for {customer.strip()}!")

        st.subheader("Receipt")

        summary = receipt(order, code, delivery)
        receipt_rows = [
            {"Description": name, "Amount": f"£{amount:.2f}"}
            for name, amount in summary.items()
        ]

        st.table(receipt_rows)
        st.write("Items ordered:", order)
