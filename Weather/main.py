import os
import urllib.request
import xml.etree.ElementTree as ET
from flask import Flask
from werkzeug.utils import url_quote

app = Flask(__name__)

def k2c(kelvin):
    c = float(kelvin) - 273.15
    return round(c, 2)

def get_weather_data():
    appid = '211dec237321e8df95005da2c4b2976f'
    mode = 'xml'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Kediri,Jatim,id&mode=json&appid=211dec237321e8df95005da2c4b2976f&units=metric'
    url = url.format(mode=mode, appid=appid)

    raw = urllib.request.urlopen(url).read()
    root = ET.fromstring(raw.decode())

    city = root.find('city')
    temperature = root.find('temperature')
    humidity = root.find('humidity')
    pressure = root.find('pressure')

    weather_data = {
        'kota': city.attrib['name'],
        'temperatur': k2c(temperature.attrib['value']),
        'kelembaban': humidity.attrib['value'] + ' ' + humidity.attrib['unit'],
        'tekanan': pressure.attrib['value'] + ' ' + pressure.attrib['unit']
    }

    return weather_data

@app.route("/weather")
def weather():
    """Route to get weather information."""
    data = get_weather_data()
    return str(data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
