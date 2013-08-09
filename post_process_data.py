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
# TODO: Replace this with a central config file.
# CHANGME: change this to match your local MySQL setup
con = MySQLdb.connect(host = "localhost", user = "root", passwd = "dflp4root", db = "seance", cursorclass=MySQLdb.cursors.DictCursor, charset='utf8', use_unicode=True)
# Autocommit defaults to off - this runs much quicker without it but means that
# if you Ctrl + c in the middle, it won't have saved any progress. Uncomment to save as we go along
# con.autocommit(True)

# Separate cursors to the read and insert parts
read_cur = con.cursor()
write_cur = con.cursor()

# Get the articles, only processing one's we haven't provessed yet.
# Uncomment to re-process them all.
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
    # We either want it to dissapear or become a word break, depending
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
    # Remove any remaining puctuation
    raw_text = re.sub(ur"\p{P}+", "", raw_text)

    # Count the words in the text
    words = raw_text.lower().split()
    word_freq = Counter(words)
    word_count = sum(word_freq.values())

    # Save the stats
    write_cur.execute("UPDATE articles SET word_count = %s, word_freq = %s WHERE id = %s", (int(word_count), jsonpickle.encode(word_freq), id))

    # Add the words from this article to the word_frequency summary table
    # Insert new word, or increment count on existing word.
    for word in word_freq:
        write_cur.execute("INSERT INTO word_frequency (word, freq, length) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE freq = freq + %s;", (word, word_freq[word], len(word), word_freq[word]))

    count = count + 1
    print 'updated ' + '{0: >6}'.format(str(count)) + '/' + str(total)

con.commit()