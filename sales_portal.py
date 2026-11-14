import csv
import numpy as np
import pandas as pd

FILE = "sales.csv"
FIELDS = ["id", "date", "product", "region", "quantity", "price"]
USERS = {"admin": "1234"}


def user_login(username, password):
    """Return True if the username and password are correct."""
    return USERS.get(username) == password


def load_sales(filename):
    """Read sales from a CSV file and return a list of dictionaries."""
    sales = []
    try:
        with open(filename, "r") as f:
            for row in csv.DictReader(f):
                row["id"] = int(row["id"])
                row["quantity"] = int(row["quantity"])
                row["price"] = float(row["price"])
                sales.append(row)
    except FileNotFoundError:
        print("File not found. Starting with no records.")
    except PermissionError:
        print("No permission to read the file.")
    except ValueError:
        print("The file has bad data.")
    finally:
        print("Records loaded:", len(sales))
    return sales


def save_sales(sales, filename):
    """Write all sales to the CSV file."""
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(sales)
    except PermissionError:
        print("Cannot save. Close the file if it is open.")


def add_record(sales, product, region, quantity, price, date):
    """Add a sale to the list, save it, and return it."""
    sale = {"id": len(sales) + 1, "date": date, "product": product.title(),
            "region": region.title(), "quantity": quantity, "price": price}
    sales.append(sale)
    save_sales(sales, FILE)
    return sale


def search_record(sales, word):
    """Return the sales that match the word in product, region or date."""
    found = []
    for s in sales:
        if word.lower() in (s["product"] + s["region"] + s["date"]).lower():
            found.append(s)
    return found


def show_sales(sales):
    """Print the sales."""
    for s in sales:
        print(s["id"], s["date"], s["product"], s["region"], s["quantity"], s["price"])


def generate_report(sales):
    """Print a summary of the sales and return the DataFrame."""
    if len(sales) == 0:
        print("No sales yet.")
        return None
    df = pd.DataFrame(sales)
    df["total"] = df["quantity"] * df["price"]
    print("Total revenue:", df["total"].sum())
    print("Average sale:", round(np.mean(df["total"]), 2))
    print("Best product:", df.groupby("product")["total"].sum().idxmax())
    print("\nRevenue by region:")
    print(df.groupby("region")["total"].sum())
    return df


def get_number(message):
    """Keep asking until the user types a number."""
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Please enter a number.")


def main():
    logged_in = False
    for i in range(3):
        if user_login(input("Username: "), input("Password: ")):
            logged_in = True
            break
        print("Wrong login.")
    if not logged_in:
        print("Access denied.")
        return

    sales = load_sales(FILE)
    while True:
        print("\n1. Add sale  2. View sales  3. Search  4. Report  5. Exit")
        choice = input("Choose: ")
        if choice == "1":
            product = input("Product: ")
            region = input("Region: ")
            quantity = int(get_number("Quantity: "))
            price = get_number("Price: ")
            date = input("Date (YYYY-MM-DD): ")
            add_record(sales, product, region, quantity, price, date)
            print("Sale added.")
        elif choice == "2":
            show_sales(sales)
        elif choice == "3":
            show_sales(search_record(sales, input("Search: ")))
        elif choice == "4":
            generate_report(sales)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Choose 1 to 5.")


main()
