import re
import pendulum
from decimal import Decimal

EAMIL_PATTERN = re.compile(r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$")
URL_PATTERN = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def format_pendulum(data):
    assert isinstance(data, dict)
    template = {
        'year': 1900,
        'month': 1,
        'day': 1,
        'hour': 0,
        'minute': 0,
        'second': 0
    }
    _data = {}
    for key in template.keys():
        _data[key] = data.get(key) or template[key]
    return _data
