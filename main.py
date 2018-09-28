import re

import requests

from bs4 import BeautifulSoup

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
    _queue = 'response'
    channel.queue_declare(queue=_queue)

    # converte o objeto para o tipo json (decodifica)
    message_rabbit_mq = json.dumps(obj)

    # envia o objeto para a fila
    channel.basic_publish(exchange='', routing_key=_queue, body=message_rabbit_mq)


def receiver():
    # define o nome da fila
    _queue = 'request-tj-sp'
    channel.queue_declare(queue=_queue)

    # número de mensagens a ser envia por vez
    channel.basic_qos(prefetch_count=1)

    # consome a fila (recebe os dados da fila)
    channel.basic_consume(callback_receiver, queue=_queue)

    print(' [*] Serviço inicializado. Para parar precione CTRL+C')
    channel.start_consuming()


def callback_receiver(ch, method, properties, body):
    time.sleep(randrange(0, 5))
    ch.basic_ack(delivery_tag=method.delivery_tag)

    data = json.loads(body)
    response = endpoint(data.get('name'))

    # Extrai os dados do content
    soup = BeautifulSoup(response.text, 'html.parser')
    processes = soup.find_all("a", class_="linkProcesso")

    if not processes:
        process_number = 'Nada Encontrado'
        process_link = 'Nada Encontrado'
    else:
        process_number = processes[0].get_text().strip()
        process_link = processes[0].get('href').strip()

    response = json.dumps({'numero_processo': process_number, 'link': process_link, 'dominio': _DOMAIN})

    obj = {
        'name': data.get('name'),
        'id': data.get('id'),
        'response': response
    }

    send(obj)


def endpoint(name):
    try:
        global _DOMAIN
        _DOMAIN = "http://esaj.tjsp.jus.br"
        _URL = _DOMAIN + "/cpopg/search.do"
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
