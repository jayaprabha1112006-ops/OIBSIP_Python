import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import os


API_KEY = "b4908298297b27d27bc5eacade9a33b3"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

ICON_FOLDER = "icons"
ICON_PATH = os.path.join(ICON_FOLDER, "weather.png")
os.makedirs(ICON_FOLDER, exist_ok=True)


def get_weather():
    city = city_entry.get().strip()
    unit = unit_var.get()

    if city == "" or city.lower() == "enter city name":
        messagebox.showerror("Error", "Please enter a valid city name")
        return

    units = "metric" if unit == "C" else "imperial"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if str(data.get("cod")) != "200":
            messagebox.showerror("Error", data.get("message", "City not found"))
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]

        temp_label.config(text=f"Temperature: {temp} °{unit}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind}")
        desc_label.config(text=f"Condition: {description}")

        load_icon(icon_code)

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error. Check your internet.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


def load_icon(icon_code):
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    img_data = requests.get(icon_url).content

    with open(ICON_PATH, "wb") as f:
        f.write(img_data)

    img = Image.open(ICON_PATH).resize((100, 100))
    photo = ImageTk.PhotoImage(img)

    icon_label.config(image=photo)
    icon_label.image = photo


root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("400x500")
root.resizable(False, False)

tk.Label(root, text="Weather App", font=("Arial", 16, "bold")).pack(pady=10)

city_entry = tk.Entry(root, width=30, font=("Arial", 12), fg="grey")
city_entry.pack(pady=5)
city_entry.insert(0, "Enter city name")

def on_entry_click(event):
    if city_entry.get() == "Enter city name":
        city_entry.delete(0, "end")  # delete placeholder
        city_entry.config(fg="black")  # text color black

def on_focus_out(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter city name")
        city_entry.config(fg="grey")

city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focus_out)


unit_var = tk.StringVar(value="C")

tk.Radiobutton(root, text="Celsius", variable=unit_var, value="C").pack()
tk.Radiobutton(root, text="Fahrenheit", variable=unit_var, value="F").pack()
tk.Button(root, text="Get Weather", command=get_weather, width=20).pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack(pady=5)

temp_label = tk.Label(root, font=("Arial", 12))
temp_label.pack()

humidity_label = tk.Label(root, font=("Arial", 11))
humidity_label.pack()

wind_label = tk.Label(root, font=("Arial", 11))
wind_label.pack()

desc_label = tk.Label(root, font=("Arial", 11))
desc_label.pack(pady=5)

root.mainloop()
