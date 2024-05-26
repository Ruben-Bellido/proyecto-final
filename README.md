# proyecto-final-iot

## Descripción
Este proyecto es un sistema que integra diferentes tecnologías con el objetivo de rastrear diferentes productos de la plataforma de comercio electrónico de Amazon (limitado al dominio español). El sistema consta de diferentes partes:
- Una interfaz web basada en Flask desde la cual pueden gestionarse los productos en seguimiento (visualización, registro y borrado). Esta información se persiste de manera local en un CSV.
- Una pipeline en MageAI que automatiza el proceso de recogida de información de los productos. Cada hora se acciona un trigger que recoge el nombre, precio, puntuación y valoraciones del producto, además del nombre del host. Esta información es enviada a un servicio de FastAPI.
- Procesamiento de datos a través de FastAPI. Se recuperan los datos recibidos mediante peticiones POST y se comprueba que el formato de los campos requeridos sea el adecuado.
- Persistencia de datos en la nube de InfluxDB. Los datos procesados en FastAPI son persistidos en la base de datos temporal InfluxDB, donde pueden filtrarse los registros por url, nombre del producto o nombre del host.
- Visualización y análisis de datos mediante la herramienta en la nube Grafana cloud. Pueden visualizarse gráficas de precio, puntuación y valoraciones a lo largo del tiempo, además de destacar los valores actuales.
- Envío de datos de prueba a través de node-red. Mediante la ejecución de esta herramienta puede probarse el flujo de los datos a través de los diferentes procesos.

## Configurar InfluxDB
1. Asignar los parámetros designados a InfluxDB en el archivo .env.
- Token
- Url
- Organización
- Bucket
2. En el caso de modificar estas variables se ha de configurar una instancia de Grafana adicionalmente (https://grafana.com/docs/grafana/latest/) y vincular esta a InfluxDB.

## Iniciar servicios
1. Dirigirse a la raíz del proyecto.
2. Iniciar el docker compose: ```docker compose up -d```.

## Gestionar productos
1. Dirigirse a la interfaz web localhost:5000
2. Añadir productos: Introducir la URL del producto en la caja de texto y presionar el botón de agregar.
3. Eliminar productos: Presionar el botón de eliminar a la derecha del producto en cuestión, se ha de confirmar el mensaje emergente.
4. Acceder a las diferentes aplicaciones con los links directos.

## Rastrear propiedades de los productos
1. Dirigirse a Grafana Cloud
- https://clauvperlado.grafana.net/, solo las personas añadidas al espacio pueden visualizar el dashboard.
- Alternativamente configurar el conector a InfluxDB (siguiendo los pasos indicados en https://grafana.com/docs/grafana/latest/getting-started/get-started-grafana-influxdb/) y añadir el dashboard ubicado en el directorio /grafana.
2. Dirigirse a los Dashboards y seleccionar el de Productos.
3. Filtrar las visualizaciones mediante los selectores de nombre de producto o host.

## Cerrar servicios
1. Apagar el docker compose: ```docker compose down```.
