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
        return not is_empty(title) and between(len(title), 16, 230) and filter_unenglish_news(title)
    
    @classmethod
    def valid_source_url(cls, source_url, **kwargs):
        return is_url(source_url)
    
    @classmethod
    def valid_news_id(cls, news_id, **kwargs):
        return not is_empty(news_id)
    
    @classmethod
    def valid_content(cls, content, **kwargs):
        return not is_empty(content) and between(len(content), 200, 55000) and not cls.is_multimedia_inside(
            content) and filter_unenglish_news(content[:20])
    
    @classmethod
    def valid_tags(cls, tags, **kwargs):
        return True if tags is None else (duplicate(tags) and not is_empty(tags))
    
    @classmethod
    def valid_categories(cls, categories, **kwargs):
        return True if categories is None else (duplicate(categories) and not is_empty(categories))
    
    @classmethod
    def valid_authors(cls, authors, **kwargs):
        return True if authors is None else (duplicate(authors) and not is_empty(authors))
    
    @classmethod
    def valid_post_ti(cls, post_ti, **kwargs):
        post_time = datetime.datetime.utcfromtimestamp(kwargs['post_ts'])
        same_post = (
        post_time.year == post_ti['year'] and post_time.month == post_ti['month'] and post_time.day == post_ti['day'])
        return same_post
    
    @classmethod
    def valid_source_categories(cls, source_categories, **kwargs):
        return duplicate(source_categories) and not is_empty(source_categories)
