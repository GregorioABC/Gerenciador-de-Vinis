import requests

DISCOGS_TOKEN = "SEU_TOKEN_AQUI"  

def buscar_preco_sugerido(nome_disco):
    url = f"https://api.discogs.com/database/search?q={nome_disco}&token={DISCOGS_TOKEN}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados['results']:
            return dados['results'][0].get('price', 100.0)  
    return None
