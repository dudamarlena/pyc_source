# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/itemclassloader.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 3550 bytes
import six, traceback, warnings, importlib
from scrapy.utils.misc import walk_modules
from scrapy import Item
import inspect
from collections import defaultdict
from .singleton import Singleton
from .utils import load_scrapy_settings

def iter_item_classes(module):
    """Return an iterator over all spider classes defined in the given module
    that can be instantiated (ie. which have name)
    """
    for obj in six.itervalues(vars(module)):
        if inspect.isclass(obj) and issubclass(obj, Item) and obj.__module__ == module.__name__:
            yield obj


@Singleton
class ItemClassLoader(object):
    __doc__ = '\n    # from scrapy import spiderloader\n    scrapy的item默认是全部写在一个`items.py`中的，但为了某种拆分的可能性，\n    参考了spiderloader的实现\n    # from scrapy.loader import ItemLoader\n    并且，显然 ItemClassLoader 与 ItemLoader 很不一样\n    '

    def __init__(self, lazy_load=False, settings=None):
        self.settings = settings if settings else load_scrapy_settings()
        self._ItemClassLoader__init(self.settings)
        if not lazy_load:
            self._load_all_items(self.settings.get('BOT_NAME') + '.items')

    def __init(self, settings):
        self._found = defaultdict(list)
        self._items = {}
        self.item_modules = settings.getlist('ITEM_MODULES')
        self._loaded = False

    def _load_items(self, module):
        for spcls in iter_item_classes(module):
            self._found[spcls.__name__].append((module.__name__, spcls.__name__))
            self._items[spcls.__name__] = spcls

    def _load_all_items(self, item_modules=None):
        if item_modules:
            self.item_modules.append(item_modules)
        for name in self.item_modules:
            try:
                for module in walk_modules(name):
                    self._load_items(module)

            except ImportError as e:
                if self.warn_only:
                    msg = "\n{tb}Could not load spiders from module '{modname}'. See above traceback for details.".format(modname=name,
                      tb=(traceback.format_exc()))
                    warnings.warn(msg, RuntimeWarning)
                else:
                    raise

        self._loaded = True

    def list(self):
        """
        Return a list with the names of all items available in the project.
        """
        if not self._loaded:
            self._load_all_items()
        return list(self._items.keys())

    def get(self, name):
        if not name:
            return
        else:
            if not self._loaded:
                self._load_all_items()
            return self._items.get(name)

    def load(self, name):
        """
        support import-on-call，like:
            cls = ItemClassloader().load('parser_engine.clue.items.ClueItem')
        :param name: absolute import path
        :return: `class` obj
        """
        try:
            cls = self.get(name)
            if not cls:
                if name:
                    module, cls_name = name.rsplit('.', 1)
                    md = importlib.import_module(module)
                    cls = getattr(md, cls_name)
                    if cls:
                        if inspect.isclass(cls):
                            self._items[name] = cls
            return cls
        except (ImportError, ModuleNotFoundError, Exception):
            warnings.warn('class %s not found' % name, RuntimeWarning)