# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/quran/urls.py
# Compiled at: 2009-12-07 18:34:22
from django.conf.urls.defaults import *
urlpatterns = patterns('quran.views', ('^$', 'index'), ('^(?P<sura_number>\\d+)/$',
                                                        'sura'), ('^(?P<sura_number>\\d+)/(?P<aya_number>\\d+)/$',
                                                                  'aya'), ('^(?P<sura_number>\\d+)/(?P<aya_number>\\d+)/(?P<word_number>\\d+)/$',
                                                                           'word'), ('^lemma/(?P<lemma_id>\\d+)/$',
                                                                                     'lemma'), ('^root/(?P<root_id>\\d+)/$',
                                                                                                'root'), ('^root/$',
                                                                                                          'root_index'))