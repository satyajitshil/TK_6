import tkinter as tk
from tkinter import ttk, messagebox


class RestaurantOrderManagement:

    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Order Management")
        self.root.geometry("800x600")

        # Menu items and prices in USD
        self.menu_items = {
            "French Fries": 1,
            "Basic Burger": 1.5,
            "Burger Delite": 2,
            "Burger Supreme": 2.5,
            "Drink": 1
        }

        # USD to INR conversion rate
        self.exchange_rate = 96

        # Main frame
        frame = ttk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        ttk.Label(
            frame,
            text="Restaurant Order Management",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Dictionaries
        self.menu_labels = {}
        self.menu_quantities = {}

        # Menu items
        for i, (item, price) in enumerate(self.menu_items.items(), start=1):

            label = ttk.Label(
                frame,
                text=f"{item} (${price})",
                font=("Arial", 12)
            )

            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            self.menu_labels[item] = label

            quantity_entry = ttk.Entry(frame, width=5)
            quantity_entry.grid(row=i, column=1, padx=10, pady=5)

            self.menu_quantities[item] = quantity_entry

        # Currency selection
        self.currency_var = tk.StringVar(value="USD")

        ttk.Label(
            frame,
            text="Currency",
            font=("Arial", 12)
        ).grid(
            row=len(self.menu_items) + 1,
            column=0,
            padx=10,
            pady=5
        )

        currency_dropdown = ttk.Combobox(
            frame,
            textvariable=self.currency_var,
            state="readonly",
            width=18,
            values=("USD", "INR")
        )

        currency_dropdown.grid(
            row=len(self.menu_items) + 1,
            column=1,
            padx=10,
            pady=5
        )

        currency_dropdown.current(0)

        # Update prices when currency changes
        self.currency_var.trace("w", self.update_menu_prices)

        # Order button
        order_button = ttk.Button(
            frame,
            text="Place Order",
            command=self.place_order
        )

        order_button.grid(
            row=len(self.menu_items) + 2,
            column=0,
            columnspan=3,
            padx=10,
            pady=10
        )

    # Method to update menu prices
    def update_menu_prices(self, *args):

        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"

        rate = self.exchange_rate if currency == "INR" else 1

        for item, label in self.menu_labels.items():

            price = self.menu_items[item] * rate

            label.config(
                text=f"{item} ({symbol}{price:.2f})"
            )

    # Method to place order
    def place_order(self):

        total_cost = 0

        order_summary = "Order Summary\n\n"

        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"

        rate = self.exchange_rate if currency == "INR" else 1

        for item, entry in self.menu_quantities.items():

            quantity = entry.get()

            if quantity.isdigit():

                quantity = int(quantity)

                if quantity > 0:

                    price = self.menu_items[item] * rate

                    cost = quantity * price

                    total_cost += cost

                    order_summary += (
                        f"{item}: {quantity} x "
                        f"{symbol}{price:.2f} = "
                        f"{symbol}{cost:.2f}\n"
                    )

        if total_cost > 0:

            order_summary += (
                f"\nTotal Cost: {symbol}{total_cost:.2f}"
            )

            messagebox.showinfo(
                "Order Placed",
                order_summary
            )

        else:

            messagebox.showerror(
                "Error",
                "Please order at least one item."
            )


# Main block
if __name__ == "__main__":

    root = tk.Tk()

    app = RestaurantOrderManagement(root)

    root.mainloop()
