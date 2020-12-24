# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/evaluation/evalattribute.py
# Compiled at: 2019-08-19 15:09:29
__all__ = [
 'EvaluationAttribute']
import numpy, re, weakref
from taurus.core.units import Quantity
from taurus.core.taurusattribute import TaurusAttribute
from taurus.core.taurusbasetypes import SubscriptionState, TaurusEventType, TaurusAttrValue, TaurusTimeVal, AttrQuality, DataType
from taurus.core.taurusexception import TaurusException
from taurus.core.taurushelper import Attribute, Manager
from taurus.core import DataFormat
from taurus.core.util.log import debug, taurus4_deprecation
from taurus.core.evaluation.evalvalidator import QUOTED_TEXT_RE, PY_VAR_RE

class EvaluationAttrValue(TaurusAttrValue):
    """Reimplementation of TaurusAttrValue to provide bck-compat via a ref

    """

    def __init__(self, attr=None, config=None):
        TaurusAttrValue.__init__(self)
        if config is not None:
            from taurus.core.util.log import deprecated
            deprecated(dep='"config" kwarg', alt='"attr"', rel='4.0')
            attr = config
        if attr is None:
            self._attrRef = None
        else:
            self._attrRef = weakref.proxy(attr)
        self.config = self._attrRef
        return

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError("'%s' object has no attribute %s" % (
             self.__class__.__name__, name))
        try:
            ret = getattr(self._attrRef, name)
        except AttributeError:
            raise AttributeError('%s has no attribute %s' % (
             self.__class__.__name__, name))

        from taurus.core.util.log import deprecated
        deprecated(dep='EvaluationAttrValue.%s' % name, alt='EvaluationAttribute.%s' % name, rel='4.0')
        return ret

    @taurus4_deprecation(alt='.rvalue')
    def _get_value(self):
        """for backwards compat with taurus < 4"""
        debug(repr(self))
        try:
            return self.__fix_int(self.rvalue.magnitude)
        except AttributeError:
            return self.rvalue

    @taurus4_deprecation(alt='.rvalue')
    def _set_value(self, value):
        """for backwards compat with taurus < 4"""
        debug('Setting %r to %s' % (value, self.name))
        if self.rvalue is None:
            import numpy
            dtype = numpy.array(value).dtype
            if numpy.issubdtype(dtype, int) or numpy.issubdtype(dtype, float):
                msg = 'Refusing to set ambiguous value (deprecated .value API)'
                raise ValueError(msg)
            else:
                self.rvalue = value
        elif hasattr(self.rvalue, 'units'):
            self.rvalue = Quantity(value, units=self.rvalue.units)
        else:
            self.rvalue = value
        return

    value = property(_get_value, _set_value)

    @taurus4_deprecation(alt='.wvalue')
    def _get_w_value(self):
        """for backwards compat with taurus < 4"""
        debug(repr(self))
        try:
            return self.__fix_int(self.wvalue.magnitude)
        except AttributeError:
            return self.wvalue

    @taurus4_deprecation(alt='.wvalue')
    def _set_w_value(self, value):
        """for backwards compat with taurus < 4"""
        debug('Setting %r to %s' % (value, self.name))
        if self.wvalue is None:
            import numpy
            dtype = numpy.array(value).dtype
            if numpy.issubdtype(dtype, int) or numpy.issubdtype(dtype, float):
                msg = 'Refusing to set ambiguous value (deprecated .value API)'
                raise ValueError(msg)
            else:
                self.wvalue = value
        elif hasattr(self.wvalue, 'units'):
            self.wvalue = Quantity(value, units=self.wvalue.units)
        else:
            self.wvalue = value
        return

    w_value = property(_get_w_value, _set_w_value)

    @property
    @taurus4_deprecation(alt='.error')
    def has_failed(self):
        return self.error

    def __fix_int(self, value):
        """cast value to int if  it is an integer.
        Works on scalar and non-scalar values"""
        if self.type != DataType.Integer:
            return value
        try:
            return int(value)
        except TypeError:
            import numpy
            return numpy.array(value, dtype='int')


