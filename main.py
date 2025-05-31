import tkinter as tk
from tkinter import ttk
from chart import switch_frame, show_expense_pie, show_income_vs_expense

# todo: add two tabs one for add entries and one for viewing charts using sample data- done
# todo: use real data user entered in the entry frame to populate the charts - done
# todo: add a summary of total income and expenses in the entry frame - done
# todo: allow user to edit entries in the table
# todo: add alert for overspending

# todo: allow user to add new categories and subcategories

# Example data
# records = [
#     ("Expense", "Rent", 1200),
#     ("Expense", "Groceries", 300),
#     ("Expense", "Clothing", 150),
#     ("Income", "Salary", 3000),
#     ("Income", "Bonus", 500)
# ]

records = []  # Initialize records as an empty list

# Create the window
root = tk.Tk()
root.title("Budget Tracker")
root.geometry("1000x1800")

# Having two frames (entry_frame, chart_frame) Use pack_forget() to hide one and pack() to show the other
# Chart display 
chart_frame = tk.Frame(root, bg="white")
chart_frame.pack(fill=tk.BOTH, expand=True)

# Entry frame
entry_frame = tk.Frame(root, bg="lightgray")
entry_frame.pack(fill=tk.BOTH, expand=True)

# default to entry frame
entry_frame.pack(fill=tk.BOTH, expand=True)  # Show this first by default
chart_frame.pack_forget() 

# add menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)
# Create a records menu
record_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Records', menu=record_menu)
record_menu.add_command(label="Add Entry", command=lambda: [switch_frame(entry_frame, chart_frame)])
record_menu.add_separator()
record_menu.add_command(label='Exit', command=root.quit)
# Create a chart menu
chart_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Charts', menu=chart_menu)
chart_menu.add_command(label="Show Expense Pie Chart", command=lambda: [switch_frame(chart_frame, entry_frame), show_expense_pie(records, chart_frame)])
chart_menu.add_command(label="Show Income vs Expense", command=lambda: [switch_frame(chart_frame, entry_frame), show_income_vs_expense(records, chart_frame)])





# salary input
salary_label = tk.Label(entry_frame, text="Salary") # Use entry_frame to avoid confusion with the chart_frame
salary_label.pack()
entry_salary = tk.Entry(entry_frame, width=30)
entry_salary.pack(pady=2)
category_salary_label = tk.Label(entry_frame, text="Category: ")
category_salary_label.pack(pady=10)
category_salary_combo_box = ttk.Combobox(entry_frame, values=["Expense", "Income"])
category_salary_combo_box.pack(pady=5)

# Rent input
rent_label = tk.Label(entry_frame, text="Rent")
rent_label.pack()
entry_rent = tk.Entry(entry_frame, width=30)
entry_rent.pack(pady=2)
category_rent_label = tk.Label(entry_frame, text="Category: ")
category_rent_label.pack(pady=10)
category_rent_combo_box = ttk.Combobox(entry_frame, values=["Expense", "Income"])
category_rent_combo_box.pack(pady=5)

# Groceries input
groceries_label = tk.Label(entry_frame, text="Groceries")
groceries_label.pack()
entry_groceries = tk.Entry(entry_frame, width=30)
entry_groceries.pack(pady=2)
category_groceries_label = tk.Label(entry_frame, text="Category: ")
category_groceries_label.pack(pady=10)
category_groceries_combo_box = ttk.Combobox(entry_frame, values=["Expense", "Income"])
category_groceries_combo_box.set("Expense")
category_groceries_combo_box.pack(pady=5)

# Transport input
transport_label = tk.Label(entry_frame, text="Transport")
transport_label.pack()
entry_transport = tk.Entry(entry_frame, width=30)
entry_transport.pack(pady=2)
category_transport_label = tk.Label(entry_frame, text="Category: ")
category_transport_label.pack(pady=10)
category_transport_combo_box = ttk.Combobox(entry_frame, values=["Expense", "Income"])
category_transport_combo_box.set("Expense")
category_transport_combo_box.pack(pady=5)

# Create table
tree = ttk.Treeview(entry_frame, columns=("Category", "Subcategory", "Amount"), show='headings')
tree.heading("Category", text="Category")
tree.heading("Subcategory", text="Subcategory")
tree.heading("Amount", text="Amount")   
tree.pack(pady=20)

# Summary label
summary_label = tk.Label(entry_frame, text="")
summary_label.pack(pady=10)

# add functions 
def calculate_total():
    try:
        income = float(entry_salary.get())
        rent = float(entry_rent.get())
        groceries = float(entry_groceries.get())
        transport = float(entry_transport.get())

        total_expenses = rent + groceries + transport
        balance = income - total_expenses

        summary_label.config(text=f"Total expenses: ${total_expenses:.2f}\nBalance: ${balance:.2f}")

    except ValueError:
        summary_label.config(text="Please enter valid numbers.")


def add_entry():
    switch_frame(entry_frame, chart_frame)

    salary_category = category_salary_combo_box.get()
    salary_amount = entry_salary.get()
    salary_label_text = salary_label.cget("text")

    rent_category = category_transport_combo_box.get()
    rent_amount = entry_rent.get()
    rent_label_text = rent_label.cget("text")
    
    groceries_category = category_groceries_combo_box.get()
    groceries_amount = entry_groceries.get()
    groceries_label_text = groceries_label.cget("text")
    
    
    transport_amount = entry_transport.get()
    transport_category = category_transport_combo_box.get()
    transport_label_text = transport_label.cget("text")

    # Add entries to the treeview
    if salary_amount:
        tree.insert("", "end", values=(salary_category, salary_label_text, salary_amount))
        records.append((salary_category, salary_label_text, float(salary_amount)))
    if rent_amount:
        tree.insert("", "end", values=(rent_category, rent_label_text, rent_amount))
        records.append((rent_category, rent_label_text, float(rent_amount)))
    if groceries_amount:
        tree.insert("", "end", values=(groceries_category, groceries_label_text, groceries_amount))
        records.append((groceries_category, groceries_label_text, float(groceries_amount)))
    if transport_amount:
        tree.insert("", "end", values=(transport_category, transport_label_text, transport_amount))
        records.append((transport_category, transport_label_text, float(transport_amount)))

    calculate_total()
    # Update summary label
    # summary_label.config(text=f"Total Income: ${totals.get('Income', 0):.2f}, Total Expenses: ${totals.get('Expense', 0):.2f}")


# Bind event to selection
# combo_box.bind("<<ComboboxSelected>>", select)

# Submit button
tk.Button(entry_frame, text="Add Entry", command=add_entry).pack(pady=5)

# Buttons to trigger imported functions
# tk.Button(root, text="Show Expense Pie Chart", command=lambda: show_expense_pie(records, chart_frame)).pack(pady=5)
# tk.Button(root, text="Show Income vs Expense", command=lambda: show_income_vs_expense(records, chart_frame)).pack(pady=5)

# Result label
label_result = tk.Label(entry_frame, text="")
label_result.pack()

root.mainloop()

