from fastapi import FastAPI
from pydantic import BaseModel, Field, constr
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

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

# Clase que compone cada producto
class Product(BaseModel):
    name: constr(min_length=1) = Field(..., description="El nombre no puede estar vacío")
    price: float = Field(gt=0, description="El precio ha de ser mayor a 0")
    rating: float = Field(ge=0, le=5, description="La puntuación no puede ser negativa ni mayor que 5")
    reviews: int = Field(ge=0, description="Las valoraciones no puede ser negativa")
    url: constr(regex=r'^https://www\.amazon\.es/.*$') = Field(..., description="La URL debe comenzar con https://www.amazon.es")
    hostname: constr(min_length=1) = Field(..., description="El nombre del host no puede estar vacío")
    timestamp: datetime = Field(..., description="El timestamp debe tener un formato válido de fecha y hora")

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
