#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors


class SeanceScrapyPipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='seance',
                user='root', passwd='dflp4root', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        tx.execute("select * from articles where id = %s", (item['id']))
        result = tx.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item['id'], level=log.DEBUG)
        else:
            tx.execute("insert into articles (id, title, url, post_date, description, body, author_id, author_name, author_url, min_read, category_slug, category_name) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item['id'], item['title'], item['url'], item['post_date'], item['description'], item['body'], item['author_id'], item['author_name'], item['author_url'], item['min_read'], item['category_slug'], item['category_name'])
            )
            log.msg("Item stored in db: %s" % item['id'], level=log.INFO)


    def handle_error(self, e):
        log.err(e)
