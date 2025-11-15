# 🌸 Sharma Travelers - Ticket Booking System 🌸
# IDLE Version (With Simple Matplotlib Chart)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import threading
import matplotlib.pyplot as plt
import numpy as np
# ===============================
# 🌸 Data Configuration
# ===============================
sources = ["Delhi", "UP", "Punjab"]

destinations = {
    "Delhi": 1200,
    "Mumbai": 1500,
    "Kolkata": 1000,
    "Bangalore": 1800
}

bookings = []

# ===============================
# 🧾 Helper Functions
# ===============================
def validate_name(name):
    return all(c.isalpha() or c.isspace() for c in name)

def show_all_prices():
    price_text = "💰 Available Destinations & Prices:\n\n"
    for city, price in destinations.items():
        price_text += f"🏙 {city}: ₹{price}\n"
    messagebox.showinfo("📍 Destination Prices", price_text)

def go_to_payment():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    source = source_var.get()
    destination = dest_var.get()

    if not name or not age or destination == "Select Destination" or source == "Select Source":
        messagebox.showwarning("⚠ Warning", "Please fill all details before proceeding.")
        return

    if not validate_name(name):
        messagebox.showerror("❌ Error", "Name can only contain letters.")
        return

    try:
        age_val = int(age)
        if age_val <= 0 or age_val > 110:
            messagebox.showerror("❌ Error", "Age must be between 1 and 110.")
            return
    except ValueError:
        messagebox.showerror("❌ Error", "Age must be a number.")
        return

    show_all_prices()
    price = destinations[destination]
    messagebox.showinfo("💰 Ticket Price", f"Your ticket price to {destination} is ₹{price}")

    ticket_frame.pack_forget()
    payment_frame.pack(fill="both", expand=True)

def show_payment_fields(event=None):
    method = payment_var.get()
    for widget in payment_details_frame.winfo_children():
        widget.destroy()

    if method == "UPI":
        tk.Label(payment_details_frame, text="Enter UPI ID:", bg="#fff0f5", font=("Arial", 11)).pack(pady=5)
        tk.Entry(payment_details_frame, width=35, bg="white").pack(pady=5)
    elif method in ("Credit Card", "Debit Card"):
        tk.Label(payment_details_frame, text="Enter Card Number:", bg="#fff0f5", font=("Arial", 11)).pack(pady=5)
        tk.Entry(payment_details_frame, width=35, bg="white").pack(pady=5)
    elif method == "Net Banking":
        tk.Label(payment_details_frame, text="Enter Account Number:", bg="#fff0f5", font=("Arial", 11)).pack(pady=5)
        tk.Entry(payment_details_frame, width=35, bg="white").pack(pady=5)

def confirm_payment():
    name = entry_name.get().strip()
    age = int(entry_age.get())
    gender = gender_var.get()
    source = source_var.get()
    destination = dest_var.get()
    payment_method = payment_var.get()

    if payment_method == "Select Payment Method":
        messagebox.showwarning("⚠ Warning", "Please select a payment method.")
        return

    if name.lower() == "achintya":
        price = 0
        special_message = "NO CHARGES FOR BOSS 😎"
    else:
        price = destinations[destination]
        special_message = "✨ Have a wonderful journey! ✨"

    booking_id = f"TKT{len(bookings)+1:03d}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    booking = {
        "Booking ID": booking_id,
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Source": source,
        "Destination": destination,
        "Price": price,
        "Payment Method": payment_method,
        "Date": now
    }
    bookings.append(booking)

    messagebox.showinfo("✅ Booking Confirmed",
                        f"🎫 Booking ID: {booking_id}\n"
                        f"Passenger: {name}\n"
                        f"From: {source} ➜ To: {destination}\n"
                        f"💰 Ticket Price: ₹{price}\n\n{special_message}")

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    gender_var.set("")
    source_var.set("Select Source")
    dest_var.set("Select Destination")
    payment_var.set("Select Payment Method")

    payment_frame.pack_forget()
    report_frame.pack(fill="both", expand=True)
    update_report_table()

def update_report_table():
    for row in report_table.get_children():
        report_table.delete(row)
    for booking in bookings:
        report_table.insert("", tk.END, values=list(booking.values()))

        

