from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
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

# Obtiene el precio del producto
def get_product_price(dom):
    try:
        # Extraer el precio del producto utilizando XPath
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        # Parsear el precio a formato float
        price = price.replace('.', '').replace(',', '.').replace('.00', '').replace('€', '')
        return float(price)
    except Exception:
        return None

# Obtiene el nombre del producto
def get_product_name(dom):
    try:
        # Extraer el nombre del producto utilizando XPath
        name = dom.xpath('//span[@id="productTitle"]/text()')[0]
        # Elimina los espacios al principio y al final del nombre
        return name.strip()
    except Exception:
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
        return None


@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Template for loading data from filesystem.
    Load data from 1 file or multiple file directories.

    For multiple directories, use the following:
        FileIO().load(file_directories=['dir_1', 'dir_2'])

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """
    
    bucket_list = [] # Lista de URLs de productos en Amazon
    data = [] # Lista de datos de cada producto
    
    # Abre el archivo en modo lectura
    with open('data_proyecto-final-iot/data_bucket.txt', 'r') as f:
        lineas = f.readlines()
        # Comprobar si hay líneas
        if (lineas):
            # Imprimir el número y el nombre de cada producto
            for linea in lineas:
                params = linea.strip().split('###')
                if len(params) == 3:  # Asegurarse de que hay tres partes
                    bucket_list.append(params[1]) # La URL es la segunda parte

    # Por cada URL en la lista
    for url in bucket_list:
        # Realizar una solicitud HTTP a la URL
        response = requests.get(url, headers=header)
        # Analizar la respuesta HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Crear un objeto DOM utilizando lxml
        amazon_dom = et.HTML(str(soup))

        # Extraer los atributos del producto utilizando funciones definidas anteriormente
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

        data.append(json_data)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    