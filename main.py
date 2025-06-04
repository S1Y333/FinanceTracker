import tkinter as tk
from tkinter import ttk
from chart import switch_frame, show_expense_pie, show_income_vs_expense
from editTable import EditableTreeview

# revise to OOP style, Remember to access/modify the records only through your MainApplication methods to maintain data integrity.
# todo: add two tabs one for add entries and one for viewing charts using sample data- done
# todo: use real data user entered in the entry frame to populate the charts - done
# todo: add a summary of total income and expenses in the entry frame - done
# todo: allow user to edit entries in the table -done
# todo: revise editable table to only allow editing of the amount column, not category or subcategory - done
# todo: refresh chart and summary when new entries are added
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

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Tracker")
        self.geometry("1000x1800")
        self.records = []  # Initialize records as an empty list

        # create frames
        # Having two frames (entry_frame, chart_frame) 
        self.chart_frame = tk.Frame(self, bg="white")
        self.entry_frame = tk.Frame(self, bg="lightgray")
        self.entry_frame.pack(fill=tk.BOTH, expand=True)
        self.chart_frame.pack_forget() # Hide chart frame initially

        # create menu bar
        self.create_menu()

        # Add widgets to entry frame
        self.create_entry_widgets()

        # Create the treeview table 
        self.create_treeview_table()

        # add a add entry button to the entry frame,need to assign it to self, so we can access it later
        self.add_entry_button = tk.Button(self.entry_frame, text="Add Entry", command=self.add_entry)
        self.add_entry_button.pack(pady=5)

    def create_menu(self):
        # add menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        # Create a records menu
        record_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Records', menu=record_menu)
        record_menu.add_command(label="Add Entry", command=lambda: [switch_frame(self.entry_frame, self.chart_frame)])
        record_menu.add_separator()
        record_menu.add_command(label='Exit', command=self.quit)
        # Create a chart menu
        chart_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Charts', menu=chart_menu)
        chart_menu.add_command(label="Show Expense Pie Chart", command=lambda: [switch_frame(self.chart_frame, self.entry_frame), show_expense_pie(self.records, self.chart_frame)])
        chart_menu.add_command(label="Show Income vs Expense", command=lambda: [switch_frame(self.chart_frame, self.entry_frame), show_income_vs_expense(self.records, self.chart_frame)])

    def create_entry_widgets(self):
        # salary input
        self.salary_label = tk.Label(self.entry_frame, text="Salary") # Use entry_frame to avoid confusion with the chart_frame
        self.salary_label.pack()
        self.entry_salary = tk.Entry(self.entry_frame, width=30)
        self.entry_salary.pack(pady=2)
        self.category_salary_label = tk.Label(self.entry_frame, text="Category: ")
        self.category_salary_label.pack(pady=10)
        self.category_salary_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_salary_combo_box.set("Income")
        self.category_salary_combo_box.pack(pady=5)

        # Rent input
        self.rent_label = tk.Label(self.entry_frame, text="Rent")
        self.rent_label.pack()
        self.entry_rent = tk.Entry(self.entry_frame, width=30)
        self.entry_rent.pack(pady=2)
        self.category_rent_label = tk.Label(self.entry_frame, text="Category: ")
        self.category_rent_label.pack(pady=10)
        self.category_rent_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_rent_combo_box.set("Expense")
        self.category_rent_combo_box.pack(pady=5)

        # Groceries input
        self.groceries_label = tk.Label(self.entry_frame, text="Groceries")
        self.groceries_label.pack()
        self.entry_groceries = tk.Entry(self.entry_frame, width=30)
        self.entry_groceries.pack(pady=2)
        self.category_groceries_label = tk.Label(self.entry_frame, text="Category: ")
        self.category_groceries_label.pack(pady=10)
        self.category_groceries_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_groceries_combo_box.set("Expense")
        self.category_groceries_combo_box.pack(pady=5)

        # Transport input
        self.transport_label = tk.Label(self.entry_frame, text="Transport")
        self.transport_label.pack()
        self.entry_transport = tk.Entry(self.entry_frame, width=30)
        self.entry_transport.pack(pady=2)
        self.category_transport_label = tk.Label(self.entry_frame, text="Category: ")
        self.category_transport_label.pack(pady=10)
        self.category_transport_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_transport_combo_box.set("Expense")
        self.category_transport_combo_box.pack(pady=5)

    def create_treeview_table(self):
        # Create a treeview to display records
        # Use EditableTreeview instead of ttk.Treeview
        # set up columns that will be editable
        self.tree = EditableTreeview(self.entry_frame, columns=("Category", "Subcategory", "Amount"), editable_columns=['Amount'], show='headings')
        self.tree.heading("Category", text="Category")
        self.tree.heading("Subcategory", text="Subcategory")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(pady=20)

        # Summary label
        self.summary_label = tk.Label(self.entry_frame, text="")
        self.summary_label.pack(pady=10)

    # cacualate total expenses and balance 
    def calculate_total(self):
        try:
            income = float(self.entry_salary.get())
            rent = float(self.entry_rent.get())
            groceries = float(self.entry_groceries.get())
            transport = float(self.entry_transport.get())

            total_expenses = rent + groceries + transport
            balance = income - total_expenses

            self.summary_label.config(text=f"Total expenses: ${total_expenses:.2f}\nBalance: ${balance:.2f}")

        except ValueError:
            self.summary_label.config(text="Please enter valid numbers.")
     
    def add_entry(self):
        switch_frame(self.entry_frame, self.chart_frame)

        self.salary_category = self.category_salary_combo_box.get()
        self.salary_amount = self.entry_salary.get()
        self.salary_label_text = self.salary_label.cget("text")

        self.rent_category = self.category_transport_combo_box.get()
        self.rent_amount = self.entry_rent.get()
        self.rent_label_text = self.rent_label.cget("text")
        
        self.groceries_category = self.category_groceries_combo_box.get()
        self.groceries_amount = self.entry_groceries.get()
        self.groceries_label_text = self.groceries_label.cget("text")
        
        
        self.transport_amount = self.entry_transport.get()
        self.transport_category = self.category_transport_combo_box.get()
        self.transport_label_text = self.transport_label.cget("text")

        # Add entries to the treeview
        if self.salary_amount:
            self.tree.insert("", "end", values=(self.salary_category, self.salary_label_text, self.salary_amount))
            self.records.append((self.salary_category, self.salary_label_text, float(self.salary_amount)))
        if self.rent_amount:
            self.tree.insert("", "end", values=(self.rent_category, self.rent_label_text, self.rent_amount))
            self.records.append((self.rent_category, self.rent_label_text, float(self.rent_amount)))
        if self.groceries_amount:
            self.tree.insert("", "end", values=(self.groceries_category, self.groceries_label_text, self.groceries_amount))
            self.records.append((self.groceries_category, self.groceries_label_text, float(self.groceries_amount)))
        if self.transport_amount:
            self.tree.insert("", "end", values=(self.transport_category, self.transport_label_text, self.transport_amount))
            self.records.append((self.transport_category, self.transport_label_text, float(self.transport_amount)))

        self.calculate_total()

    
    
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

