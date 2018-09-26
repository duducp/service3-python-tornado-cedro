import requests

import json
import pika
import time
from random import randrange


def connect():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    global channel
    channel = connection.channel()
    print(' [*] Serviço estabaleceu conexão com RabbitMQ')


def receiver():
    # nome da fila
    channel.queue_declare(queue='request-tj-sp')

    # número de mensagens a ser envia por vez
    channel.basic_qos(prefetch_count=1)

    # Consumindo a fila
    channel.basic_consume(callback_receiver, queue='request-tj-sp')

    print(' [*] Serviço inicializado. Para parar precione CTRL+C')
    channel.start_consuming()


def callback_receiver(ch, method, properties, body):
    time.sleep(randrange(0, 5))
    ch.basic_ack(delivery_tag=method.delivery_tag)

    data = json.loads(body)
    endpoint(data.get('name'))


def endpoint(name):
    _URL = "http://esaj.tjsp.jus.br/cpopg/search.do"
    _PARAMS = {
        'conversationId': '',
        'dadosConsulta.localPesquisa.cdLocal': -1,
        'cbPesquisa': 'NMPARTE',
        'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
        'dadosConsulta.valorConsulta': name
    }

    response = requests.get(url=_URL, params=_PARAMS)
    print(response.status_code)
    print(len(response.content))
    print(response.content[:100])


if __name__ == '__main__':
    try:
        connect()
        receiver()
    except KeyboardInterrupt:
        print('tef')
