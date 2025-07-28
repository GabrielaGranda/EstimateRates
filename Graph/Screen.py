from js import document, console
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

API_URL = "https://estimateratesapi.onrender.com/proxy/estimate"
API_KEY = "clavePublica123"  # Debe coincidir con PROXY_KEY en backend

async def calculate_estimate(event):
    try:
        event.preventDefault()

        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value

        data = {
            "loading_city": loading_city,
            "delivery_city": delivery_city,
        }

        response = await pyfetch(
            url=API_URL,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            },
            body=json.dumps(data)
        )

        result = await response.json()

        # Mostrar estimación en la interfaz
        document.getElementById("rate").innerText = str(result.get("estimate", "N/A"))
        document.getElementById("currency").innerText = result.get("currency", "N/A")
        document.getElementById("miles").innerText = str(result.get("miles", "N/A"))
        document.getElementById("ppm").innerText = str(result.get("ppm", "N/A"))

    except Exception as e:
        document.getElementById("rate").innerText = "Error"
        console.log(f"❌ Error al calcular la estimación: {e}")

# Asignar evento al botón
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))
