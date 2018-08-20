# -*- coding: utf-8 -*-
import scrapy

from quotespider.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'Quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('.quote'):
            item = QuotesItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            author_link = 'http://quotes.toscrape.com' + quote.css('span a::attr(href)').extract_first()
            tags = quote.css('.tags .tag::text').extract()

            item['text'] = text
            item['author'] = author
            item['author_link'] = author_link
            item['tags'] = tags

            yield item

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
