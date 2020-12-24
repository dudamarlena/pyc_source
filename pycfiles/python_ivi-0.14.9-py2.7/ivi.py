# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/ivi.py
# Compiled at: 2014-09-01 23:09:59
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import inspect, numpy as np, re
from functools import partial
try:
    import vxi11
except ImportError:
    pass

try:
    import usbtmc
except ImportError:
    pass

try:
    from .interface import linuxgpib
except ImportError:
    pass

try:
    from .interface import pyserial
except ImportError:
    pass

try:
    from .interface import pyvisa
except ImportError:
    pass

_prefer_pyvisa = False

def get_prefer_pyvisa():
    global _prefer_pyvisa
    return _prefer_pyvisa


def set_prefer_pyvisa(value=True):
    global _prefer_pyvisa
    _prefer_pyvisa = bool(value)


from .version import __version__
version = __version__

class IviException(Exception):
    pass


class IviDriverException(IviException):
    pass


class FileFormatException(IviDriverException):
    pass


class IdQueryFailedException(IviDriverException):
    pass


class InstrumentStatusExcpetion(IviDriverException):
    pass


class InvalidOptionValueException(IviDriverException):
    pass


class IOException(IviDriverException):
    pass


class IOTimeoutException(IviDriverException):
    pass


class MaxTimeoutExceededException(IviDriverException):
    pass


class NotInitializedException(IviDriverException):
    pass


class OperationNotSupportedException(IviDriverException):
    pass


class OperationPendingException(IviDriverException):
    pass


class OptionMissingException(IviDriverException):
    pass


class OptionStringFormatException(IviDriverException):
    pass


class OutOfRangeException(IviDriverException):
    pass


class ResetFailedException(IviDriverException):
    pass


class ResetNotSupportedException(IviDriverException):
    pass


class SelectorFormatException(IviDriverException):
    pass


class SelectorHierarchyException(IviDriverException):
    pass


class SelectorNameException(IviDriverException):
    pass


class SelectorNameRequiredException(IviDriverException):
    pass


class SelectorRangeException(IviDriverException):
    pass


class SimulationStateException(IviDriverException):
    pass


class TriggerNotSoftwareException(IviDriverException):
    pass


class UnexpectedResponseException(IviDriverException):
    pass


class UnknownOptionException(IviDriverException):
    pass


class UnknownPhysicalNameException(IviDriverException):
    pass


class ValueNotSupportedException(IviDriverException):
    pass


def get_index(l, i):
    """Validate index from list or dict of possible values"""
    if type(l) is dict:
        try:
            return l[i]
        except KeyError:
            if type(i) is int:
                raise SelectorRangeException()
            raise SelectorNameException()

    if i in l:
        return l.index(i)
    if type(i) == int:
        if i < 0 or i >= len(l):
            raise SelectorRangeException()
        return i
    raise SelectorNameException()


def get_index_dict(l):
    """Construct a dict object for faster index lookups"""
    d = {}
    for i in range(len(l)):
        d[l[i]] = i
        d[i] = i

    return d


class PropertyCollection(object):
    """A building block to create hierarchical trees of methods and properties"""

    def __init__(self):
        d = object.__getattribute__(self, '__dict__')
        d.setdefault('_props', dict())
        d.setdefault('_docs', dict())
        d.setdefault('_locked', False)

    def _add_property(self, name, fget=None, fset=None, fdel=None, doc=None):
        """Add a managed property"""
        d = object.__getattribute__(self, '__dict__')
        d['_props'][name] = (fget, fset, fdel)
        d['_docs'][name] = doc
        d[name] = None
        return

    def _add_method(self, name, f=None, doc=None):
        """Add a managed method"""
        d = object.__getattribute__(self, '__dict__')
        d['_docs'][name] = doc
        d[name] = f

    def _del_property(self, name):
        """Remove managed property or method"""
        d = object.__getattribute__(self, '__dict__')
        del d['_props'][name]
        del d['_docs'][name]
        del d[name]

    def _lock(self, lock=True):
        """Set lock state to prevent creation or deletion of unmanaged members"""
        d = object.__getattribute__(self, '__dict__')
        d['_locked'] = lock

    def _unlock(self):
        """Unlock object to allow creation or deletion of unmanaged members, equivalent to _lock(False)"""
        self._lock(False)

    def __getattribute__(self, name):
        if name == '__dict__':
            return object.__getattribute__(self, name)
        else:
            d = object.__getattribute__(self, '__dict__')
            d.setdefault('_props', dict())
            d.setdefault('_locked', False)
            if name in d['_props']:
                f = d['_props'][name][0]
                if f is None:
                    raise AttributeError('unreadable attribute')
                return f()
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        d = object.__getattribute__(self, '__dict__')
        d.setdefault('_props', dict())
        d.setdefault('_locked', False)
        if name in d['_props']:
            f = d['_props'][name][1]
            if f is None:
                raise AttributeError("can't set attribute")
            f(value)
            return
        else:
            if name not in d and self._locked:
                raise AttributeError('locked')
            object.__setattr__(self, name, value)
            return

    def __delattr__(self, name):
        d = object.__getattribute__(self, '__dict__')
        d.setdefault('_props', dict())
        d.setdefault('_locked', False)
        if name in d['_props']:
            f = d['_props'][name][2]
            if f is None:
                raise AttributeError("can't delete attribute")
            f()
            return
        else:
            if name not in d and self._locked:
                raise AttributeError('locked')
            object.__delattr__(self, name)
            return


class IndexedPropertyCollection(object):
    """A building block to create hierarchical trees of methods and properties with an index that is converted to a parameter"""

    def __init__(self):
        self._props = dict()
        self._docs = dict()
        self._indicies = list()
        self._indicies_dict = dict()
        self._objs = list()

    def _add_property(self, name, fget=None, fset=None, fdel=None, doc=None, props=None, docs=None):
        """Add a managed property"""
        if props is None:
            props = self._props
        if docs is None:
            docs = self._docs
        l = name.split('.', 1)
        n = l[0]
        r = ''
        if len(l) > 1:
            r = l[1]
        if n not in props:
            props[n] = dict()
            docs[n] = dict()
        if type(props[n]) != dict:
            raise AttributeError('property already defined')
        if len(r) > 0:
            self._add_property(r, fget, fset, fdel, doc, props[n], docs[n])
        else:
            props[n] = (
             fget, fset, fdel)
            docs[n] = doc
        return

    def _add_method(self, name, f=None, doc=None, props=None, docs=None):
        """Add a managed method"""
        if props is None:
            props = self._props
        if docs is None:
            docs = self._docs
        l = name.split('.', 1)
        n = l[0]
        r = ''
        if len(l) > 1:
            r = l[1]
        if n not in props:
            props[n] = dict()
            docs[n] = dict()
        if type(props[n]) != dict:
            raise AttributeError('property already defined')
        if len(r) > 0:
            self._add_method(r, f, doc, props[n], docs[n])
        else:
            props[n] = f
            docs[n] = doc
        return

    def _add_sub_property(self, sub, name, fget=None, fset=None, fdel=None, doc=None):
        """Add a sub-property (equivalent to _add_property('sub.name', ...))"""
        self._add_property(sub + '.' + name, fget, fset, fdel, doc)

    def _add_sub_method(self, sub, name, f=None, doc=None):
        """Add a sub-method (equivalent to _add_method('sub.name', ...))"""
        self._add_method(sub + '.' + name, f, doc)

    def _del_property(self, name):
        """Delete property"""
        l = name.split('.', 1)
        n = l[0]
        r = ''
        if len(l) > 1:
            r = l[1]
        if len(r) > 0:
            self._del_property(r)
        else:
            del self._props[name]
            del self._docs[name]

    def _build_obj(self, props, docs, i):
        """Build a tree of PropertyCollection objects with the proper index associations"""
        obj = PropertyCollection()
        for n in props:
            itm = props[n]
            doc = docs[n]
            if type(itm) == tuple:
                fget, fset, fdel = itm
                fgeti = fseti = fdeli = None
                if fget is not None:
                    fgeti = partial(fget, i)
                if fset is not None:
                    fseti = partial(fset, i)
                if fdel is not None:
                    fdeli = partial(fdel, i)
                obj._add_property(n, fgeti, fseti, fdeli, doc)
            elif type(itm) == dict:
                o2 = self._build_obj(itm, doc, i)
                obj.__dict__[n] = o2
            elif hasattr(itm, '__call__'):
                obj._add_method(n, partial(itm, i), doc)

        obj._lock()
        return obj

    def _set_list(self, l):
        """Set a list of allowable indicies as an associative array"""
        self._indicies = list(l)
        self._indicies_dict = get_index_dict(self._indicies)
        self._objs = list()
        for i in range(len(self._indicies)):
            self._objs.append(self._build_obj(self._props, self._docs, i))

    def __getitem__(self, key):
        i = get_index(self._indicies_dict, key)
        return self._objs[i]

    def __iter__(self):
        return self._objs.__iter__()

    def __len__(self):
        return len(self._indicies)

    def count(self):
        return len(self._indicies)


