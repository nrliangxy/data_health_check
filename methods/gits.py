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
NUMBER_PATTERN = re.compile(u"[\d]")

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


def time_compare(data1, operate, data2):
    """
    时间比较example：
    data1 = {
    'year': 1900,
    'month':1,
    'day':1,
    'hour':0,
    'minute':0,
    'second':0
    }  or '1975-05-21 22:00:00'
    operate = '>='
    data2 = {'year':1990} or '1975-05-21 22:00:00'
    """
    if not all([data1, data2]):
        return False
    if not isinstance(data1, (int, Decimal)):
        if isinstance(data1, str):
            data1 = int(pendulum.parse(data1).timestamp())
        elif isinstance(data1, dict):
            data1 = int(pendulum.create(**format_pendulum(data1)).timestamp())
        else:
            return False
    if not isinstance(data2, (int, Decimal)):
        if isinstance(data2, str):
            data2 = int(pendulum.parse(data2).timestamp())
        elif isinstance(data2, dict):
            data2 = int(pendulum.create(**format_pendulum(data2)).timestamp())
        else:
            return False
    if operate == '<':
        return data1 < data2
    if operate == '==':
        return data1 == data2
    if operate == '<=':
        return data1 <= data2
    if operate == '>':
        return data1 >= data2
    if operate == '>=':
        return data1 >= data2
    return False


def duplicate(value):
    """判断重复条目"""
    if isinstance(value, list):
        return len(value) == len(list(set(value)))
    return False


def between(value, minimum=None, maximum=None):
    """
    判断value值的范围：
    三种用法：
    只给上限：value <= maximum
    只给下限：value >= minimum
    上下限都给：minimum <= value <= maximum
    """
    if minimum is not None and maximum is not None:
        try:
            min_gt_max = minimum > maximum
        except TypeError:
            min_gt_max = maximum < minimum
        if min_gt_max:
            return False
        return minimum <= value <= maximum
    elif minimum is None and maximum is None:
        return False
    else:
        if minimum is not None:
            return value >= minimum
        if maximum is not None:
            return value <= maximum
    return False


def is_empty(value):
    """验证该值是否为空"""
    if value is None:
        return True
    try:
        return len(value) == 0
    except:
        return False


def has_empty_str(data):
    """空字符串判断"""
    if isinstance(data, str):
        data = [data]
    if isinstance(data, list):
        for d in data:
            if not isinstance(d, str):
                return False
            if not d:
                return False
        else:
            return True
    return False

#邮箱
def is_email(value):
    return bool(re.match(EAMIL_PATTERN, value))

#url
def is_url(url):
    return bool(re.match(URL_PATTERN, url))

#过滤非英文新闻
def filter_unenglish_news(content):
    r = '[£！？｡＂＃＄％＆＇（）• ∙＊＋－／：™ ；＜＝＞＠ ®［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.【】、|{}；‘：“，、《》’!"#$%&\'()（）*+,-./:；，;<=>?@[\\]^_`{|}~– ¼ ¾ ½ ]+'
    content = re.sub(r, '', content)
    check = [False for name in content.split() if any(ord(c) > 128 for c in name.split()[0])]
    if len(check) > 0:
        return False
    else:
        return True

#判读师傅包含数字
def is_contain_number(s:str):
    for c in s:
        if re.match(NUMBER_PATTERN, c):
            return True
    return False