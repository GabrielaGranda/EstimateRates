from js import document, console, drawRoute
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

API_URL = "https://estimateratesapi.onrender.com/proxy/estimate"
API_KEY = "clavePublica123"  # Debe coincidir con PROXY_KEY en backend

async def calculate_estimate(event):
    try:
        event.preventDefault()

        # Mostrar spinner y mensaje
        status_el = document.getElementById("status")
        calculate_button = document.getElementById("calculate")
        status_el.innerHTML = 'Loading Estimate Rate... <span class="spinner"></span>'
        calculate_button.disabled = True

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

        # Dibujar ruta en el mapa si los datos existen
        if "route" in result and result["route"]:
            r = result["route"]
            drawRoute(
                r["lat_load"], r["lon_load"],
                r["lat_del"], r["lon_del"],
                r["loading_city"], r["delivery_city"],
                result["geoapi_key"]
            )
        
        status_el.innerText = ""  # Limpiar mensaje
        calculate_button.disabled = False  # Reactivar botón

    except Exception as e:
        document.getElementById("rate").innerText = "Error"
        status_el.innerText = "Ocurrió un error"
        console.log(f"❌ Error al calcular la estimación: {e}")
        calculate_button.disabled = False

# Asignar evento al botón
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))



