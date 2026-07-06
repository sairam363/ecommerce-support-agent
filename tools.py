import pandas as pd
import re

# Load orders.csv
df = pd.read_csv("sample_data/orders.csv")



def extract_order_id(query: str):
    """
    Extract order ID like ORD1004 from user query.
    """
    match = re.search(r"ORD\d+", query.upper())

    if match:
        return match.group()

    return None


def get_order_details(query: str):
    """
    Look up an order in orders.csv.
    """

    order_id = extract_order_id(query)

    if not order_id:
        return " Please provide a valid Order ID."

    order = df[df["order_id"].str.upper() == order_id]

    if order.empty:
        return f" Order {order_id} was not found."

    order = order.iloc[0]

    return f"""
###  Order Details

**Order ID:** {order['order_id']}

**Customer:** {order['customer_name']}

**Product:** {order['product']}

**Category:** {order['category']}

**Status:** {order['status']}

**Amount:** ₹{order['amount_inr']}

**Payment:** {order['payment_method']}

**Order Date:** {order['order_date']}
"""
import re
def get_order(query: str):
    """
    Returns complete order details as a dictionary.
    Used for hybrid reasoning.
    """

    order_id = extract_order_id(query)

    if not order_id:
        return None

    order = df[df["order_id"].str.upper() == order_id]

    if order.empty:
        return None

    return order.iloc[0].to_dict()
