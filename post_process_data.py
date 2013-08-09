#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import Counter
import jsonpickle

#
# Run through all the articles and compute word count & frequency and store results back into DB
#

# Setup DB connection
import MySQLdb.cursors

con = MySQLdb.connect(host = "localhost", user = "root", passwd = "dflp4root", db = "seance", cursorclass=MySQLdb.cursors.DictCursor, charset='utf8', use_unicode=True)
# con.autocommit(True)
read_cur = con.cursor()
write_cur = con.cursor()

# Get the articles
# read_cur.execute("select id, body from articles")
read_cur.execute("select id, body from articles where word_count is NULL")
total = read_cur.rowcount
count = 0

for i in range(total):
    row = read_cur.fetchone()
    id, raw_text = row['id'], row['body'].encode('ascii', 'xmlcharrefreplace')

    # TODO: compile these regexes
    # Process the text to remove entities
    entities = r'\&\#?.+?;'
    raw_text = raw_text.replace('&nbsp;', ' ')
    raw_text = re.sub(entities, '', raw_text)

    # Process the text to remove punctuation
    raw_text = raw_text.replace('.', ' ')
    raw_text = raw_text.replace(',', ' ')
    raw_text = raw_text.replace('-', ' ')
    raw_text = raw_text.replace('_', ' ')
    raw_text = raw_text.replace('/', ' ')
    raw_text = raw_text.replace(')', '')
    raw_text = raw_text.replace('(', '')
    raw_text = raw_text.replace('!', '')
    raw_text = raw_text.replace('?', '')
    raw_text = raw_text.replace(':', '')
    raw_text = raw_text.replace('#', '')
    raw_text = raw_text.replace('$', '')
    raw_text = raw_text.replace('"', '')
    raw_text = raw_text.replace("'", '')
    raw_text = re.sub(ur"\p{P}+", "", raw_text)

    # Count the words in the text
    words = raw_text.lower().split()
    word_freq = Counter(words)
    word_count = sum(word_freq.values())

    # print id
    # print word_count
    # print word_freq

    # Save the stats
    write_cur.execute("update articles set word_count = %s, word_freq = %s where id = %s", (int(word_count), jsonpickle.encode(word_freq), id))

    # Add the words from this article to the word_frequency summary table
    # print word_freq
    for word in word_freq:
        # print word, word_freq[word]
        write_cur.execute("INSERT INTO word_frequency (word, freq, length) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE freq = freq + %s;", (word, word_freq[word], len(word), word_freq[word]))
    # print sum(word_freq.values())

    count = count + 1
    print 'updated ' + '{0: >6}'.format(str(count)) + '/' + str(total)

con.commit()