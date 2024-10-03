import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import json

history_file = "water_history.json"


def save_history():
    with open(history_file, "w") as f:
        json.dump(water_history, f)


def load_history():
    try:
        with open(history_file, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


root = tk.Tk()
root.title("DrinkWater")
root.geometry("965x1080")

canvas = tk.Canvas(root, bg="white", width=200, height=200)
canvas.pack(fill=tk.BOTH, expand=True)

canvas.create_rectangle(10, 10, 955, 1000, outline="black")
canvas.create_rectangle(11, 11, 955, 1000, fill="#C6DDFF", outline="")
canvas.create_rectangle(11, 11, 955, 300, fill="#BCD1FF", outline="")

canvas.create_line(11, 301, 955, 301, width=5, fill="white", dash=50)
canvas.create_line(301, 301, 301, 1000, width=5, fill="white", dash=50)
canvas.create_line(11, 601, 955, 601, width=5, fill="white", dash=50)

image1 = Image.open("Logo1.png")
photo1 = ImageTk.PhotoImage(image1)
image2 = Image.open("Logo2.png")
photo2 = ImageTk.PhotoImage(image2)

canvas.create_image(450, 0, anchor=tk.NW, image=photo1)
canvas.create_image(-30, 8, anchor=tk.NW, image=photo2)

water_history = load_history()
current_drunk = 0
goal = 0


def create_date_dropdowns(parent, start_year, end_year):
    global year_cb, month_cb, day_cb
    year_cb = ttk.Combobox(parent, values=list(range(start_year, end_year+1)), state="readonly", width=5)
    year_cb.set(datetime.now().year)
    year_cb.grid(row=0, column=0)

    month_cb = ttk.Combobox(parent, values=list(range(1, 13)), state="readonly", width=3)
    month_cb.set(datetime.now().month)
    month_cb.grid(row=0, column=1)

    day_cb = ttk.Combobox(parent, values=list(range(1, 32)), state="readonly", width=3)
    day_cb.set(datetime.now().day)
    day_cb.grid(row=0, column=2)


def get_selected_date():
    try:
        selected_date = f"{day_cb.get()}-{month_cb.get()}-{year_cb.get()}"
        datetime.strptime(selected_date, "%d-%m-%Y")
        date_label.config(text=f"Date: {selected_date}")
    except ValueError:
        tk.messagebox.showerror("Invalid date", "Please select a valid date.")


def add_to_history():
    global goal, current_drunk
    selected_date = f"{day_cb.get()}-{month_cb.get()}-{year_cb.get()}"
    purpose = num_entry.get()

    if purpose:
        goal = float(purpose)
        current_drunk = 0
        history_entry = f"✖ {selected_date}: {purpose} L"
        water_history.append(history_entry)
        update_history_display()
        update_process()
        num_entry.delete(0, tk.END)
    else:
        tk.messagebox.showerror("Error", "Please enter a purpose.")


def update_history_display():
    history_text.delete(1.0, tk.END)
    history_text.insert(tk.END, "\n".join(water_history))


def update_process():
    remains = max(0, goal - current_drunk / 1000)
    process_label.config(text=f"Drunk: {current_drunk / 1000:.2f} L\nRemains: {remains:.2f} L")

    if current_drunk / 1000 >= goal:
        mark_as_completed(len(water_history) - 1)


def mark_as_completed(index):
    if index < len(water_history):
        water_history[index] = water_history[index].replace("✖", "✔", 1)
        update_history_display()


def add_ml():
    global current_drunk
    try:
        ml = float(ml_entry.get())
        current_drunk += ml
        update_process()
        ml_entry.delete(0, tk.END)
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid amount of ml.")


def reset_history():
    global water_history, current_drunk, goal
    water_history = []
    current_drunk = 0
    goal = 0
    update_history_display()
    process_label.config(text="Drunk: 0.00 L\nRemains: 0.00 L")
    tk.messagebox.showinfo("History Reset", "History has been reset.")


frame = tk.Frame(root, bg='#C6DDFF')
frame.place(x=80, y=350)
create_date_dropdowns(frame, 2000, 2030)

date_label = tk.Label(root, text="Date: ", bg='#C6DDFF', fg='#8293FF', anchor='w', font=("Arial", 30))
date_label.place(x=330, y=350, width=350, height=70)

purpose_label = tk.Label(root, text="Purpose: ", bg='#C6DDFF', fg='#8293FF', anchor='w', font=("Arial", 30))
purpose_label.place(x=650, y=350, width=170, height=70)

l_label = tk.Label(root, text="L", bg='#C6DDFF', fg='#8293FF', anchor='w', font=("Arial", 30))
l_label.place(x=900, y=350, width=30, height=70)

num_entry = tk.Entry(root, font=("Arial", 30), width=3, bg='white', fg='#8293FF')
num_entry.place(x=830, y=359)

btn = tk.Button(root, text="Select a date", font=("Arial", 15), command=get_selected_date, bg="#8293FF", fg="white", width=15, height=1)
btn.place(x=60, y=550)

btn_add = tk.Button(root, text="+ Add purpose", command=add_to_history, bg="#8293FF", fg="white", width=30, height=1, font=("Arial", 25))
btn_add.place(x=350, y=500)

history_label = tk.Label(root, text="History:", bg='#C6DDFF', fg='#8293FF', anchor='w', font=("Arial", 30))
history_label.place(x=15, y=630, width=140, height=40)

btn_reset = tk.Button(root, text="Reset", command=reset_history, bg="#FF5C5C", fg="white", width=7, height=1, font=("Arial", 20))
btn_reset.place(x=170, y=615)

process_label = tk.Label(root, text="Drunk: 0.00 L\nRemains: 0.00 L", bg='#C6DDFF', fg='#8293FF', font=("Arial", 30))
process_label.place(x=400, y=630, width=300, height=100)

ml_entry = tk.Entry(root, font=("Arial", 30), width=5, bg='white', fg='#8293FF')
ml_entry.place(x=400, y=750)

ml_label = tk.Label(root, text="ml", bg='#C6DDFF', fg='#8293FF', font=("Arial", 30))
ml_label.place(x=550, y=750)

btn_done = tk.Button(root, text="Done", command=add_ml, bg="#4CAF50", fg="white", width=10, height=1, font=("Arial", 20))
btn_done.place(x=650, y=750)

history_text = tk.Text(root, bg='#C6DDFF', fg='#8293FF', font=("Arial", 20), width=17, height=10)
history_text.place(x=15, y=670)

update_history_display()

root.protocol("WM_DELETE_WINDOW", lambda: [save_history(), root.destroy()])
root.mainloop()
