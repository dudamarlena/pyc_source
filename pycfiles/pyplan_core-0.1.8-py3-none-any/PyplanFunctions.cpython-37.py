# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/PyplanFunctions.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 3297 bytes
import pandas as pd, re

class Selector(object):
    __doc__ = ' Class to manage UI Pyplan selectors.\n    '
    SERIALIZABLE_PROPERTIES = [
     'options', 'selected', 'multiselect']

    def __init__(self, options, selected, multiselect=False):
        """ Create UI Pyplan selector for desicion nodes
        Params:
            options: List or pd.Index with available values that can be selected 
            selected: current selected index value's
            multiselect: True to allow multiple selection
        """
        self._options = options
        self._multiselect = multiselect
        self.selected = selected

    @property
    def value(self):
        if self.multiselect:
            return [self.options[i] for i in self.selected]
        return self.options[self.selected]

    @property
    def options(self):
        return self._options

    @property
    def multiselect(self):
        return self._multiselect

    @property
    def selected(self):
        res = None
        if self.multiselect:
            res = []
            for nn in self._selected:
                if nn < len(self._options):
                    res.append(nn)

            if len(res) == 0:
                res = list(range(len(self._options)))
        else:
            res = self._selected if self._selected < len(self._options) else 0
        return res

    @selected.setter
    def selected(self, value):
        if self.multiselect:
            if value is None:
                self._selected = []
            elif isinstance(value, list):
                self._selected = value
            else:
                self._selected = [
                 value]
        elif isinstance(value, list):
            self._selected = value[0]
        else:
            self._selected = value

    def toObj(self):
        res = dict()
        for k in Selector.SERIALIZABLE_PROPERTIES:
            if hasattr(self, k):
                if k == 'options':
                    if isinstance(getattr(self, k), pd.Index):
                        res[k] = getattr(self, k).tolist()
                res[k] = getattr(self, k)

        return res

    def isSameValue(self, value):
        if self.multiselect:
            if isinstance(self.selected, list):
                if isinstance(value, list):
                    l1 = self.selected.copy()
                    l2 = value.copy()
                    l1.sort()
                    l2.sort()
                    return l1 == l2
        return self.selected == value

    def generateDefinition(self, definition, value):
        if self.multiselect:
            if not isinstance(value, list):
                if value is None:
                    value = 0
                value = list(value)
            else:
                if len(value) == 0:
                    value = list(range(len(self.options)))
        newPos = str(value)
        reg = '(?:[^\\]\\[,]+|\\[[^\\]\\[]+\\])'
        groups = re.findall(reg, definition)
        if len(groups) > 2:
            if str(groups[(-1)]) not in ('False)', 'True)', 'multiselect=False)', 'multiselect=True)'):
                groups.append('False)')
            newDef = ''
            for nn in range(len(groups) - 2):
                newDef += groups[nn]

            newDef = f"{newDef},{newPos},{groups[(-1)]}"
            return newDef