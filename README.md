# EstimateRates

📄 Estimate Rates API - Documentación

🌐 Endpoint
POST https://estimateratesapi.onrender.com/proxy/estimate

🔐 Autenticación

Header	       Valor	      Requerido
X-API-Key	 clavePublica123	   ✅

📤 Cuerpo de la solicitud (JSON)

{
  "loading_city": "Lumberton, NC, USA",
  "delivery_city": "Dayton, VA, USA",
  "origin": "USA",
  "destination": "USA"
}

Campo	          Tipo	   Descripción	         Requerido
loading_city	 string	  Ciudad de carga	           ✅
delivery_city	 string	  Ciudad de destino	         ✅
origin	       string	  País de origen (USA o CA)	 ✅
destination	   string	  País destino (USA o CA)	   ✅

📥 Ejemplo de solicitud

curl -X POST https://estimateratesapi.onrender.com/proxy/estimate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: clavePublica123" \
  -d '{
        "loading_city": "Lumberton, NC, USA",
        "delivery_city": "Dayton, VA, USA",
        "origin": "USA",
        "destination": "USA"
      }'
      
📤 Respuesta exitosa (200 OK)

{
  "origin": "USA",
  "destination": "USA",
  "miles": 810.34,
  "estimate": 1782,
  "currency": "USD",
  "ppm": 2.2,
  "route": {
    "lat_load": 34.6188,
    "lon_load": -79.006,
    "lat_del": 38.4176,
    "lon_del": -78.9389,
    "loading_city": "Lumberton, NC, USA",
    "delivery_city": "Dayton, VA, USA"
  }
}

⚠️ Respuestas de error

Código	   Descripción
401	       Unauthorized. Invalid proxy key.
500	       Error interno del servidor o error de API externa

🛠️ ¿Qué hace esta API?

Esta API estima el costo de transporte entre dos ciudades, considerando:
Distancia real (con Geoapify)
Precio actual del combustible (con EIA API)
Penalización de cruce fronterizo (si aplica)
Mínimo de millas (800) para rutas cortas

