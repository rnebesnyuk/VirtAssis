import requests
import datetime

exchanger_id = 9
currency = ['USD', 'EUR']

# https://kurstoday.com.ua/api/chart?from=2000-01&to=2020-05&exchanger_id=9&currency=usd
def exchange_list():
    date_list_EUR = []
    date_list_USD = []
    for cur in currency:
        date_start = (datetime.datetime.now()).strftime('%Y-%m')
        try:
            res = requests.get(
                "https://kurstoday.com.ua/api/chart?",
                params={"from": date_start, "to": date_start, "exchanger_id": exchanger_id, "currency": cur},
            )
            source = res.json()
            for s in source:
                new_Date = datetime.datetime.strptime(s['date'], '%Y-%m-%d')
                data = {
                    'new_Date': new_Date.strftime('%Y, %m, %d'),
                    'buying': float(s['buying']),
                    'selling': float(s['selling']),
                    'previousDate': new_Date.strftime('%d-%m-%Y')
                }
                date_list_USD.append(data) if cur == 'USD' else date_list_EUR.append(data)

        except Exception as e:
            print("Exception (find):", e)
            pass
    print(f"USD :{date_list_USD}")
    print(f"EUR :{date_list_EUR}")
    return date_list_USD, date_list_EUR