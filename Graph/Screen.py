from js import document, console, drawRoute
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

# Endpoint PROXY público
API_URL = "https://estimateratesapi.onrender.com/proxy/estimate"
API_KEY = "clavePublica123"  # Esta debe coincidir con PROXY_KEY en el backend

async def calculate_estimate(event):
    try:
        event.preventDefault()  # Evita recarga del formulario

        # Obtener datos del formulario
        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value

        # Construir el JSON
        data = {
            "loading_city": loading_city,
            "delivery_city": delivery_city,
        }

        # Llamada al endpoint proxy
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

        # Mostrar resultados en pantalla
        document.getElementById("rate").innerText = str(result.get("estimate", "N/A"))
        document.getElementById("currency").innerText = result.get("currency", "N/A")
        document.getElementById("miles").innerText = str(result.get("miles", "N/A"))
        document.getElementById("ppm").innerText = str(result.get("ppm", "N/A"))

        # Dibujar ruta en el mapa si los datos existen
        if "route" in result and result["route"]:
            r = result["route"]
            drawRoute(
                r["lat_load"], r["lon_load"],
                r["lat_del"], r["lon_del"],
                r["loading_city"], r["delivery_city"],
                result["geoapi_key"]
            )

    except Exception as e:
        document.getElementById("rate").innerText = "Error"
        print(f"❌ Error al calcular la estimación: {e}")

# Conectar botón con función
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))
