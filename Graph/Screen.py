from js import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
import json

# Constantes
API_URL = "https://estimateratesapi.onrender.com/proxy/estimate"
API_KEY = "clavePublica123"  # Esta es la clave pública segura de uso frontend

async def calculate_estimate(event):
    try:
        event.preventDefault()  # Evita que el formulario recargue la página (si aplica)

        # Obtener valores del formulario
        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value
        origin = document.getElementById("origin").value
        destination = document.getElementById("destination").value

        # Construir payload
        data = {
            "loading_city": loading_city,
            "delivery_city": delivery_city,
            "origin": origin,
            "destination": destination
        }

        # Llamar al endpoint seguro
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

        # Mostrar resultados
        document.getElementById("rate").innerText = str(result.get("estimate", "N/A"))
        document.getElementById("currency").innerText = result.get("currency", "N/A")
        document.getElementById("miles").innerText = str(result.get("miles", "N/A"))
        document.getElementById("ppm").innerText = str(result.get("ppm", "N/A"))

    except Exception as e:
        document.getElementById("rate").innerText = "Error"
        print(f"Error al calcular la estimación: {e}")

# Conectar el botón con la función
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))

