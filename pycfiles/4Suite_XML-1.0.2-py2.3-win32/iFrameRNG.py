# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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