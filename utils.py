import requests

def consulta_cep(cep:str) -> dict:
    ch = ['/', 'c', 'e', 'p', ' ', '-']
    for c in ch:
        if c in cep:
            cep = cep.replace(c, '')
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        resposta = requests.get(url).json()
    except:
        resposta = None
    return resposta
