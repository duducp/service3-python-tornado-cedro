import requests

import json
import pika
import time
from random import randrange


def connect():
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    global channel
    channel = connection.channel()
    print(' [*] Serviço estabaleceu conexão com RabbitMQ')


def send(obj):
    # Cria a fila
    channel.queue_declare(queue='response')

    message_rabbit_mq = json.dumps(obj)

    # envia a mensagem para a fila
    channel.basic_publish(exchange='', routing_key='response', body=message_rabbit_mq)


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
    response = endpoint(data.get('name'))

    obj = {
        'name': data.get('name'),
        'id': data.get('id'),
        'response': response.text
    }

    send(obj)


def endpoint(name):
    _URL = "http://esaj.tjsp.jus.br/cpopg/search.do"
    _PARAMS = {
        'conversationId': '',
        'dadosConsulta.localPesquisa.cdLocal': -1,
        'cbPesquisa': 'NMPARTE',
        'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
        'dadosConsulta.valorConsulta': name
    }

    req = requests.get(url=_URL, params=_PARAMS)
    return req


if __name__ == '__main__':
    try:
        connect()
        receiver()
    except KeyboardInterrupt:
        connection.close()
