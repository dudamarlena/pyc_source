# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/metrics/ncss/ncss.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 2018 bytes
import javalang

class NCSSMetric:

    def __init__(self, filename):
        """Initialize class."""
        if len(filename) == 0:
            raise ValueError('Empty file for analysis')
        self.filename = filename

    def value(self):
        f = open((self.filename), 'r', encoding='utf8')
        code = f.read()
        f.close()
        tree = javalang.parse.parse(code)
        metric = 0
        for path, node in tree:
            node_type = str(type(node))
            if 'Statement' in node_type:
                metric += 1
            elif 'VariableDeclarator' == node_type:
                metric += 1
            elif 'Assignment' == node_type:
                metric += 1
            else:
                if 'Declaration' in node_type and 'LocalVariableDeclaration' not in node_type and 'PackageDeclaration' not in node_type:
                    metric += 1

        return metric