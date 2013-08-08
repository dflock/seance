#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
# from scrapy.selector import XmlXPathSelector
# from scrapy.spider import BaseSpider

from scrapy.contrib.spiders import SitemapSpider
from seance_scrapy.items import MediumArticle

import datetime

class MediumSpider(SitemapSpider):
    name = "medium"
    allowed_domains = ["medium.com"]
    # start_urls = ["https://medium.com/static/posts.xml"]
    # sitemap_urls = ['https://medium.com/static/posts.xml']
    sitemap_urls = ['https://medium.com/static/posts/posts-2013-07-30.xml']

    items = []

    def parse(self, response):
        # Load posts.xml and churn through it, one article at a time, collecting and populating MediumArticle items as we find them.
        hxs = HtmlXPathSelector(response)

        item = MediumArticle()

        item['url'] = response.url
        item['id'] = hxs.select('//article/@data-post-id').extract()[0]
        item['title'] = hxs.select('//h1[@class="post-title"]/text()').extract()[0]

        item['post_date'] = hxs.select('//div[@class="post-author-card"]//time[@class="post-date"]/text()').extract()[0]
        item['post_date'] = datetime.datetime.strptime(item['post_date'], "%B %d, %Y").date().strftime("%Y-%m-%d")

        item['author_id'] = hxs.select('//article/@data-author').extract()[0]
        item['author_name'] = hxs.select('//article/@data-author-name').extract()[0]

        try:
            item['author_url'] = hxs.select('//div[@class="post-author-card"]//a[@rel="author"]/@href').extract()[0]
        except IndexError:
            item['author_url'] = None


        article_meta = hxs.select('//ul[@class="post-meta"]')
        # Category isn't always set, so don't rely on it being there
        try:
            item['category_name'] = article_meta.select('./li[1]//a[@data-collection-slug]/text()').extract()[0]
        except IndexError:
            item['category_name'] = None

        try:
            item['category_slug'] = article_meta.select('./li[1]//a/@data-collection-slug').extract()[0]
        except IndexError:
            item['category_slug'] = None

        item['min_read'] = article_meta.select('./li[2]//span[@class="reading-time"]/text()').re('\d+')[0]

        self.items.append(item)

        return self.items
