# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/evaluation/evaldevice.py
# Compiled at: 2019-08-19 15:09:29
__all__ = [
 'EvaluationDevice']
from taurus import Factory
from taurus.core.taurusdevice import TaurusDevice
from taurus.core.util.safeeval import SafeEvaluator
from taurus.core.taurusbasetypes import TaurusDevState, TaurusAttrValue

class EvaluationDevice(TaurusDevice, SafeEvaluator):
    """The evaluator object. It is a :class:`TaurusDevice` and is used as the
    parent of :class:`EvaluationAttribute` objects for which it performs the
    mathematical evaluation.

    .. seealso:: :mod:`taurus.core.evaluation`

    .. warning:: In most cases this class should not be instantiated directly.
                 Instead it should be done via the
                 :meth:`EvaluationFactory.getDevice`
    """
    _symbols = []
    _factory = None
    _scheme = 'eval'

    def __init__(self, name='', **kw):
        """Object initialization."""
        self.call__init__(TaurusDevice, name, **kw)
        safedict = {}
        for s in self._symbols:
            if hasattr(self, s):
                safedict[s] = getattr(self, s)

        SafeEvaluator.__init__(self, safedict=safedict)

    def _createHWObject(self):
        return 'Evaluation'

    def getAttribute(self, attrname):
        """Returns the attribute object given its name"""
        full_attrname = '%s;%s' % (self.getFullName(), attrname)
        return self.factory().getAttribute(full_attrname)

    def decode(self, event_value):
        if isinstance(event_value, int):
            new_sw_state = event_value
        else:
            self.info('Unexpected value to decode: %s' % str(event_value))
            new_sw_state = TaurusDevState.NotReady
        value = TaurusAttrValue()
        value.rvalue = new_sw_state
        return value