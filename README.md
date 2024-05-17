# proyecto-final

## Pasos seguidos
- Levantar docker-compose
- Acceder a Mage.ai con las claves de acceso premeditadas, la [documentación](https://docs.mage.ai/production/authentication/overview)
	usuario: admin@admin.com
    contraseña: admin

## Librerías
Para la libreria de MySQL usar: 
    ```bash 
    pip install mysql-connector-python==8.3.0
    ```

Para ejecutar FastAPI: 
    ```
    uvicorn api_config:app --reload
    ```
para descargar grafa:
```bash
sudo apt-get install -y adduser libfontconfig1 musl
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_10.4.2_amd64.deb
sudo dpkg -i grafana-enterprise_10.4.2_amd64.deb
```
abrir grafana, dashboard ejemplo: https://clauvperlado.grafana.net/goto/LPiF9NBIR?orgId=1

## Recursos
FastAPI body fields para comprobar datos:
https://fastapi.tiangolo.com/tutorial/body-fields/#__tabbed_1_1

https://www.amazon.es/Angles-Horn-Tocadiscos-Bluetooth-preamplificador/dp/B09CRJ4CB3/?_encoding=UTF8&_encoding=UTF8&ref_=dlx_deals_sc_dcl_img_dt_dealz_m1&pd_rd_w=Klvc1&content-id=amzn1.sym.e45ac59e-9108-446a-aadb-27a97420a75d&pf_rd_p=e45ac59e-9108-446a-aadb-27a97420a75d&pf_rd_r=1CMRY1PH8G29RCW4M3FC&pd_rd_wg=GzeDn&pd_rd_r=a95c7e3c-c007-4cab-8aed-cf21b6ebc140

Conectar fast api a influxdb:
https://levelup.gitconnected.com/recording-time-series-data-via-apis-influxdb-fastapi-d5ba29fb6f18

Pipelines para automatizar la recolección: airflow, mageai (más sencillo)
Amazon API?
Generación de datos: fakerjs

# Bibliografía
«Recording Time Series Data Via APIs: InfluxDB + FastAPI | by Alex | Level Up Coding». Accedido 23 de abril de 2024. https://levelup.gitconnected.com/recording-time-series-data-via-apis-influxdb-fastapi-d5ba29fb6f18?gi=025a9f1d51d1.
«Request Body - FastAPI». Accedido 23 de abril de 2024. https://fastapi.tiangolo.com/tutorial/body/.
«Use Grafana to query and visualize data stored in InfluxDB | InfluxDB Cloud Serverless Documentation». Accedido 23 de abril de 2024. https://docs.influxdata.com/influxdb/cloud-serverless/process-data/visualize/grafana/?_gl=1*1htdgyg*_ga*MTgzNjAxNTc1MC4xNzAwODIyODc5*_ga_CNWQ54SDD8*MTcxMzg5NTczMC44LjEuMTcxMzg5NTc0OC40Mi4wLjU3NzAyNDgwMw..
>>>>>>> 80a3b8f86ba7e3cf1af0c2b98f5d863ca760480c
