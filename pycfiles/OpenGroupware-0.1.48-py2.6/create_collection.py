# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/create_collection.py
# Compiled at: 2012-10-12 07:02:39
import uuid
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class CreateCollection(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'create-collection'
    __aliases__ = ['createCollection', 'createCollectionAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def read_omphalos_entities(self):
        f.seek(0)
        for (event, element) in etree.iterparse(self._rfile, events=('start', 'end')):
            if event == 'start' and element.tag == 'entity':
                object_id = None
                entity_name = None
            elif event == 'end' and element.tag == 'entity':
                yield (
                 element.attrib.get('objectId'), element.attrib.get('entityName'))
                element.clear()

        return

    def do_action(self):
        assignments = []
        for (object_id, entity_name) in self.read_omphalos_entities():
            assignments.append({'objectId': int(object_id)})

        collection = self._ctx.run_command('collection::new', values={'name': self._collection_name, 'dav_enabled': self._webdav_enabled}, assignments=assignments)

    @property
    def result_mimetype(self):
        return 'plain/text'

    def parse_action_parameters(self):
        self._collection_name = self.action_parameters.get('collectionName', str(uuid.uuid()))
        self._collection_name = self.process_label_substitutions(self._collection_name)
        self._webdav_enabled = self.action_parameters.get('webDAVEnabled', 'NO')
        self._webdav_enabled = self.process_label_substitutions(self._webdav_enabled)

    def do_epilogue(self):
        pass