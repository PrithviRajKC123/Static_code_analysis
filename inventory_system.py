"""Inventory management system with static analysis fixes."""

import json
from datetime import datetime
import ast

# Inventory data storage
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item and quantity to the stock log."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        print("Invalid item or quantity type.")
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Remove a specified quantity of an item from stock."""
    try:
        if item in stock_data:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
        else:
            print(f"Item '{item}' not found in stock.")
    except KeyError as err:
        print(f"Error removing item: {err}")


def get_qty(item):
    """Return the quantity of the given item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        print("Inventory file not found. Starting fresh.")
        stock_data = {}


def save_data(file="inventory.json"):
    """Save current inventory data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)


def print_data():
    """Display current stock items and quantities."""
    print("\n=== Items Report ===")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return items with quantity below the given threshold."""
    result = [item for item, qty in stock_data.items() if qty < threshold]
    return result


def main():
    """Main execution block for testing the inventory system."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, will be handled
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()

    # Removed unsafe eval and replaced with safe demonstration
    code_str = "{'note': 'eval avoided'}"
    try:
        safe_eval = ast.literal_eval(code_str)
        print("Safe eval result:", safe_eval)
    except Exception as e:
        print(f"Evaluation error: {e}")


if __name__ == "__main__":
    main()
