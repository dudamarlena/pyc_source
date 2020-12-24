# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: foaflib/utils/basicscutter.py
# Compiled at: 2009-06-06 03:43:05
from robotparser import RobotFileParser
from urlparse import urljoin
import rdflib
from foaflib.classes.person import Person

class BasicScutter(object):

    def __init__(self, seed_uris=None):
        self.useragent = 'foaflib'
        if seed_uris is None:
            seed_uris = []
        self.current_list = seed_uris
        self.next_list = []
        self.seen_uris = []
        self.rp = RobotFileParser()
        return

    def _can_access(self, uri):
        try:
            self.rp.set_url(urljoin(uri, '/robots.txt'))
            self.rp.read()
            return self.rp.can_fetch(self.useragent, uri)
        except IOError:
            return False

    def handle_person(self, person):
        return person

    def scutter(self, uri_limit=0, depth_limit=0):
        uri_count = 0
        depth_count = -1
        while self.current_list:
            if depth_limit and depth_count == depth_limit:
                return
            for uri in self.current_list:
                if uri in self.seen_uris:
                    continue
                if not self._can_access(uri):
                    continue
                try:
                    p = Person(uri)
                    self.seen_uris.append(uri)
                except:
                    continue

                if not depth_limit or depth_limit and depth_count < depth_limit - 1:
                    for friend in p._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/knows')):
                        for uri in p._graph.objects(subject=friend, predicate=rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#seeAlso')):
                            self.next_list.append(uri)
                            break

                uri_count += 1
                yield self.handle_person(p)
                if uri_count == uri_limit:
                    return

            self.current_list = self.next_list[:]
            self.next_list = []
            depth_count += 1