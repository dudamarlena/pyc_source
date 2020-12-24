# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/batchcompute/resources/image.py
# Compiled at: 2019-11-25 04:45:47
import copy
from batchcompute.utils import partial, add_metaclass, CamelCasedClass
from batchcompute.utils.jsonizable import Jsonizable
from batchcompute.utils.constants import STRING, NUMBER, TIME

class ImageDescription(Jsonizable):
    """
    Description class of image resource type in batchcompute service.
    """
    resource_name = 'images'
    descriptor_type = 'data descriptor'
    descriptor_map = {'Name': STRING, 
       'Description': STRING, 
       'Platform': STRING, 
       'EcsImageId': STRING, 
       'IdempotentToken': STRING}
    required = [
     'Platform',
     'EcsImageId']

    def __init__(self, dct={}):
        super(ImageDescription, self).__init__(dct)

    def setproperty(self, key, value):
        super_set = super(ImageDescription, self).setproperty
        new_value = value
        super_set(key, new_value)


ImageDescription = add_metaclass(ImageDescription, CamelCasedClass)