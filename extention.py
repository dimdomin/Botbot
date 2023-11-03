import requests
import json
from config import cash


class APIConverter(Exception):
    pass

class Cryptoconverter:
    @staticmethod
    def convert(quote : str, base : str, amount : str):
        if quote == base:
            raise APIConverter(f"Невозможно ввести одинаковые валюты {base}")

        try:
            quote_ticker = cash[quote]
        except KeyError:
            raise APIConverter(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = cash[base]
        except KeyError:
            raise APIConverter(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except KeyError:
            raise APIConverter(f"Не удалось обработать колличество {amount}")
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[cash[base]]
        return total_base