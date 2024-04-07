import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import csv

# Cabeceras para simular una solicitud de navegador real (evita los sistemas anti tracking de Amazon)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

# Lista de URLs de productos en Amazon
bucket_list = []

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
def get_amazon_price(dom):
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
        name = dom.xpath('//span[@id="productTitle"]/text()')
        # Extrae el primer elemento (contiene el nombre del producto) y elimina los espacios al principio y al final
        [name.strip() for name in name]
        return name[0]
    except Exception:
        name = 'Not Available'
        return None


# Escribir datos en un archivo CSV
while True:
    with open('master_data.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        # Escribir encabezados en la primera fila del archivo
        writer.writerow(['product name', 'price', 'url'])

        # Por cada URL del listado
        for url in bucket_list:
            # Realizar una solicitud HTTP a la URL
            response = requests.get(url, headers=header)
            # Analizar la respuesta HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Crear un objeto DOM utilizando lxml
            amazon_dom = et.HTML(str(soup))

            # Extraer el nombre del producto y el precio utilizando funciones definidas anteriormente
            product_name = get_product_name(amazon_dom)
            product_price = get_amazon_price(amazon_dom)

            # Escribir los datos en el archivo CSV y mostrarlos en la consola
            writer.writerow([product_name, product_price, url])
            print(product_name, product_price)

    # Introducir un retraso de 1 min
    time.sleep(60)
