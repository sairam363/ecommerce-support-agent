import re

from tools import get_order_details, get_order
from rag import answer_policy, get_llm


HYBRID_KEYWORDS = [
    "return",
    "refund",
    "exchange",
    "cancel"
]

ORDER_KEYWORDS = [
    "order",
    "status",
    "track",
    "tracking",
    "shipped",
    "delivered"
]


def has_order_id(question):
    return re.search(r"ORD\d+", question.upper()) is not None


def is_hybrid_question(question):

    question = question.lower()

    if not has_order_id(question):
        return False

    return any(word in question for word in HYBRID_KEYWORDS)


def is_order_question(question):

    question = question.lower()

    if has_order_id(question):
        return True

    return any(word in question for word in ORDER_KEYWORDS)


def handle_query(question):

    # -----------------------------
    # Hybrid Questions
    # -----------------------------

    if is_hybrid_question(question):
        print("[ROUTE] HYBRID")

        order = get_order(question)

        if order is None:
            return "❌ Order not found."

        category = order["category"]

        q = question.lower()

        if "return" in q:
            policy_question = f"What is the return policy for {category}?"

        elif "refund" in q:
            policy_question = f"What is the refund policy for {category}?"

        elif "exchange" in q:
            policy_question = f"What is the exchange policy for {category}?"

        elif "cancel" in q:
            policy_question = "What is the order cancellation policy?"

        else:
            policy_question = question

        policy = answer_policy(policy_question)

        llm = get_llm()

        prompt = f"""
You are an e-commerce customer support assistant.

Customer Question:
{question}

Order Details:
Order ID: {order['order_id']}
Product: {order['product']}
Category: {order['category']}
Status: {order['status']}
Order Date: {order['order_date']}
Payment Method: {order['payment_method']}

Relevant Policy:
{policy}

Answer the customer's question naturally.

Rules:
- Use BOTH the order details and the policy.
- Do not invent information.
- Only use the information provided.
- If the policy depends on information that is NOT available (for example, delivery date), clearly say that you cannot determine the final eligibility.
- Mention what additional information is needed instead of guessing.
- Mention the order status if it is relevant.
- Keep the answer under 120 words.
"""

        response = llm.invoke(prompt)

        return response.content

   

    if is_order_question(question):
        print("[ROUTE] TOOL")
        return get_order_details(question)

    

    print("[ROUTE] RAG")

    return answer_policy(question)