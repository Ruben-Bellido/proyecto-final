from fastapi import FastAPI
from pydantic import BaseModel, Field
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Inicializar FastAPI
app = FastAPI()

# Definir parámetros de la conexión a base de datos
url = "https://eu-central-1-1.aws.cloud2.influxdata.com/"
token = "A1hkiA517pl-fA9RnY-9hy2-PnZU6nIlGEibeJvQNsb3QTQbJx_KiTbWlo7FzZCNMewZDgJxtsUV5tIukmNRcQ=="
org = "R&C"
bucket = "amazon_products"

# Crear la conexión a la base de datos
client = InfluxDBClient(url=url, token=token, org=org)

# Crear el objeto para escribir en la base de datos
write_api = client.write_api(write_options=SYNCHRONOUS)

# Clase que componen cada producto
class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="El precio ha de ser mayor a 0")
    rating: float
    reviews: int
    url: str
    hostname: str
    timestamp: str

# Publicar medidas del generador
@app.post("/products")
async def post_product(product: Product):
    # Crear un punto para cada fila
    p = Point("products")
    # Añadir el nombre y url del producto y nombre del host como tags
    p.tag("name", product.name)
    p.tag("url", product.url)
    p.tag("hostname", product.hostname)
    # Añadir campos
    p.field("price", product.price)
    p.field("rating", product.rating)
    p.field("reviews", product.reviews)
    # Fijar clave temporal
    p.time(product.timestamp, WritePrecision.NS)
    # Escribir punto en base de datos
    write_api.write(bucket=bucket, org=org, record=p)

    return {"message": f"Datos almacenados para el producto {product.name}"}
