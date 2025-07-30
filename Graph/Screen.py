from js import document, console, L
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

API_URL = "https://estimateratesapi.onrender.com/proxy/estimate"
API_KEY = "clavePublica123"  # Tu PROXY_KEY pública

async def calculate_estimate(event):
    try:
        event.preventDefault()

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

        # Convierte el proxy a dict Python nativo
        result_proxy = await response.json()
        result = result_proxy.to_py()
        console.log("🔍 Respuesta del backend:", result)

        # Mostrar estimación
        document.getElementById("rate").innerText = str(result.get("estimate", "N/A"))
        document.getElementById("currency").innerText = result.get("currency", "N/A")
        document.getElementById("miles").innerText = str(result.get("miles", "N/A"))
        document.getElementById("ppm").innerText = str(result.get("ppm", "N/A"))

        # Obtener ruta
        route = result.get("route", {})
        console.log("Ruta recibida:", route)

        lat_load = route.get("lat_load")
        lon_load = route.get("lon_load")
        lat_del = route.get("lat_del")
        lon_del = route.get("lon_del")

        if not all([lat_load, lon_load, lat_del, lon_del]):
            console.log("❌ Coordenadas no válidas o incompletas:", route)
            status_el.innerText = "No se pudo obtener la ruta."
            calculate_button.disabled = False
            return

        # Mostrar mapa
        map_div = document.getElementById("map")
        map_div.innerHTML = ""
        map_obj = L.map(map_div).setView([lat_load, lon_load], 6)

        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            "attribution": "&copy; OpenStreetMap contributors"
        }).addTo(map_obj)

        L.polyline([[lat_load, lon_load], [lat_del, lon_del]], {
            "color": "blue",
            "weight": 4
        }).addTo(map_obj)

        L.marker([lat_load, lon_load]).addTo(map_obj).bindPopup("Loading City").openPopup()
        L.marker([lat_del, lon_del]).addTo(map_obj).bindPopup("Delivery City")

        status_el.innerText = ""
        calculate_button.disabled = False

    except Exception as e:
        document.getElementById("rate").innerText = "Error"
        status_el.innerText = f"Ocurrió un error: {str(e)}"
        console.log(f"❌ Error al calcular la estimación: {e}")
        calculate_button.disabled = False

calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))
