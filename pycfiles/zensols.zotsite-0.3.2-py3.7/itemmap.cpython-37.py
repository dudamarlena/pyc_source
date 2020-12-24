# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/zotsite/itemmap.py
# Compiled at: 2020-01-03 18:29:22
# Size of source mod 2**32: 2381 bytes
from abc import ABC, abstractmethod
import logging, re
from zensols.zotsite import Item, Library
logger = logging.getLogger(__name__)

class ItemMapper(ABC):
    EXT_RE = re.compile('.+\\.(.+)?$')

    def _item_to_ext(self, item: Item):
        m = self.EXT_RE.match(item.path.name)
        if m is not None:
            return f".{m.group(1)}"
        return ''

    @abstractmethod
    def get_resource_name(self, item: Item) -> str:
        pass

    @abstractmethod
    def get_file_name(self, item: Item) -> str:
        pass


class RegexItemMapper(ItemMapper):
    __doc__ = 'Map by using regular expression replacements.\n\n    '

    def __init__(self, lib: Library, fmatch_re=None, repl_re=None):
        self.lib = lib
        if fmatch_re is not None:
            self.fmatch_re = re.compile(fmatch_re)
        else:
            self.fmatch_re = None
        if repl_re is not None:
            self.repl_re = re.compile(repl_re)
        else:
            self.repl_re = None

    def _map(self, item: Item) -> str:
        """Return the regular expression matched/modified string of ``fname``.'

        """
        fname = self.lib.attachment_resource(item)
        if fname is not None:
            if self.fmatch_re:
                if self.repl_re:
                    if self.fmatch_re.match(fname):
                        fname = self.repl_re.sub('_', fname)
        return fname

    def get_resource_name(self, item: Item) -> str:
        return self._map(item)

    def get_file_name(self, item: Item) -> str:
        return self._map(item)


class IdItemMapper(ItemMapper):
    __doc__ = 'Map by using ids.\n\n    '

    def __init__(self, lib: Library, fmatch_re=None, repl_re=None):
        self.lib = lib
        if fmatch_re is not None:
            self.fmatch_re = re.compile(fmatch_re)
        else:
            self.fmatch_re = None
        if repl_re is not None:
            self.repl_re = re.compile(repl_re)
        else:
            self.repl_re = None

    def _map(self, item: Item) -> str:
        """Return the regular expression matched/modified string of ``fname``.'

        """
        if item.type == 'attachment':
            if item.path is not None:
                ext = self._item_to_ext(item)
                return f"{self.lib.storage_dirname}/{item.id}{ext}"

    def get_resource_name(self, item: Item) -> str:
        return self._map(item)

    def get_file_name(self, item: Item) -> str:
        return self._map(item)