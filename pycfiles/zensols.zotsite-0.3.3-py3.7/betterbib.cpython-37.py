# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/zotsite/betterbib.py
# Compiled at: 2020-04-25 23:55:42
# Size of source mod 2**32: 1937 bytes
import logging, json, sqlite3
from zensols.persist import persisted
from zensols.zotsite import ZoteroObject, Item, Visitor, Library
logger = logging.getLogger(__name__)

class BetterBibtexMapper(object):
    __doc__ = 'Read the BetterBibtex database and create a mapping from item DB ids to\n    citation keys.\n\n    '

    def __init__(self, lib: Library):
        self.lib = lib

    @property
    def data(self):
        path = self.lib.data_dir / 'better-bibtex.sqlite'
        logger.info(f"reading bibtex DB at {path}")
        conn = sqlite3.connect(path)
        try:
            rows = tuple(conn.execute('select * from `better-bibtex`'))
            assert len(rows) == 3
            rows = tuple(filter(lambda r: r[0] == 'better-bibtex.citekey', rows))
            assert len(rows) == 1
            jstr = rows[0][1]
            return json.loads(jstr)
        finally:
            conn.close()

    @property
    @persisted('_mapping')
    def mapping(self):
        lib_id = self.lib.library_id
        data = self.data['data']
        data = filter(lambda x: x['libraryID'] == lib_id, data)
        return {x['itemID']:x['citekey'] for x in data}

    def tmp(self):
        from pprint import pprint
        pprint(self.mapping)


class BetterBibtexVisitor(Visitor):
    __doc__ = 'Use the ``BetterBibtexMapper`` to change the keys in mapped items to the\n    respective citation keys.\n\n    '

    def __init__(self, lib: Library):
        self.mapper = BetterBibtexMapper(lib)

    def enter_parent(self, parent: ZoteroObject):
        pass

    def visit_child(self, child: ZoteroObject):
        if isinstance(child, Item):
            dbid = child.get_db_id()
            bbid = self.mapper.mapping.get(dbid)
            if bbid is not None:
                child.set_id(bbid)
                child.metadata['citationKey'] = bbid

    def leave_parent(self, parent: ZoteroObject):
        pass