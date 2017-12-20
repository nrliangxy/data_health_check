from methods.gits import *
from base.main import BaseHealthCheck
import time, datetime, pendulum


class NewsHealthCheck(BaseHealthCheck):
    MUST_REQUIRE_FIELD_SET = {"title", "source_url", "content", "source_categories", "post_ti"}
    
    # limit the content's long
    @classmethod
    def is_length_over_limit(cls, content, limit=5000):
        return len(content.split()) > limit
    
    @classmethod
    def is_multimedia_inside(cls, content):
        keywords = [
            "<((/|[a-zA-Z]){1})|(.*>$)",
            "image credit$", "contact us$", "about us$", "@",
            ".img", ".image", ".jpg", ".jpeg", ".bmp",
            ".mp3", ".aac", ".wma", ".flac", "404",
        ]
        regex = '|'.join(["({})".format(word) for word in keywords])
        return True if re.match(regex, content.lower()) else False
    
    @classmethod
    def is_length(cls, data, operate, num):
        def _is_length(_data):
            _data = len(_data)
            if operate == '<':
                return _data < num
            if operate == '<=':
                return _data <= num
            if operate == '>':
                return _data > num
            if operate == '>=':
                return _data >= num
            return False
        
        if not isinstance(data, list):
            data = [data]
        for d in data:
            if not _is_length(d):
                return False
        return True
    
    @classmethod
    def is_time_duration(cls, data):
        if isinstance(data, int) or isinstance(data, Decimal):
            return -2208988800 < int(data) < int(time.time())
        if isinstance(data, datetime.datetime):
            return datetime.datetime(year=1900, month=1, day=1) < data < datetime.datetime.now()
        if isinstance(data, str):
            try:
                return pendulum.create(1900, 1, 1, 0, 0, 0, 0) < pendulum.parse(data) < pendulum.now('UTC')
            except:
                return False
        if isinstance(data, dict):
            data = pendulum.create(**format_pendulum(data))
            return pendulum.create(1900, 1, 1) < data < pendulum.now('UTC')
    
    @classmethod
    def valid_title(cls, title, **kwargs):
        return not is_empty(title) and between(len(title), 16, 230)
