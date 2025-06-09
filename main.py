import tkinter as tk
from tkinter import ttk
from chart import switch_frame, show_expense_pie, show_income_vs_expense
from editTable import EditableTreeview
from tkinter import messagebox
from chat_with_ai import SpendingAdvisorAI
from dotenv import load_dotenv
import os

load_dotenv()  

# revise to OOP style, Remember to access/modify the records only through your MainApplication methods to maintain data integrity.
# add two tabs one for add entries and one for viewing charts using sample data- done
# use real data user entered in the entry frame to populate the charts - done
# add a summary of total income and expenses in the entry frame - done
# allow user to edit entries in the table -done
# revise editable table to only allow editing of the amount column, not category or subcategory - done
# refresh chart and summary when new entries are added - done
# how to change the layout of the entry frame to have a better user experience - done
# set the non-editable columns to be a different color to indicate they are not editable - can't be done with ttk.Treeview, need to use a custom widget
# add alert for overspending -done
# update readme file -done
# allow user to delete entries from the table and lose focus on the entry fields - done
# add security features to restrict what user can enter in the entry fields (e.g., only numbers for amounts) 
# allow user to add a new subcategorie with amount and add into the table
# when user add a new  entry to the table, it should include the new subcategories and amounts, also calculating, it needs to include the new subcategories in the summary and charts
# Alert for no data in the charts

# optional: add AI feature to provide insights on spending habits

