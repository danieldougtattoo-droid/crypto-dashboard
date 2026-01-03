import requests

COIN_GECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTOS = ["bitcoin", "ethereum"]
VS_CURRENCIES = "usd"
TIMEOUT = 10

def get_crypto_prices():
    """
    Busca preços das criptomoedas configuradas.
    Retorna:
        tuple: (bitcoin, ethereum) - Preços em USD
    """
    params = {
        "ids": ",".join(CRYPTOS),
        "vs_currencies": VS_CURRENCIES
    }

    try:
        response = requests.get(COIN_GECKO_API_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        return _extract_prices(data)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro de conexão com a API: {e}")
    except KeyError as e:
        raise ValueError(f"Erro ao processar dados da API. Chave não encontrada: {str(e)}")

def _extract_prices(data: dict) -> tuple:
    """Extrai e valida os preços retornados pela API."""
    for crypto in CRYPTOS:
        if crypto not in data:
            raise ValueError(f"Criptomoeda {crypto} não encontrada na resposta: {data}")
    
    bitcoin = data["bitcoin"][VS_CURRENCIES]
    ethereum = data["ethereum"][VS_CURRENCIES]
    
    return bitcoin, ethereum


    