# Terceiro Serviço

#### Descrição
Esse serviço é reponsavel por:
- ouvir a fila "request-tj-sp"
- ir até o site TJSP e pesquisar os processos da pessoa informada
- inserir em outra fila chamada "response", o número do processo e o link para acessá-lo

## Como utilizar
Após o clone do projeto você deve instalar os pacotes necessários. Para isso rode o comando abaixo no terminal:

```
pip install -r requirements.txt
```

Após a instalação dos pacotes execute o comando abaixo para inicar o servidor:

```
python main.py
```

Obs.: Você deve estar no diretório do projeto.

## Instalação do RabbitMq
1º Instalar o [OTP](http://www.erlang.org/downloads);

2º Instalar o [Rabbitmq Server](https://www.rabbitmq.com/download.html):

- Iniciar o cmd do rabbitmq e digitar o comando: rabbitmq-plugins enable rabbitmq_management
- Rodar o executavel que inicia o serviços

```
Url do painel: http://localhost:15672
Usuário: guest
Senha: guest
```

Mais detalhes: https://www.rabbitmq.com/install-windows-manual.html

Primeiros passos: https://blog.ateliedocodigo.com.br/primeiros-passos-com-rabbitmq-e-python-938fb0957019