class IviContainer(PropertyCollection):

    def __init__(self, *args, **kwargs):
        super(IviContainer, self).__init__(*args, **kwargs)

    def _add_attribute(self, name, attr, doc=None):
        cur_obj = self
        rest = name
        while len(rest) > 0:
            l = rest.split('.', 1)
            base = l[0]
            rest = ''
            if len(l) > 1:
                rest = l[1]
                k = base.find('[')
                if k > 0:
                    base = base[:k]
                    cur_obj.__dict__.setdefault(base, IndexedPropertyCollection())
                    cur_obj = cur_obj.__dict__[base]
                    base = rest
                    rest = ''
                else:
                    cur_obj.__dict__.setdefault(base, PropertyCollection())
                    cur_obj = cur_obj.__dict__[base]

        if type(doc) == Doc:
            doc.name = name
        if cur_obj == self:
            if type(attr) == tuple:
                fget, fset, fdel = attr
                PropertyCollection._add_property(self, base, fget, fset, fdel, doc)
            else:
                PropertyCollection._add_method(self, base, attr, doc)
        elif type(attr) == tuple:
            fget, fset, fdel = attr
            cur_obj._add_property(base, fget, fset, fdel, doc)
        else:
            cur_obj._add_method(base, attr, doc)

    def _add_method(self, name, f, doc=None):
        self._add_attribute(name, f, doc)

    def _add_property(self, name, fget, fset=None, fdel=None, doc=None):
        self._add_attribute(name, (fget, fset, fdel), doc)


class Doc(object):
    """IVI documentation object"""

    def __init__(self, doc='', cls='', grp='', section='', name=''):
        self.doc = trim_doc(doc)
        self.name = name
        self.cls = cls
        self.grp = grp
        self.section = section

    def render(self):
        txt = '.. attribute:: ' + self.name + '\n\n'
        if self.cls != '':
            txt += '   *IVI class ' + self.cls + ', capability group ' + self.cls + self.grp + ', section ' + self.section + '*\n\n'
        txt += ('\n').join('   ' + x for x in self.doc.splitlines())
        txt += '\n'
        return txt

    def __str__(self):
        return self.doc


def add_attribute(obj, name, attr, doc=None):
    IviContainer._add_attribute(obj, name, attr, doc)


def add_method(obj, name, f, doc=None):
    add_attribute(obj, name, f, doc)


def add_property(obj, name, fget, fset=None, fdel=None, doc=None):
    add_attribute(obj, name, (fget, fset, fdel), doc)


def add_group_capability(obj, cap):
    obj.__dict__.setdefault('_identity_group_capabilities', list())
    obj._identity_group_capabilities.insert(0, cap)


def build_ieee_block(data):
    """Build IEEE block"""
    return str('#8%08d' % len(data)).encode('utf-8') + data


def decode_ieee_block(data):
    """Decode IEEE block"""
    if len(data) == 0:
        return ''
    else:
        ind = 0
        c = ('#').encode('utf-8')
        while data[ind:ind + 1] != c:
            ind += 1

        ind += 1
        l = int(data[ind:ind + 1])
        ind += 1
        if l > 0:
            num = int(data[ind:ind + l].decode('utf-8'))
            ind += l
            return data[ind:ind + num]
        return data[ind:]


def get_sig(sig):
    """Parse various signal inputs into x and y components"""
    if type(sig) == tuple and len(sig) == 2:
        x, y = sig
        x = np.array(x)
        y = np.array(y)
    elif type(sig) == list and type(sig[0]) == tuple and len(sig[0]) == 2:
        x, y = zip(*sig)
        x = np.array(x)
        y = np.array(y)
    elif (type(sig) == np.ndarray or type(sig) == np.matrix) and len(sig.shape) == 2 and sig.shape[0] == 2:
        x = np.array(sig[0])
        y = np.array(sig[1])
    elif (type(sig) == np.ndarray or type(sig) == np.matrix) and len(sig.shape) == 2 and sig.shape[1] == 2:
        x = np.array(sig[:, 0])
        y = np.array(sig[:, 1])
    else:
        raise Exception('Unknown argument')
    if len(x) != len(y):
        raise Exception('Signals must be the same length!')
    return (x, y)


def rms(y):
    """Calculate the RMS value of the signal"""
    return np.linalg.norm(y) / np.sqrt(y.size)


def trim_doc(docstring):
    if not docstring:
        return ''
    docstring = str(docstring)
    lines = docstring.expandtabs().splitlines()
    indent = 10000
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    trimmed = [
     lines[0].strip()]
    if indent < 10000:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[(-1)]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return ('\n').join(trimmed)


def doc(obj=None, itm=None, docs=None, prefix=None):
    """Python IVI documentation generator"""
    st = ''
    if prefix is None or len(prefix) == 0:
        prefix = ''
    elif not prefix[(-1)] == '.':
        prefix += '.'
    if docs is not None:
        for n in sorted(docs.keys()):
            d = docs[n]
            if type(d) == dict:
                st += doc(docs=d, prefix=prefix + n)
            else:
                st += prefix + n + '\n'

        return st
    if itm is not None:
        l = itm.split('.', 1)
        n = l[0]
        r = ''
        k = n.find('[')
        if k > 0:
            n = n[:k]
        if len(l) > 1:
            r = l[1]
            if type(obj) == dict and n in obj:
                return doc(obj[n], r, prefix=prefix + n)
            if n in obj.__dict__:
                return doc(obj.__dict__[n], r, prefix=prefix + n)
            if hasattr(obj, '_docs') and n in obj._docs:
                d = obj._docs[n]
                if type(d) == dict:
                    return doc(d, r, prefix=prefix + n)
        else:
            d = None
            if type(obj) == dict and n in obj:
                d = obj[n]
            else:
                if hasattr(obj, '_docs') and n in obj._docs:
                    d = obj._docs[n]
                if type(d) == Doc:
                    return d
                if type(d) == str:
                    return trim_doc(d)
        return 'error'
    if hasattr(obj, '__dict__'):
        for n in sorted(obj.__dict__.keys()):
            o = obj.__dict__[n]
            extra = ''
            if type(o) == IndexedPropertyCollection:
                extra = '[]'
            if n == '_docs':
                st += doc(docs=o, prefix=prefix)
            elif hasattr(o, '_docs'):
                st += doc(o, prefix=prefix + n)

        if len(st) > 0:
            return st
    return 'error'


