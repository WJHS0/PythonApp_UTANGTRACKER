import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

#init
debts = []
next_id = 1
DATA_FILE = "debts_data.json"

#save data function
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"debts": debts, "next_id": next_id}, f, indent=4)


def load_data(): #load data when program is opened
    global debts, next_id

    if os.path.exists(DATA_FILE):
        data = json.load(open(DATA_FILE))
        debts = data.get("debts", [])
        next_id = data.get("next_id", 1)

    for d in debts:
        d.setdefault("remaining", d.get("amount", 0))
        d.setdefault("status", "Unpaid")
        d.setdefault("interest", 0)
        d.setdefault("date", "N/A")
def refresh_table(): #refreshes the table meaning it update the table when an action is done        
    for item in tree.get_children():
        tree.delete(item)

    for d in debts:
        if d["remaining"] == 0:
            tag = "paid"
        elif d["remaining"] < d["amount"]:
            tag = "partial"
        else:
            tag = "unpaid"

        tree.insert("", "end", values=(
            d["id"],
            d["lender"],
            d["remaining"],
            d["interest"],
            d["date"],
            d["status"]
        ), tags=(tag,))       

#UI
root = tk.Tk()
root.title("UtangTracker")
root.geometry("1000x720")

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

#live clock function
def live_clock():
    now = datetime.now()
    format = now.strftime("Y%-%m-%d %H:%M:%S")
    label_clock.config(text=format)
    root.after(1000, live_clock)
#live clock updated
def update_clock():
    now = datetime.now()
    formatted = now.strftime("%B %d, %Y | %I:%M:%S %p")
    label_clock.config(text=formatted)
    root.after(1000, update_clock)

#CLOCK
label_clock = tk.Label(root, text="", font=("Arial", 12))
label_clock.pack(pady=5)

# INPUTS
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Lender").grid(row=0, column=0)
entry_lender = tk.Entry(frame_inputs)
entry_lender.grid(row=0, column=1)

tk.Label(frame_inputs, text="Amount").grid(row=1, column=0)
entry_amount = tk.Entry(frame_inputs)
entry_amount.grid(row=1, column=1)

tk.Label(frame_inputs, text="Interest").grid(row=2, column=0)
entry_interest = tk.Entry(frame_inputs)
entry_interest.grid(row=2, column=1)

tk.Label(frame_inputs, text="Date").grid(row=3, column=0)
entry_date = tk.Entry(frame_inputs)
entry_date.grid(row=3, column=1)


#ADD DEBT
def add_debt():
    global next_id
    try:
        debt = {
            "id": next_id,
            "lender": entry_lender.get(),
            "amount": float(entry_amount.get()),
            "remaining": float(entry_amount.get()),
            "interest": float(entry_interest.get()),
            "date": entry_date.get(),
            "status": "Unpaid"
        }

        debts.append(debt)
        next_id += 1

        refresh_table()
        save_data()

        messagebox.showinfo("Success", "Debt added!")

    except:
        messagebox.showerror("Error", "Invalid input")
tk.Button(frame_inputs, text="Add Debt", command=add_debt).grid(row=4, columnspan=2, pady=5) #BUTTON add debt

# TABLE
tree = ttk.Treeview(
    root,
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
frame_pay = tk.Frame(root)
frame_pay.pack(pady=10)

tk.Label(frame_pay, text="Payment").grid(row=0, column=0)
entry_payment = tk.Entry(frame_pay)
entry_payment.grid(row=0, column=1)

#pay debt
def pay_debt():
    try:
        selected = tree.item(tree.focus(), "values")
        if not selected:
            return messagebox.showwarning("Warning", "Select a debt first.")

        debt_id = int(selected[0])
        payment = float(entry_payment.get())

        for d in debts:
            if d["id"] == debt_id:

                if d["status"] == "Paid":
                    return messagebox.showinfo("Info", "Already paid")

                if payment <= 0 or payment > d["remaining"]: #if the input is negative and if the input exceeds the remaining debt
                    return messagebox.showerror("Error", "Invalid payment")

                d["remaining"] -= payment

                if d["remaining"] == 0: #if the remaining debt is zero, the status will be "paid"
                    d["status"] = "Paid"
                else:
                    d["status"] = "Partial"
                refresh_table()
                save_data()
                
                messagebox.showinfo("Success", "Payment recorded")
                return

    except:
        messagebox.showerror("Error", "Invalid input")
tk.Button(frame_pay, text="Pay Selected", command=pay_debt).grid(row=0, column=2) #pAY DEBT

# SEARCH
frame_search = tk.Frame(root)
frame_search.pack(pady=10)

tk.Label(frame_search, text="Search").grid(row=0, column=0)
entry_search = tk.Entry(frame_search)
entry_search.grid(row=0, column=1)



# SEARCH
def search_debt():
    keyword = entry_search.get().lower()

    for item in tree.get_children(): #deletes the current list on the table once the keyword or id is searched
        tree.delete(item)

    for d in debts:
        if keyword == "" or keyword in d["lender"].lower() or keyword == str(d["id"]): #searches for keywords, and id of the lender, converts all values to lowercase 
            if d["remaining"] == 0:
             tag = "paid"
            elif d["remaining"] < d["amount"]:
             tag = "partial"
            else:
             tag = "unpaid" #indicate the color of paid and unpaid
            tree.insert("", "end", values=(
                d["id"],
                d["lender"],
                d["remaining"],
                d["interest"],
                d["date"],
                d["status"]
            ), tags=(tag,))
def clear_search():
    for item in tree.get_children():
        tree.delete(item)
    for d in debts:
        if d["remaining"] == 0:
             tag = "paid"
        elif d["remaining"] < d["amount"]:
             tag = "partial"
        else:
            tag = "unpaid" #indicate the color of paid and unpaid
            tree.insert("", "end", values=(
                d["id"],
                d["lender"],
                d["remaining"],
                d["interest"],
                d["date"],
                d["status"]
            ), tags=(tag,))
refresh_table()

tk.Button(frame_search, text="Search", command=search_debt).grid(row=0, column=2) #search button
tk.Button(frame_search, text="clear", command=clear_search).grid(row=0, column=3) #clear search button

# BUTTONS
frame_extra = tk.Frame(root)
frame_extra.pack(pady=10)

# DELETE DEBT
def delete_debt():
    selected = tree.item(tree.focus(), "values")

    if not selected:
        return messagebox.showwarning("Warning", "Select a debt first.")

    debt_id = int(selected[0])

    if not messagebox.askyesno("Confirm", f"Delete debt ID {debt_id}?"):
        return

    for d in debts:
        if d["id"] == debt_id:
            debts.remove(d)
            break
    refresh_table()
    save_data()
    
    messagebox.showinfo("Success", "Debt deleted")
tk.Button(frame_extra, text="Delete Selected", command=delete_debt).grid(row=0, column=0, padx=5)#Delete debt button

#clear all debts , ID iterations proceeds +=1
def clear_debts():
    if messagebox.askyesno("Confirm", "Delete ALL debts?"):
        debts.clear()
        refresh_table()
        save_data()
tk.Button(frame_extra, text="Clear All", command=clear_debts).grid(row=0, column=1, padx=5)#clear debts button


#reset all the system, ID will be re-initilize to 1
def reset_system():
    global next_id

    if messagebox.askyesno("Confirm", "Reset system?"):
        debts.clear()
        next_id = 1
        refresh_table()
        save_data()
        
tk.Button(frame_extra, text="Reset", command=reset_system).grid(row=0, column=2, padx=5)#reset button

    

# LOAD
load_data()
refresh_table()
update_clock()

# RUN
root.mainloop()