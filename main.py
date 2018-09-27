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
    # define o nome da fila
    channel.queue_declare(queue='response')

    # converte o objeto para o tipo json (decodifica)
    message_rabbit_mq = json.dumps(obj)

    # envia o objeto para a fila
    channel.basic_publish(exchange='', routing_key='response', body=message_rabbit_mq)


def receiver():
    # define o nome da fila
    channel.queue_declare(queue='request-tj-sp')

    # número de mensagens a ser envia por vez
    channel.basic_qos(prefetch_count=1)

    # consome a fila (recebe os dados da fila)
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
    try:
        _URL = "http://esaj.tjsp.jus.br/cpopg/search.do"
        _PARAMS = {
            'conversationId': '',
            'dadosConsulta.localPesquisa.cdLocal': '-1',
            'cbPesquisa': 'NMPARTE',
            'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
            'dadosConsulta.valorConsulta': name
        }

        req = requests.get(url=_URL, params=_PARAMS)
        return req
    except requests.exceptions.Timeout:
        return 'O site TJSP não está respondendo'
    except requests.exceptions.TooManyRedirects:
        return 'A URL informada parece não estar correta'
    except requests.exceptions.RequestException as e:
        return 'Ocorreu um erro ao buscar as informações no site TJSP'


if __name__ == '__main__':
    try:
        connect()
        receiver()
    except KeyboardInterrupt:
        connection.close()
