from config import BASESCAN_URL, BASE_API_KEYS
import random


def make_api_url(module,
                 action: str,
                 address: str,
                 **kwargs) -> str:
    """
    Создает URL для отправки запроса к API blockscan
    :param module: Module for api
    :param action: Action for api
    :param address: wallet address
    :param kwargs: other arguments
    :return: Готовый url для отправки запроса
    """
    url = BASESCAN_URL + f'?module={module}' \
                         f'&action={action}' \
                         f'&address={address}' \
                         f'&tag=latest' \
                         f'&apikey={random.choice(BASE_API_KEYS)}'

    if kwargs:
        for key, value in kwargs.items():
            url += f'&{key}={value}'

    return url
