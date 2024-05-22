if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
import requests

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    for json_data in data:
        try:
            # URL del endpoint FastAPI
            url = "http://fastapi:8000/products"
            # Envía la petición POST con los datos
            response = requests.post(url, json=json_data)
            # Debug para comprobar el estado de la petición
            if response.status_code == 200:
                print("Petición POST exitosa")
            else:
                print(f"Error en la petición POST. Código de estado: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error en la conexión: {e}")
