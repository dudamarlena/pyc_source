# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/web/config.py
# Compiled at: 2015-07-08 07:34:06
from __future__ import absolute_import, division, print_function
from gensim import models
from dossier.models.openquery.google import Google
import dossier.web as web

class Config(web.Config):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self._tfidf = None
        return

    @property
    def config_name(self):
        return 'dossier.models'

    def normalize_config(self, config):
        super(Config, self).normalize_config(config)
        try:
            tfidf_path = self.config['tfidf_path']
        except KeyError:
            self._tfidf = False
        else:
            self._tfidf = models.TfidfModel.load(tfidf_path)

    @property
    def tfidf(self):
        return self._tfidf

    @property
    def google(self):
        api_key = self.config.get('google_api_search_key')
        if api_key is None:
            return
        else:
            return Google(api_key)