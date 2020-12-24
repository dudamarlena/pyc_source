# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/models/analysis.py
# Compiled at: 2020-01-02 09:27:00
# Size of source mod 2**32: 478 bytes
from .model import Model
from ..endpoints import API_PATH

class Analysis(Model):

    def domain(self, domain):
        """Request the PhishDetect Node to statically analyse a domain name.
        :param domain: Domain to analyse.
        """
        return self._phishdetect.post((API_PATH['analysis_domain']), json={'url': domain})