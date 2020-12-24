# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/parameter/empty.py
# Compiled at: 2014-07-07 15:44:50
from parameter import Parameter

class Empty(Parameter):

    def galaxy_input(self, xml_node):
        return

    def galaxy_output(self, xml_node):
        return

    def validate_individual(self, value):
        return True