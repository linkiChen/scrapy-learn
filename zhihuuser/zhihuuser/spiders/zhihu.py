# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Spider, Request

from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'excited-vczh'

    # 用户详情url
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

    # 关注用户url
    follows_url = 'https://www.zhihu.com/api/v4/members/{follow_user}/followees?include={follow_include}offset={offset}&limit={limit}'
    follow_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&'

    # 关注者(粉丝)
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}offset={offset}&limit={limit}'
    followers_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&'

    def start_requests(self):
        # 用户详细信息
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        yield Request(
            self.follows_url.format(follow_user=self.start_user, follow_include=self.follow_query, offset=0, limit=20),
            callback=self.parse_follow)
        yield Request(
            self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),
            callback=self.parse_follower)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        # 获取当前用户的关注列表,递归获取关注列表用户的关注者信息
        yield Request(
            self.follows_url.format(follow_user=result.get('url_token'), follow_include=self.follow_query, offset=0,
                                    limit=20), callback=self.parse_follow)

    def parse_follow(self, response):
        results = json.loads(response.text)
        # 循环获取当前页的关注用户url_token ,使用url_token获取用户的详情信息
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              callback=self.parse_user)
        # 若有下一页的关注者列表，则获取下一页的关注列表url
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, self.parse_follow)

    def parse_follower(self, response):
        results = json.loads(response.text)
        # 循环获取当前页的关注用户url_token ,使用url_token获取用户的详情信息
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              callback=self.parse_user)
        # 若有下一页的关注者列表，则获取下一页的关注列表url
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, self.parse_follower)
