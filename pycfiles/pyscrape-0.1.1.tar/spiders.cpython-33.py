# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jorge/pyscrap3/pyscrap3/spiders.py
# Compiled at: 2014-05-12 15:10:42
# Size of source mod 2**32: 10300 bytes
import logging, inspect, importlib

def getEmptyPipes():
    """Estas 'pipes' vacías serán usadas en caso de que la función
    getPipes no este definida en pipeline.py"""
    pipes = {'items': {},  'itemLists': {}}
    return pipes


def emptyGetUrls(*args, **kwargs):
    logging.warning('getUrls not defined in pipeline.py')
    return


def emptyGetSearchData(*args, **kwargs):
    logging.warning('getSearchData not defined in pipeline.py')
    return


class Spider:
    """Spider"""

    def __init__(self):
        self.pipelineUrls = emptyGetUrls
        self.pipelineSearchData = emptyGetSearchData
        pipeline = None
        try:
            try:
                from pipeline import getUrls
                self.pipelineUrls = getUrls
            except ImportError as e:
                if e.msg == "No module named 'pipeline'" or e.msg == 'cannot import name getUrls':
                    subpackage = inspect.getmodule(self.parse).__package__
                    try:
                        pipeline = importlib.import_module('.pipeline', subpackage)
                        self.pipelineUrls = pipeline.getUrls
                    except TypeError as e:
                        logging.warning('getUrls not defined in pipeline.py')

                else:
                    raise

        except ImportError as e:
            if e.msg == "No module named 'pipeline'" or e.msg == 'cannot import name getUrls':
                logging.warning('getUrls not defined in pipeline.py')
            else:
                raise

        if pipeline:
            self.pipelineSearchData = pipeline.getSearchData
        else:
            try:
                from pipeline import getSearchData
                self.pipelineSearchData = getSearchData
            except ImportError as e:
                if e.msg == 'cannot import name getSearchData':
                    logging.warning('getSearchData not defined in pipeline.py')
                else:
                    raise

        return

    def start(self, *args, **kwargs):
        """Ejecuta la función/generador 'parse' y por cada
        Item o ItemList que retorne se ejecutará su función __parseItem__.
        Los objetos que no sean Item o Itemlist se ignorarán.
        Si se retorna un iterable, se intentará ejecutar la función __parseItem__
        de cada objeto que retorne dicho iterable."""
        for dataItem in self.parse(*args, **kwargs):
            if hasattr(dataItem, '__parseItem__'):
                dataItem.__parseItem__()
            elif isinstance(dataItem, (list, tuple)):
                for item in dataItem:
                    if hasattr(dataItem, '__parseItem__'):
                        dataItem.__parseItem__()
                        continue

                continue

    def getUrls(self, *args, **kwargs):
        """Ejecuta la función/generador 'getUrls' que el usuario haya
        definido en pipeline.py"""
        yield from self.pipelineUrls(*args, **kwargs)

    def getSearchData(self, *args, **kwargs):
        """Ejecuta la función/generador 'getSearchData' que el usuario haya
        definido en pipeline.py"""
        yield from self.pipelineSearchData(*args, **kwargs)


class FieldNotDefined(Exception):
    """FieldNotDefined"""

    def __init__(self, fieldName, itemName):
        self.fieldName = fieldName
        self.itemName = itemName

    def __unicode__(self):
        return 'Field ' + self.fieldName + ' not defined in item.py for item: ' + self.itemName


class ItemList(list):
    """ItemList"""

    def __init__(self):
        list.__init__(self)
        self.__fields__ = {}
        pipes = getEmptyPipes()
        self.__pipelineFunction__ = lambda *args**args: None
        try:
            try:
                from pipeline import getPipes
                pipes = getPipes()
            except:
                subpackage = inspect.getmodule(self.parse).__package__
                pipeline = importlib.import_module('.pipeline', subpackage)
                pipes = pipeline.getPipes

        except:
            logging.warning('getPipes not defined in pipeline.py')

        className = self.__class__.__name__
        self.__pipelineFunction__ = pipes['itemLists'].get(className)

    def __parseItem__(self):
        """Llama la función asociada definida en pipeline.py"""
        self.__pipelineFunction__(self)

    def newfield(self, name, default=None):
        """Define un campo para ser manipulado en notación
        itemList["campoPorNombre"]"""
        self.__fields__[name] = default

    def getfields(self):
        return self.__fields__

    def __setitem__(self, keyField, value):
        """Agrega objetos, dependiendo de la notación
            itemList[<int>] = objeto1
        agregará un objeto a la lista interna.
            itemList[<objeto>] = objeto1
        agregará objeto1 al diccionario interno."""
        if type(keyField) == type(int()):
            list.__setitem__(self, keyField, value)
        else:
            if keyField in self.__fields__:
                self.__fields__[keyField] = value
            else:
                raise FieldNotDefined(keyField, self.__class__.__name__)

    def __getitem__(self, keyField):
        """Retorna objetos, dependiendo de la notación.
            itemList[<int>]
        retornará un objeto desde la lista interna.
            itemList[<objeto_key>]
        retornará un objeto desde el diccionario interno."""
        if type(keyField) == type(int()):
            return list.__getitem__(self, keyField)
        if keyField in self.__fields__:
            return self.__fields__.get(keyField)
        raise FieldNotDefined(keyField, self.__class__.__name__)


class Item:
    """Item"""

    def __init__(self):
        self.__fields__ = {}
        pipes = getEmptyPipes()
        self.__pipelineFunction__ = lambda *args**args: None
        try:
            try:
                from pipeline import getPipes
                pipes = getPipes()
            except:
                subpackage = inspect.getmodule(self.parse).__package__
                pipeline = importlib.import_module('.pipeline', subpackage)
                pipes = pipeline.getPipes

        except:
            logging.warning('getPipes not defined in pipeline.py')

        className = self.__class__.__name__
        self.__pipelineFunction__ = pipes['items'].get(className)

    def __parseItem__(self):
        """Llama la función asociada definida en pipeline.py"""
        self.__pipelineFunction__(self)

    def newfield(self, name, default=None):
        """Define un campo para ser manipulado en notación
        itemList["campoPorNombre"]"""
        self.__fields__[name] = default

    def get(self, keyField):
        return self.__fields__.get(keyField)

    def getDict(self):
        return self.__fields__

    def __getitem__(self, keyField):
        if keyField in self.__fields__:
            return self.__fields__.get(keyField)
        raise FieldNotDefined(keyField, self.__class__.__name__)

    def __setitem__(self, keyField, value):
        if keyField in self.__fields__:
            self.__fields__[keyField] = value
        else:
            raise FieldNotDefined(keyField, self.__class__.__name__)