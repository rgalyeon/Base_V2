from config import BASESCAN_URL, BASESCAN_API_KEY


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
                         f'&apikey={BASESCAN_API_KEY}'

    if kwargs:
        for key, value in kwargs.items():
            url += f'&{key}={value}'

    return url
