import tkinter as tk
from tkinter import ttk, messagebox


class Item:
    def __init__(self, item_name, price, buyer_list):
        self.item_name = item_name
        self.price = price
        self.buyer_list = buyer_list

class Buyer:
    def __init__(self, buyer_name):
        self.buyer_name = buyer_name
        self.total_payment_due = 0

class ReceiptItem(Item):
    def __str__(self):
        return f"{self.item_name} - ${self.price:.2f}"



class ReceiptSplitter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Receipt Splitter 9004")
        self.geometry("600x400")

        self.buyers = {}
        self.items = {}

        self.create_widgets()

        self.last_selected_item = None

        self.prev_index = -1

        self.summary_text.grid(column=0, row=2, padx=10, pady=(10, 0), columnspan=3)
                    
        

    def assign_item_to_buyer(self, event=None):
        selected_buyer = self.buyers_listbox.get(self.buyers_listbox.curselection())
        self.update_buyers_list(selected_buyer)
        self.assignment_window.destroy()

    def focus_next_widget(self, event, next_widget):
        next_widget.focus_set()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        self.buyer_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.buyer_tab, text="Buyers")

        self.item_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.item_tab, text="Items")

        self.summary_frame = tk.Frame(self.master)
        self.summary_frame.pack(pady=10)
        
        self.summary_text = tk.Text(self.summary_frame, width=80, height=25, wrap=tk.WORD)

        self.summary_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.summary_tab, text="Summary")

        self.create_buyer_frame()
        self.create_item_frame()
        self.create_summary_frame()

        self.summary_text = tk.Text(self.summary_frame, width=80, height=25, wrap=tk.WORD)  # Move this line here
        self.summary_text.grid(column=0, row=2, padx=10, pady=(10, 0), columnspan=3)

        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)


    def create_buyer_frame(self):
        self.buyer_label = ttk.Label(self.buyer_tab, text="Buyer Name:")
        self.buyer_label.grid(column=0, row=0, padx=10, pady=(10, 0))

        self.buyer_name_entry = ttk.Entry(self.buyer_tab)
        self.buyer_name_entry.grid(column=1, row=0, padx=10, pady=(10, 0))

        self.add_buyer_button = ttk.Button(self.buyer_tab, text="Add Buyer", command=self.add_buyer)
        self.add_buyer_button.grid(column=2, row=0, padx=10, pady=(10, 0))

        self.buyer_listbox = tk.Listbox(self.buyer_tab)
        self.buyer_listbox.grid(column=0, row=1, padx=10, pady=(10, 0), columnspan=3)

        for buyer in self.buyers:
            self.buyers_listbox.insert(tk.END, buyer)
        
        self.buyer_name_entry.bind("<Return>", lambda event: self.add_buyer())

        self.buyer_delete_button = ttk.Button(self.buyer_tab, text="Delete Buyer", command=self.delete_buyer)
        self.buyer_delete_button.grid(column=3, row=0, padx=10, pady=(10, 0))

        self.buyer_listbox.bind("<BackSpace>", lambda event: self.delete_buyer())



    def create_item_frame(self):
        # Create item related widgets here
        self.item_name_label = ttk.Label(self.item_tab, text="Item Name:")
        self.item_name_label.grid(column=0, row=2, padx=10, pady=(10, 0))

        self.item_name_entry = ttk.Entry(self.item_tab)
        self.item_name_entry.grid(column=1, row=2, padx=10, pady=(10, 0))

        self.item_price_label = ttk.Label(self.item_tab, text="Item Price:")
        self.item_price_label.grid(column=2, row=2, padx=10, pady=(10, 0))

        self.item_price_entry = ttk.Entry(self.item_tab)
        self.item_price_entry.grid(column=3, row=2, padx=10, pady=(10, 0))

        self.add_item_button = ttk.Button(self.item_tab, text="Add Item", command=self.add_item)
        self.add_item_button.grid(column=4, row=2, padx=10, pady=(10, 0))

        self.item_name_entry.bind("<Return>", lambda event: self.add_item())
        self.item_price_entry.bind("<Return>", lambda event: self.add_item())

        self.item_name_entry.bind("<Right>", lambda event: self.focus_next_widget(event, self.item_price_entry))
        self.item_price_entry.bind("<Left>", lambda event: self.focus_next_widget(event, self.item_name_entry))

        self.item_listbox = tk.Listbox(self.item_tab, selectmode=tk.MULTIPLE)
        self.item_listbox.grid(column=0, row=3, padx=10, pady=(10, 0), columnspan=6)

        self.item_delete_button = ttk.Button(self.item_tab, text="Delete Item", command=self.delete_item)
        self.item_delete_button.grid(column=6, row=2, padx=10, pady=(10, 0))

        self.item_listbox.bind("<BackSpace>", lambda event: self.delete_item())
        self.item_listbox.bind("<Button-1>", lambda event: self.select_multiple_items(event, self.item_listbox))

        self.item_listbox.bind('<Shift-Button-1>', self.shift_click)

        self.assign_button = ttk.Button(self.item_tab, text="Assign Items to Buyers", command=self.assign_selected_items)
        self.assign_button.grid(column=0, row=4, padx=10, pady=(10, 0), columnspan=7)



    def create_summary_frame(self):
        self.tax_label = ttk.Label(self.summary_tab, text="Tax:")
        self.tax_label.grid(column=0, row=0, padx=10, pady=(10, 0))

        self.tax_entry = ttk.Entry(self.summary_tab)
        self.tax_entry.grid(column=1, row=0, padx=10, pady=(10, 0))
        self.tax_entry.insert(0, "0")  # Set default tax value to 0

        self.summary_label = ttk.Label(self.summary_tab, text="Summary:")
        self.summary_label.grid(column=0, row=1, padx=10, pady=(10, 0))

        self.summary_text = tk.Text(self.summary_tab, wrap=tk.WORD, width=80, height=25)
        self.summary_text.grid(column=0, row=2, padx=10, pady=(10, 0), columnspan=3)

        self.finish_button = ttk.Button(self.summary_tab, text="Finish", command=self.finish_summary)
        self.finish_button.grid(column=1, row=3, padx=10, pady=(10, 0))

        self.tax_entry.bind("<Return>", lambda event: self.finish_summary())
        self.finish_button.bind("<Return>", lambda event: self.finish_summary())

    def finish_summary(self):
        self.calculate_totals()
        self.tax_entry.delete(0, tk.END)

        
    
    def create_assignment_window(self):
        self.assignment_window = tk.Toplevel(self)
        self.assignment_window.title("Assign Buyer")

        buyers_listbox_frame = tk.Frame(self.assignment_window)
        buyers_listbox_frame.pack(side=tk.TOP, padx=5, pady=5)

        scrollbar = tk.Scrollbar(buyers_listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.buyers_listbox = tk.Listbox(buyers_listbox_frame, yscrollcommand=scrollbar.set)
        self.buyers_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.buyers_listbox.yview)

        for buyer in self.buyers:
            self.buyers_listbox.insert(tk.END, buyer)

        assign_button = tk.Button(self.assignment_window, text="Assign", command=self.assign_item_to_buyer)
        assign_button.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.buyers_listbox.bind('<Return>', self.assign_item_to_buyer)




    def add_buyer(self, event=None):
        buyer_name = self.buyer_name_entry.get().strip()
        if buyer_name:
            self.buyer_listbox.insert(tk.END, buyer_name)
            self.buyer_name_entry.delete(0, tk.END)

    def delete_buyer(self, event=None):
        selected_indices = self.buyer_listbox.curselection()
        for index in reversed(selected_indices):
            self.buyer_listbox.delete(index)

    def add_item(self):
        item_name = self.item_name_entry.get().strip()
        if not item_name:
            messagebox.showerror("Error", "Please enter an item name.")
            return

        try:
            price = float(self.item_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price.")
            return

        self.items[item_name] = {"price": price, "buyer": []}

        self.item_listbox.insert(tk.END, f"{item_name} - ${price:.2f}")

        self.item_name_entry.delete(0, tk.END)
        self.item_price_entry.delete(0, tk.END)

        self.item_name_entry.focus_set()

        

    def delete_item(self, event=None):
        selected_indices = self.item_listbox.curselection()
        for index in reversed(selected_indices):
            self.item_listbox.delete(index)

            
    def assign_buyers_to_item(self):
        selected_items = self.item_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Error", "Please select an item.")
            return

        item_names = [self.item_listbox.get(i).split(" ($")[0] for i in selected_items]

        buyers_window = tk.Toplevel(self)
        buyers_window.title("Select Buyers")

        buyers_listbox = tk.Listbox(buyers_window, selectmode=tk.MULTIPLE)
        for buyer in self.buyers:
            buyers_listbox.insert(tk.END, buyer)
        buyers_listbox.pack(padx=10, pady=10)

        def update_buyers_list():
            selected_buyers = [buyers_listbox.get(i) for i in buyers_listbox.curselection()]
            for item_name in item_names:
                item = ReceiptItem(item_name, self.items[item_name]['price'], self.items[item_name]['buyer'])
                item.buyer_list = selected_buyers
            buyers_window.destroy()

        assign_button = ttk.Button(buyers_window, text="Assign", command=update_buyers_list)
        assign_button.pack(padx=10, pady=(0, 10))

        assign_button.bind("<Return>", lambda event: update_buyers_list())


    def assign_selected_items(self):
        selected_items = self.item_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Error", "Please select an item.")
            return

        item_names = [self.item_listbox.get(i).split(" - $")[0] for i in selected_items]

        buyers_window = tk.Toplevel(self)
        buyers_window.title("Select Buyers")

        buyers_listbox = tk.Listbox(buyers_window, selectmode=tk.MULTIPLE)
        for buyer_name in self.buyer_listbox.get(0, tk.END):
            buyers_listbox.insert(tk.END, buyer_name)
        buyers_listbox.pack(padx=10, pady=10)

        def update_buyers_list():
            selected_buyers = [buyers_listbox.get(i) for i in buyers_listbox.curselection()]
            for item_name in item_names:
                if item_name in self.items:
                    item = self.items[item_name]
                    item['buyer'] = selected_buyers
                else:
                    print(f"Item '{item_name}' not found in the items dictionary.")

            buyers_window.destroy()

        assign_button = ttk.Button(buyers_window, text="Assign", command=update_buyers_list)
        assign_button.pack(padx=10, pady=(0, 10))

        buyers_listbox.bind("<Return>", lambda event: update_buyers_list())


            
    def on_tab_changed(self, event):
        self.calculate_totals()

    def clear_output(self):
        self.summary_listbox.delete(0, tk.END)

    def reset(self):
        self.buyers = {}
        self.items = {}
        self.buyer_listbox.delete(0, tk.END)
        self.item_listbox.delete(0, tk.END)
        self.summary_listbox.delete(0, tk.END)


    def shift_click(self, event):
        if event.state == 1 and self.prev_index != -1:
            current_index = self.item_listbox.nearest(event.y)
            for index in range(min(self.prev_index, current_index), max(self.prev_index, current_index) + 1):
                self.item_listbox.selection_set(index)
        else:
            self.prev_index = self.item_listbox.nearest(event.y)
            

    #doesnt really work wtf
    def select_multiple_items(self, event, listbox):
        widget = event.widget
        if event.state & 0x0001:  # Shift key pressed
            index = widget.nearest(event.y)
            if self.last_selected_item is not None:
                widget.selection_clear(0, tk.END)
                start, end = sorted((index, self.last_selected_item))
                for i in range(start, end + 1):
                    widget.selection_set(i)
            else:
                widget.selection_clear(0, tk.END)
                widget.selection_set(index)
                self.last_selected_item = index
        else:
            selection = widget.curselection()
            if selection:
                index = selection[0]
                if index == self.last_selected_item:
                    widget.selection_clear(index)
                    self.last_selected_item = None
                else:
                    widget.selection_clear(0, tk.END)
                    widget.selection_set(index)
                    self.last_selected_item = index





    def calculate_totals(self):
        try:
            tax = float(self.tax_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid tax amount.")
            return

        buyer_totals = {}
        total_cost = sum(item["price"] for item in self.items.values())

        for item_name, item in self.items.items():
            for buyer in item["buyer"]:
                if buyer not in buyer_totals:
                    buyer_totals[buyer] = 0
                buyer_totals[buyer] += item["price"] / len(item["buyer"])

        if total_cost > 0:
            for buyer_name, total_due in buyer_totals.items():
                tax_per_buyer = tax * (total_due / total_cost)
                amount_due = total_due + tax_per_buyer
                buyer_totals[buyer_name] = amount_due

        self.summary_text.delete(1.0, tk.END)
        for buyer, amount_due in buyer_totals.items():
            self.summary_text.insert(tk.END, f"{buyer}: ${amount_due:.2f}\n")


        # Add reset button
        self.reset_button = ttk.Button(self.summary_tab, text="Reset", command=self.reset_summary)
        self.reset_button.grid(column=2, row=3, padx=10, pady=(10, 0))

        self.reset_button.bind("<Return>", lambda event: self.reset_summary())

    def reset_summary(self):
        self.summary_text.delete(1.0, tk.END)


        
def main():
    root = tk.Tk()
    app = SplitBillApp(root)
    root.mainloop()


if __name__ == "__main__":
    app = ReceiptSplitter()
    app.mainloop()
