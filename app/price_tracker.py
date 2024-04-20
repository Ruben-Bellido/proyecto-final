from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time

# Cabeceras para simular una solicitud de navegador real (evita los sistemas anti tracking de Amazon)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

# Lista de URLs de productos en Amazon
bucket_list = ['https://www.amazon.es/Apple-2022-Pulgadas-Wi-Fi-64-GB/dp/B0BJMXBJJJ/ref=sr_1_7',
               'https://www.amazon.es/2022-Apple-Ordenador-Portátil-MacBook/dp/B0B3CV8XSG/ref=zg_bs_g_938008031_d_sccl_26/259-7954607-9722901?psc=1',
               'https://www.amazon.es/fire-tv-stick-con-mando-por-voz-alexa/dp/B08C1KN5J2/ref=zg_bs_g_electronics_d_sccl_1/259-7954607-9722901?psc=1'
               ]

# Registrar urls mediante inputs
while True:
    url = input('Introduce la url del producto a trackear ("fin" para salir): ')
    # Condición de salida
    if url == 'fin':
        break
    try:
        # Validar la URL mediante una solicitud HTTP
        requests.get(url, headers=header)
        # Añadir URL al listado
        bucket_list.append(url)
        print('URL añadida\n')
    except Exception:
        print('URL inválida\n')


# Obtiene el precio del producto
def get_product_price(dom):
    try:
        # Extraer el precio del producto utilizando XPath
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        # Parsear el precio a formato float
        price = price.replace('.', '').replace(',', '.').replace('.00', '').replace('€', '')
        return float(price)
    except Exception:
        price = 'Not Available'
        return None

# Obtiene el nombre del producto
def get_product_name(dom):
    try:
        # Extraer el nombre del producto utilizando XPath
        name = dom.xpath('//span[@id="productTitle"]/text()')[0]
        # Elimina los espacios al principio y al final del nombre
        return name.strip()
    except Exception:
        name = 'Not Available'
        return None

# Obtiene el rating del producto
def get_product_rating(dom):
    try:
        # Extraer el rating del producto utilizando XPath
        rating = dom.xpath('//span[@id="acrPopover"]/span[1]/a/span/text()')[0]
        # Parsear el precio a formato float
        rating = rating.replace(',', '.').strip()
        return float(rating)
    except Exception:
        rating = 'Not Available'
        return None
    
# Obtiene las valoraciones del producto
def get_product_reviews(dom):
    try:
        # Extraer las valoraciones del producto utilizando XPath
        reviews = dom.xpath('//span[@id="acrCustomerReviewText"]/text()')[0]
        # Obtener únicamente el valor numérico
        reviews = reviews.replace(' valoraciones', '').replace('.', '')
        return int(reviews)
    except Exception:
        reviews = 'Not Available'
        return None


# Escribir datos en un archivo CSV
while True:
    # Por cada URL en la lista
    for url in bucket_list:
        # Realizar una solicitud HTTP a la URL
        response = requests.get(url, headers=header)
        # Analizar la respuesta HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Crear un objeto DOM utilizando lxml
        amazon_dom = et.HTML(str(soup))

        # Extraer el nombre del producto y el precio utilizando funciones definidas anteriormente
        product_name = get_product_name(amazon_dom)
        product_price = get_product_price(amazon_dom)
        product_rating = get_product_rating(amazon_dom)
        product_reviews = get_product_reviews(amazon_dom)

        # Agregar los datos al objeto JSON
        json_data = {
            "name": product_name,
            "price": product_price,
            "rating": product_rating,
            "reviews": product_reviews,
            "url": url,
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        # Debug para visualizar los datos
        print(f"Enviando datos: {json_data}")
        
        try:
            # URL del endpoint FastAPI
            url = "http://127.0.0.1:8000/products"
            # Envía la petición POST con los datos
            response = requests.post(url, json=json_data)
            # Debug para comprobar el estado de la petición
            if response.status_code == 200:
                print("Petición POST exitosa")
            else:
                print(f"Error en la petición POST. Código de estado: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error en la conexión: {e}")

    # Introducir un retraso de 1 min
    time.sleep(10)
