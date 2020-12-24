# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\iFrameRNG.py
# Compiled at: 2005-09-19 16:44:10
import rng

def validate(self, node):
    if node == None:
        return node
    if isinstance(node, list):
        res = self.applyElt
        for token in node:
            res = res.deriv(token)
            if res == rng.NotAllowed():
                return None

    else:
        res = self.applyElt.deriv(node)
    if res == rng.NotAllowed() or not res.nullable():
        return None
    else:
        return node
    return