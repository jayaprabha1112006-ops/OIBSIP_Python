import tkinter as tk
from tkinter import messagebox
import random
import string


def generate_password():
    try:
        length = int(length_entry.get())

        if length < 8:
            messagebox.showerror("Error", "Password length must be at least 8")
            return

        characters = ""

        if letters_var.get():
            characters += string.ascii_letters
        if numbers_var.get():
            characters += string.digits
        if symbols_var.get():
            characters += string.punctuation

        exclude_chars = exclude_entry.get()
        for ch in exclude_chars:
            characters = characters.replace(ch, "")

        if characters == "":
            messagebox.showerror("Error", "Select at least one character type")
            return

        password = "".join(random.choice(characters) for _ in range(length))

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")


def copy_to_clipboard():
    pwd = password_entry.get()
    if pwd == "":
        messagebox.showinfo("Info", "No password to copy")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard")


root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x420")

tk.Label(root, text="Advanced Password Generator", font=("Arial", 14)).pack(pady=10)

tk.Label(root, text="Password Length").pack()
length_entry = tk.Entry(root)
length_entry.pack()

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=letters_var).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).pack(anchor="w", padx=40)

tk.Label(root, text="Exclude Characters (optional)").pack(pady=5)
exclude_entry = tk.Entry(root)
exclude_entry.pack()

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

password_entry = tk.Entry(root, width=30, font=("Arial", 12))
password_entry.pack(pady=5)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)

root.mainloop()
