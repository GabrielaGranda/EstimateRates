from js import document, console, drawRoute
import asyncio
import js

async def estimate():
    loading = document.getElementById("loading").value
    delivery = document.getElementById("delivery").value
    origin = document.getElementById("origin").value
    destination = document.getElementById("destination").value

    payload = {
        "loading_city": loading,
        "delivery_city": delivery,
        "origin": origin,
        "destination": destination
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "clavePublica123"
    }

    res = await js.fetch(
        "https://estimateratesapi.onrender.com/proxy/estimate",
        {
            "method": "POST",
            "body": js.JSON.stringify(payload),
            "headers": headers
        }
    )

    data = await res.json()
    console.log("✅ Datos recibidos:", data)

    # Mostrar resultados
    document.getElementById("rate").innerText = data.estimate
    document.getElementById("currency").innerText = data.currency
    document.getElementById("miles").innerText = data.miles
    document.getElementById("ppm").innerText = data.ppm

    # Extraer coordenadas
    route = data.route
    geoapi = data.geoapi_key

    lat1 = route.lat_load
    lon1 = route.lon_load
    lat2 = route.lat_del
    lon2 = route.lon_del
    city1 = route.loading_city
    city2 = route.delivery_city

    # Llamar a la función de JavaScript
    drawRoute(lat1, lon1, lat2, lon2, city1, city2, geoapi)

# Conectar al botón
document.getElementById("calculate").addEventListener("click", lambda e: asyncio.ensure_future(estimate()))

