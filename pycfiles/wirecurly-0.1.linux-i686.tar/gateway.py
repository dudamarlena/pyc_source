# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/configuration/gateway.py
# Compiled at: 2014-01-08 15:34:56
import logging
log = logging.getLogger(__name__)
__all__ = [
 'Gateway']

class Gateway(object):
    """A gateway object"""

    def __init__(self, name):
        super(Gateway, self).__init__()
        self.name = name
        self.parameters = []

    def addParameter(self, param, val):
        """
                        Set an extra parameter for a gateway
                """
        try:
            self.getParameter(param)
        except ValueError:
            self.parameters.append({'name': param, 'value': val})
            return

        log.warning('Cannot replace existing parameter.')
        raise ValueError

    def getParameter(self, param):
        """
                        Retrieve the value of a parameter by its name
                """
        for p in self.parameters:
            if p.get('name') == param:
                return p.get('value')

        raise ValueError

    def todict(self):
        """
                        Create a dict so it can be converted/serialized
                """
        if self.parameters:
            children = [ {'tag': 'param', 'attrs': p} for p in self.parameters ]
        return {'tag': 'gateway', 'children': children, 'attrs': {'name': self.name}}