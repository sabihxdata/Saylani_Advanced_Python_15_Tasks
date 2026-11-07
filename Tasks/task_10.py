''' Task 10 | CSV Inventory Reconciliation
Concepts: CSV, file handling, validation
Problem: Read inventory.csv (sku,name,quantity) and movements.csv (sku,type,units). Apply IN and OUT movements in order, then write updated_inventory.csv and rejected_movements.csv.
Requirements: Reject unknown SKUs, negative or zero units, invalid movement types, and any OUT causing negative stock. Continue processing after rejected rows.
Sample / expected behavior: SKU P01 starts at 10; OUT 4, OUT 9, IN 2 -> final 8; second movement rejected.'''


import csv
import os


def create_sample_files():
 
    inventory_data = [
        ["sku", "name", "quantity"],
        ["P01", "Laptop", 10],
        ["P02", "Mouse", 20],
        ["P03", "Keyboard", 15]
    ]

    with open("inventory.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(inventory_data)

   
    movements_data = [
        ["sku", "type", "units"],
        ["P01", "OUT", 4],
        ["P01", "OUT", 9],
        ["P01", "IN", 2],
        ["P02", "IN", 5],
        ["P99", "OUT", 3],
        ["P02", "INVALID", 2],
        ["P03", "OUT", -5]
    ]

    with open("movements.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(movements_data)


def reconcile_inventory(inventory_file, movements_file):
    inventory = {}

    
    with open(inventory_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sku = row["sku"].strip()
            name = row["name"].strip()

            try:
                quantity = int(row["quantity"])
            except ValueError:
                raise ValueError("Invalid inventory quantity for " + sku)

            if not sku or sku in inventory:
                raise ValueError("Missing or duplicate SKU: " + sku)

            if quantity < 0:
                raise ValueError("Inventory quantity cannot be negative")

            inventory[sku] = {
                "name": name,
                "quantity": quantity
            }

    rejected = []

   
    with open(movements_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sku = row["sku"].strip()
            movement_type = row["type"].strip().upper()

            try:
                units = int(row["units"])
            except (ValueError, TypeError):
                rejected.append({
                    "sku": sku,
                    "type": movement_type,
                    "units": row["units"],
                    "reason": "Invalid units"
                })
                continue

            if sku not in inventory:
                reason = "Unknown SKU"

            elif units <= 0:
                reason = "Units must be positive"

            elif movement_type not in ("IN", "OUT"):
                reason = "Invalid movement type"

            elif movement_type == "OUT" and units > inventory[sku]["quantity"]:
                reason = "Insufficient stock"

            else:
                reason = None

            if reason is not None:
                rejected.append({
                    "sku": sku,
                    "type": movement_type,
                    "units": units,
                    "reason": reason
                })
                continue

            if movement_type == "IN":
                inventory[sku]["quantity"] += units

            elif movement_type == "OUT":
                inventory[sku]["quantity"] -= units

 
    with open("updated_inventory.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["sku", "name", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for sku, details in inventory.items():
            writer.writerow({
                "sku": sku,
                "name": details["name"],
                "quantity": details["quantity"]
            })


    with open("rejected_movements.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["sku", "type", "units", "reason"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rejected)

    return inventory, rejected



create_sample_files()


inventory, rejected = reconcile_inventory(
    "inventory.csv",
    "movements.csv"
)

print("INVENTORY RECONCILIATION REPORT")
print("-" * 50)

for sku, details in inventory.items():
    print(
        sku,
        "|",
        details["name"],
        "| Final Quantity:",
        details["quantity"]
    )

print("\nREJECTED MOVEMENTS")
print("-" * 50)

for movement in rejected:
    print(movement)

print("\nSUMMARY")
print("-" * 50)
print("Total products:", len(inventory))
print("Accepted movements:", 7 - len(rejected))
print("Rejected movements:", len(rejected))

print("\nOUTPUT FILES CREATED")
print("updated_inventory.csv")
print("rejected_movements.csv")
