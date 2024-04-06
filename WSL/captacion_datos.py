import requests
import json

def celsius_to_kelvin(celsius):
    return celsius - 273.15

def kelvin_to_celsius(kelvin):
    return kelvin + 273.15

# 1. Hacer consulta
lat = 44.34
lon = 10.99
api_key = "adcb483d6e66d26b8fe5c68375662968"
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
response = requests.get(url)

if response.status_code == 200:
    # 2. Recibir datos
    data = response.text

    # 3. Parsear datos
    datos = json.loads(data)
    
    # 4. Extraer datos
    ciudad = datos["name"]
    main = datos["main"]
    t_min = celsius_to_kelvin(main["temp_min"])
    t_max = celsius_to_kelvin(main["temp_max"])
    print("Temperaturas de {}: minima {}, maxima {}".format(ciudad, t_min, t_max))

    resumen = {
        'maxima': t_max,
        'minima': t_min,
        'ciudad': ciudad,
        'latitud': lat,
        'longitud': lon
    }

    print(resumen)
