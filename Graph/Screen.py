from js import document
from pyodide.http import pyfetch
import json
from pyodide.ffi import create_proxy

async def calculate_estimate(event):
    try:
        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value
        origin = document.getElementById("origin").value
        destination = document.getElementById("destination").value

        data = {
            "loading_city": loading_city,
            "delivery_city": delivery_city,
            "origin": origin,
            "destination": destination
        }

        response = await pyfetch(
            url="https://estimateratesapi.onrender.com/estimate",
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(data)
        )

        result = await response.json()

        # Ahora muestras los resultados en el DOM
        document.getElementById("rate").innerText = str(result["estimate"])
        document.getElementById("currency").innerText = result["currency"]
        document.getElementById("miles").innerText = str(result["miles"])
        document.getElementById("ppm").innerText = str(result["ppm"])

    except Exception as e:
        print(f"Error al obtener la estimación: {e}")




# Bind the button
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))



