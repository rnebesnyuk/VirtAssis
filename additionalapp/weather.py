import requests


appid = "79d1ca96933b0328e1c7e3e7a26cb347"
key = "d84e1e5cc61040c2a6d111812231406"
days = 3
aqi = 'no'
alerts = 'no'


def read_weather(city='Kiev'):
    date_list = []
    try:
        res = requests.get("http://api.openweathermap.org/geo/1.0/direct?",
                           params={'q': city, 'appid': appid})
        source = res.json()
        print(f"lat: {source[0]['lat']}  |  lon: {source[0]['lon']}")
        print(f"Місто: {source[0]['local_names']['uk']}")
        city = source[0]['local_names']['uk']
    except Exception as e:
        print("Exception (find):", e)
        pass

    try:
        res = requests.get("https://api.weatherapi.com/v1/forecast.json?",
                           params={'key': key, 'q': f"{source[0]['lat']},{source[0]['lon']}", 'days': days, 'aqi': aqi, 'alerts': alerts})
        source = res.json()
        for l in source['forecast']['forecastday']:
            date = l['date']
            maxtemp = l['day']['maxtemp_c']
            mintemp = l['day']['mintemp_c']
            maxwind = l['day']['maxwind_kph']
            avghumidity = l['day']['avghumidity']
            condition_icon = l['day']['condition']['icon']
            list = {
                'date': date,
                'maxtemp': maxtemp,
                'mintemp': mintemp,
                'maxwind': maxwind,
                'avghumidity': avghumidity,
                'icon': condition_icon,
                'city': city,
            }
            date_list.append(list)
        print('Weather complete')
        return date_list
    except Exception as e:
        print("Exception (find):", e)
        pass
