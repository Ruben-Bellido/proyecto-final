# proyecto-final

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



# Bibliografía
«Recording Time Series Data Via APIs: InfluxDB + FastAPI | by Alex | Level Up Coding». Accedido 23 de abril de 2024. https://levelup.gitconnected.com/recording-time-series-data-via-apis-influxdb-fastapi-d5ba29fb6f18?gi=025a9f1d51d1.
«Request Body - FastAPI». Accedido 23 de abril de 2024. https://fastapi.tiangolo.com/tutorial/body/.
«Use Grafana to query and visualize data stored in InfluxDB | InfluxDB Cloud Serverless Documentation». Accedido 23 de abril de 2024. https://docs.influxdata.com/influxdb/cloud-serverless/process-data/visualize/grafana/?_gl=1*1htdgyg*_ga*MTgzNjAxNTc1MC4xNzAwODIyODc5*_ga_CNWQ54SDD8*MTcxMzg5NTczMC44LjEuMTcxMzg5NTc0OC40Mi4wLjU3NzAyNDgwMw..