def help(obj=None, itm=None, complete=False, indent=0):
    """Python IVI help system"""
    if complete:
        l = doc(obj).split('\n')
        l = sorted(filter(None, l))
        for m in l:
            d = doc(obj, m)
            if type(d) == Doc:
                print d.render()
            if type(d) == str:
                print indent * ' ' + '.. attribute:: ' + m + '\n'
                d = ('\n').join((indent + 3) * ' ' + x for x in d.splitlines())
                print d
                print '\n'

    elif obj is not None:
        print doc(obj, itm)
    else:
        print trim_doc('\n            Using Python IVI help\n            ---------------------\n            \n            Use the help method to get documentation on IVI methods and properties. The\n            IVI help system is a little different from the built-in Python help system.\n            Here are some examples on how to use it correctly:\n\n            This help method can be called with no parameters:\n\n                import ivi\n                instr = ivi.Driver()\n                instr.help()\n\n            This will print a list of all of the available methods and properties,\n            like so:\n\n                close\n                initialized\n                initialize\n                driver_operation.cache\n                driver_operation.clear_interchange_warnings\n                driver_operation.driver_setup\n                ...\n\n            The higher level groups can also be passed to the help method:\n\n                import ivi\n                instr = ivi.Driver()\n                instr.help(instr.identity)\n\n            This will output everything inside of the sub group:\n\n                get_supported_instrument_models\n                get_group_capabilities\n                specification_major_version\n                ...\n\n            Finally, individual methods and properties can be passed as strings:\n\n                import ivi\n                instr = ivi.Driver()\n                instr.help("identity.supported_instrument_models")\n\n            This will result in the complete documentation:\n\n                Returns a comma-separated list of names of instrument models with which\n                the IVI specific driver is compatible. The string has no white space\n                ...\n            ')
    return


