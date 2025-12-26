import tkinter as tk    
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime


FILE_NAME = "bmi_data.csv"


def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def save_data(name, bmi):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Name", "BMI", "Date"])

        writer.writerow([name, bmi, datetime.now().strftime("%Y-%m-%d")])


def calculate():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        if name == "" or weight <= 0 or height_cm <= 0:
            messagebox.showerror("Error", "Please enter valid inputs")
            return

        height = height_cm / 100
        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)

        result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}"
        )

        save_data(name, bmi)

    except ValueError:
        messagebox.showerror("Error", "Enter numeric values only")


def show_graph():
    if not os.path.isfile(FILE_NAME):
        messagebox.showinfo("Info", "No data available yet")
        return

    dates = []
    bmis = []

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["Date"])
            bmis.append(float(row["BMI"]))

    plt.plot(dates, bmis, marker="o")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Trend Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



root = tk.Tk()
root.title(" BMI Calculator")
root.geometry("350x400")

tk.Label(root, text=" BMI Calculator", font=("Arial", 14)).pack(pady=10)

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (cm)").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Button(root, text="Calculate BMI", command=calculate).pack(pady=10)
tk.Button(root, text="View BMI Graph", command=show_graph).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
