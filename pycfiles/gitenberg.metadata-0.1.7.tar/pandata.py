# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seth/code/metadata/gitenberg/metadata/pandata.py
# Compiled at: 2015-07-25 16:11:21
import yaml, json
from . import marc
import pymarc

def subject_constructor(loader, node):
    return (
     node.tag[1:], loader.construct_scalar(node))


yaml.add_constructor('!lcsh', subject_constructor)
yaml.add_constructor('!lcc', subject_constructor)
PANDATA_STRINGFIELDS = [
 '_repo',
 'description',
 'funding_info',
 'gutenberg_issued',
 'language',
 'publication_date_original',
 'publisher_original',
 'rights',
 'rights_url',
 'title']
PANDATA_AGENTFIELDS = [
 'authors',
 'editors_of_a_compilation',
 'translators',
 'illustrators']
PANDATA_LISTFIELDS = PANDATA_AGENTFIELDS + [
 'subjects']
PANDATA_DICTFIELDS = [
 'identifiers', 'creator', 'contributor']

class Pandata(object):

    def __init__(self, datafile):
        self.metadata = yaml.load(file(datafile, 'r'))

    def __getattr__(self, name):
        if name in PANDATA_STRINGFIELDS:
            value = self.metadata.get(name, '')
            if isinstance(value, str):
                return value
        if name in PANDATA_LISTFIELDS:
            return self.metadata.get(name, [])
        else:
            if name in PANDATA_DICTFIELDS:
                return self.metadata.get(name, {})
            return self.metadata.get(name, None)

    def agents(self, agent_type):
        agents = self.metadata.get(agent_type, [])
        if agents:
            return agents
        return []

    def downloads(self):
        return []

    def download_via_url(self):
        return []

    def authnames(self):
        return [ auth.get('author_sortname', '') for auth in self.authors ]

    @staticmethod
    def get_by_isbn(isbn):
        return