class DriverOperation(IviContainer):
    """Inherent IVI methods for driver operation"""

    def __init__(self, *args, **kwargs):
        super(DriverOperation, self).__init__(*args, **kwargs)
        self._driver_operation_cache = True
        self._driver_operation_driver_setup = ''
        self._driver_operation_interchange_check = False
        self._driver_operation_logical_name = ''
        self._driver_operation_query_instrument_status = False
        self._driver_operation_range_check = True
        self._driver_operation_record_coercions = False
        self._driver_operation_io_resource_descriptor = ''
        self._driver_operation_simulate = False
        self._driver_operation_interchange_warnings = list()
        self._driver_operation_coercion_records = list()
        self._add_property('driver_operation.cache', self._get_driver_operation_cache, self._set_driver_operation_cache, None, '\n                        If True, the specific driver caches the value of attributes, and the IVI\n                        specific driver keeps track of the current instrument settings so that it\n                        can avoid sending redundant commands to the instrument. If False, the\n                        specific driver does not cache the value of attributes.\n                        \n                        The default value is True. When the user opens an instrument session\n                        through an IVI class driver or uses a logical name to initialize a\n                        specific driver, the user can override this value by specifying a value in\n                        the IVI configuration store. The Initialize function allows the user to\n                        override both the default value and the value that the user specifies in\n                        the IVI configuration store.\n                        ')
        self._add_property('driver_operation.driver_setup', self._get_driver_operation_driver_setup, None, None, '\n                        Returns the driver setup string that the user specified in the IVI\n                        configuration store when the instrument driver session was initialized or\n                        passes in the OptionString parameter of the Initialize function. Refer to\n                        Section 6.14, Initialize, for the restrictions on the format of the driver\n                        setup string.\n                        \n                        The string that this attribute returns does not have a predefined maximum\n                        length.\n                        ')
        self._add_property('driver_operation.interchange_check', self._get_driver_operation_interchange_check, self._set_driver_operation_interchange_check, None, '\n                        If True, the specific driver performs interchangeability checking. If the\n                        Interchange Check attribute is enabled, the specific driver maintains a\n                        record of each interchangeability warning that it encounters. The user\n                        calls the Get Next Interchange Warning function to extract and delete the\n                        oldest interchangeability warning from the list. Refer to Section 6.11,\n                        Get Next Interchange Warning, Section 6.2, Clear Interchange Warnings,\n                        and Section 6.18, Reset Interchange Check, for more information. If False,\n                        the specific driver does not perform interchangeability checking.\n                        \n                        If the user opens an instrument session through an IVI class driver and\n                        the Interchange Check attribute is enabled, the IVI class driver may\n                        perform additional interchangeability checking. The IVI class driver\n                        maintains a list of the interchangeability warnings that it encounters.\n                        The user can retrieve both class driver interchangeability warnings and\n                        specific driver interchangeability warnings by calling the Get Next\n                        Interchange Warning function on the class driver session.\n                        \n                        If the IVI specific driver does not implement interchangeability checking,\n                        the specific driver returns the Value Not Supported error when the user\n                        attempts to set the Interchange Check attribute to True. If the specific\n                        driver does implement interchangeability checking and the user opens an\n                        instrument session through an IVI class driver, the IVI class driver\n                        accepts True as a valid value for the Interchange Check attribute even if\n                        the class driver does not implement interchangeability checking\n                        capabilities of its own.\n                        \n                        The default value is False. If the user opens an instrument session\n                        through an IVI class driver or initializes an IVI specific driver with a\n                        logical name, the user can override this value in the IVI configuration\n                        store. The Initialize function allows the user to override both the\n                        default value and the value that the userspecifies in the IVI\n                        configuration store.\n                        ')
        self._add_property('driver_operation.logical_name', self._get_driver_operation_logical_name, None, None, '\n                        Returns the IVI logical name that the user passed to the Initialize\n                        function. If the user initialized the IVI specific driver directly and did\n                        not pass a logical name, then this attribute returns an empty string.\n                        Refer to IVI-3.5: Configuration Server Specification for restrictions on\n                        the format of IVI logical names.\n                        \n                        The string that this attribute returns contains a maximum of 256\n                        characters including the NULL character.\n                        ')
        self._add_property('driver_operation.query_instrument_status', self._get_driver_operation_query_instrument_status, self._set_driver_operation_query_instrument_status, None, '\n                        If True, the IVI specific driver queries the instrument status at the end\n                        of each user operation. If False, the IVI specific driver does not query\n                        the instrument status at the end of each user operation. Querying the\n                        instrument status is very useful for debugging. After validating the\n                        program, the user can set this attribute to False to disable status\n                        checking and maximize performance. The user specifies this value for the\n                        entire IVI driver session.\n                        \n                        The default value is False. When the user opens an instrument session\n                        through an IVI class driver or uses a logical name to initialize an IVI\n                        specific driver, the user can override this value by specifying a value in\n                        the IVI configuration store. The Initialize function allows the user to\n                        override both the default value and the value that the user specifies in\n                        the IVI configuration store.\n                        ')
        self._add_property('driver_operation.range_check', self._get_driver_operation_range_check, self._set_driver_operation_range_check, None, '\n                        If True, the IVI specific driver validates attribute values and function\n                        parameters. If False, the IVI specific driver does not validate attribute\n                        values and function parameters.\n                        \n                        If range check is enabled, the specific driver validates the parameter\n                        values that users pass to driver functions. Validating attribute values\n                        and function parameters is useful for debugging. After validating the\n                        program, the user can set this attribute to False to disable range\n                        checking and maximize performance. The default value is True. When the\n                        user opens an instrument session through an IVI class driver or uses a\n                        logical name to initialize an IVI specific driver, the user can override\n                        this value by specifying a value in the IVI configuration store. The\n                        Initialize function allows the user to override both the default value and\n                        the value that the user specifies in the IVI configuration store.\n                        ')
        self._add_property('driver_operation.record_coercions', self._get_driver_operation_record_coercions, self._set_driver_operation_record_coercions, None, '\n                        If True, the IVI specific driver keeps a list of the value coercions it\n                        makes for ViInt32 and ViReal64 attributes. If False, the IVI specific\n                        driver does not keep a list of the value coercions it makes for ViInt32 and\n                        ViReal64 attributes.\n                        \n                        If the Record Value Coercions attribute is enabled, the specific driver\n                        maintains a record of each coercion. The user calls the Get Next Coercion\n                        Record function to extract and delete the oldest coercion record from the\n                        list. Refer to Section 6.10, Get Next Coercion Record, for more\n                        information.\n                        \n                        If the IVI specific driver does not implement coercion recording, the\n                        specific driver returns the Value Not Supported error when the user\n                        attempts to set the Record Value Coercions attribute to True.\n                        \n                        The default value is False. When the user opens an instrument session\n                        through an IVI class driver or uses a logical name to initialize a IVI\n                        specific driver, the user can override this value by specifying a value in\n                        the IVI configuration store. The Initialize function allows the user to\n                        override both the default value and the value that the user specifies in\n                        the IVI configuration store.\n                        ')
        self._add_property('driver_operation.io_resource_descriptor', self._get_driver_operation_io_resource_descriptor, None, None, '\n                        Returns the resource descriptor that the user specified for the physical\n                        device. The user specifies the resource descriptor by editing the IVI\n                        configuration store or by passing a resource descriptor to the Initialize\n                        function of the specific driver. Refer to Section 6.14, Initialize, for the\n                        restrictions on the contents of the resource descriptor string.\n                        \n                        The string that this attribute returns contains a maximum of 256 characters\n                        including the NULL character.\n                        ')
        self._add_property('driver_operation.simulate', self._get_driver_operation_simulate, None, None, '\n                        If True, the IVI specific driver simulates instrument driver I/O\n                        operations. If False, the IVI specific driver communicates directly with\n                        the instrument.\n                        \n                        If simulation is enabled, the specific driver functions do not perform\n                        instrument I/O. For output parameters that represent instrument data, the\n                        specific driver functions return simulated values.\n                        \n                        The default value is False. When the user opens an instrument session\n                        through an IVI class driver or uses a logical name to initialize an IVI\n                        specific driver, the user can override this value by specifying a value in\n                        the IVI configuration store. The Initialize function allows the user to\n                        override both the default value and the value that the user specifies in\n                        the IVI configuration store.\n                        ')
        self._add_method('driver_operation.clear_interchange_warnings', self._driver_operation_clear_interchange_warnings, '\n                        This function clears the list of interchangeability warnings that the IVI\n                        specific driver maintains.\n                        \n                        When this function is called on an IVI class driver session, the function\n                        clears the list of interchangeability warnings that the class driver and\n                        the specific driver maintain.\n                        \n                        Refer to the Interchange Check attribute for more information on\n                        interchangeability checking.\n                        ')
        self._add_method('driver_operation.get_next_coercion_record', self._driver_operation_get_next_coercion_record, '\n                        If the Record Value Coercions attribute is set to True, the IVI specific\n                        driver keeps a list of all value coercions it makes on integer and\n                        floating point attributes. This function obtains the coercion information\n                        associated with the IVI session. It retrieves and clears the oldest\n                        instance in which the specific driver coerced a value the user specified\n                        to another value.\n                        \n                        The function returns an empty string in the CoercionRecord parameter if no\n                        coercion records remain for the session.\n                        \n                        The coercion record string shall contain the following information:\n                        \n                        * The name of the attribute that was coerced. This can be the generic name,\n                          the COM property name, or the C defined constant.\n                        * If the attribute applies to a repeated capability, the name of the\n                          virtual or physical repeated capability identifier.\n                        * The value that the user specified for the attribute.\n                        * The value to which the attribute was coerced.\n                        \n                        A recommended format for the coercion record string is as follows::\n                        \n                            " Attribute " + <attribute name> + [" on <repeated capability> " +\n                            <repeated capability identifier>] + " was coerced from " +\n                            <desiredVal> + " to " + <coercedVal>\n                        \n                        .\n                        \n                        And example coercion record string is as follows::\n                        \n                            Attribute TKTDS500_ATTR_VERTICAL_RANGE on channel ch1 was coerced from\n                            9.0 to 10.0.\n                        \n                        ')
        self._add_method('driver_operation.get_next_interchange_warning', self._driver_operation_get_next_interchange_warning, '\n                        If the Interchange Check attribute is set to True, the IVI specific driver\n                        keeps a list of all interchangeability warnings that it encounters. This\n                        function returns the interchangeability warnings associated with the IVI\n                        session. It retrieves and clears the oldest interchangeability warning\n                        from the list. Interchangeability warnings indicate that using the\n                        application with a different instrument might cause different behavior.\n                        \n                        When this function is called on an IVI class driver session, it may return\n                        interchangeability warnings generated by the IVI class driver as well as\n                        interchangeability warnings generated by the IVI specific driver. The IVI\n                        class driver determines the relative order in which the IVI class driver\n                        warnings are returned in relation to the IVI specific driver warnings.\n                        \n                        The function returns an empty string in the InterchangeWarning parameter\n                        if no interchangeability warnings remain for the session.\n                        \n                        Refer to the Interchange Check attribute for more information on\n                        interchangeability checking.\n                        ')
        self._add_method('driver_operation.invalidate_all_attributes', self._driver_operation_invalidate_all_attributes, '\n                        This function invalidates the cached values of all attributes for the\n                        session.\n                        ')
        self._add_method('driver_operation.reset_interchange_check', self._driver_operation_reset_interchange_check, '\n                        This function resets the interchangeability checking algorithms of the IVI\n                        specific driver so that specific driver functions that execute prior to\n                        calling this function have no effect on whether future calls to the\n                        specific driver generate interchangeability warnings.\n                        \n                        When developing a complex test system that consists of multiple test\n                        modules, it is generally a good idea to design the test modules so that\n                        they can run in any order. To do so requires ensuring that each test\n                        module completely configures the state of each instrument it uses. If a\n                        particular test module does not completely configure the state of an\n                        instrument, the state of the instrument depends on the configuration from\n                        a previously executed test module. If the test modules execute in a\n                        different order, the behavior of the instrument and therefore the entire\n                        test module is likely to change. This change in behavior is generally\n                        instrument specific and represents an interchangeability problem.\n                        \n                        Users can use this function to test for such cases. By calling this\n                        function at the beginning of a test module, users can determine whether\n                        the test module has dependencies on the operation of previously executed\n                        test modules. Any interchangeability warnings that occur after the user\n                        calls this function indicate that the section of the test program that\n                        executes after this function and prior to the generation of the warning\n                        does not completely configure the instrument and that the user is likely\n                        to experience different behavior if the user changes the execution order\n                        of the test modules or if the user changes instruments.\n                        \n                        Note: This function does not clear interchangeability warnings from the\n                        list of interchangeability warnings. To guarantee that the Get Next\n                        Interchange Warning function returns interchangeability warnings that\n                        occur only after the program calls function, the user must clear the list\n                        of interchangeability warnings by calling the Clear Interchange Warnings\n                        function.\n                        \n                        Refer to the Interchange Check attribute for more information on\n                        interchangeability checking.\n                        ')
        return

    def _get_driver_operation_cache(self):
        return self._driver_operation_cache

    def _set_driver_operation_cache(self, value):
        self._driver_operation_cache = bool(value)

    def _get_driver_operation_driver_setup(self):
        return self._driver_operation_driver_setup

    def _get_driver_operation_interchange_check(self):
        return self._driver_operation_interchange_check

    def _set_driver_operation_interchange_check(self, value):
        self._driver_operation_interchange_check = bool(value)

    def _get_driver_operation_logical_name(self):
        return self._driver_operation_logical_name

    def _get_driver_operation_query_instrument_status(self):
        return self._driver_operation_query_instrument_status

    def _set_driver_operation_query_instrument_status(self, value):
        self._driver_operation_query_instrument_status = bool(value)

    def _get_driver_operation_range_check(self):
        return self._driver_operation_range_check

    def _set_driver_operation_range_check(self, value):
        self._driver_operation_range_check = bool(value)

    def _get_driver_operation_record_coercions(self):
        return self._driver_operation_record_coercions

    def _set_driver_operation_record_coercions(self, value):
        self._driver_operation_record_coercions = bool(value)

    def _get_driver_operation_io_resource_descriptor(self):
        return self._driver_operation_io_resource_descriptor

    def _get_driver_operation_simulate(self):
        return self._driver_operation_simulate

    def _set_driver_operation_simulate(self, value):
        value = bool(value)
        if self._driver_operation_simulate and not value:
            raise SimulationStateException()
        self._driver_operation_simulate = value

    def _driver_operation_clear_interchange_warnings(self):
        self._driver_operation_interchange_warnings = list()

    def _driver_operation_get_next_coercion_record(self):
        if len(self._driver_operation_coercion_records) > 0:
            return self._driver_operation_coercion_records.pop()
        return ''

    def _driver_operation_get_next_interchange_warning(self):
        if len(self._driver_operation_interchange_warnings) > 0:
            return self._driver_operation_interchange_warnings.pop()
        return ''

    def _driver_operation_invalidate_all_attributes(self):
        pass

    def _driver_operation_reset_interchange_check(self):
        pass


