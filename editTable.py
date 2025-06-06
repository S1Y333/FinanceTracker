import tkinter as tk
from tkinter import ttk

# use function to edit table entries

class EditableTreeview(ttk.Treeview):
    def __init__(self, master,editable_columns=None, on_cell_edit=None, **kwargs):
        super().__init__(master, **kwargs)
        self.editable_columns = editable_columns or self['columns']
        self.on_cell_edit = on_cell_edit
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
        
         # Convert "#2" → 1 → 'Name'
        col_index = int(column[1:]) - 1
        col_name = self['columns'][col_index]
    
        # Skip non-editable columns
        if col_name not in self.editable_columns:
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
            # Call the callback with item id, column, and new value
            if self.on_cell_edit:
                self.on_cell_edit(self.current_item, self.current_column, new_value)
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
    
    
    