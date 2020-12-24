# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/autoreload.py
# Compiled at: 2007-12-02 16:26:55
"""
'stolen' from http://starship.python.net/crew/zack/
 thanks: Zachary_Roadhouse@brown.edu
"""

class Autoreload:
    """Creates instance objects that automatically import the corresponding
       module when any attribute is referenced for the first time.  When
       the reference is next used, the module is reloaded.

       Example:
               string = Autoreload('string')
               if something:
                   # Module string gets imported only if the next statement
                   # gets executed
                   string.join(stringlist)

       If the optional dict arguement is used, a reference to the Autoreload
       object will be placed in that dictionary.
    """
    __module__ = __name__

    def __init__(self, name, dict=None):
        self.module_name = name
        self.module = None
        if dict:
            dict[name] = self
        return

    def __getattr__(self, item):
        if self.module:
            locals()[self.module_name] = self.module
            self.module = eval('reload(%s)' % self.module_name)
        else:
            exec 'import ' + self.module_name
            self.module = locals()[self.module_name]
        attr = getattr(self.module, item)
        return attr


from salamoia.tests import *
runDocTests()