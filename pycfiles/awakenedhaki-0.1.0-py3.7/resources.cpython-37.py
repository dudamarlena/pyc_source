# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/crossrefapiclient/resources.py
# Compiled at: 2020-04-09 16:44:31
# Size of source mod 2**32: 3358 bytes
import requests
from abc import ABCMeta
from uritemplate import URITemplate
from urllib.parse import urlencode, urljoin
from crossrefapiclient.utils import validate, prefix_query, create_logger, _filter_builder
VERSION = 'v1'
BASE = URITemplate('https://api.crossref.org/{version}/{resource}/')
logger = create_logger(__name__)

class MetaResource(ABCMeta):
    __doc__ = '\n    Metaclass for Crossref Resources.\n\n    Sets the `resources` attribute with __new__ constructor from class name.\n    '

    def __new__(cls, name, bases, body):
        body['resource'] = name.lower()
        return super().__new__(cls, name, bases, body)


class Resource(metaclass=MetaResource):
    __doc__ = '\n    Abstract class for a CrossRef Resource.\n\n    Currently available resources in the CrossRef API are:\n        - /works\n        - /funders\n        - /members\n        - /types\n        - /licenses\n        - /journals\n    '

    def __init__(self):
        self.url = BASE.expand({'version':VERSION, 
         'resource':self.resource})
        logger.info(f"{self.__class__.__name__} URL has been set to {self.url}")
        self.params = {}

    def execute(self):
        """
        Sends a GET request to CrossRef API.

        Returns
        -------
        A JSON object.
        """
        params = urlencode(self.params)
        url = self.url + f"?{params}" if params else self.url
        logger.info(f"Request being sent to {url}")
        with requests.get(url) as (r):
            logger.warning(f"Request status code: {r.status_code}")
            r.raise_for_status()
            return r.json()

    def get(self, identifier):
        self.url = urljoin(self.url, f"{identifier}/")
        logger.info(f"Identifier: {identifier}")
        return self

    @validate()
    @prefix_query
    def query(self, **kwargs):
        (self.params.update)(**kwargs)
        return self

    @validate('{resource}')
    def filter(self, **kwargs):
        self.params.update({'filter': _filter_builder(**kwargs)})
        return self

    @validate()
    def sort(self, sorter, order='asc'):
        self.params.update({'sort':sorter, 
         'order':order})

    def reset(self):
        return self.__class__()

    def __repr__(self):
        attrs = ', '.join([f"{k}={v}" for k, v in vars(self).items()])
        return f"{self.__class__.__name__}({attrs})"


class CombinationResource(Resource):

    def works(self):
        self.url = urljoin(self.url, 'works/')
        logger.info(f"Combining with /works: {self.url}")
        return self


class Works(Resource):
    pass


class Funders(CombinationResource):
    pass


class Members(CombinationResource):
    pass


class Journals(CombinationResource):
    pass


class Licenses(CombinationResource):
    pass


class Types(CombinationResource):
    pass


class Prefixes(CombinationResource):
    pass