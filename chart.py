import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox




# ===== Chart Functions =====
def show_expense_pie(records, chart_frame, entry_frame):
    if not records:
        messagebox.showwarning("No Data", "No records to display. Please add entries first.")
        switch_frame(entry_frame, chart_frame)
        return
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

    show_chart(fig, chart_frame)

def show_income_vs_expense(records, chart_frame, entry_frame):
    if not records:
        messagebox.showwarning("No Data", "No records to display. Please add entries first.")
        switch_frame(entry_frame, chart_frame)
        return
    # Calculate totals
    totals = {"Income": 0, "Expense": 0}
    for record in records:
        totals[record[0]] += record[2]

    # Create bar chart
    fig, ax = plt.subplots()
    ax.bar(totals.keys(), totals.values(), color=["green", "red"])
    ax.set_title("Income vs Expense")
    ax.set_ylabel("Amount ($)")

    show_chart(fig, chart_frame)

def show_chart(fig, chart_frame):
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    chart_frame.grid_rowconfigure(0, weight=1)
    chart_frame.grid_columnconfigure(0, weight=1)

def switch_frame(show_frame, hide_frame):
    hide_frame.grid_remove()
    show_frame.grid(row=0, column=0, sticky="nsew")

    # this only clears the frame, not the widgets inside it
    # for widget in frame.winfo_children():
    #     widget.destroy()
