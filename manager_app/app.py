from flask import Flask, request, render_template, redirect, url_for
import csv
import os
import requests
from bs4 import BeautifulSoup
from lxml import etree as et

# Cabeceras para simular una solicitud de navegador real (evita los sistemas anti tracking de Amazon)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

# Dirección del archivo que almacena los productos rastreados
bucket_path = './data/data_proyecto-final-iot/data_bucket.csv'

# Obtiene el nombre del producto
def get_product_name(dom):
    try:
        # Extraer el nombre del producto utilizando XPath
        name = dom.xpath('//span[@id="productTitle"]/text()')[0]
        # Elimina los espacios al principio y al final del nombre
        return name.strip()
    except Exception:
        return None

def leer_enlaces():
    enlaces = []
    if os.path.exists(bucket_path):
        with open(bucket_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Saltar la cabecera
            for row in reader:
                enlaces.append({'id': row[0], 'url': row[1], 'name': row[2]})
    return enlaces

def escribir_enlaces(enlaces):
    with open(bucket_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'url', 'name'])  # Escribir la cabecera
        for enlace in enlaces:
            writer.writerow([enlace['id'], enlace['url'], enlace['name']])


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    enlaces = leer_enlaces()

    if request.method == 'POST':
        url = request.form.get('url')
        # Comprueba si la URL ya existe
        if any(enlace['url'] == url for enlace in enlaces):
            error = 'El producto ya ha sido registrado. Por favor, introduce una URL diferente.'
            return render_template('index.html', enlaces=enlaces, error=error)
        try:
            # Validar la URL mediante una solicitud HTTP
            response = requests.get(url, headers=header)
            # Analizar la respuesta HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Crear un objeto DOM utilizando lxml
            amazon_dom = et.HTML(str(soup))
            # Extraer el nombre del producto y el precio utilizando funciones definidas anteriormente
            name = get_product_name(amazon_dom)

            # Si no se obtiene un nombre se muestra un error
            if (name is None):
                error = 'La URL del producto es inválida. Se aceptan únicamente enlaces pertenecientes al dominio amazon.es.'
                return render_template('index.html', enlaces=enlaces, error=error)
            
            # ID incremental
            if len(enlaces) > 0:
                id = str(int(enlaces[-1]['id']) + 1)
            else:
                id = 1

            enlaces.append({'id': id, 'url': url, 'name': name})
            escribir_enlaces(enlaces)
            return redirect(url_for('index'))
        # Si da un error
        except Exception:
            error = 'La URL del producto es inválida. Se aceptan únicamente enlaces pertenecientes al dominio amazon.es.'
            return render_template('index.html', enlaces=enlaces, error=error)
    else:
        return render_template('index.html', enlaces=enlaces)

@app.route('/eliminar/<id>')
def eliminar(id):
    enlaces = leer_enlaces()
    enlaces = [enlace for enlace in enlaces if enlace['id'] != id]
    escribir_enlaces(enlaces)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
