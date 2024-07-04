import requests

import json

from config import currencies

class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(base: str, quote: str, base_amount: str):

        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты: {base} , {quote}. Введите различные валюты.')
        try:
            base_ticker = currencies[base.lower()]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена . Введите валюту из списка доступных валют: /currencies')
        try:
            quote_ticker = currencies[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не найдена. Введите валюту из списка доступных валют: /currencies')
        try:
            base_amount = float(base_amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {base_amount}. Введите количество в числовом формате')
        if float(base_amount) < 0:
            raise APIException(f'Не удалось обработать количество: {base_amount}. Количество должно быть > 0')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[currencies[quote]]
        total_base_amount = round(total_base * base_amount, 2)

        return f'{base_amount:.2f} {base_ticker} → {total_base_amount} {quote_ticker}'
