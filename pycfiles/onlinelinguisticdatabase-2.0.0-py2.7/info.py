# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/info.py
# Compiled at: 2016-09-19 13:30:00
"""Contains the :class:`InfoController`

"""
import logging, datetime, re, simplejson as json
from pylons import request, response, config
from formencode.validators import Invalid
from onlinelinguisticdatabase.lib.base import BaseController
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.config.routing import make_map
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.declarative import DeclarativeMeta
log = logging.getLogger(__name__)

class InfoController(BaseController):
    """

    """

    @h.jsonify
    @h.restrict('GET')
    def index(self):
        """Making a request to an OLD with no path in the URL should return
        information about that OLD. This method returns a JSON object with the
        following keys:

        - app = 'Online Linguistic Database'
        - version = the current version of the OLD
        - paths = an array of valid URL paths and HTTP methods that this OLD
          exposes, e.g., "GET /forms"

        .. warning::

            The 'version' key must be valuated with a valid version string,
            i.e., only digits and period characters. When ``python setup.py``
            is run, the 'version' key will be updated with the current version
            as specified in setup.py.

        """
        resources = {}
        for rname in ['ApplicationSettings', 'Collection', 'CollectionBackup',
         'Corpus', 'CorpusBackup', 'ElicitationMethod', 'File', 'Form',
         'FormBackup', 'FormSearch', 'Keyboard', 'Language',
         'MorphemeLanguageModel', 'MorphemeLanguageModelBackup',
         'MorphologicalParser', 'MorphologicalParserBackup', 'Morphology',
         'MorphologyBackup', 'Orthography', 'Page', 'Phonology',
         'PhonologyBackup']:
            resources[rname] = []
            r_class = getattr(model, rname)
            for k in sorted(r_class.__dict__):
                if k.endswith('_id'):
                    continue
                v = r_class.__dict__[k]
                if type(v) is InstrumentedAttribute:
                    resources[rname].append(k)

            resources[rname].sort()

        map = make_map(config)
        p1 = re.compile(':\\((.+?)\\)')
        p2 = re.compile('\\{(.+?)\\}')
        myroutes = []
        for r in map.matchlist:
            if ':(format)' not in r.routepath:
                if r.conditions:
                    if type(r.conditions['method']) is list:
                        method = ('/').join(sorted(r.conditions['method']))
                    else:
                        method = r.conditions['method']
                else:
                    method = 'GET'
                if method != 'OPTIONS':
                    path = p2.sub('<\\1>', p1.sub('<\\1>', r.routepath))
                    myroutes.append((path, method))

        meta = {'app': 'Online Lingusitic Database', 
           'version': '2.0.0', 
           'paths': [ '%s %s' % (r[1], r[0]) for r in sorted(myroutes) ], 'resources': resources}
        return meta