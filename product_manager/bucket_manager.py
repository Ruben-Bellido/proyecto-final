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
bucket_path = 'mage/data_proyecto-final-iot/data_bucket.txt'

# Obtiene el nombre del producto
def get_product_name(dom):
    try:
        # Extraer el nombre del producto utilizando XPath
        name = dom.xpath('//span[@id="productTitle"]/text()')[0]
        # Elimina los espacios al principio y al final del nombre
        return name.strip()
    except Exception:
        return None

def listar_productos():
    # Abre el archivo en modo lectura
    with open(bucket_path, 'r') as f:
        lineas = f.readlines()
        # Comprobar si hay líneas
        if (lineas):
            print("Productos rastreados actualmente:")
            # Imprimir el número y el nombre de cada producto
            for linea in lineas:
                params = linea.strip().split('###')
                if len(params) == 3:  # Asegurarse de que hay tres partes
                    print(params[0] + " - " + params[2])  # La URL es la segunda parte
        else:
            print("No se están rastreando productos actualmente.")

def agregar_producto(enlace):
    try:
        # Validar la URL mediante una solicitud HTTP
        response = requests.get(enlace, headers=header)
        # Analizar la respuesta HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Crear un objeto DOM utilizando lxml
        amazon_dom = et.HTML(str(soup))
        # Extraer el nombre del producto y el precio utilizando funciones definidas anteriormente
        nombre = get_product_name(amazon_dom)

        # Abre el archivo en modo lectura
        with open(bucket_path, 'r') as f:
            lineas = f.readlines()
            if lineas:
                ultima_linea = lineas[-1]
                params = ultima_linea.strip().split('###')
                if len(params) == 3:  # Asegurarse de que hay tres partes
                    # Número de la línea a añadir
                    num = int(params[0]) + 1
            else:
                num = 0

        # Abre el archivo para añadir líneas
        with open(bucket_path, 'a') as f:
            # Añadir producto al archivo
            f.write(f'\n{num}###{enlace}###{nombre}')

        print('El producto ha sido añadido.')
    except Exception:
        print('La URL proporcionada es inválida.')

def eliminar_producto(num):
    # Abre el archivo en modo lectura
    with open(bucket_path, 'r') as f:
        # Obtiene las líneas
        lineas = f.readlines()
    # Abre el archivo en modo escritura
    with open(bucket_path, 'w') as f:
        encontrado = False
        # Recorrer las líneas
        for linea in lineas:
            params = linea.strip().split('###')
            if len(params) == 3:  # Asegurarse de que hay tres partes
                # Descarta el producto que tenga el id especificado
                if num != params[0]:
                    f.write(linea)
                else:
                    print(f'"{params[2]}" eliminado.')
                    encontrado = True
    if not encontrado:
        print("El producto no existe.")


def main():

    while True:
        print("\n1. Listar productos rastreados")
        print("2. Agregar producto")
        print("3. Eliminar producto")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            listar_productos()
        elif opcion == '2':
            enlace = input("Introduce la URL del producto a agregar: ")
            agregar_producto(enlace)
        elif opcion == '3':
            enlace = input("Introduce el ID del producto a eliminar: ")
            eliminar_producto(enlace)
        else:
            print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    main()
