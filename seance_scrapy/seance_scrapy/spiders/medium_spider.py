#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from seance_scrapy.items import MediumArticle

class MediumSpider(BaseSpider):
    name = "medium"
    allowed_domains = ["medium.com"]
    start_urls = [
        "https://medium.com/"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//article')
        items = []
        for site in sites:
            item = MediumArticle()

            item['title'] = site.select('.//h3/a/text()').extract()
            item['url'] = site.select('.//h3/a/@href').extract()
            item['desc'] = site.select('.//a[@class="post-item-snippet"]/p/text()').extract()

            article_meta = site.select('.//ul[@class="post-item-meta"]')
            item['author_name'] = article_meta.select('.//li[1]/a[1]/text()').extract()
            item['min_read'] = article_meta.select('.//li[2]//span[@class="reading-time"]/text()').re('\d+')
            items.append(item)

        return items
