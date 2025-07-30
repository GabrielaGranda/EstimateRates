from js import document, console, L
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

API_URL = "https://estimateratesapi.onrender.com/proxy/estimate"
API_KEY = "clavePublica123"  # Debe coincidir con PROXY_KEY en backend

async def calculate_estimate(event):
    try:
        event.preventDefault()

        # Mostrar spinner y desactivar botón
        status_el = document.getElementById("status")
        calculate_button = document.getElementById("calculate")
        status_el.innerHTML = 'Loading Estimate Rate... <span class="spinner"></span>'
        calculate_button.disabled = True

        # Leer valores del formulario
        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value

        data = {
            "loading_city": loading_city,
            "delivery_city": delivery_city,
        }

        # Solicitud al backend
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
        console.log("📦 Respuesta JSON:", result)

        # Mostrar estimación
        document.getElementById("rate").innerText = str(result.get("estimate", "N/A"))
        document.getElementById("currency").innerText = result.get("currency", "N/A")
        document.getElementById("miles").innerText = str(result.get("miles", "N/A"))
        document.getElementById("ppm").innerText = str(result.get("ppm", "N/A"))

        # Obtener coordenadas
        route = result.get("route")
        if not route:
            status_el.innerText = "❌ No se encontró la ruta. Verifica las ciudades ingresadas."
            return

        lat1 = route["lat_load"]
        lon1 = route["lon_load"]
        lat2 = route["lat_del"]
        lon2 = route["lon_del"]

        if not all([lat1, lon1, lat2, lon2]):
            console.log("❌ Coordenadas no válidas o incompletas:", route)
            status_el.innerText = "No se pudo obtener la ruta."
            return

        # Mostrar mapa
        map_div = document.getElementById("map")
        map_div.innerHTML = ""  # Limpiar mapa anterior
        map_obj = L.map(map_div).setView([ (lat1 + lat2)/2 , (lon1 + lon2)/2 ], 5)

        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            "attribution": "&copy; OpenStreetMap contributors"
        }).addTo(map_obj)

        # Dibujar la línea de ruta
        L.polyline([[lat1, lon1], [lat2, lon2]], {
            "color": "blue",
            "weight": 4
        }).addTo(map_obj)

        # Marcadores
        L.marker([lat1, lon1]).addTo(map_obj).bindPopup("Loading City").openPopup()
        L.marker([lat2, lon2]).addTo(map_obj).bindPopup("Delivery City")

        # Limpiar estado y reactivar botón
        status_el.innerText = ""
        calculate_button.disabled = False

    except Exception as e:
        document.getElementById("rate").innerText = "Error"
        status_el.innerText = "Ocurrió un error"
        console.log(f"❌ Error al calcular la estimación: {e}")
        calculate_button.disabled = False

# Asignar evento al botón
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))
