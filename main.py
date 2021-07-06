from parser import Parser, Parser_Zonaprops
import smtplib
import requests
import os
from dotenv import load_dotenv
import json


def filter_data():
    # filters = []
    with open('data.json') as file:
        data = json.load(file)
        lower_price = 9999999999
        selected_prop = {
                'url': '',
                'price': 0,
                }
        for prop in data:
            current_price = int(data[prop]['price'].replace('.', ''))
            if data[prop]['coin'] == 'U$S':
                # convert dolar price in to argentinians pesos
                # We should have an env var for conversion
                current_price = current_price * 160
            if current_price < lower_price:
                selected_prop['url'] = data[prop]['url']
                selected_prop['price'] = current_price
                lower_price = current_price
        print(lower_price)
        return selected_prop


def send_notification(telegram_id=None, content=''):

    if telegram_id:
        print(f'Sending telegram notification to {telegram_id}')
        load_dotenv()
        telegram_token = os.getenv("TELEGRAM_TOKEN")
        dest = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        data = {
                'chat_id': telegram_id,
                'text': content,
                }

        req = requests.post(dest, data)
        if req.ok:
            print("SUCCESS")
            return True
        else:
            print(req.text)
            return False


def main():
    selected_prop = filter_data()
    quarter = "TEST_ZONE"
    price = selected_prop['price']
    link = selected_prop['url']
    data = f"I've found a nice place for you in {quarter}. Price ${price}. "\
           f"Follow the link for more information {link}"
    # send_notification('1090248198', content=data)
    send_notification('-593008804', content=data)
    return 0


# uncomment for test with the interactive shell ( python -i main.py ):

meliprops = Parser(
    website='https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/capital-federal', # noqa
    soup_tag='a',
    next_page_path='/_Desde_',
    starts_with='https://departamento.mercadolibre.com.ar/MLA',
    page_limit=0,
    next_page_index=48,
)


argenprop = Parser(
    website='https://www.argenprop.com/departamento-alquiler-localidad-capital-federal', # noqa
    soup_tag='a',
    next_page_path='-pagina-',
    starts_with='/departamento-en-alquiler',
    page_limit=2,
    next_page_index=1,
)
