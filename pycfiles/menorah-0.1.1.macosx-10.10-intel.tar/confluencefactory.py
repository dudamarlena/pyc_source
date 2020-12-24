# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/menorah/confluencefactory.py
# Compiled at: 2015-10-24 23:22:30
from confluence import Confluence

def create(streamIds, **kwargs):
    """
  Creates and loads data into a Confluence, which is a collection of River 
  Streams.
  :param streamIds: (list) Each data id in this list is a list of strings:
                    1. river name
                    2. stream name
                    3. field name 
  :param kwargs: Passed into Confluence constructor
  :return: (Confluence)
  """
    print 'Creating Confluence for the following RiverStreams:\n\t%s' % (',\n\t').join([ (':').join(row) for row in streamIds ])
    confluence = Confluence(streamIds, **kwargs)
    confluence.load()
    return confluence