# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lymon/view/selectors.py
# Compiled at: 2008-06-23 12:24:02
__all__ = [
 'W3CTypes']

class W3CTypes(object):

    def Universal(self, tag={}):
        return '*'

    def ByType(self, tag={}):
        """
                # rule for selecting by tag type
                """
        selector = tag['tag']
        return selector

    def ById(self, tag={}):
        if 'id' in tag['attrs'].keys():
            tagType = tag['tag']
            id = tag['attrs']['id']
            selector = '%s#%s' % (tagType, id)
        else:
            selector = self.ByType(tag)
            print 'Not Id for this Tag, Using a Type selector instead'
        return selector