# Scrapy settings for seance_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'seance_scrapy'

SPIDER_MODULES = ['seance_scrapy.spiders']
NEWSPIDER_MODULE = 'seance_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'seance_scrapy (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
    'seance_scrapy.pipelines.SeanceScrapyPipeline'
]

# The amount of time (in secs) that the downloader should wait before downloading consecutive pages from the same spider.
DOWNLOAD_DELAY = 2
