import requests

def get_usd_to_brl():
    """
    Busca a cotação do dólar para o real."""

    url = "https://api.FrankFurter.app/latest"
    params = {
        "from": "USD",
        "to": "BRL"
    }

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data['rates']['BRL']

