# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MediumArticle(Item):
    id = Field()
    title = Field()
    url = Field()
    post_date = Field()

    author_id = Field()
    author_name = Field()
    author_url = Field()

    min_read = Field()

    category_name = Field()
    category_slug = Field()