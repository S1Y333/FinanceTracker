import tkinter as tk
from tkinter import ttk


# Goal: compare two methonds of making a treeview editable
# main difference
#   Key Differences:
# Structure:

# Basic: Uses standalone functions

# Enhanced: Encapsulates functionality in a class inheriting from ttk.Treeview

# Entry Widget Management:

# Basic: Creates new entry each time (no tracking)

# Enhanced: Maintains reference to entry widget (self.entry)

# Item Tracking:

# Basic: Uses local variables in edit_cell

# Enhanced: Uses instance variables (self.current_item, self.current_column)

# Column Handling:

# Basic: Works directly with column IDs (#1, #2 etc.)

# Enhanced: Extracts column names from treeview configuration

# Event Handling:

# Basic: Uses lambda functions for destroy

# Enhanced: Has dedicated methods (save_edit, cancel_edit)

# FocusOut Handling:

# Basic: Destroys entry on focus loss

# Enhanced: Saves value on focus loss (more user-friendly)
# Basic Editable Treeview
# import tkinter as tk
# from tkinter import ttk

# def edit_cell(event):
#     """Make selected cell editable"""
#     # Get the clicked item and column
#     region_clicked = tree.identify_region(event.x, event.y)
#     if region_clicked not in ('cell', 'tree'):
#         return
    
#     column = tree.identify_column(event.x)
#     item = tree.identify_row(event.y)
    
#     # Get cell position and value
#     x, y, width, height = tree.bbox(item, column)
#     value = tree.set(item, column)
    
#     # Create entry widget for editing
#     entry_edit = ttk.Entry(root)
#     entry_edit.place(x=x, y=y, width=width, height=height)
    
#     # Insert current value
#     entry_edit.insert(0, value)
#     entry_edit.select_range(0, tk.END)
#     entry_edit.focus()
    
#     def save_edit(event):
#         """Save the edited value"""
#         tree.set(item, column, entry_edit.get())
#         entry_edit.destroy()
    
#     # Bind Return and Escape keys
#     entry_edit.bind('<Return>', save_edit)
#     entry_edit.bind('<Escape>', lambda e: entry_edit.destroy())
#     entry_edit.bind('<FocusOut>', lambda e: entry_edit.destroy())

# # Create main window
# root = tk.Tk()
# root.title("Editable Treeview")

# # Create Treeview
# tree = ttk.Treeview(root, columns=('Name', 'Age', 'Occupation'), show='headings')
# tree.heading('Name', text='Name')
# tree.heading('Age', text='Age')
# tree.heading('Occupation', text='Occupation')

# # Insert sample data
# tree.insert('', tk.END, values=('John Doe', 30, 'Engineer'))
# tree.insert('', tk.END, values=('Jane Smith', 25, 'Designer'))
# tree.insert('', tk.END, values=('Bob Johnson', 40, 'Manager'))

# # Bind double-click to edit
# tree.bind('<Double-1>', edit_cell)

# tree.pack(padx=10, pady=10)

# root.mainloop()




# Enhanced Editable Treeview with Double-Click Editing
# save edits when loss focus, and cancel edits on Escape key

class EditableTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Double-1>', self.on_double_click)
        self.entry = None
        self.current_item = None
        self.current_column = None
        
    def on_double_click(self, event):
        """Handle double-click event"""
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked not in ('cell', 'tree'):
            return
        
        column = self.identify_column(event.x)
        item = self.identify_row(event.y)
        
        # Don't edit if it's a heading click
        if item == '':
            return
            
        self.start_edit(item, column)
    
    def start_edit(self, item, column):
        """Start editing a cell"""
        # Destroy any existing entry widget
        if self.entry:
            self.entry.destroy()
            
        # Get column info
        col_index = int(column[1:]) - 1
        col_name = self['columns'][col_index]
        
        # Get cell position and value
        x, y, width, height = self.bbox(item, column)
        value = self.set(item, column)
        
        # Create entry widget
        self.entry = ttk.Entry(self)
        self.entry.place(x=x, y=y, width=width, height=height)
        
        # Insert current value and select all
        self.entry.insert(0, value)
        self.entry.select_range(0, tk.END)
        self.entry.focus()
        
        # Save references
        self.current_item = item
        self.current_column = col_name
        
        # Bind events
        self.entry.bind('<Return>', self.save_edit)
        self.entry.bind('<Escape>', self.cancel_edit)
        self.entry.bind('<FocusOut>', self.save_edit)
    
    def save_edit(self, event=None):
        """Save the edited value"""
        if self.entry and self.current_item and self.current_column:
            new_value = self.entry.get()
            self.set(self.current_item, self.current_column, new_value)
            self.entry.destroy()
            self.entry = None
            self.current_item = None
            self.current_column = None
    
    def cancel_edit(self, event=None):
        """Cancel editing"""
        if self.entry:
            self.entry.destroy()
            self.entry = None
            self.current_item = None
            self.current_column = None

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enhanced Editable Treeview")
    
    tree = EditableTreeview(root, columns=('Name', 'Age', 'Occupation'), show='headings')
    tree.heading('Name', text='Name')
    tree.heading('Age', text='Age')
    tree.heading('Occupation', text='Occupation')
    
    # Insert sample data
    tree.insert('', tk.END, values=('Alice Brown', 28, 'Developer'))
    tree.insert('', tk.END, values=('Charlie Green', 35, 'Analyst'))
    tree.insert('', tk.END, values=('David White', 42, 'Director'))
    
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    root.mainloop()

    #  explain: vcmd = (self.register(self.validate_number), "%P")

    #     This line:

    # is used to set up input validation for Tkinter Entry widgets. Here’s a detailed breakdown:

    # 1. self.register(self.validate_number)
    # self.validate_number is a method you defined to check if the input is a valid number.
    # self.register(...) tells Tkinter to make this Python method callable from Tk’s internal validation system (which expects a Tcl function).
    # The result is a reference to a Tcl wrapper for your Python function.
    # 2. "%P"
    # "%P" is a Tkinter substitution code.
    # When validation is triggered, "%P" will be replaced with the new value of the entry field if the edit is allowed.
    # This means your validate_number function will receive the would-be new value of the entry after the user types or deletes something.

    # 3. The Tuple
    # The tuple (self.register(self.validate_number), "%P") is how Tkinter expects you to pass the validation command and its arguments.
    # When you set validatecommand=vcmd in your Entry, Tkinter will call your function with the new value every time the user types.
    # Usage Example
    # Every time the user types in self.entry_salary, Tkinter calls self.validate_number(new_value) where new_value is what the entry would become.
    # If your function returns True, the change is allowed. If it returns False, the change is rejected.