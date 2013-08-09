Scrape medium.com & compile stats.

Features
===========

- # of articles published: total, per author
- # of authors
- # of words published: total, per author
- # of mins reading time: total, per author
- Word cloud

TODO
======

- Rewrite crawler & break into two:
    - One that crawls the sitemap tree and records a list of article urls in the db. along with a last_crawled timestamp
        - Also needs to record a list of processes sitemap files
    - Another that works through that list and crawls the articles, records the stats & updates the last_crawled timestamp
- Add information on number of comments
- I couldn't find anything in the article markup to specify the language the article is written in - maybe have another look?
- The XPath for importing categories isn't working.