class DriverIdentity(IviContainer):
    """Inherent IVI methods for identification"""

    def __init__(self, *args, **kwargs):
        super(DriverIdentity, self).__init__(*args, **kwargs)
        self._identity_description = 'Base IVI Driver'
        self._identity_identifier = ''
        self._identity_revision = ''
        self._identity_vendor = ''
        self._identity_instrument_manufacturer = 'Cannot query from instrument'
        self._identity_instrument_model = 'Cannot query from instrument'
        self._identity_instrument_firmware_revision = 'Cannot query from instrument'
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list()
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._add_property('identity.description', self._get_identity_description, None, None, '\n                        Returns a brief description of the IVI software component.\n                        \n                        The string that this attribute returns has no maximum size.\n                        ')
        self._add_property('identity.identifier', self._get_identity_identifier, None, None, '\n                        Returns the case-sensitive unique identifier of the IVI software\n                        component. The string that this attribute returns contains a maximum of 32\n                        characters including the NULL character.\n                        ')
        self._add_property('identity.revision', self._get_identity_revision, None, None, '\n                        Returns version information about the IVI software component. Refer to\n                        Section 3.1.2.2, Additional Compliance Rules for Revision String\n                        Attributes, for additional rules regarding this attribute.\n                        \n                        The string that this attribute returns has no maximum size.\n                        ')
        self._add_property('identity.vendor', self._get_identity_vendor, None, None, '\n                        Returns the name of the vendor that supplies the IVI software component.\n                        \n                        The string that this attribute returns has no maximum size.\n                        ')
        self._add_property('identity.instrument_manufacturer', self._get_identity_instrument_manufacturer, None, None, '\n                        Returns the name of the manufacturer of the instrument. The IVI specific\n                        driver returns the value it queries from the instrument as the value of\n                        this attribute or a string indicating that it cannot query the instrument\n                        identity.\n                        \n                        In some cases, it is not possible for the specific driver to query the\n                        manufacturer of the instrument. This can occur when the Simulate attribute\n                        is set to True or if the instrument is not capable of returning the\n                        manufacturer. For these cases, the specific driver returns defined strings\n                        for this attribute. If the Simulate attribute is set to True, the specific\n                        driver returns "Not available while simulating" as the value of this\n                        attribute. If the instrument is not capable of returning the manufacturer\n                        and the Simulate attribute is set to False, the specific driver returns\n                        "Cannot query from instrument" as the value of this attribute.\n                        \n                        The string that this attribute returns does not have a predefined maximum\n                        length.\n                        ')
        self._add_property('identity.instrument_model', self._get_identity_instrument_model, None, None, '\n                        Returns the model number or name of the physical instrument. The IVI\n                        specific driver returns the value it queries from the instrument or a\n                        string indicating that it cannot query the instrument identity.\n                        \n                        In some cases, it is not possible for the specific driver to query the\n                        model of the instrument. This can occur when the Simulate attribute is\n                        set to True or if the instrument is not capable of returning the model.\n                        For these cases, the specific driver returns defined strings for this\n                        attribute. If the Simulate attribute is set to True, the specific driver\n                        returns "Not available while simulating" as the value of this attribute.\n                        If the instrument is not capable of returning the model and the Simulate\n                        attribute is set to False, the specific driver returns "Cannot query\n                        from instrument" as the value of this attribute.\n                        \n                        The string that this attribute returns does not have a predefined maximum\n                        length.\n                        ')
        self._add_property('identity.instrument_firmware_revision', self._get_identity_instrument_firmware_revision, None, None, '\n                        Returns an instrument specific string that contains the firmware\n                        revision information of the physical instrument. The IVI specific driver\n                        returns the value it queries from the instrument as the value of this\n                        attribute or a string indicating that it cannot query the instrument\n                        identity.\n                        \n                        In some cases, it is not possible for the specific driver to query the\n                        firmware revision of the instrument. This can occur when the Simulate\n                        attribute is set to True or if the instrument is not capable of returning\n                        the firmware revision. For these cases, the specific driver returns\n                        defined strings for this attribute. If the Simulate attribute is set to\n                        True, the specific driver returns "Not available while simulating" as the\n                        value of this attribute. If the instrument is not capable of returning the\n                        firmware version and the Simulate attribute is set to False, the specific\n                        driver returns "Cannot query from instrument" as the value of this\n                        attribute.\n                        \n                        The string that this attribute returns does not have a predefined maximum\n                        length.\n                        ')
        self._add_property('identity.specification_major_version', self._get_identity_specification_major_version, None, None, '\n                        Returns the major version number of the class specification in accordance\n                        with which the IVI software component was developed. The value is a\n                        positive integer value.\n                        \n                        If the software component is not compliant with a class specification, the\n                        software component returns zero as the value of this attribute.\n                        ')
        self._add_property('identity.specification_minor_version', self._get_identity_specification_minor_version, None, None, '\n                        Returns the minor version number of the class specification in accordance\n                        with which the IVI software component was developed. The value is a\n                        positive integer value.\n                        \n                        If the software component is not compliant with a class specification, the\n                        software component returns zero as the value of this attribute.\n                        ')
        self._add_property('identity.supported_instrument_models', self._get_identity_supported_instrument_models, None, None, '\n                        Returns a comma-separated list of names of instrument models with which\n                        the IVI specific driver is compatible. The string has no white space\n                        except possibly embedded in the instrument model names. An example of a\n                        string that this attribute might return is "TKTDS3012,TKTDS3014,TKTDS3016".\n                        \n                        It is not necessary for the string to include the abbreviation for the\n                        manufacturer if it is the same for all models. In the example above, it is\n                        valid for the attribute to return the string "TDS3012,TDS3014,TDS3016".\n                        \n                        The string that this attribute returns does not have a predefined maximum\n                        length.\n                        ')
        self._add_property('identity.group_capabilities', self._get_identity_group_capabilities, None, None, '\n                        Returns a comma-separated list that identifies the class capability groups\n                        that the IVI specific driver implements. The items in the list are\n                        capability group names that the IVI class specifications define. The\n                        string has no white space except for white space that might be embedded in\n                        a capability group name.\n                        \n                        If the IVI specific driver does not comply with an IVI class specification,\n                        the specific driver returns an empty string as the value of this attribute.\n                        \n                        The string that this attribute returns does not have a predefined maximum\n                        length.\n                        ')
        self._add_method('identity.get_group_capabilities', self._identity_get_group_capabilities, '\n                        Returns a list of names of class capability groups that the IVI specific\n                        driver implements. The items in the list are capability group names that\n                        the IVI class specifications define. The list is returned as a list of\n                        strings.\n                        \n                        If the IVI specific driver does not comply with an IVI class specification,\n                        the specific driver returns an array with zero elements.\n                        ')
        self._add_method('identity.get_supported_instrument_models', self._identity_get_supported_instrument_models, '\n                        Returns a list of names of instrument models with which the IVI specific\n                        driver is compatible. The list is returned as a list of strings. For\n                        example, this attribute might return the strings "TKTDS3012", "TKTDS3014",\n                        and "TKTDS3016" .\n                        \n                        It is not necessary for the string to include the abbreviation for the\n                        manufacturer if it is the same for all models. In the example above, it is\n                        valid for the attribute to return the strings "TDS3012", "TDS3014", and\n                        "TDS3016".\n                        ')
        return

    def _add_group_capability(self, name):
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, name)

    def _get_identity_description(self):
        return self._identity_description

    def _get_identity_identifier(self):
        return self._identity_identifier

    def _get_identity_revision(self):
        return self._identity_revision

    def _get_identity_vendor(self):
        return self._identity_vendor

    def _get_identity_instrument_manufacturer(self):
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        return self._identity_instrument_model

    def _get_identity_instrument_firmware_revision(self):
        return self._identity_instrument_firmware_revision

    def _get_identity_specification_major_version(self):
        return self._identity_specification_major_version

    def _get_identity_specification_minor_version(self):
        return self._identity_specification_minor_version

    def _get_identity_supported_instrument_models(self):
        return (',').join(self._identity_supported_instrument_models)

    def _get_identity_group_capabilities(self):
        return (',').join(self._identity_group_capabilities)

    def _identity_get_group_capabilities(self):
        return self._identity_group_capabilities

    def _identity_get_supported_instrument_models(self):
        return self._identity_supported_instrument_models


