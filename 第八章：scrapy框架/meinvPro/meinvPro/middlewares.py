# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent_list):
        super().__init__()
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agent_list=crawler.settings.get('USER_AGENT_LIST'))

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent
        return None