# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/autoimport.py
# Compiled at: 2007-12-02 16:26:55
"""
'stolen' from http://starship.python.net/crew/zack/
 thanks: Zachary_Roadhouse@brown.edu
"""

class Autoimport:
    """Creates instance objects that automatically import the corresponding
       module when any attribute is referenced.
       
       Example:
               string = Autoimport('string', locals())
               if something:
                   # Module string gets imported only if the next statement
                   # gets executed
                   string.join(stringlist)
    """
    __module__ = __name__

    def __init__(self, name, dict):
        self.module_name = name
        self.dict = dict

    def __getattr__(self, item):
        exec 'import %s' % self.module_name
        module = locals()[self.module_name]
        self.dict[self.module_name] = module
        attr = getattr(module, item)
        return attr


from salamoia.tests import *
runDocTests()