from js import document
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch
import pandas as pd

# Replace these with your actual keys
geoapify_key = "664e08db960a41e89ece23f94c9edbdd"
api_key = "YWTB7x6n6dkyEEkRvnKaHBEe8WZCZAgCW48rUrxj"

async def calculate_estimate(event):
    try:
        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value
        origin = document.getElementById("origin").value
        destination = document.getElementById("destination").value

        # Fetch coordinates
        url_geo = f"https://api.geoapify.com/v1/geocode/search?format=json&apiKey={geoapify_key}&text="
        res_load = await pyfetch(url_geo + loading_city)
        data_load = await res_load.json()
        lat_load = data_load['results'][0]['lat']
        lon_load = data_load['results'][0]['lon']

        res_del = await pyfetch(url_geo + delivery_city)
        data_del = await res_del.json()
        lat_del = data_del['results'][0]['lat']
        lon_del = data_del['results'][0]['lon']

        # Distance route
        dist_url = f"https://api.geoapify.com/v1/routing?mode=drive&units=imperial&apiKey={geoapify_key}&waypoints={lat_load},{lon_load}|{lat_del},{lon_del}"
        res_dist = await pyfetch(dist_url)
        data_dist = await res_dist.json()
        miles = round(float(data_dist['features'][0]['properties']['distance']), 2)
        miles = max(miles, 800)

        # Fuel price
        fuel_url = f"https://api.eia.gov/v2/petroleum/pri/gnd/data/?frequency=weekly&data[0]=value&facets[duoarea][]=R20&facets[product][]=EPD2D&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={api_key}"
        res_fuel = await pyfetch(fuel_url)
        fuel_data = await res_fuel.json()
        fuel_price = round(float(fuel_data['response']['data'][0]['value']), 2)

        # Load Fuelperc CSV
        df = pd.read_csv("Graph/Fuelperc.csv")
        print("CSV Columns:", df.columns)
        fuelper = 0.30

        estimate = round((miles * 1.8) + (miles * fuelper), 0)
        if (origin == "USA" and destination == "CA") or (origin == "CA" and destination == "USA"):
            estimate += 400

        currency = "USD" if origin == "USA" else "CAD"

        document.getElementById("rate").innerText = str(estimate)
        document.getElementById("currency").innerText = currency
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Bind the button
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))