def export_to_csv():
    if not bookings:
        messagebox.showwarning("⚠ Warning", "No bookings to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save Report As"
    )

    if file_path:
        booking = bookings[0]
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = list(booking.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for b in bookings:
                filtered = {k: b.get(k, "") for k in fieldnames}
                writer.writerow(filtered)
        messagebox.showinfo("💾 Exported", "Report exported successfully!")

# ✅ Simple Matplotlib Chart Function
def show_sales_chart():
    if not bookings:
        messagebox.showwarning("⚠ Warning", "No data to display chart.")
        return

    # Extract booking info
    destinations_list = [b["Destination"] for b in bookings]
    prices = [b["Price"] for b in bookings]

    # Calculate total sales per destination
    unique_dests = sorted(set(destinations_list))
    sales = [np.sum([p for d, p in zip(destinations_list, prices) if d == city]) for city in unique_dests]

    # 🎨 Fancy color themes
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_dests)))

    # 🌌 Black background
    plt.style.use("dark_background")

    # Create figure with 2 charts (side by side)
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("🌸 Sharma Travelers - Sales Analytics 🌸", fontsize=16, fontweight="bold", color="#ff80ab")

    # === BAR CHART ===
    bars = axs[0].bar(unique_dests, sales, color=colors, edgecolor='white', linewidth=1.5)
    axs[0].set_title("💰 Total Revenue by Destination", color="white", fontsize=12)
    axs[0].set_xlabel("Destination", color="white", fontsize=11)
    axs[0].set_ylabel("Revenue (₹)", color="white", fontsize=11)
    axs[0].grid(axis='y', linestyle='--', alpha=0.4, color="gray")

    for bar in bars:
        yval = bar.get_height()
        axs[0].text(bar.get_x() + bar.get_width()/2, yval + 30, f"₹{int(yval)}",
                    ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')

    # === PIE CHART ===
    axs[1].pie(sales, labels=unique_dests, autopct='%1.1f%%', startangle=90,
               colors=colors, textprops={'color': "white", 'fontsize': 10})
    axs[1].set_title("📊 Revenue Share by Destination", color="white", fontsize=12)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # === FUTURE GROWTH PREDICTION ===
    future_growth_chart(unique_dests, sales)


def future_growth_chart(unique_dests, sales):
    # 📈 Simple growth model: assume 10% yearly increase
    years = np.arange(2025, 2031)
    plt.style.use("dark_background")
    plt.figure(figsize=(8, 5))

    for i, city in enumerate(unique_dests):
        growth = [sales[i] * (1.1 ** (year - 2025)) for year in years]
        plt.plot(years, growth, marker='o', linewidth=2,
                 color=plt.cm.rainbow(i / len(unique_dests)),
                 label=city)

    plt.title("🚀 Future Revenue Growth Prediction (2025–2030)", fontsize=14, color="#ff80ab", fontweight="bold")
    plt.xlabel("Year", color="white", fontsize=11)
    plt.ylabel("Projected Revenue (₹)", color="white", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.4, color="gray")
    plt.legend(facecolor='black', edgecolor='white', labelcolor='white')
    plt.tight_layout()
    plt.show()


def go_to_home():
    report_frame.pack_forget()
    ticket_frame.pack(fill="both", expand=True)

# ===============================
# 🖥 GUI Setup
# ===============================
def run_gui():
    global root, entry_name, entry_age, gender_var, source_var, dest_var
    global ticket_frame, payment_frame, report_frame, payment_var, payment_details_frame, report_table

    root = tk.Tk()
    root.title("🌸 Sharma Travelers - Ticket Booking System 🌸")
    root.geometry("850x700")
    root.configure(bg="#ffe6f2")

    header = tk.Label(root, text="🌸 Sharma Travelers 🌸", font=("Verdana", 20, "bold"),
                      fg="white", bg="#ff4081", pady=10)
    header.pack(fill="x")

    sub_header = tk.Label(root, text="✨ Your Journey, Our Promise ✨",
                          font=("Comic Sans MS", 12, "italic"),
                          fg="#3f3d56", bg="#ffe6f2")
    sub_header.pack()

    # 🎫 Ticket Frame
    ticket_frame = tk.Frame(root, bg="#ffe6f2")
    ticket_frame.pack(fill="both", expand=True)

    tk.Label(ticket_frame, text="🎫 Passenger Details", bg="#ffe6f2",
             font=("Arial", 14, "bold"), fg="#c2185b").pack(pady=10)

    form = tk.Frame(ticket_frame, bg="#ffe6f2")
    form.pack(pady=10)

    tk.Label(form, text="👤 Name:", bg="#ffe6f2").grid(row=0, column=0, sticky="w", pady=5)
    entry_name = tk.Entry(form, width=35, bg="#fff0f5")
    entry_name.grid(row=0, column=1, pady=5)

    tk.Label(form, text="🎂 Age:", bg="#ffe6f2").grid(row=1, column=0, sticky="w", pady=5)
    entry_age = tk.Entry(form, width=35, bg="#fff0f5")
    entry_age.grid(row=1, column=1, pady=5)

    tk.Label(form, text="🚻 Gender:", bg="#ffe6f2").grid(row=2, column=0, sticky="w", pady=5)
    gender_var = tk.StringVar(value="")
    ttk.Combobox(form, textvariable=gender_var, values=["M", "F", "O"], width=32, state="readonly").grid(row=2, column=1, pady=5)

    tk.Label(form, text="🏙 Source:", bg="#ffe6f2").grid(row=3, column=0, sticky="w", pady=5)
    source_var = tk.StringVar(value="Select Source")
    ttk.Combobox(form, textvariable=source_var, values=sources, width=32, state="readonly").grid(row=3, column=1, pady=5)

    tk.Label(form, text="🗺 Destination:", bg="#ffe6f2").grid(row=4, column=0, sticky="w", pady=5)
    dest_var = tk.StringVar(value="Select Destination")
    ttk.Combobox(form, textvariable=dest_var, values=list(destinations.keys()), width=32, state="readonly").grid(row=4, column=1, pady=5)

    tk.Button(ticket_frame, text="💳 Proceed to Payment", bg="#d81b60", fg="white",
              font=("Arial", 12, "bold"), command=go_to_payment).pack(pady=15)


    

    # 💳 Payment Frame
    payment_frame = tk.Frame(root, bg="#fff0f5")
    tk.Label(payment_frame, text="💳 Payment Processing", bg="#fff0f5",
             font=("Arial", 14, "bold"), fg="#ad1457").pack(pady=15)

    tk.Label(payment_frame, text="Select Payment Method:", bg="#fff0f5", font=("Arial", 11)).pack()
    payment_var = tk.StringVar(value="Select Payment Method")
    payment_box = ttk.Combobox(payment_frame, textvariable=payment_var,
                               values=["UPI", "Credit Card", "Debit Card", "Net Banking"],
                               width=40, state="readonly")
    payment_box.bind("<<ComboboxSelected>>", show_payment_fields)
    payment_box.pack(pady=10)

    payment_details_frame = tk.Frame(payment_frame, bg="#fff0f5")
    payment_details_frame.pack(pady=10)

    tk.Button(payment_frame, text="✅ Confirm Payment", bg="#ff4081", fg="white",
              font=("Arial", 12, "bold"), command=confirm_payment).pack(pady=20)

    # 📊 Report Frame
    report_frame = tk.Frame(root, bg="#ffe6f2")
    tk.Label(report_frame, text="📊 Booking Reports & Management",
             font=("Arial", 14, "bold"), bg="#ffe6f2", fg="#c2185b").pack(pady=15)

    cols = ["Booking ID", "Name", "Age", "Gender", "Source", "Destination", "Price", "Payment Method", "Date"]
    report_table = ttk.Treeview(report_frame, columns=cols, show="headings", height=12)
    for col in cols:
        report_table.heading(col, text=col)
        report_table.column(col, width=90, anchor="center")
    report_table.pack(padx=15, pady=10, fill="both", expand=True)






    

    btn_frame = tk.Frame(report_frame, bg="#ffe6f2")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="💾 Export Report", bg="#4caf50", fg="white",
              font=("Arial", 11, "bold"), command=export_to_csv).pack(side="left", padx=10)
    tk.Button(btn_frame, text="📊 Show Chart", bg="#ff9800", fg="white",
              font=("Arial", 11, "bold"), command=show_sales_chart).pack(side="left", padx=10)
    tk.Button(btn_frame, text="🏠 New Booking", bg="#0078d4", fg="white",
              font=("Arial", 11, "bold"), command=go_to_home).pack(side="left", padx=10)

    root.mainloop()

# ✅ Launch App
threading.Thread(target=run_gui).start()
