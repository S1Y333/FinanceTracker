import tkinter as tk
from tkinter import ttk


# todo: add reporting and visualization features

# todo: add alert for overspending

# todo: allow user to add new categories and subcategories

# store records, 
records = []

def calculate_total():
    try:
        income = float(entry_income.get())
        rent = float(entry_rent.get())
        groceries = float(entry_groceries.get())
        transport = float(entry_transport.get())

        total_expenses = rent + groceries + transport
        balance = income - total_expenses

        label_result.config(text=f"Total expenses: ${total_expenses:.2f}\nBalance: ${balance:.2f}")

    except ValueError:
        label_result.config(text="Please enter valid numbers.")




# Create the window
root = tk.Tk()
root.title("Budget Tracker")
root.geometry("1000x1000")

# salary input
tk.Label(root, text="Salary:").pack()
entry_salary = tk.Entry(root, width=30)
entry_salary.pack(pady=2)
category_salary_label = tk.Label(root, text="Category: ")
category_salary_label.pack(pady=10)
category_salary_combo_box = ttk.Combobox(root, values=["Expense", "Income"])
category_salary_combo_box.pack(pady=5)

# Rent input
tk.Label(root, text="Rent:").pack()
entry_rent = tk.Entry(root, width=30)
entry_rent.pack(pady=2)
category_rent_label = tk.Label(root, text="Category: ")
category_rent_label.pack(pady=10)
category_rent_combo_box = ttk.Combobox(root, values=["Expense", "Income"])
category_rent_combo_box.pack(pady=5)

# Groceries input
tk.Label(root, text="Groceries:").pack()
entry_groceries = tk.Entry(root, width=30)
entry_groceries.pack(pady=2)
category_groceries_label = tk.Label(root, text="Category: ")
category_groceries_label.pack(pady=10)
category_groceries_combo_box = ttk.Combobox(root, values=["Expense", "Income"])
category_groceries_combo_box.set("Expense")
category_groceries_combo_box.pack(pady=5)

# Transport input
tk.Label(root, text="Transport:").pack()
entry_transport = tk.Entry(root, width=30)
entry_transport.pack(pady=2)
category_transport_label = tk.Label(root, text="Category: ")
category_transport_label.pack(pady=10)
category_transport_combo_box = ttk.Combobox(root, values=["Expense", "Income"])
category_transport_combo_box.set("Expense")
category_transport_combo_box.pack(pady=5)

# Create table
tree = ttk.Treeview(root, columns=("Category", "Subcategory", "Amount"), show='headings')
tree.heading("Category", text="Category")
tree.heading("Subcategory", text="Subcategory")
tree.heading("Amount", text="Amount")   
tree.pack(pady=20)

# Summary label
summary_label = tk.Label(root, text="")
summary_label.pack(pady=10)

# add functions 
def add_entry():
    salary_category = category_salary_combo_box.get()
    salary_amount = entry_salary.get()

    rent_category = category_transport_combo_box.get()
    rent_amount = entry_rent.get()
    
    groceries_category = category_groceries_combo_box.get()
    groceries_amount = entry_groceries.get()
    
    
    transport_amount = entry_transport.get()
    transport_category = category_transport_combo_box.get()

    # Add entries to the treeview
    if salary_amount:
        tree.insert("", "end", values=(salary_category, salary_amount))
    if rent_amount:
        tree.insert("", "end", values=(rent_category, rent_amount))
    if groceries_amount:
        tree.insert("", "end", values=(groceries_category, groceries_amount))
    if transport_amount:
        tree.insert("", "end", values=(transport_category, transport_amount))

    # calculate each category total
    totals = {"Expense": 0, "Income": 0}
    for item in tree.get_children():
        category, amount = tree.item(item, "values")
        try:
            amount = float(amount)
        except ValueError:
            continue  # Skip if amount is not a valid number
        if category not in totals:
            totals[category] = 0
        totals[category] += amount
    # Update summary label
    summary_label.config(text=f"Total Income: ${totals.get('Income', 0):.2f}, Total Expenses: ${totals.get('Expense', 0):.2f}")
    
# make a pie chart of the different categories
   


# Bind event to selection
# combo_box.bind("<<ComboboxSelected>>", select)

# Submit button
tk.Button(root, text="Add Entry", command=add_entry).pack(pady=5)

# Result label
label_result = tk.Label(root, text="")
label_result.pack()

root.mainloop()

