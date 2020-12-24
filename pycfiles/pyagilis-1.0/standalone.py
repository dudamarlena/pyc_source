# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyaggregator/standalone.py
# Compiled at: 2007-04-30 07:48:57
from elixir import *
metadata.connect('mysql://root@localhost:3306/pyaggregator')
from pyaggregator.aggregator import Aggregator
from pyaggregator.elixirsupport import ElixirAggregatorMixin
from pyaggregator.elixirsupport import Feed
create_all()

class MyAggregator(ElixirAggregatorMixin, Aggregator):
    __module__ = __name__


tags = {}
options = {'verbose': True, 'reraiseentryexceptions': True}
processor = MyAggregator(**options)
for feed in Feed.select():
    processor.process_feed(feed)

objectstore.flush()