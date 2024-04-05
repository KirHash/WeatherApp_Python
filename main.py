import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#Function to get the weather info. from OpenWeatherMap API
def get_weather(city):
    API_key = "16fa71cde375b981b6864828e6935865"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    #Parsing the response JSON to get weather info.
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    #Getting the icon URL and return all the weather info.
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)


#Function for searching the weather of a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    #If the city is found
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    #Getting the weather icon image from the URL and updating the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    #Updating the temp. and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")




root = ttkbootstrap.Window(themename = "morph")
root.title("Weather App")
root.geometry("400x400")

#Entry widget: To enter the city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

#Button widget: To search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

#Label widget: To show the city/county name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady = 20)

#Label widget: To show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

#Label widget: To show the tempretuare
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

#Label widget: To show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()