class DriverUtility(IviContainer):
    """Inherent IVI utility methods"""

    def __init__(self, *args, **kwargs):
        super(DriverUtility, self).__init__(*args, **kwargs)
        self._add_method('utility.disable', self._utility_disable, '\n                        The Disable operation places the instrument in a quiescent state as\n                        quickly as possible. In a quiescent state, an instrument has no or minimal\n                        effect on the external system to which it is connected. The Disable\n                        operation might be similar to the Reset operation in that it places the\n                        instrument in a known state. However, the Disable operation does not\n                        perform the other operations that the Reset operation performs such as\n                        configuring the instrument options on which the IVI specific driver\n                        depends. For some instruments, the disable function may do nothing.\n                        \n                        The IVI class specifications define the exact behavior of this function\n                        for each instrument class. Refer to the IVI class specifications for more\n                        information on the behavior of this function.\n                        ')
        self._add_method('utility.error_query', self._utility_error_query, "\n                        Queries the instrument and returns instrument specific error information.\n                        \n                        Generally, the user calls this function after another function in the IVI\n                        driver returns the Instrument Status error. The IVI specific driver\n                        returns the Instrument Status error when the instrument indicates that it\n                        encountered an error and its error queue is not empty. Error Query\n                        extracts an error out of the instrument's error queue.\n                        \n                        For instruments that have status registers but no error queue, the IVI\n                        specific driver emulates an error queue in software.\n                        \n                        The method returns a tuple containing the error code and error message.\n                        ")
        self._add_method('utility.lock_object', self._utility_lock_object, '\n                        This function obtains a multithread lock for this instance of the driver.\n                        Before it does so, Lock Session waits until all other execution threads\n                        have released their locks or for the length of time specified by the\n                        maximum time parameter, whichever come first. The type of lock obtained\n                        depends upon the parameters passed to the specific driver constructor.\n                        \n                        The user can use Lock Session with IVI specific drivers to protect a\n                        section of code that requires exclusive access to the instrument. This\n                        occurs when the user takes multiple actions that affect the instrument\n                        and the user wants to ensure that other execution threads do not disturb\n                        the instrument state until all the actions execute. For example, if the\n                        user sets various instrument attributes and then triggers a measurement,\n                        the user must ensure no other execution thread modifies the attribute\n                        values until the user finishes taking the measurement. \n                        \n                        It is important to note that this lock is not related to I/O locks such as\n                        the VISA resource locking mechanism.\n                        \n                        The user can safely make nested calls to Lock Session within the same\n                        thread. To completely unlock the session, the user must balance each call\n                        to Lock Session with a call to Unlock Session. Calls to Lock Session must\n                        always obtain the same lock that is used internally by the IVI driver to\n                        guard individual method calls.\n                        ')
        self._add_method('utility.reset', self._utility_reset, '\n                        This function performs the following actions:\n                        \n                        * Places the instrument in a known state. In an IEEE 488.2 instrument, the\n                          Reset function sends the command string ``*RST`` to the instrument.\n                        * Configures instrument options on which the IVI specific driver depends.\n                          A specific driver might enable or disable headers or enable binary mode\n                          for waveform transfers.\n                        \n                        The user can either call the Reset function separately or specify that it\n                        be called from the Initialize function. The Initialize function performs\n                        additional operations after performing the reset operation to place the\n                        instrument in a state more suitable for interchangeable programming. To\n                        reset the device and perform these additional operations, call the Reset\n                        With Defaults function instead of the Reset function.\n                        ')
        self._add_method('utility.reset_with_defaults', self._utility_reset_with_defaults, '\n                        The Reset With Defaults function performs the same operations that the\n                        Reset function performs and then performs the following additional\n                        operations in the specified order:\n                        \n                        * Disables the class extension capability groups that the IVI specific\n                          driver implements.\n                        * If the class specification with which the IVI specific driver is\n                          compliant defines initial values for attributes, this function sets\n                          those attributes to the initial values that the class specification\n                          defines.\n                        * Configures the initial settings for the specific driver and instrument\n                          based on the information retrieved from the IVI configuration store when\n                          the instrument driver session was initialized.\n                        \n                        Notice that the Initialize function also performs these functions. To\n                        place the instrument and the IVI specific driver in the exact same state\n                        that they attain when the user calls the Initialize function, the user\n                        must first call the Close function and then the Initialize function.\n                        ')
        self._add_method('utility.self_test', self._utility_self_test, "\n                        Causes the instrument to perform a self test. Self Test waits for the\n                        instrument to complete the test. It then queries the instrument for the\n                        results of the self test and returns the results to the user.\n                        \n                        If the instrument passes the self test, this function returns the tuple::\n                        \n                            (0, 'Self test passed')\n                       \n                        Otherwise, the function returns a tuple of the result code and message.\n                        ")
        self._add_method('utility.unlock_object', self._utility_unlock_object, '\n                        This function releases a lock that the Lock Session function acquires.\n                        \n                        Refer to Lock Session for additional information on IVI session locks.\n                        ')

    def _utility_disable(self):
        pass

    def _utility_error_query(self):
        error_code = 0
        error_message = 'No error'
        return (error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_reset(self):
        pass

    def _utility_reset_with_defaults(self):
        self.utility_reset()

    def _utility_self_test(self):
        code = 0
        message = 'Self test passed'
        return (code, message)

    def _utility_unlock_object(self):
        pass


class Driver(DriverOperation, DriverIdentity, DriverUtility):
    """Inherent IVI methods for all instruments"""

    def __init__(self, resource=None, id_query=False, reset=False, *args, **kwargs):
        kw = {}
        for k in ('range_check', 'query_instr_status', 'cache', 'simulate', 'record_coercions',
                  'interchange_check', 'driver_setup', 'prefer_pyvisa'):
            if k in kwargs:
                kw[k] = kwargs.pop(k)

        self._interface = None
        self._initialized = False
        self.__dict__.setdefault('_instrument_id', '')
        self._cache_valid = dict()
        super(Driver, self).__init__(*args, **kwargs)
        self._add_method('initialize', self._initialize, '\n                        The user must call the Initialize function prior to calling other IVI\n                        driver functions that access the instrument. The Initialize function is\n                        called automatically by the constructor if a resource string is passed as\n                        the first argument to the constructor.  \n                        \n                        If simulation is disabled when the user calls the Initialize function, the\n                        function performs the following actions:\n                        \n                        * Opens and configures an I/O session to the instrument.\n                        * If the user passes True for the IdQuery parameter, the function queries\n                          the instrument for its ID and verifies that the IVI specific driver\n                          supports the particular instrument model. If the instrument cannot\n                          return its ID, the specific driver returns the ID Query Not Supported\n                          warning.\n                        * If the user passes True for the Reset parameter, the function places the\n                          instrument in a known state. In an IEEE 488.2 instrument, the function\n                          sends the command string "*RST" to the instrument. If the instrument\n                          cannot perform a reset, the IVI specific driver returns the Reset Not\n                          Supported warning. \n                        * Configures instrument options on which the IVI specific driver depends.\n                          For example, a specific driver might enable or disable headers or enable\n                          binary mode for waveform transfers.\n                        * Performs the following operations in the given order:\n                            1. Disables the class extension capability groups that the IVI\n                               specific driver does not implement.\n                            2. If the class specification with which the IVI specific driver is\n                               compliant defines initial values for attributes, this function sets\n                               the attributes to the values that the class specification defines.\n                            3. If the ResourceName parameter is a logical name, the IVI specific\n                               driver configures the initial settings for the specific driver and\n                               instrument based on the configuration of the logical name in the IVI \n                               configuration store.\n                        \n                        If simulation is enabled when the user calls the Initialize function, the\n                        function performs the following actions:\n                        \n                        * If the user passes True for the IdQuery parameter and the instrument\n                          cannot return its ID, the IVI specific driver returns the ID Query Not\n                          Supported warning.\n                        * If the user passes True for the Reset parameter and the instrument\n                          cannot perform a reset, the IVI specific driver returns the Reset Not\n                          Supported warning.\n                        * If the ResourceName parameter is a logical name, the IVI specific driver\n                          configures the initial settings for the specific driver based on the\n                          configuration of the logical name in the IVI configuration store.\n                        \n                        Some instrument driver operations require or take into account information\n                        from the IVI configuration store. Examples of such information are virtual\n                        repeated capability name mappings and the value of certain inherent\n                        attributes. An IVI driver shall retrieve all the information for a session\n                        from the IVI configuration store during the Initialization function. The\n                        IVI driver shall not read any information from the IVI configuration store\n                        for a session after the Initialization function completes. Refer to\n                        Section 3.2.3, Instantiating the Right Configuration Store From Software\n                        Modules, of IVI-3.5: Configuration Server Specification for details on how\n                        to correctly instantiate the configuration store.\n                        \n                        The ResourceName parameter must contain either a logical name that is\n                        defined in the IVI configuration store or an instrument specific string\n                        that identifies the I/O address of the instrument, such as a VISA resource\n                        descriptor string. Refer to IVI-3.5: Configuration Server Specification\n                        for restrictions on the format of IVI logical names. Refer to the\n                        VXIplug&play specifications for the grammar of VISA resource descriptor\n                        strings. \n                        \n                        Example resource strings::\n                            \n                            \'TCPIP::10.0.0.1::INSTR\'\n                            \'TCPIP0::10.0.0.1::INSTR\'\n                            \'TCPIP::10.0.0.1::gpib,5::INSTR\'\n                            \'TCPIP0::10.0.0.1::gpib,5::INSTR\'\n                            \'TCPIP0::10.0.0.1::usb0::INSTR\'\n                            \'TCPIP0::10.0.0.1::usb0[1234::5678::MYSERIAL::0]::INSTR\'\n                            \'USB::1234::5678::INSTR\'\n                            \'USB::1234::5678::SERIAL::INSTR\'\n                            \'USB0::0x1234::0x5678::INSTR\'\n                            \'USB0::0x1234::0x5678::SERIAL::INSTR\'\n                            \'GPIB::10::INSTR\'\n                            \'GPIB0::10::INSTR\'\n                            \'ASRL1::INSTR\'\n                            \'ASRL::COM1,9600,8n1::INSTR\'\n                            \'ASRL::/dev/ttyUSB0,9600::INSTR\'\n                            \'ASRL::/dev/ttyUSB0,9600,8n1::INSTR\'\n                        \n                        The user can use additional parameters to specify the initial values of\n                        certain IVI inherent attributes for the session. The following table lists\n                        the inherent attributes that the user can set through these named\n                        parameters. The user does not have to specify all or any of the\n                        attributes. If the user does not specify the initial value of an inherent\n                        attribute, the initial value of the attribute depends on the value of the\n                        ResourceName parameter:\n                        \n                        * If the ResourceName parameter contains an IVI logical name, the IVI\n                          specific driver configures the initial settings based on the\n                          configuration of the logical name in the IVI configuration store.\n                        * If the ResourceName parameter contains a resource descriptor string that\n                          identifies the I/O address of the instrument, the IVI specific driver\n                          sets inherent attributes to their default initial values. The following\n                          table shows the default initial value for each attribute.\n                        \n                        The following table lists the IVI inherent attributes that the user can\n                        set, their default initial values, and the name that represents each\n                        attribute. These options are passed to the initialize function or the\n                        constructor as key-value pairs.  \n                        \n                        +-------------------------+----------------------+---------------------+\n                        | Attribute               | Default Inital Value | Options String Name |\n                        +=========================+======================+=====================+\n                        | Range Check             | True                 | range_check         |\n                        +-------------------------+----------------------+---------------------+\n                        | Query Instrument Status | False                | query_instr_status  |\n                        +-------------------------+----------------------+---------------------+\n                        | Cache                   | True                 | cache               |\n                        +-------------------------+----------------------+---------------------+\n                        | Simulate                | False                | simulate            |\n                        +-------------------------+----------------------+---------------------+\n                        | Record Value Coercions  | False                | record_coercions    |\n                        +-------------------------+----------------------+---------------------+\n                        | Interchange Check       | False                | interchange_check   |\n                        +-------------------------+----------------------+---------------------+\n                        | Driver Setup            | \'\'                   | driver_setup        |\n                        +-------------------------+----------------------+---------------------+\n                        | Prefer PyVISA           | False                | prefer_pyvisa       |\n                        +-------------------------+----------------------+---------------------+\n                        \n                        Each IVI specific driver defines it own meaning and valid values for the\n                        Driver Setup attribute. Many specific drivers ignore the value of the\n                        Driver Setup attribute. Other specific drivers use the Driver Setup string\n                        to configure instrument specific features at initialization. For example,\n                        if a specific driver supports a family of instrument models, the driver\n                        can use the Driver Setup attribute to allow the user to specify a\n                        particular instrument model to simulate.\n                        \n                        If the user attempts to initialize the instrument a second time without\n                        first calling the Close function, the Initialize function returns the\n                        Already Initialized error.\n                        ')
        self._add_property('initialized', self._get_initialized, None, None, '\n                        Returns a value that indicates whether the IVI specific driver is in the\n                        initialized state. After the specific driver is instantiated and before\n                        the Initialize function successfully executes, this attribute returns\n                        False. After the Initialize function successfully executes and prior to\n                        the execution of the Close function, this attribute returns True. After\n                        the Close function executes, this attribute returns False. \n                        \n                        The Initialized attribute is one of the few IVI specific driver attributes\n                        that can be accessed while the specific driver is not in the initialized\n                        state. All the attributes of an IVI specific driver that can be accessed\n                        while the specific driver is not in the initialized state are listed below.\n                        \n                        * Component Class Spec Major Version\n                        * Component Class Spec Minor Version\n                        * Component Description\n                        * Component Prefix\n                        * Component Identifier\n                        * Component Revision\n                        * Component Vendor\n                        * Initialized\n                        * Supported Instrument Models\n                        ')
        self._add_method('close', self._close, '\n                        When the user finishes using a Python IVI driver, the user should call\n                        either the Close method or __del__.  Note that __del__ will call close\n                        automatically.  \n                        \n                        This function also does the following:\n                        \n                        * Prevents the user from calling other functions in the driver that\n                          access the instrument until the user calls the Initialize function\n                          again.\n                        * May deallocate internal resources used by the IVI session.\n                        ')
        self._prefer_pyvisa = _prefer_pyvisa
        self._initialized_from_constructor = False
        if resource is not None or len(kw) > 0:
            self._initialized_from_constructor = True
            self.initialize(resource, id_query, reset, **kw)
        return

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        """Opens an I/O session to the instrument."""
        for op in keywargs:
            val = keywargs[op]
            if op == 'range_check':
                self._driver_operation_range_check = bool(val)
            elif op == 'query_instr_status':
                self._driver_operation_query_instrument_status = bool(val)
            elif op == 'cache':
                self._driver_operation_cache = bool(val)
            elif op == 'simulate':
                self._driver_operation_simulate = bool(val)
            elif op == 'record_coercions':
                self._driver_operation_record_coercions = bool(val)
            elif op == 'interchange_check':
                self._driver_operation_interchange_check = bool(val)
            elif op == 'driver_setup':
                self._driver_operation_driver_setup = val
            elif op == 'prefer_pyvisa':
                self._prefer_pyvisa = bool(val)
            else:
                raise UnknownOptionException('Invalid option')

        if self._driver_operation_simulate:
            print 'Simulating; ignoring resource'
        elif resource is None:
            raise IOException('No resource specified!')
        elif type(resource) == str:
            m = re.match('^(?P<prefix>(?P<type>TCPIP|USB|GPIB|ASRL)\\d*)(::(?P<arg1>[^\\s:]+))?(::(?P<arg2>[^\\s:]+(\\[.+\\])?))?(::(?P<arg3>[^\\s:]+))?(::(?P<suffix>INSTR))$', resource, re.I)
            if m is None:
                if 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                else:
                    raise IOException('Invalid resource string')
            res_type = m.group('type').upper()
            res_prefix = m.group('prefix')
            res_arg1 = m.group('arg1')
            res_arg2 = m.group('arg2')
            res_arg3 = m.group('arg3')
            res_suffix = m.group('suffix')
            if res_type == 'TCPIP':
                if self._prefer_pyvisa and 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                elif 'vxi11' in globals():
                    self._interface = vxi11.Instrument(resource)
                elif 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                else:
                    raise IOException('Cannot use resource type %s' % res_type)
            elif res_type == 'USB':
                if self._prefer_pyvisa and 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                elif 'usbtmc' in globals():
                    self._interface = usbtmc.Instrument(resource)
                elif 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                else:
                    raise IOException('Cannot use resource type %s' % res_type)
            elif res_type == 'GPIB':
                if self._prefer_pyvisa and 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                elif 'linuxgpib' in globals():
                    self._interface = linuxgpib.LinuxGpibInstrument(resource)
                elif 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                else:
                    raise IOException('Cannot use resource type %s' % res_type)
            elif res_type == 'ASRL':
                if self._prefer_pyvisa and 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                elif 'pyserial' in globals():
                    self._interface = pyserial.SerialInstrument(resource)
                elif 'pyvisa' in globals():
                    self._interface = pyvisa.PyVisaInstrument(resource)
                else:
                    raise IOException('Cannot use resource type %s' % res_type)
            elif 'pyvisa' in globals():
                self._interface = pyvisa.PyVisaInstrument(resource)
            else:
                raise IOException('Unknown resource type %s' % res_type)
            self._driver_operation_io_resource_descriptor = resource
        elif 'vxi11' in globals() and resource.__class__ == vxi11.Instrument:
            self._interface = resource
        elif 'usbtmc' in globals() and resource.__class__ == usbtmc.Instrument:
            self._interface = resource
        elif set(['read_raw', 'write_raw']).issubset(set(resource.__class__.__dict__)):
            self._interface = resource
        else:
            raise IOException('Invalid resource')
        self.driver_operation.invalidate_all_attributes()
        self._initialized = True
        return

    def _close(self):
        """Closes an IVI session"""
        if self._interface:
            try:
                self._interface.close()
            except:
                pass

        self._interface = None
        self._initialized = False
        return

    def _get_initialized(self):
        """Returnes initialization state of driver"""
        return self._initialized

    def _get_cache_tag(self, tag=None, skip=1):
        if tag is None:
            stack = inspect.stack()
            start = 0 + skip
            if len(stack) < start + 1:
                return ''
            tag = stack[start][3]
        if tag[0:4] == '_get':
            tag = tag[4:]
        if tag[0:4] == '_set':
            tag = tag[4:]
        if tag[0] == '_':
            tag = tag[1:]
        return tag

    def _get_cache_valid(self, tag=None, index=-1, skip_disable=False):
        if not skip_disable and not self._driver_operation_cache:
            return False
        tag = self._get_cache_tag(tag, 2)
        if index >= 0:
            tag = tag + '_%d' % index
        try:
            return self._cache_valid[tag]
        except KeyError:
            self._cache_valid[tag] = False
            return False

    def _set_cache_valid(self, valid=True, tag=None, index=-1):
        tag = self._get_cache_tag(tag, 2)
        if index >= 0:
            tag = tag + '_%d' % index
        self._cache_valid[tag] = valid

    def _driver_operation_invalidate_all_attributes(self):
        self._cache_valid = dict()

    def _write_raw(self, data):
        """Write binary data to instrument"""
        if self._driver_operation_simulate:
            print '[simulating] Call to write_raw'
            return
        else:
            if not self._initialized or self._interface is None:
                raise NotInitializedException()
            self._interface.write_raw(data)
            return

    def _read_raw(self, num=-1):
        """Read binary data from instrument"""
        if self._driver_operation_simulate:
            print '[simulating] Call to read_raw'
            return ''
        else:
            if not self._initialized or self._interface is None:
                raise NotInitializedException()
            return self._interface.read_raw(num)

    def _ask_raw(self, data, num=-1):
        """Write then read binary data"""
        if self._driver_operation_simulate:
            print '[simulating] Call to ask_raw'
            return ''
        else:
            if not self._initialized or self._interface is None:
                raise NotInitializedException()
            try:
                return self._interface.ask_raw(data, num)
            except AttributeError:
                self._write_raw(data)
                return self._read_raw(num)

            return

    def _write(self, data, encoding='utf-8'):
        """Write string to instrument"""
        if self._driver_operation_simulate:
            print "[simulating] Write (%s) '%s'" % (encoding, data)
            return
        else:
            if not self._initialized or self._interface is None:
                raise NotInitializedException()
            try:
                self._interface.write(data, encoding)
            except AttributeError:
                if type(data) is tuple or type(data) is list:
                    for data_i in data:
                        self._write(data_i, encoding)

                    return
                self._write_raw(str(data).encode(encoding))

            return

    def _read(self, num=-1, encoding='utf-8'):
        """Read string from instrument"""
        if self._driver_operation_simulate:
            print '[simulating] Read (%s)' % encoding
            return ''
        else:
            if not self._initialized or self._interface is None:
                raise NotInitializedException()
            try:
                return self._interface.read(num, encoding)
            except AttributeError:
                return self._read_raw(num).decode(encoding).rstrip('\r\n')

            return

    def _ask(self, data, num=-1, encoding='utf-8'):
        """Write then read string"""
        if self._driver_operation_simulate:
            print "[simulating] Ask (%s) '%s'" % (encoding, data)
            return ''
        else:
            if not self._initialized or self._interface is None:
                raise NotInitializedException()
            try:
                return self._interface.ask(data, num, encoding)
            except AttributeError:
                if type(data) is tuple or type(data) is list:
                    val = list()
                    for data_i in data:
                        val.append(self._ask(data_i, num, encoding))

                    return val
                self._write(data, encoding)
                return self._read(num, encoding)

            return

    def _read_stb(self):
        """Read status byte"""
        if self._driver_operation_simulate:
            print '[simulating] Read status'
            return 0
        else:
            if not self._initialized or self._interface is None:
                raise NotInitializedException()
            try:
                return self._interface.read_stb()
            except (AttributeError, NotImplementedError):
                return int(self._ask('*STB?'))

            return

    def _trigger(self):
        """Device trigger"""
        if self._driver_operation_simulate:
            print '[simulating] Trigger'
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        try:
            self._interface.trigger()
        except (AttributeError, NotImplementedError):
            self._write('*TRG')

        return

    def _clear(self):
        """Device clear"""
        if self._driver_operation_simulate:
            print '[simulating] Clear'
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        try:
            return self._interface.clear()
        except (AttributeError, NotImplementedError):
            self._write('*CLS')

        return

    def _remote(self):
        """Device set remote"""
        if self._driver_operation_simulate:
            print '[simulating] Remote'
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        return self._interface.remote()

    def _local(self):
        """Device set local"""
        if self._driver_operation_simulate:
            print '[simulating] Local'
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        return self._interface.local()

    def _read_ieee_block(self):
        """Read IEEE block"""
        return decode_ieee_block(self._read_raw())

    def _write_ieee_block(self, data, prefix=None, encoding='utf-8'):
        """Write IEEE block"""
        block = ''
        if type(prefix) == str:
            block = prefix.encode(encoding)
        elif type(prefix) == bytes:
            block = prefix
        block = block + build_ieee_block(data)
        self._write_raw(block)

    def doc(self, obj=None, itm=None, docs=None, prefix=None):
        """Python IVI documentation generator"""
        if obj is None:
            obj = self
        if type(obj) == str:
            itm = obj
            obj = self
        return doc(obj, itm, docs, prefix)

    def help(self, itm=None, complete=False, indent=0):
        """Python IVI help system"""
        return help(self, itm, complete, indent)