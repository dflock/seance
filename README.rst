Welcome to the Séance!
=========================

Taking a little peek behind the curtain at medium.com - Just for fun.

Features
----------

Scrape medium.com to compile and display some data about activity on the site. It currently collects and displays the following things:

- Totals: Authors, Articles, Words, Reading Time, Avg Words Per Article
- Articles published over time, by Year, by Day of the Week
- The first ever and most recent articles
- Most prolific authors: By Articles Published, By Words Published, By Time to Read
- Most Popular Words: Work Frequency by: All words, Medium Words (5-7 chars), Long Words (> 7 chars), V. Long Words (> 10 chars), Danke, Deutschland: (> 20 chars)
- Word Frequency by Word Length

It uses `scrapy <http://scrapy.org/>`_ for the crawling, `pygreen <http://pygreen.neoname.eu/>`_ to generate the static frontend page and MySQL to store everything.

Frontend
---------

The interesting bit! See the results here: http://dflock.github.io/seance/

Running It
-----------

Don't - it's against Medium.com's T&C's. Also, it takes ages and doesn't work very well yet.

If you really want to, you'll need a vitrualenv with the stuff from ``requirements.txt`` installed in it and *lots* of patience. Here's the basic idea:

- Create the MySQL database using ``/db/re-create-db.sql``
- Change the MySQL login credentials in the following files to match your setup (yes, I know):
  - post_process_data.py
  - frontend/index.html
  - seance_scrapy/seance_scrapy/pipelines.py

- To start the crawl:

.. code-block:: console

    $ cd seance_scrapy
    $ scrapy crawl medium

- Once this finishes (I left it overnight and it didn't, so good luck - see below), run the ``post_process_data.py`` to calculate the word frequency data. you can press Ctrl + c to abort the crawl at any point.
- Then do this to generate the frontend/report page, putting it into the ``/output`` folder:

.. code-block:: console

    $ cd frontend
    $ pygreen gen ../output/


TODO
--------

I made a mistake by relying on the scrapy sitemap crawler - either I'm using it wrong, medium.com's sitemaps overlap/duplicate themselves a lot, or it crawls *way* more stuff that it needs to. In light of that, and a desire for less magic and the ability to cleanly and efficiently re-start things where they left off, I want to rewrite the crawler part of this:

Rewrite crawler & break into two parts:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- One that crawls the medium.com sitemap.xml tree and records a list of article urls in the db, along with a last_crawled timestamp
  - Also needs to record a list of sitemap files, along with a timestamp
- Another that works through that list and crawls the articles, records the stats & updates the last_crawled timestamp

Other minor issues:
^^^^^^^^^^^^^^^^^^^^^

- Add information on number of comments
- I couldn't find anything in the article markup to specify the language the article is written in - maybe have another look?
- The XPath for importing categories isn't working.