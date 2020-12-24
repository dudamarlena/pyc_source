# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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