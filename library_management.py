import tkinter as tk
from tkinter import messagebox, ttk

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")

        self.library_items = []

        # Create GUI Elements
        self.create_gui()

    def create_gui(self):
        # Tabs for different operations
        tab_control = ttk.Notebook(self.root)
        self.add_tab = ttk.Frame(tab_control)
        self.manage_tab = ttk.Frame(tab_control)
        self.search_tab = ttk.Frame(tab_control)

        tab_control.add(self.add_tab, text="Add Items")
        tab_control.add(self.manage_tab, text="Manage Items")
        tab_control.add(self.search_tab, text="Search Items")
        tab_control.pack(expand=1, fill="both")

        # Add Items Tab
        self.create_add_tab()
        
        # Manage Items Tab
        self.create_manage_tab()

        # Search Items Tab
        self.create_search_tab()

    def create_add_tab(self):
        tk.Label(self.add_tab, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        self.title_entry = tk.Entry(self.add_tab)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_tab, text="Author:").grid(row=1, column=0, padx=10, pady=5)
        self.author_entry = tk.Entry(self.add_tab)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_tab, text="Category:").grid(row=2, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(self.add_tab)
        self.category_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_tab, text="Type:").grid(row=3, column=0, padx=10, pady=5)
        self.type_var = tk.StringVar(value="Book")
        tk.OptionMenu(self.add_tab, self.type_var, "Book", "Magazine", "DVD").grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.add_tab, text="Add Item", command=self.add_item).grid(row=4, column=0, columnspan=2, pady=10)

    def create_manage_tab(self):
        self.items_listbox = tk.Listbox(self.manage_tab, width=80, height=15)
        self.items_listbox.pack(pady=10)

        tk.Button(self.manage_tab, text="Check Out", command=self.check_out_item).pack(pady=5)
        tk.Button(self.manage_tab, text="Return Item", command=self.return_item).pack(pady=5)

    def create_search_tab(self):
        tk.Label(self.search_tab, text="Search By Title:").grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.search_tab)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.search_tab, text="Search", command=self.search_items).grid(row=0, column=2, padx=10, pady=5)

        self.search_results = tk.Listbox(self.search_tab, width=80, height=15)
        self.search_results.grid(row=1, column=0, columnspan=3, pady=10)

    def add_item(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        category = self.category_entry.get()
        item_type = self.type_var.get()

        if not title or not author or not category:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        item = {
            "title": title,
            "author": author,
            "category": category,
            "type": item_type,
            "checked_out": False
        }
        self.library_items.append(item)
        messagebox.showinfo("Success", f"{item_type} '{title}' added successfully.")
        self.clear_add_tab_fields()
        self.refresh_items_list()

    def clear_add_tab_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    def refresh_items_list(self):
        self.items_listbox.delete(0, tk.END)
        for idx, item in enumerate(self.library_items):
            status = "Checked Out" if item["checked_out"] else "Available"
            self.items_listbox.insert(tk.END, f"{idx+1}. {item['title']} by {item['author']} [{item['type']}] - {status}")

    def check_out_item(self):
        selected = self.items_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No item selected.")
            return

        idx = selected[0]
        if self.library_items[idx]["checked_out"]:
            messagebox.showerror("Error", "Item is already checked out.")
        else:
            self.library_items[idx]["checked_out"] = True
            messagebox.showinfo("Success", f"Checked out '{self.library_items[idx]['title']}'.")
        self.refresh_items_list()

    def return_item(self):
        selected = self.items_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No item selected.")
            return

        idx = selected[0]
        if not self.library_items[idx]["checked_out"]:
            messagebox.showerror("Error", "Item is not checked out.")
        else:
            self.library_items[idx]["checked_out"] = False
            messagebox.showinfo("Success", f"Returned '{self.library_items[idx]['title']}'.")
        self.refresh_items_list()

    def search_items(self):
        query = self.search_entry.get().lower()
        self.search_results.delete(0, tk.END)
        for idx, item in enumerate(self.library_items):
            if query in item["title"].lower():
                status = "Checked Out" if item["checked_out"] else "Available"
                self.search_results.insert(tk.END, f"{idx+1}. {item['title']} by {item['author']} [{item['type']}] - {status}")

# Create the Tkinter root window
root = tk.Tk()
app = LibrarySystem(root)
root.mainloop()
