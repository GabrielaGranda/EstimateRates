from js import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

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

        document.getElementById("rate").innerText = str(result.get("estimate", "N/A"))
        document.getElementById("currency").innerText = result.get("currency", "N/A")
        document.getElementById("miles").innerText = str(result.get("miles", "N/A"))
        document.getElementById("ppm").innerText = str(result.get("ppm", "N/A"))

    except Exception as e:
        print(f"Error al calcular la estimación: {e}")

calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))