# Example data
# records = [
#     ("Expense", "Rent", 1200),
#     ("Expense", "Groceries", 300),
#     ("Expense", "Clothing", 150),
#     ("Income", "Salary", 3000),
#     ("Income", "Bonus", 500)
# ]

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
AGENT_ID = os.getenv("AGENT_ID")

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Tracker")
        self.geometry("850x800")
        self.records = []  # Initialize records as an empty list
        self.ai_agent = SpendingAdvisorAI(PROJECT_CONNECTION_STRING, AGENT_ID)

        # Create a canvas and a vertical scrollbar for the entry frame
        self.entry_canvas = tk.Canvas(self, bg="lightgray")
        self.entry_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.entry_canvas.yview)
        self.entry_canvas.configure(yscrollcommand=self.entry_scrollbar.set)

        # Use grid for the canvas and scrollbar
        self.entry_canvas.grid(row=0, column=0, sticky="nsew")
        self.entry_scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure root grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a frame inside the canvas
        self.entry_frame = tk.Frame(self.entry_canvas, bg="lightgray")
        self.entry_canvas.create_window((0, 0), window=self.entry_frame, anchor="nw")

        # Make sure the canvas scrolls when the frame size changes
        self.entry_frame.bind(
            "<Configure>",
            lambda e: self.entry_canvas.configure(
                scrollregion=self.entry_canvas.bbox("all")
            )
        )

        # Chart frame (hidden initially)
        self.chart_frame = tk.Frame(self, bg="white")
        self.chart_frame.grid(row=0, column=0, sticky="nsew")
        self.chart_frame.grid_remove()  # Hide chart frame initially

        # create menu bar
        self.create_menu()

        # Add widgets to entry frame
        self.create_entry_widgets()

        # Add a divider line
        divider1 = tk.Frame(self.entry_frame, height=2, bd=0, relief="ridge", bg="gray")
        divider1.grid(row=9, column=0, columnspan=14, sticky="ew", pady=10)

        divider2 = tk.Frame(self.entry_frame, height=2, bd=0, relief="ridge", bg="gray")
        divider2.grid(row=13, column=0, columnspan=14, sticky="ew", pady=10)

        # Create the treeview table 
        self.create_treeview_table()

        # Allow user to add a entry with a new subcategory name
        self.add_new_subcategory()

        # add a frame for the delete button and get AI advice button
        button_frame = tk.Frame(self.entry_frame, bg="lightgray")
        button_frame.grid(row=11, column=5, rowspan=2, columnspan=3, pady=5, sticky="n")

        # add a delete button fo
        self.delete_button = tk.Button(
        button_frame, text="Delete Selected", command=self.delete_selected_record, bg="red", fg="white")
        self.delete_button.grid(row=0, column=0, pady=(0, 5), sticky="ew")

        self.ai_advice_button = tk.Button(
        button_frame, text="Get AI Advice", command=self.get_ai_advice, bg="#4CAF50", fg="white")
        self.ai_advice_button.grid(row=1, column=0, pady=(5, 0), sticky="ew")

        # Add entry button to the entry frame
        self.add_entry_button = tk.Button(self.entry_frame, text="Add Entry", command=self.add_entry, bg="#4CAF50", fg="white")
        self.add_entry_button.grid(row=5, column=0, columnspan=4, pady=5)

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
        chart_menu.add_command(label="Show Expense Pie Chart", command=lambda: [switch_frame(self.chart_frame, self.entry_frame), show_expense_pie(self.records, self.chart_frame, self.entry_frame)])
        chart_menu.add_command(label="Show Income vs Expense", command=lambda: [switch_frame(self.chart_frame, self.entry_frame), show_income_vs_expense(self.records, self.chart_frame, self.entry_frame)])

    def create_entry_widgets(self):

        # create validation tip label
        self.validation_tips_label = tk.Label(self.entry_frame, text="", fg="red", bg="lightgray")
        self.validation_tips_label.grid(row=8, column=0, columnspan=4, pady=(0, 10))


        # set up validation for entry fields
        vcmd = (self.register(self.validate_number), "%P")

        # Salary input
        self.salary_label = tk.Label(self.entry_frame, text="Salary")
        self.salary_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_salary = tk.Entry(self.entry_frame, width=30, validate="key", validatecommand=vcmd)
        self.entry_salary.grid(row=0, column=1, padx=10, pady=5)
        self.category_salary_label = tk.Label(self.entry_frame, text="Category:")
        self.category_salary_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.category_salary_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_salary_combo_box.set("Income")
        self.category_salary_combo_box.grid(row=0, column=3, padx=10, pady=5)

        # Rent input
        self.rent_label = tk.Label(self.entry_frame, text="Rent")
        self.rent_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_rent = tk.Entry(self.entry_frame, width=30, validate="key", validatecommand=vcmd)
        self.entry_rent.grid(row=1, column=1, padx=10, pady=5)
        self.category_rent_label = tk.Label(self.entry_frame, text="Category:")
        self.category_rent_label.grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.category_rent_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_rent_combo_box.set("Expense")
        self.category_rent_combo_box.grid(row=1, column=3, padx=10, pady=5)

        # Groceries input
        self.groceries_label = tk.Label(self.entry_frame, text="Groceries")
        self.groceries_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_groceries = tk.Entry(self.entry_frame, width=30, validate="key", validatecommand=vcmd)
        self.entry_groceries.grid(row=2, column=1, padx=10, pady=5)
        self.category_groceries_label = tk.Label(self.entry_frame, text="Category:")
        self.category_groceries_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.category_groceries_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_groceries_combo_box.set("Expense")
        self.category_groceries_combo_box.grid(row=2, column=3, padx=10, pady=5)

        # Transport input
        self.transport_label = tk.Label(self.entry_frame, text="Transport")
        self.transport_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_transport = tk.Entry(self.entry_frame, width=30, validate="key", validatecommand=vcmd)
        self.entry_transport.grid(row=3, column=1, padx=10, pady=5)
        self.category_transport_label = tk.Label(self.entry_frame, text="Category:")
        self.category_transport_label.grid(row=3, column=2, padx=10, pady=5, sticky="e")
        self.category_transport_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_transport_combo_box.set("Expense")
        self.category_transport_combo_box.grid(row=3, column=3, padx=10, pady=5)
        
        # add a instruction label
        self.instruction_label = tk.Label(self.entry_frame, text="You can add a new subcategory with amount", bg="lightgray")
        self.instruction_label.grid(row=14, column=0, columnspan=10, pady=(10, 0))

        # Add a label for adding new sub categories
        self.new_subcategory_label = tk.Label(self.entry_frame, text="New Sub Category:")
        self.new_subcategory_label.grid(row=15, column=0, padx=10, pady=5, sticky="e")
        # Entry for new sub category name
        self.new_subcategory_entry = tk.Entry(self.entry_frame, width=20)
        self.new_subcategory_entry.grid(row=15, column=1, padx=10, pady=5)

        # add a label for entering Amount for the new subcategory
        self.amount_new_subcategory_label = tk.Label(self.entry_frame, text="Amount:")
        self.amount_new_subcategory_label.grid(row=15, column=2, padx=10, pady=5, sticky="e")
        # Entry for amount for the new subcategory
        self.amount_new_subcategory_entry = tk.Entry(self.entry_frame, width=20, validate="key", validatecommand=(self.register(self.validate_number), "%P"))
        self.amount_new_subcategory_entry.grid(row=15, column=3, padx=10, pady=5)

        self.category_new_subcategory_label = tk.Label(self.entry_frame, text="Category:")
        self.category_new_subcategory_label.grid(row=16, column=0, padx=10, pady=5, sticky="e")

        # Combobox for selecting category for the new subcategory
        self.category_new_subcategory_combo_box = ttk.Combobox(self.entry_frame, values=["Expense", "Income"])
        self.category_new_subcategory_combo_box.set("Expense")  
        self.category_new_subcategory_combo_box.grid(row=16, column=1, padx=10, pady=5)

        # Button to add the new category
        self.add_category_button = tk.Button(self.entry_frame, text="Add Entry with new Sub Category", command=self.add_new_subcategory,bg="#4CAF50", fg="white") 
        self.add_category_button.grid(row=16, column=3, padx=10, pady=5, )

    def create_treeview_table(self):
       
        self.table_tips_label = tk.Label(
        self.entry_frame,
        text="- You can edit the amount column by double-clicking on it.\n- Select a record and click 'Delete Selected' to remove it.")
        self.table_tips_label.grid(row=10, column=0, columnspan=4, pady=(20, 10))
        
        tree_frame = tk.Frame(self.entry_frame)
        tree_frame.grid(row=11, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")
        
        # Configure grid weights for resizing
        self.entry_frame.grid_rowconfigure(4, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Create a treeview to display records
        # Use EditableTreeview instead of ttk.Treeview
        # set up columns that will be editable

        self.tree = EditableTreeview(
            tree_frame, 
            columns=("Category", "Subcategory", "Amount"), 
            editable_columns=['Amount'], 
            show='headings',
            on_cell_edit=self.on_table_edit)
        self.tree.heading("Category", text="Category")
        self.tree.heading("Subcategory", text="Subcategory")
        self.tree.heading("Amount", text="Amount")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Summary label
        self.summary_label = tk.Label(self.entry_frame, text="", bg="lightgray")
        self.summary_label.grid(row=12, column=0, columnspan=1, pady=10)

        # add a label for displaying AI advice
        self.ai_advice_label = tk.Label(self.entry_frame, text="", bg="lightgray", wraplength=400)
        self.ai_advice_label.grid(row=12, column=3, columnspan=4, pady=(10, 0))

    # get AI advice based on the records
    def get_ai_advice(self):
        advice = self.ai_agent.get_advice_from_records(self.records)
        self.ai_advice_label.config(text=advice)

    # cacualate total expenses and balance    
    def calculate_total(self):
        try:
            total_income = sum(r[2] for r in self.records if r[0] == "Income")
            total_expenses = sum(r[2] for r in self.records if r[0] == "Expense")
            balance = total_income - total_expenses

            # add alert message for overspending
            if balance < 0:
                messagebox.showwarning("Overspending Alert", "You have overspent your budget!")
            elif balance == 0:
                messagebox.showinfo("Budget Alert", "You have balanced your budget!")
            elif balance > 0 and balance < 100:
                messagebox.showinfo("Budget Alert", "You have a small surplus in your budget.")

            self.summary_label.config(
                text=f"Total income: ${total_income:.2f}\n"
                    f"Total expenses: ${total_expenses:.2f}\n"
                    f"Balance: ${balance:.2f}"
            )
        except Exception as e:
            self.summary_label.config(text="Error calculating summary.")

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

        # clear the entry fields after adding an entry
        self.entry_salary.delete(0, tk.END)
        self.entry_rent.delete(0, tk.END)
        self.entry_groceries.delete(0, tk.END)
        self.entry_transport.delete(0, tk.END)
        self.category_salary_combo_box.set("Income")
        self.category_rent_combo_box.set("Expense")
        self.category_groceries_combo_box.set("Expense")
        self.category_transport_combo_box.set("Expense")

        # lose focus on the entry fields
        self.entry_frame.focus_set()

    def add_new_subcategory(self):
            new_subcategory = self.new_subcategory_entry.get().strip()
            new_amount = self.amount_new_subcategory_entry.get().strip()
            new_category = self.category_new_subcategory_combo_box.get().strip()

            if new_subcategory and new_amount and new_category:
                self.tree.insert("", "end", values=(new_category, new_subcategory, new_amount))
                self.records.append((new_category, new_subcategory, float(new_amount)))
                self.calculate_total()
                # print(self.records)
                # Clear the entry fields after adding a new subcategory
                self.new_subcategory_entry.delete(0, tk.END)
                self.amount_new_subcategory_entry.delete(0, tk.END)

    def on_table_edit(self, item_id, column, new_value):
        # Find the index of the item in the treeview
        item_index = self.tree.index(item_id)
        # Update the corresponding record in self.records
        record = list(self.records[item_index])
        if column == "Amount":
            try:
                record[2] = float(new_value)
            except ValueError:
                record[2] = 0
        self.records[item_index] = tuple(record)
        self.calculate_total()
    
    def delete_selected_record(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("No selection", "Please select a record to delete.")
            return
        for item in selected:
            index = self.tree.index(item)
            self.tree.delete(item)
            if index < len(self.records):
                del self.records[index]

        self.calculate_total()

    def validate_number(self, value):

        # set the  validation_tips_label when user entered invalid input
        if value == "" or value == ".":
            return True  # Allow empty or just a dot (for typing floats)
        try:
            float(value)
            self.validation_tips_label.config(text="")  # Clear tip if valid
            return True
        except ValueError:
            self.validation_tips_label.config(text="Please enter a valid number." , fg="red")
            return False  

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

