
"""
Task 01 | Nested Transaction Analyzer

Requirements:
- Calculate successful spending for each customer.
- Ignore failed transactions.
- Reject duplicate transaction IDs.
- Find each customer's top category.
- Sort by spending descending, then customer name ascending.
- Include customers with zero successful transactions.
"""

transactions = [
    {"id": 1, "customer": "Ali", "category": "Food", "amount": 500, "status": "success"},
    {"id": 2, "customer": "Ali", "category": "Travel", "amount": 200, "status": "failed"},
    {"id": 3, "customer": "Sara", "category": "Food", "amount": 700, "status": "success"},
    {"id": 4, "customer": "Ahmed", "category": "Shopping", "amount": 300, "status": "success"},
    {"id": 5, "customer": "Ali", "category": "Food", "amount": 200, "status": "success"},
    {"id": 6, "customer": "Ahmed", "category": "Food", "amount": 100, "status": "failed"}
]

customers = ["Ali", "Sara", "Ahmed", "Usman"]


def transaction_report(transactions, customers):

    seen_ids = set()
    customer_data = {}

    # Initialize all customers
    for customer in customers:
        customer_data[customer] = {
            "total": 0,
            "categories": {}
        }

    # Process transactions
    for transaction in transactions:

        transaction_id = transaction["id"]

        # Reject duplicate transaction IDs
        if transaction_id in seen_ids:
            raise ValueError("Duplicate transaction ID found")

        seen_ids.add(transaction_id)

        customer = transaction["customer"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total": 0,
                "categories": {}
            }

        # Ignore failed transactions
        if transaction["status"] == "success":

            category = transaction["category"]
            amount = transaction["amount"]

            customer_data[customer]["total"] += amount

            if category not in customer_data[customer]["categories"]:
                customer_data[customer]["categories"][category] = 0

            customer_data[customer]["categories"][category] += amount

    # Create report
    report = []

    for customer, details in customer_data.items():

        total = details["total"]
        categories = details["categories"]

        if categories:
            top_category = max(categories, key=categories.get)
        else:
            top_category = None

        report.append({
            "customer": customer,
            "total_spending": total,
            "top_category": top_category
        })

    # Sort by spending descending and customer ascending
    report.sort(
        key=lambda x: (-x["total_spending"], x["customer"])
    )

    # Assign ranks
    for rank, customer in enumerate(report, start=1):
        customer["rank"] = rank

    return report


# Display report
try:
    result = transaction_report(transactions, customers)

    print("TRANSACTION REPORT")
    print("-" * 40)

    for customer in result:
        print(customer)

except ValueError as error:
    print("Error:", error)
