# -*- coding: utf-8 -*-
from configparser import ConfigParser
import os
import requests
import telebot
from utils import consulta_cep


PROD = True

if PROD is False:
    cfg = ConfigParser()
    cfg.read('config.ini')
    TOKEN = cfg.get('bot', 'token')
    WEATHER_API_KEY = cfg.get('api_keys', 'clima')
else:
    TOKEN = os.environ.get('TOKEN')
    WEATHER_API_KEY = os.environ.get('CLIMA')

LAT = '-48.8241'
LONG = '-26.901'


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def boas_vindas(message):
    msn = (f'Olá Jovem, bem-vindo ao bot da Juventude do Baú!\n'
           f'Comandos disponíveis:\n'
           f'/start ou /help -> Exibe esta ajuda\n'
           f'/tempo ou /clima -> Exibe dados metereológicos do baú\n'
           f'/cep 88320-000 -> para consultar cep')
    bot.reply_to(message, msn)


@bot.message_handler(commands=['tempo', 'clima'])
def clima(message):
    '''Informa a previsão do tempo'''
    url = 'http://api.openweathermap.org/data/2.5/weather?' \
        'q={}&units={}&lang={}&appid={}'.format('Ilhota,BR', 'metric',
                                                'pt', WEATHER_API_KEY)
    r = requests.get(url)
    descricao = r.json()['weather'][0]['description'].title()
    # icone = r.json()['weather'][0]['icon']
    tempo = r.json()['main']
    temperatura = str(tempo['temp'])
    maxima = str(tempo['temp_max'])
    minima = str(tempo['temp_min'])

    prev = '{}\n' \
           u'Temperatura: {}°\n' \
           u'Pressão: {}hPa\n' \
           u'Humidade: {}%\n' \
           u'Máxima: {}°\n' \
           u'Mínima: {}°'.format(descricao, temperatura, tempo['pressure'],
                                 tempo['humidity'], maxima, minima)
    bot.reply_to(message, prev)


@bot.message_handler(commands=['cep'])
def cep(message):
    re = consulta_cep(message.text)
    if re is not None:
        rp = (f'Estado: {re["uf"]}\n'
              f'Cidade: {re["localidade"]}\n'
              f'Bairro: {re["bairro"]}\n'
              f'Rua: {re["logradouro"]}')
    else:
        rp = 'Desculpe não encontrei esse CEP :('
    bot.reply_to(message, rp)


bot.polling()
