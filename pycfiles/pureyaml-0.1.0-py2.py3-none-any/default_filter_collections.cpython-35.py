# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filter_collection/default_filter_collections.py
# Compiled at: 2018-08-07 00:26:58
# Size of source mod 2**32: 1278 bytes
__doc__ = 'default document filter collection'
import os
from .base_filter_collection import BaseFilterCollection
from purewords.filters import url_filter
from purewords.filters import time_filter
from purewords.filters import phone_filter
from purewords.filters import title_filter
from purewords.filters import abbreviation_filter
from purewords.filters import angle_brackets_filter
from purewords.filters import blank_filter
from purewords.filters import token_number_filter
from purewords.filters import StopwordsFilter
document_filters = BaseFilterCollection()
document_filters.add(url_filter)
document_filters.add(blank_filter)
document_filters.add(time_filter)
document_filters.add(phone_filter)
document_filters.add(title_filter)
document_filters.add(abbreviation_filter)
document_filters.add(angle_brackets_filter)
filter_collection_path = os.path.abspath(__file__)
filter_collection_dir = os.path.dirname(filter_collection_path)
stopwords_path = os.path.join(filter_collection_dir, '../configs/stopwords.txt')
with open(stopwords_path, 'r') as (stopwords_file):
    stopwords_set = set(stopwords_file.read().splitlines())
document_filters.add(StopwordsFilter(stopwords_set))
token_filters = BaseFilterCollection()
token_filters.add(token_number_filter)