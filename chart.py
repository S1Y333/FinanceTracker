import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("Finance Tracker")

# Example data
records = [
    ("Expense", "Rent", 1200),
    ("Expense", "Groceries", 300),
    ("Expense", "Clothing", 150),
    ("Income", "Salary", 3000),
    ("Income", "Bonus", 500)
]

# ===== Chart Functions =====
def show_expense_pie():
    # Filter only expenses
    expense_data = {}
    for record in records:
        if record[0] == "Expense":
            subcategory = record[1]
            amount = record[2]
            expense_data[subcategory] = expense_data.get(subcategory, 0) + amount

    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(expense_data.values(), labels=expense_data.keys(), autopct='%1.1f%%', startangle=140)
    ax.set_title("Expenses by Category")

    show_chart(fig)

def show_income_vs_expense():
    # Calculate totals
    totals = {"Income": 0, "Expense": 0}
    for record in records:
        totals[record[0]] += record[2]

    # Create bar chart
    fig, ax = plt.subplots()
    ax.bar(totals.keys(), totals.values(), color=["green", "red"])
    ax.set_title("Income vs Expense")
    ax.set_ylabel("Amount ($)")

    show_chart(fig)

def show_chart(fig):
    # Clear previous chart if any
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# ===== UI Buttons =====
tk.Button(root, text="Show Expense Pie Chart", command=show_expense_pie).pack(pady=5)
tk.Button(root, text="Compare Income vs Expense", command=show_income_vs_expense).pack(pady=5)

# Chart display area
chart_frame = tk.Frame(root)
chart_frame.pack(pady=10)

root.mainloop()
