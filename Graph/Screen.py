from pyodide.http import pyfetch
import json
from js import document

async def calculate_estimate(event):
    try:
        const data = {
            "loading_city": document.getElementById("loading").value,
            "delivery_city": document.getElementById("delivery").value,
            "origin": document.getElementById("origin").value,
            "destination": document.getElementById("destination").value
        };

        const response = await pyfetch({
            url: "https://estimateratesapi.onrender.com/estimate",
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        document.getElementById("rate").innerText = result["estimate"];
        document.getElementById("currency").innerText = result["currency"];
        document.getElementById("miles").innerText = result["miles"];
        document.getElementById("ppm").innerText = result["ppm"];

        // Si la API devuelve ruta, puedes usar drawRoute aquí
        // drawRoute(result["route"]["lat_load"], result["route"]["lon_load"], ...)

    except Exception as e:
        console.error("Error fetching estimate:", e);



# Bind the button
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))



