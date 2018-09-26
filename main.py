import requests


def endpoint(name):
    URL = "http://esaj.tjsp.jus.br/cpopg/search.do"
    PARAMS = {
        'conversationId': '',
        'dadosConsulta.localPesquisa.cdLocal': -1,
        'cbPesquisa': 'NMPARTE',
        'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
        'dadosConsulta.valorConsulta': name
    }

    response = requests.get(URL, params=PARAMS)
    print(response.status_code)
    print(len(response.content))
    print(response.content[:100])


if __name__ == '__main__':
    endpoint('Carlos Eduardo da silva dorneles')
