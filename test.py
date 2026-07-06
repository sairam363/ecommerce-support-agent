from router import handle_query

questions = [
    "What is your return policy?",
    "How long does shipping take?",
    "What is the status of ORD1004?",
    "Show details of ORD1002",
    "Can I return ORD1004?",
    "Can I cancel ORD1002?",
    "What is your GST policy?",
    "What is the status of ORD9999?"
]

for i, q in enumerate(questions, 1):
    print("=" * 80)
    print(f"Test {i}: {q}")
    print("-" * 80)
    print(handle_query(q))
    print()