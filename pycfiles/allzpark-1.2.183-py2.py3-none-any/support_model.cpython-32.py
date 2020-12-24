# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/spec/transform/support_model.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jul 27, 2012\n\n@package: ally core http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides support model encode implementations. \n'
from ally.core.spec.resources import Path
from ally.design.bean import Attribute, Bean
from collections import OrderedDict, Callable
import abc
NO_MODEL_PATH = 2

class DataModel(Bean):
    """
    Contains data used for additional support in encoding the model. The data model is used by the encode model to alter
    the encoding depending on path elements and filters.
    """
    flag = int
    flag = Attribute(flag, default=0, doc='\n    @rtype: integer\n    Flag indicating several situations for the data encode.\n    ')
    modelPaths = dict
    modelPaths = Attribute(modelPaths, factory=dict, doc='\n    @rtype: dictionary{ModelType:Path}\n    The model paths that are directly linked with the encoded model. When a model instance is processed\n    this model paths will get updated with the encoded model information. The key represents the model type\n    that the path needs to be updated with and the value the path to be updated.\n    ')
    path = Path
    path = Attribute(path, doc='\n    @rtype: Path|None\n    The path of the model.\n    ')
    accessiblePath = Path
    accessiblePath = Attribute(accessiblePath, doc='\n    @rtype: Path|None\n    The path for the accessible paths.\n    ')
    accessibleIsProcessed = bool
    accessibleIsProcessed = Attribute(accessibleIsProcessed, default=False, doc='\n    @rtype: boolean\n    Flag indicating that the accessible dictionary has been processed.\n    ')
    accessible = dict
    accessible = Attribute(accessible, factory=OrderedDict, doc='\n    @rtype: dictionary{string, Path}\n    The accessible path for the encoded model.\n    ')
    filter = set
    filter = Attribute(filter, frozenset, factory=set, doc='\n    @rtype: set(string)\n    The properties to be rendered for the model encode, this set needs to include also the accessible paths.\n    ')
    datas = dict
    datas = Attribute(datas, factory=dict, doc='\n    @rtype: dictionary{string, DataModel}\n    The data models to be used for the properties of the encoded model.\n    ')
    fetchReference = object
    fetchReference = Attribute(fetchReference, doc='\n    @rtype: object\n    The fetch reference for the fetch encode.\n    ')
    fetchEncode = Callable
    fetchEncode = Attribute(fetchEncode, doc='\n    @rtype: Callable\n    The fetch encode to be used.\n    ')
    fetchData = object
    fetchData = Attribute(fetchData, doc='\n    @rtype: DataModel\n    The fetch data model to be used.\n    ')


class IFetcher(metaclass=abc.ABCMeta):
    """
    Specification for model fetching.
    """
    __slots__ = ()

    @abc.abstractclassmethod
    def fetch(self, reference, valueId):
        """
        Fetch the model object that is specific for the provided reference.
        
        @param reference: Reference
            The reference of the model object to fetch.
        @param valueId: object
            The value id for the model object to fetch.
        @return: object|None
            The model object corresponding to the reference and value id, None if the object cannot be provided.
        """
        pass