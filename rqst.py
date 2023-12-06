import requests
import json
from collections import namedtuple


class Request:

    URL = 'https://api-fns.ru/api/check'
    DATA = namedtuple('data', ['positive', 'negative'])

    def __init__(self, key: str):
        self.key = key


    def get_positive_and_negative(self, inn: str) -> namedtuple:
        '''TODO add a try-exept
        Return namedtuple with positive and negative info'''

        r = requests.get(url=f'{self.URL}?req={inn}&key={self.key}')
        if r.status_code==403:
            raise ConnectionError(f'Warning! Error {r.status_code}')

        if r.status_code==200:
            data = r.json()
            for item in data['items'][0].values():
                positive, negative = json.dumps(item.get('Позитив', {}), ensure_ascii=False), json.dumps(item.get('Негатив', {}), ensure_ascii=False)
            return self.DATA(positive, negative)
