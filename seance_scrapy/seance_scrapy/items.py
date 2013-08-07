# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MediumArticle(Item):
    title = Field()
    url = Field()
    desc = Field()
    author_name = Field()
    min_read = Field()