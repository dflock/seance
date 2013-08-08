#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
# from scrapy.selector import XmlXPathSelector
# from scrapy.spider import BaseSpider

from scrapy.contrib.spiders import SitemapSpider

from seance_scrapy.items import MediumArticle

class MediumSpider(SitemapSpider):
    name = "medium"
    allowed_domains = ["medium.com"]
    start_urls = ["https://medium.com/static/posts.xml"]
    # sitemap_urls = ['https://medium.com/static/posts.xml']
    sitemap_urls = ['https://medium.com/static/posts/posts-2013-07-30.xml']

    items = []

    def parse(self, response):
        # Load posts.xml and churn through it, one article at a time, collecting and populating MediumArticle items as we find them.
        hxs = HtmlXPathSelector(response)

        item = MediumArticle()

        item['url'] = response.url
        item['title'] = hxs.select('//h1[@class="post-title"]/text()').extract()
        item['desc'] = hxs.select('//meta[@name="description"]/text()').extract()

        article_meta = hxs.select('//ul[@class="post-meta"]')
        item['author_name'] = article_meta.select('.//li[1]/a[1]/text()').extract()
        item['min_read'] = article_meta.select('.//li[2]//span[@class="reading-time"]/text()').re('\d+')

        self.items.append(item)

        return self.items
