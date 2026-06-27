import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

# ─── YOUR API KEY ─────────────────────────────────────────────
API_KEY = "bfcdf96a87cf6ed9e73411a2282d5caa"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

# ─── API CALLS ────────────────────────────────────────────────
def get_current_weather(city, unit):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units={unit}"
    response = requests.get(url, timeout=10)
    return response

def get_forecast(city, unit):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units={unit}&cnt=40"
    response = requests.get(url, timeout=10)
    return response

# ─── MAIN APP ─────────────────────────────────────────────────
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App — OIBSIP")
        self.root.geometry("540x750")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        self.unit = tk.StringVar(value="metric")
        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.root, text="🌦️ Weather App",
                 font=("Helvetica", 22, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=20)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="#1e1e2e")
        search_frame.pack(padx=40, fill="x")

        self.city_entry = tk.Entry(search_frame,
                                    font=("Helvetica", 13),
                                    bg="#313244", fg="#cdd6f4",
                                    insertbackground="white",
                                    relief="flat")
        self.city_entry.pack(side="left", fill="x",
                              expand=True, ipady=10, padx=(0,10))
        self.city_entry.insert(0, "Enter city name...")
        self.city_entry.bind("<FocusIn>",  self.clear_placeholder)
        self.city_entry.bind("<FocusOut>", self.add_placeholder)
        self.city_entry.bind("<Return>",   lambda e: self.fetch_weather())

        tk.Button(search_frame, text="Search",
                  font=("Helvetica", 12, "bold"),
                  bg="#89b4fa", fg="#1e1e2e",
                  relief="flat", cursor="hand2",
                  command=self.fetch_weather).pack(side="left", ipady=10, ipadx=15)

        # Unit Toggle
        unit_frame = tk.Frame(self.root, bg="#1e1e2e")
        unit_frame.pack(pady=10)

        tk.Radiobutton(unit_frame, text="°C Celsius",
                       variable=self.unit, value="metric",
                       bg="#1e1e2e", fg="#cdd6f4",
                       selectcolor="#313244",
                       font=("Helvetica", 11),
                       command=self.fetch_weather).pack(side="left", padx=15)

        tk.Radiobutton(unit_frame, text="°F Fahrenheit",
                       variable=self.unit, value="imperial",
                       bg="#1e1e2e", fg="#cdd6f4",
                       selectcolor="#313244",
                       font=("Helvetica", 11),
                       command=self.fetch_weather).pack(side="left", padx=15)

        # Current Weather Card
        self.weather_frame = tk.Frame(self.root, bg="#313244",
                                       padx=20, pady=20)
        self.weather_frame.pack(padx=40, pady=10, fill="x")

        self.city_label = tk.Label(self.weather_frame, text="—",
                                    font=("Helvetica", 20, "bold"),
                                    bg="#313244", fg="#cdd6f4")
        self.city_label.pack()

        self.desc_label = tk.Label(self.weather_frame, text="",
                                    font=("Helvetica", 13),
                                    bg="#313244", fg="#a6adc8")
        self.desc_label.pack()

        self.temp_label = tk.Label(self.weather_frame, text="",
                                    font=("Helvetica", 42, "bold"),
                                    bg="#313244", fg="#89b4fa")
        self.temp_label.pack(pady=5)

        # Details Row
        details_frame = tk.Frame(self.weather_frame, bg="#313244")
        details_frame.pack(fill="x", pady=10)

        self.humidity_label = self.make_detail(details_frame, "💧 Humidity", "—")
        self.wind_label     = self.make_detail(details_frame, "💨 Wind",     "—")
        self.feels_label    = self.make_detail(details_frame, "🌡️ Feels Like","—")

        # 5 Day Forecast Title
        tk.Label(self.root, text="5-Day Forecast",
                 font=("Helvetica", 14, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=(15,5))

        # Forecast Cards Frame
        self.forecast_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.forecast_frame.pack(padx=20, fill="x")

        # Hourly Title
        tk.Label(self.root, text="Next 6 Hours",
                 font=("Helvetica", 14, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=(15,5))

        # Hourly Frame
        self.hourly_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.hourly_frame.pack(padx=20, fill="x")

    def make_detail(self, parent, title, value):
        f = tk.Frame(parent, bg="#313244")
        f.pack(side="left", expand=True)
        tk.Label(f, text=title, font=("Helvetica", 10),
                 bg="#313244", fg="#a6adc8").pack()
        lbl = tk.Label(f, text=value, font=("Helvetica", 12, "bold"),
                       bg="#313244", fg="#cdd6f4")
        lbl.pack()
        return lbl

    # ─── PLACEHOLDER ──────────────────────────────────────────
    def clear_placeholder(self, e):
        if self.city_entry.get() == "Enter city name...":
            self.city_entry.delete(0, tk.END)
            self.city_entry.config(fg="#cdd6f4")

    def add_placeholder(self, e):
        if not self.city_entry.get():
            self.city_entry.insert(0, "Enter city name...")
            self.city_entry.config(fg="#6c7086")

    # ─── FETCH WEATHER ────────────────────────────────────────
    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city or city == "Enter city name...":
            messagebox.showerror("Error", "Please enter a city name.")
            return

        unit = self.unit.get()
        unit_symbol = "°C" if unit == "metric" else "°F"
        speed_unit  = "m/s" if unit == "metric" else "mph"

        # Current Weather
        try:
            resp = get_current_weather(city, unit)
            if resp.status_code == 404:
                messagebox.showerror("Error", f"City '{city}' not found.")
                return
            elif resp.status_code == 401:
                messagebox.showerror("Error", "Invalid API key.")
                return
            resp.raise_for_status()
            data = resp.json()

            self.city_label.config(
                text=f"{data['name']}, {data['sys']['country']}")
            self.desc_label.config(
                text=data['weather'][0]['description'].title())
            self.temp_label.config(
                text=f"{round(data['main']['temp'])}{unit_symbol}")
            self.humidity_label.config(
                text=f"{data['main']['humidity']}%")
            self.wind_label.config(
                text=f"{data['wind']['speed']} {speed_unit}")
            self.feels_label.config(
                text=f"{round(data['main']['feels_like'])}{unit_symbol}")

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No internet connection.")
            return
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Request timed out.")
            return

        # Forecast
        try:
            resp2 = get_forecast(city, unit)
            resp2.raise_for_status()
            fdata = resp2.json()

            # Clear old forecast cards
            for w in self.forecast_frame.winfo_children():
                w.destroy()
            for w in self.hourly_frame.winfo_children():
                w.destroy()

            # 5 Day — one entry per day (every 8th item = 24hrs)
            seen_dates = []
            for item in fdata['list']:
                date = datetime.fromtimestamp(
                    item['dt']).strftime("%a\n%d %b")
                if date not in seen_dates:
                    seen_dates.append(date)
                    temp = round(item['main']['temp'])
                    desc = item['weather'][0]['main']
                    self.make_forecast_card(
                        self.forecast_frame, date, temp, unit_symbol, desc)
                if len(seen_dates) == 5:
                    break

            # Hourly — next 6 items (every 3hrs)
            for item in fdata['list'][:6]:
                time = datetime.fromtimestamp(
                    item['dt']).strftime("%H:%M")
                temp = round(item['main']['temp'])
                desc = item['weather'][0]['main']
                self.make_hourly_card(
                    self.hourly_frame, time, temp, unit_symbol, desc)

        except Exception:
            pass

    def make_forecast_card(self, parent, date, temp, unit, desc):
        card = tk.Frame(parent, bg="#313244", padx=10, pady=10)
        card.pack(side="left", expand=True, fill="x", padx=4)
        tk.Label(card, text=date, font=("Helvetica", 10, "bold"),
                 bg="#313244", fg="#cdd6f4").pack()
        tk.Label(card, text=self.weather_emoji(desc),
                 font=("Helvetica", 18),
                 bg="#313244").pack()
        tk.Label(card, text=f"{temp}{unit}",
                 font=("Helvetica", 12, "bold"),
                 bg="#313244", fg="#89b4fa").pack()

    def make_hourly_card(self, parent, time, temp, unit, desc):
        card = tk.Frame(parent, bg="#313244", padx=10, pady=8)
        card.pack(side="left", expand=True, fill="x", padx=4)
        tk.Label(card, text=time, font=("Helvetica", 10),
                 bg="#313244", fg="#a6adc8").pack()
        tk.Label(card, text=self.weather_emoji(desc),
                 font=("Helvetica", 16),
                 bg="#313244").pack()
        tk.Label(card, text=f"{temp}{unit}",
                 font=("Helvetica", 11, "bold"),
                 bg="#313244", fg="#89b4fa").pack()

    def weather_emoji(self, desc):
        emojis = {
            "Clear": "☀️", "Clouds": "☁️",
            "Rain": "🌧️", "Drizzle": "🌦️",
            "Thunderstorm": "⛈️", "Snow": "❄️",
            "Mist": "🌫️", "Fog": "🌫️",
            "Haze": "🌫️", "Smoke": "🌫️"
        }
        return emojis.get(desc, "🌡️")

# ─── RUN ──────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()