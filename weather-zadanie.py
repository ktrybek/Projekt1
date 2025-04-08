import datetime as dt
import requests, os, csv


def rain_possibility(rain_sum):
    if rain_sum > 0.0:
        return "Bedzie padac"
    elif rain_sum == 0.0:
        return "Nie bedzie padac"
    else:
        return "Nie wiem"

csv_file = "weather_data.csv"


def initialize_csv():
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Rain Sum"])

def read_csv_file():
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        return list(reader)

def write_csv_file(data):
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    initialize_csv()
    result = []
    base_url = "https://api.open-meteo.com/v1/forecast"

    date_input = input("Podaj dla którego dnia chcesz sprawdzić prognozę (w formacie YYYY-MM-DD): ")
    if not date_input:
        date = (dt.datetime.today() + dt.timedelta(days=1)).date()
    else:
        try:
            date = dt.datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Nieprawidłowy format daty.")
            return

    date_str = date.isoformat()
    records = read_csv_file()

    for row in records[1:]:
        if row[0] == date_str:
            print(f"Dla dnia {date_str} prognoza jest następująca: {row[1]}")
            return

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
        info = rain_possibility(rain_sum)
        print(f"Suma opadów: {rain_sum} mm – {info}")
        result.append([date_str, info])
        write_csv_file(result)
        print("Dane zapisano do pliku.")
    else:
        print(f"Błąd pobierania danych: {response.status_code}")


main()