class EvaluationAttribute(TaurusAttribute):
    """A :class:`TaurusAttribute` that can be used to perform mathematical
    operations involving other arbitrary Taurus attributes. The mathematical
    operation is described in the attribute name itself. An Evaluation Attribute
    will keep references to any other attributes being referenced and it will
    update its own value whenever any of the referenced attributes change.

    .. seealso:: :mod:`taurus.core.evaluation`

    .. warning:: In most cases this class should not be instantiated directly.
                 Instead it should be done via the
                 :meth:`EvaluationFactory.getAttribute`
    """
    _factory = None
    _scheme = 'eval'

    def __init__(self, name='', parent=None, **kwargs):
        self.call__init__(TaurusAttribute, name, parent, **kwargs)
        self._value = EvaluationAttrValue(attr=self)
        self._label = self.getSimpleName()
        self._references = []
        self._validator = self.getNameValidator()
        self._transformation = None
        self.__subscription_state = SubscriptionState.Unsubscribed
        self._value_setter = None
        trstring = self._validator.getExpandedExpr(str(name))
        trstring, ok = self.preProcessTransformation(trstring)
        if ok:
            self._transformation = trstring
            self.applyTransformation()
        self._initWritable(trstring)
        return

    def _initWritable(self, trstring):
        self.writable = False
        try:
            dev = self.getParentObj()
            names = trstring.split('.')
            obj = instance = dev.getSafe()[names[0]]
            for n in names[1:-1]:
                obj = getattr(obj, n)

            obj = getattr(obj.__class__, names[(-1)])
        except Exception as e:
            return

        self.writable = hasattr(obj, 'fset') and obj.fset is not None
        if self.writable:

            def value_setter(value):
                obj.fset(instance, value)

            self._value_setter = value_setter
            self._value.wvalue = self._value.rvalue
        return

    @staticmethod
    def getId(obj, idFormat='_V%i_'):
        """returns an id string for the given object which has the following
           two properties:
            - It is unique for this object during all its life
            - It is a string that can be used as a variable or method name

        :param obj: (object) the python object whose id is requested
        :param idFormat: (str) a format string containing a "`%i`" which,
                         when expanded must be a valid variable name
                         (i.e. it must match
                         `[a-zA-Z_][a-zA-Z0-9_]*`). The default is `_V%i_`
        """
        return idFormat % id(obj)

    def preProcessTransformation(self, trstring):
        """
        parses the transformation string and creates the necessary symbols for
        the evaluator. It also connects any referenced attributes so that the
        transformation gets re-evaluated if they change.

        :param trstring: (str) a string to be pre-processed

        :return: (tuple<str,bool>) a tuple containing the processed string
                 and a boolean indicating if the preprocessing was successful.
                 if ok==True, the string is ready to be evaluated
        """
        for ref in self._references:
            ref.removeListener(self)

        self._references = []
        evaluator = self.getParentObj()
        v = self._validator
        refs = v.getRefs(trstring, ign_quoted=True)
        for r in refs:
            symbol = self.__ref2Id(r)
            trstring = v.replaceUnquotedRef(trstring, '{%s}' % r, symbol)

        safesymbols = list(evaluator.getSafe().keys())
        trimmedstring = re.sub(QUOTED_TEXT_RE, '', trstring)
        for s in set(re.findall(PY_VAR_RE, trimmedstring)):
            if s not in safesymbols:
                self.warning('Missing symbol "%s"' % s)
                return (
                 trstring, False)

        wantpolling = not self.isUsingEvents()
        haspolling = self.isPollingEnabled()
        if wantpolling:
            self._activatePolling()
        elif haspolling and not wantpolling:
            self.disablePolling()
        return (trstring, True)

    def __ref2Id(self, ref):
        """
        Returns the id of an
        existing taurus attribute corresponding to the match.
        The attribute is created if it didn't previously exist.

        :param ref: (str)  string corresponding to a reference. e.g. eval:1
        """
        refobj = self.__createReference(ref)
        return self.getId(refobj)

    def __createReference(self, ref):
        """
        Receives a taurus attribute name and creates/retrieves a reference to
        the attribute object. If the object was not already referenced, it adds
        it to the reference list and adds its id and current value to the
        symbols dictionary of the evaluator.

        :param ref: (str)

        :return: (TaurusAttribute)

        """
        refobj = Attribute(ref)
        if refobj not in self._references:
            evaluator = self.getParentObj()
            v = refobj.read().rvalue
            evaluator.addSafe({self.getId(refobj): v})
            self._references.append(refobj)
        return refobj

    def eventReceived(self, evt_src, evt_type, evt_value):
        try:
            v = evt_value.rvalue
        except AttributeError:
            self.trace('Ignoring event from %s' % repr(evt_src))
            return

        evaluator = self.getParentObj()
        evaluator.addSafe({self.getId(evt_src): v})
        self.applyTransformation()
        if self.isUsingEvents():
            self.fireEvent(evt_type, self._value)

    def applyTransformation(self):
        if self._transformation is None:
            return
        else:
            try:
                evaluator = self.getParentObj()
                rvalue = evaluator.eval(self._transformation)
                if hasattr(rvalue, 'magnitude'):
                    value_dimension = len(numpy.shape(rvalue.magnitude))
                else:
                    value_dimension = len(numpy.shape(rvalue))
                value_dformat = DataFormat(value_dimension)
                self.data_format = value_dformat
                self.type = self._encodeType(rvalue, value_dformat)
                if self.type is None:
                    raise TypeError('Unsupported returned type, %r' % rvalue)
                if self.type in [DataType.Integer, DataType.Float] and not isinstance(rvalue, Quantity):
                    self.debug('Transformation converted to Quantity')
                    rvalue = Quantity(rvalue)
                elif self.type == DataType.Boolean and value_dimension > 1:
                    self.debug('Transformation converted to numpy.array')
                    rvalue = numpy.array(rvalue)
                self._value.rvalue = rvalue
                self._value.time = TaurusTimeVal.now()
                self._value.quality = AttrQuality.ATTR_VALID
            except Exception as e:
                self._value.quality = AttrQuality.ATTR_INVALID
                msg = " the function '%s' could not be evaluated. Reason: %s" % (
                 self._transformation, repr(e))
                self.warning(msg)

            return

    def _encodeType(self, value, dformat):
        """ Encode the value type into Taurus data type. In case of non-zero
        dimension attributes e.g. 1D, 2D the type corresponds to the type of the
        first element.

        :param value: (obj)
        :param dformat: (taurus.DataFormat)

        :return: (taurus.DataType)
        """
        try:
            value = value.magnitude
        except AttributeError:
            pass

        try:
            value = value.item(0)
        except ValueError:
            value = value.item()
        except AttributeError:
            if dformat is DataFormat._1D:
                value = value[0]
            elif dformat is DataFormat._2D:
                value = value[0][0]

        dataType = type(value)
        return DataType.from_python_type(dataType)

    def isBoolean(self):
        return isinstance(self._value.rvalue, bool)

    def getDisplayValue(self, cache=True):
        return str(self.read(cache=cache).rvalue)

    def encode(self, value):
        return value

    def decode(self, attr_value):
        return attr_value

    def write(self, value, with_read=True):
        if not self.isWritable():
            raise TaurusException('Attempt to write on read-only attribute %s', self.getFullName())
        self._value_setter(value)
        self._value.wvalue = value
        if with_read:
            ret = self.read(cache=False)
            return ret

    def read(self, cache=True):
        """returns the value of the attribute.

        :param cache: (bool) If True (default), the last calculated value will
                      be returned. If False, the referenced values will be re-
                      read and the transformation string will be re-evaluated

        :return: attribute value
        """
        if not cache:
            symbols = {}
            for ref in self._references:
                symbols[self.getId(ref)] = ref.read(cache=False).rvalue

            evaluator = self.getParentObj()
            evaluator.addSafe(symbols)
            self.applyTransformation()
        return self._value

    def poll(self):
        v = self.read(cache=False)
        self.fireEvent(TaurusEventType.Periodic, v)

    def isUsingEvents(self):
        return bool(len(self._references))

    def __fireRegisterEvent(self, listener):
        try:
            v = self.read()
            self.fireEvent(TaurusEventType.Change, v, listener)
        except:
            self.fireEvent(TaurusEventType.Error, None, listener)

        return

    def addListener(self, listener):
        """ Add a TaurusListener object in the listeners list.
            If it is the first listener, it triggers the subscription to
            the referenced attributes.
            If the listener is already registered nothing happens."""
        initial_subscription_state = self.__subscription_state
        ret = TaurusAttribute.addListener(self, listener)
        if not ret:
            return ret
        if self.__subscription_state == SubscriptionState.Unsubscribed:
            for refobj in self._references:
                refobj.addListener(self)

            self.__subscription_state = SubscriptionState.Subscribed
        assert len(self._listeners) >= 1
        if len(self._listeners) > 1 and (initial_subscription_state == SubscriptionState.Subscribed or self.isPollingActive()):
            Manager().enqueueJob(self.__fireRegisterEvent, job_args=(
             (
              listener,),))
        return ret

    def removeListener(self, listener):
        """ Remove a TaurusListener from the listeners list. If polling enabled
            and it is the last element then stop the polling timer.
            If the listener is not registered nothing happens."""
        ret = TaurusAttribute.removeListener(self, listener)
        if ret and not self.hasListeners():
            self._deactivatePolling()
            self.__subscription_state = SubscriptionState.Unsubscribed
        return ret