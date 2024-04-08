from datetime import datetime
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
bucket_list = ['https://www.amazon.es/HP-15-fd0042ns-Ordenador-portátil-Graphics/dp/B0CFBGWVQD/ref=sr_1_4?dib=eyJ2IjoiMSJ9.aoMhGcee8VYmgN3D0U2sTAqtFmpV83m0jdH6lkzhsI6oPWLraNdPXElQ1tFkt8lard6Fj0KKREb4PzAtGwtXQJNRfN9oNldoc6N1mjYSHDWIVcA3RVW-X7JIG49CmXXsetu4R-RZw-4Ds8_vJ5VLLErHwRSxLzZMs4qkUIV7W-6h432NypNPo6cWpcaaUxum9c6-uSKtsPxbB8wX1eUB2Wq2WstpRLjoXu2YWVCUMf0v-01oAbVDA1bQKgqlN4PfBQ88kfLecQieqlcPEmLpgRdqr0IxGtHDlxA608kr6Zk.DPLrA6WevfsiJ3BGsxTOnyC4w8H1-nO2TJ-DMu2dVYY&dib_tag=se&qid=1712414913&s=computers&sr=1-4&ufe=app_do%3Aamzn1.fos.0fd54328-1d46-4534-bd0f-16141b40bb5b']

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
        price = price.replace(',', '.').replace('€', '').replace('.00', '')
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
        reviews = reviews.replace(' valoraciones', '')
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
            "product name": product_name,
            "price": product_price,
            "rating": product_rating,
            "reviews": product_reviews,
            "url": url,
            "timestamp": str(datetime.now())
        }

        # Envío
        print(json_data)

    # Introducir un retraso de 1 min
    time.sleep(60)
