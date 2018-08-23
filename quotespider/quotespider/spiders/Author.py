# -*- coding: utf-8 -*-
import scrapy

from quotespider.items import AuthorItem


class AuthorSpider(scrapy.Spider):
    name = 'Author'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        item = AuthorItem()

        item['name'] = extract_with_css('h3.author-title::text')
        item['birthdate'] = extract_with_css('.author-born-date::text')
        item['bio'] = extract_with_css('.author-description::text')
        yield item
