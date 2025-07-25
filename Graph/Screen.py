from js import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

# Endpoint PROXY público (no el protegido directamente)
API_URL = "https://estimateratesapi.onrender.com/proxy/estimate"
API_KEY = "clavePublica123"  # Esta debe coincidir con PROXY_KEY en el backend

async def calculate_estimate(event):
    try:
        event.preventDefault()  # Evita recarga del formulario

        # Obtener datos del formulario
        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value
        origin = document.getElementById("origin").value
        destination = document.getElementById("destination").value

        # Construir el JSON
        data = {
            "loading_city": loading_city,
            "delivery_city": delivery_city,
            "origin": origin,
            "destination": destination
        }

        # Llamada al endpoint proxy
        response = await pyfetch(
            url=API_URL,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": API_KEY  # Esta es la pública: clavePublica123
            },
            body=json.dumps(data)
        )
        if response.status == 200:
            result = await response.json()
            console.log("✅ Resultado recibido:", result)

        # Mostrar resultados en pantalla
        document.getElementById("rate").innerText = str(result.get("estimate", "N/A"))
        document.getElementById("currency").innerText = result.get("currency", "N/A")
        document.getElementById("miles").innerText = str(result.get("miles", "N/A"))
        document.getElementById("ppm").innerText = str(result.get("ppm", "N/A"))

        # Dibujar ruta si existe en la respuesta
        route = result.get("route")
        if route:
                lat1 = route.get("lat_load")
                lon1 = route.get("lon_load")
                lat2 = route.get("lat_del")
                lon2 = route.get("lon_del")
                city1 = route.get("loading_city")
                city2 = route.get("delivery_city")
                geoapi_key = route.get("geoapi_key")
            
                # Llamar a la función JS
                window.drawRoute(lat1, lon1, lat2, lon2, city1, city2, geoapi_key)
        else:
            console.log(f"❌ Error en la respuesta: {response.status}")
            document.getElementById("rate").innerText = "Error"
            document.getElementById("currency").innerText = ""
            document.getElementById("miles").innerText = "—"
            document.getElementById("ppm").innerText = "—"
            
    except Exception as e:
        document.getElementById("rate").innerText = "Error"
        print(f"Error al calcular la estimación: {e}")

# Conectar botón con función
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))
