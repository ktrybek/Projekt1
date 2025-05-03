import datetime as dt
import requests, os, csv

class WeatherForecast:
    def __init__(self, filename="weather_data.csv"):
        self.filename = filename
        self.data = {}
        self.initialize_csv()
        self.read_csv()

    def initialize_csv(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Rain Info"])

    def read_csv(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    self.data[row[0]] = row[1]

    def write_to_csv(self, date_str, info):
        with open(self.filename, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date_str, info])

    def fetch_weather_from_api(self, date_str):
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": "54.372158",
            "longitude": "18.638306",
            "daily": "rain_sum",
            "start_date": date_str,
            "end_date": date_str,
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            rain_sum = data["daily"]["rain_sum"][0]
            return self.rain_interpretation(rain_sum)
        else:
            return "Brak danych"

    def rain_interpretation(self, rain_sum):
        if rain_sum > 0.0:
            return "Będzie padać"
        elif rain_sum == 0.0:
            return "Nie będzie padać"
        else:
            return "Nie wiem"

    def __getitem__(self, date_str):
        if date_str in self.data:
            return self.data[date_str]
        else:
            info = self.fetch_weather_from_api(date_str)
            self.data[date_str] = info
            self.write_to_csv(date_str, info)
            return info

    def __setitem__(self, date_str, info):
        self.data[date_str] = info
        self.write_to_csv(date_str, info)

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return ((date, forecast) for date, forecast in self.data.items())

def main():
    weather_forecast = WeatherForecast()

    date_input = input("Podaj dzień, dla którego chcesz sprawdzić prognozę (YYYY-MM-DD): ")
    if not date_input:
        date_str = (dt.datetime.today() + dt.timedelta(days=1)).date().isoformat()
    else:
        try:
            date_str = dt.datetime.strptime(date_input, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Nieprawidłowy format daty.")
            exit()

    print(f"Dla dnia {date_str} prognoza jest następująca: {weather_forecast[date_str]}")

main()