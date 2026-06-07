import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

root = None
tree = None
label_clock = None

entry_lender = None
entry_amount = None
entry_interest = None
entry_date = None

entry_payment = None
entry_search = None

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
#clear all debts , ID iterations proceeds +=1
def clear_debts():
    if messagebox.askyesno("Confirm", "Delete ALL debts?"):
        debts.clear()
        refresh_table()
        save_data()
def reset_system():
    global next_id

    if messagebox.askyesno("Confirm", "Reset system?"):
        debts.clear()
        next_id = 1
        refresh_table()
        save_data()