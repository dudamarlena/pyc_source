# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/parametertree/ParameterSystem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4598 bytes
from .parameterTypes import GroupParameter
from .. import functions as fn
from .SystemSolver import SystemSolver

class ParameterSystem(GroupParameter):
    """ParameterSystem"""

    def __init__(self, *args, **kwds):
        (GroupParameter.__init__)(self, *args, **kwds)
        self._system = None
        self._fixParams = []
        sys = kwds.pop('system', None)
        if sys is not None:
            self.setSystem(sys)
        self._ignoreChange = []
        self.sigTreeStateChanged.connect(self.updateSystem)

    def setSystem(self, sys):
        self._system = sys
        defaults = {}
        vals = {}
        for param in self:
            name = param.name()
            constraints = ''
            if hasattr(sys, '_' + name):
                constraints += 'n'
            elif not param.readonly():
                constraints += 'f'
                if 'n' in constraints:
                    ch = param.addChild(dict(name='fixed', type='bool', value=False))
                    self._fixParams.append(ch)
                    param.setReadonly(True)
                    param.setOpts(expanded=False)
                else:
                    vals[name] = param.value()
                ch = param.addChild(dict(name='fixed', type='bool', value=True, readonly=True))
            defaults[name] = [
             None, param.type(), None, constraints]

        sys.defaultState.update(defaults)
        sys.reset()
        for name, value in vals.items():
            setattr(sys, name, value)

        self.updateAllParams()

    def updateSystem(self, param, changes):
        changes = [ch for ch in changes if ch[0] not in self._ignoreChange]
        sets = [ch[0] for ch in changes if ch[1] == 'value']
        for param in sets:
            if param in self._fixParams:
                parent = param.parent()
                if param.value():
                    setattr(self._system, parent.name(), parent.value())
                else:
                    setattr(self._system, parent.name(), None)
            else:
                setattr(self._system, param.name(), param.value())

        self.updateAllParams()

    def updateAllParams(self):
        try:
            self.sigTreeStateChanged.disconnect(self.updateSystem)
            for name, state in self._system._vars.items():
                param = self.child(name)
                try:
                    v = getattr(self._system, name)
                    if self._system._vars[name][2] is None:
                        self.updateParamState(self.child(name), 'autoSet')
                        param.setValue(v)
                    else:
                        self.updateParamState(self.child(name), 'fixed')
                except RuntimeError:
                    self.updateParamState(param, 'autoUnset')

        finally:
            self.sigTreeStateChanged.connect(self.updateSystem)

    def updateParamState(self, param, state):
        if state == 'autoSet':
            bg = fn.mkBrush((200, 255, 200, 255))
            bold = False
            readonly = True
        elif state == 'autoUnset':
            bg = fn.mkBrush(None)
            bold = False
            readonly = False
        elif state == 'fixed':
            bg = fn.mkBrush('y')
            bold = True
            readonly = False
        param.setReadonly(readonly)