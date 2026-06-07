import main_functions as f
import tkinter as tk
from tkinter import ttk, messagebox



#UI
f.root = tk.Tk()
f.root.title("UtangTracker")
f.root.geometry("1000x720")

#for color
style = ttk.Style()
style.theme_use("clam") 

# Heading style (grey header)
style.configure(
    "Treeview.Heading",
    background="#d9d9d9",
    foreground="black",
    font=("Arial", 10, "bold")
)


#CLOCK
f.label_clock = tk.Label(f.root, text="", font=("Arial", 12))
f.label_clock.pack(pady=5)

# INPUTS
f.frame_inputs = tk.Frame(f.root)
f.frame_inputs.pack(pady=10)

tk.Label(f.frame_inputs, text="Lender").grid(row=0, column=0)
entry_lender = tk.Entry(f.frame_inputs)
entry_lender.grid(row=0, column=1)

tk.Label(f.frame_inputs, text="Amount").grid(row=1, column=0)
entry_amount = tk.Entry(f.frame_inputs)
entry_amount.grid(row=1, column=1)

tk.Label(f.frame_inputs, text="Interest").grid(row=2, column=0)
entry_interest = tk.Entry(f.frame_inputs)
entry_interest.grid(row=2, column=1)

tk.Label(f.frame_inputs, text="Date").grid(row=3, column=0)
entry_date = tk.Entry(f.frame_inputs)
entry_date.grid(row=3, column=1)


#ADD DEBT
tk.Button(f.frame_inputs, text="Add Debt", command=f.add_debt).grid(row=4, columnspan=2, pady=5) #BUTTON add debt

# TABLE
tree = ttk.Treeview(
    f.root,
    columns=("ID", "Lender", "Remaining", "Interest", "Date", "Status"),
    show="headings"
)
tree.tag_configure("paid", background="#c8f7c5")    
tree.tag_configure("unpaid", background="#f5b7b1")
tree.tag_configure("partial", background="#fff3a0")  

for c in ("ID", "Lender", "Remaining", "Interest", "Date", "Status"):
    tree.heading(c, text=c)
    tree.column(c, width=150, anchor="center")
    
tree.pack(fill="both", expand="true")

# PAYMENT
f.frame_pay = tk.Frame(f.root)
f.frame_pay.pack(pady=10)

tk.Label(f.frame_pay, text="Payment").grid(row=0, column=0)
entry_payment = tk.Entry(f.frame_pay)
entry_payment.grid(row=0, column=1)


tk.Button(f.frame_pay, text="Pay Selected", command=f.pay_debt).grid(row=0, column=2) #pAY DEBT

# SEARCH
f.frame_search = tk.Frame(f.root)
f.frame_search.pack(pady=10)

tk.Label(f.frame_search, text="Search").grid(row=0, column=0)
f.entry_search = tk.Entry(f.frame_search)
f.entry_search.grid(row=0, column=1)


tk.Button(f.frame_search, text="Search", command=f.search_debt).grid(row=0, column=2) #search button
tk.Button(f.frame_search, text="clear", command=f.clear_search).grid(row=0, column=3) #clear search button

# BUTTONS
f.frame_extra = tk.Frame(f.root)
f.frame_extra.pack(pady=10)


tk.Button(f.frame_extra, text="Delete Selected", command=f.delete_debt).grid(row=0, column=0, padx=5)#Delete debt button

tk.Button(f.frame_extra, text="Clear All", command=f.clear_debts).grid(row=0, column=1, padx=5)#clear debts button


#reset all the system, ID will be re-initilize to 1
        
tk.Button(f.frame_extra, text="Reset", command=f.reset_system).grid(row=0, column=2, padx=5)#reset button

# LOAD
f.load_data()
f.refresh_table()
f.update_clock()

# RUN
f.root.mainloop()