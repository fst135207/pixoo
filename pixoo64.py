import os
import sys
import time
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
from dotenv import load_dotenv
sys.path.append('/home/pixoo64/pixoo64/InstallModuls/pixoo')
from pixoo import Pixoo

# Load .env variables
load_dotenv()

# API-Schlüssel für die OpenWeatherMap API
API_KEY = '928bec8b39284910a4464309241305'

def defined_value(value, default):
    return default if value is None else value

def ping():
    response = requests.get('http://api.weatherapi.com/v1/current.json?key=928bec8b39284910a4464309241305&q=Bern&aqi=no')
    return response.status_code == 200

def retrieve_current_weather(city):
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key=928bec8b39284910a4464309241305&q=Bern&aqi=no')
    data = response.json()
    if 'current' in data:
        temperature = data['current']['temp_c'] # Temperatur aus API-Antwort extrahieren
        weather_icon = data['current']['condition']['icon']  # Icon-URL aus der API-Antwort extrahieren
        weather_icon_url_parts = weather_icon.split('/')[-4:]
        weather_icon = '/'.join(weather_icon_url_parts)  # Die Teile wieder zu einem Pfad verbinden
         # Den lokalen Pfad zur Bilddatei erstellen
        weather_icon = os.path.join(os.getcwd(), weather_icon)
        return temperature, weather_icon
    else:
        return None, None

def retrieve_current_time():
    current_time = datetime.now().strftime('%H:%M')
    return current_time

def retrieve_current_date():
    current_date = datetime.now().strftime('%d.%m.%y')
    return current_date

def main():
    # Initialisierungsmeldung ausgeben
    print('[.] Booting..')

    # Prüfen, ob die Openweather-API erreichbar ist
    if ping():
        print('[.] Openweather API reachable')
    else:
        print('[x] Openweather API is not reachable. Perhaps check your internet settings')
        return

    # IP-Adresse des Pixoo64-Displays aus der Umgebungsvariable laden
    ip_address = os.environ.get('PIXOO_IP_ADDRESS')
    if ip_address is None:
        print('[x] Please set the `PIXOO_IP_ADDRESS` value in the .env file')
        return

    # Farben definieren
    green = (99, 199, 77)
    red = (255, 0, 68)
    white = (255, 255, 255)

    # Timeout-Wert und Benutzer-ID laden oder Standardwerte verwenden
    timeout = int(defined_value(os.environ.get('TIMEOUT'), 3600))
    city = defined_value(os.environ.get('CITY'), 'BERN')

    # Verbindung zum Pixoo64-Display herstellen
    pixoo = Pixoo(ip_address, 64, True)
    pixoo.draw_image('background.png')  # Hintergrundbild anzeigen
    pixoo.draw_text('-------------', (6, 50), red) # Texte anzeigen
    pixoo.draw_text('-------------', (6, 57), red)
    pixoo.push()  # Anzeigen

    print('[.] Starting update loop in 2 seconds')
    time.sleep(1)

    # Hauptaktualisierungsschleife
    while True:
        temperature, weather_icon = retrieve_current_weather(city)  # Aktuelle Wetterdaten abrufen
        current_time = retrieve_current_time() # Aktuelle Zeit abrufen
        current_date = retrieve_current_date() # Aktuelles Datum abrufen

        # Anzeigen der Hintergrundbildes und der aktualisierten Informationen auf dem Pixoo64-Display
        pixoo.draw_image('background.png')
        if weather_icon is not None:
            icon_image = Image.open(weather_icon)
            icon_image = icon_image.resize((25, 25))  # Größe anpassen
            pixoo.draw_image(icon_image, (5, 25))  # Position des Icons anpassen
        pixoo.draw_text(f'{current_time}', (2, 2), white)
        pixoo.draw_text(f'{current_date}', (8, 55), white)
        pixoo.push()  # Anzeigen

if __name__ == '__main__':
    main()
