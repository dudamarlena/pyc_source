# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ccodeinline/ccodeinline.py
# Compiled at: 2013-10-28 00:21:11
import os, sys, re, numpy as np, multiprocessing, imp, tempfile
from tempfile import NamedTemporaryFile
from distutils.core import setup, Extension
_COMP_LOCK = multiprocessing.Lock()

class CCITypeSupportWarning(Warning):
    msg = 'Warning This type is not supported by the current processor. Value:{}'

    def __init__(self, value):
        Warning.__init__(self, self.msg.format(value))


class CCITypeDictWarning(Warning):
    msg = 'Warning will not accept this Dict-Type inside this property: Dict:{}'

    def __init__(self, value):
        Warning.__init__(self, self.msg.format(value))


class CCItagRegistrationWarning(Warning):
    msg = 'Warning Tag is not registred inside ListTag, TAG:{}'

    def __init__(self, value):
        Warning.__init__(self, self.msg.format(value))


class CCITagDictWarning(Warning):
    msg = 'Warning Tag is not listed inside Operation-Dict and will not be parsed, TAG:{}'

    def __init__(self, value):
        Warning.__init__(self, self.msg.format(value))


class CCITagSkeletonWarning(Warning):
    msg = 'Warning Tag is not found inside Skeleton and will not be located.'

    def __init__(self, value):
        Warning.__init__(self, self.msg.format(value))


class CCIIncludeTypeDictException(Exception):
    msg = 'Exception, use of property self.IncludeHeaderType is mandatory prior to call property '

    def __init__(self, value):
        Warning.__init__(self, self.msg.format(value))


class CCodeInline(object):
    _SKEL = '\n\n  __INCLUDE_HEADER__\n  \n  // Forward declarations of our function.\n  static PyObject *__FUNCTION__(PyObject *self, PyObject *args); \n\n\n  // Boilerplate: function list.\n  static PyMethodDef methods[] = {\n      { "__FUNCTION__", __FUNCTION__, METH_VARARGS, "Doc string."},\n      { NULL, NULL, 0, NULL } /* Sentinel */\n  };\n\n  // Boilerplate: Module initialization.\n  PyMODINIT_FUNC init__MODULE_NAME__(void) {\n          (void) Py_InitModule("__MODULE_NAME__", methods);\n          import_array();\n  }\n\n\n  /*****************************************************************************\n   * Array access macros.                                                      *\n   *****************************************************************************/\n  __NUMPY_ARRAY_MACROS__\n\n\n  /*****************************************************************************\n   * Support code.                                                             *\n   *****************************************************************************/\n  __SUPPORT_CODE__\n\n\n  /*****************************************************************************\n   * The function.                                                             *\n   *****************************************************************************/\n  PyObject *__FUNCTION__(PyObject *self, PyObject *args) {\n\n\n  /***************************************\n   * Variable declarations.              *\n   ***************************************/\n  __FUNC_VAR_DECLARATIONS__\n\n\n  /***************************************\n   * Parse variables.                    *\n   ***************************************/\n  if (!PyArg_ParseTuple(args, "__PARSE_ARG_TYPES__", __PARSE_ARG_LIST__))\n  {\n      return NULL;\n  } \n\n\n  /***************************************\n   * User code.                          *\n   ***************************************/\n  __USER_CODE__\n\n\n  /***************************************\n   * Return value.                       *\n   ***************************************/\n  __RETURN_VAL__\n\n  } // End of function(self, args).\n\n  '
    IncludeType = {'internal': ['Python.h', 'numpy/arrayobject.h', 'math.h'], 'external': [], 'key-list': [
                  'internal', 'external']}
    ListTag = [
     '__INCLUDE_HEADER__', '__FUNCTION__', '__MODULE_NAME__', '__NUMPY_ARRAY_MACROS__', '__SUPPORT_CODE__',
     '__FUNC_VAR_DECLARATIONS__', '__PARSE_ARG_TYPES__', '__PARSE_ARG_LIST__', '__USER_CODE__', '__RETURN_VAL__']
    ListTypeDict = ('_TYPE_CONV_DICT', '_RETURN_FUNC_DICT', '_TYPE_PARSE_SPEC_DICT',
                    '_NP_TYPE_CONV_DICT')
    __Loader__ = [
     'SetNpFloat128', 'SetTempDirCompilation', 'SetSystemTypeLib']
    DictOperation = {'__MODULE_NAME__': '_gen_name', '__FUNCTION__': '_gen_function', 
       '__INCLUDE_HEADER__': '_gen_include_header', 
       '__SUPPORT_CODE__': '_gen_support_code', 
       '__USER_CODE__': '_gen_code', 
       '__NUMPY_ARRAY_MACROS__': '_gen_numpy_array_macros', 
       '__FUNC_VAR_DECLARATIONS__': '_gen_var_decls', 
       '__PARSE_ARG_TYPES__': '_gen_parse_arg_types', 
       '__PARSE_ARG_LIST__': '_gen_parse_arg_list', 
       '__RETURN_VAL__': '_gen_return_val'}
    IsDisabledCCITagSkeletonWarning = True
    _FUNCS = {}
    Platform = {'lib': {'widows': '{}.dll', 'linux': '{}.so', 
               'osx': '{}.so'}}
    SkeletonDict = {0: {'Body': None, 'Include': [], 'function_name': 'function'}}
    SkeletonTagVar = None
    SkeletonIndexVar = 0
    SkeletonSubIndexVar = 'Body'
    ModSkeletonVar = None
    SubIndexSkelFormatVar = None
    RegExpTagDetection = '(?mui){}'
    RegExpHeaderDetection = '(?ui)[<\\\'\\"]{}[>\\\'\\"]'
    _PATH = '/tmp/np_inline'
    TemporaryFile = None
    IndexTypeDictVar = None
    TypeDictVar = None
    IncludeHeaderTypeVar = None
    IncludeHeaderVar = None
    IncludeHeaderParsedVar = None
    ContextOSVar = None
    OSLibVar = None
    OSLibFormatVar = None
    ContextLibOsVar = None
    NpTypeVar = None
    DimsVar = None
    CNameVar = None
    CCodeVar = None
    ModNameVar = None
    args = ()
    py_types = ()
    np_types = ()
    code_path = None
    support_code = None
    support_code_path = None
    extension_kwargs = {}
    return_type = None
    UniqueNameVar = None

    def GetContextOS(self):
        return self.Platform[self.ContextOSVar]

    def SetContextOS(self, value):
        self.ContextOSVar = value

    ContextOS = property(GetContextOS, SetContextOS)

    @property
    def ContextOSList(self):
        return getattr(self.ContextOS, 'keys')()

    @property
    def ContextLibOs(self):
        ReturnValue = None
        ReturnIndex = None
        if self.ContextLibOsVar != None:
            ReturnValue = self.ContextLibOsVar
        else:
            StrPlatform = sys.platform
            for ItemStrReg in self.ContextOSList:
                Areg = re.compile(('(?ui){}').format(ItemStrReg))
                if Areg.match(StrPlatform):
                    ReturnIndex = ItemStrReg

            self.ContextLibOsVar = self.ContextOS[ReturnIndex]
            ReturnValue = self.ContextLibOsVar
        return ReturnValue

    def GetIndexSkel(self):
        return self.SkeletonIndexVar

    def SetIndexSkel(self, value):
        self.SkeletonIndexVar = value

    SkeletonIndex = property(GetIndexSkel, SetIndexSkel)

    def GetSubIndexSkelFormat(self):
        return self.SubIndexSkelFormatVar

    def SetSubIndexSkelFormat(self, value):
        self.SubIndexSkelFormatVar = value

    SubIndexSkelFormat = property(GetSubIndexSkelFormat, SetSubIndexSkelFormat)

    @property
    def AddSubIndexSkel(self):
        if self.SubIndexSkel not in self.SkeletonDict.keys():
            if self.SubIndexSkelFormat == None:
                self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel] = None
            else:
                self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel] = getattr(__builtins__, self.SubIndexSkelFormat)()
        return

    def GetSubIndexSkel(self):
        return self.SkeletonSubIndexVar

    def SetSubIndexSkel(self, value):
        self.SkeletonSubIndexVar = value

    SubIndexSkel = property(GetSubIndexSkel, SetSubIndexSkel)

    @property
    def AddSkeleton(self):
        OldIndex = self.SubIndexSkel
        self.SubIndexSkel = 'Body'
        self.SkeletonDict[self.SkeletonIndex] = {self.SubIndexSkel: str(self._SKEL), 'Include': [], 'function_name': 'function'}
        self.SubIndexSkel = OldIndex

    def GetVSkeleton(self):
        ValueReturn = False
        OldIndex = self.SubIndexSkel
        self.SubIndexSkel = 'Body'
        ValueReturn = self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel]
        self.SubIndexSkel = OldIndex
        return ValueReturn

    def SetVSkeleton(self, value):
        OldIndex = self.SubIndexSkel
        self.SubIndexSkel = 'Body'
        self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel] = value
        self.SubIndexSkel = OldIndex

    VarDefSkeleton = property(GetVSkeleton, SetVSkeleton)

    def GetVFunc(self):
        ValueReturn = False
        OldIndex = self.SubIndexSkel
        self.SubIndexSkel = 'function_name'
        ValueReturn = self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel]
        self.SubIndexSkel = OldIndex
        return ValueReturn

    def SetVFunc(self, value):
        OldIndex = self.SubIndexSkel
        self.SubIndexSkel = 'function_name'
        self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel] = value
        self.SubIndexSkel = OldIndex

    VarDefFunction = property(GetVFunc, SetVFunc)

    def GetIncHeaderType(self):
        return self.IncludeHeaderTypeVar

    def SetIncHeaderType(self, value):
        self.IncludeHeaderTypeVar = value

    IncludeHeaderType = property(GetIncHeaderType, SetIncHeaderType)

    def GetIncludeHFormat(self):
        ValueReturn = False
        StrRegExp = str(self.RegExpHeaderDetection)
        Areg = re.compile(StrRegExp.format(self.IncludeHeaderVar))
        if len(Areg.findall(str(self.VarDefIncludeHeader))) > 0:
            ValueReturn = True
        return ValueReturn

    def SetIncludeHFormat(self, value):
        self.IncludeHeaderVar = value

    IncludeHeaderFormat = property(GetIncludeHFormat, SetIncludeHFormat)

    def GetIncHeader(self):
        ValueReturn = None
        OldIndex = self.SubIndexSkel
        self.SubIndexSkel = 'Include'
        ValueReturn = self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel]
        self.SubIndexSkel = OldIndex
        return ValueReturn

    def SetIncHeader(self, value):
        OldIndex = self.SubIndexSkel
        self.SubIndexSkel = 'Include'
        self.SkeletonDict[self.SkeletonIndex][self.SubIndexSkel].append(value)
        self.SubIndexSkel = OldIndex

    VarDefIncludeHeader = property(GetIncHeader, SetIncHeader)

    def GetIncludeHeader(self):
        return self.IncludeHeaderParsedVar

    def SetIncludeHeader(self, value):
        ValueSet = None
        if self.IncludeHeaderType == 'internal':
            ValueSet = ('<{}>').format(value)
        if self.IncludeHeaderType == 'external':
            ValueSet = ("'{}'").format(value)
        self.IncludeHeaderParsedVar = ValueSet
        return

    ParseIncludeHeader = property(GetIncludeHeader, SetIncludeHeader)

    def GetToDictIncludeHeader(self):
        return self.IncludeType[self.IncludeHeaderType]

    def SetToDictIncludeHeader(self, value):
        if self.IncludeHeaderType not in self.IncludeType['key-list']:
            raise CCIIncludeTypeDictException, 'IncludeHeaderType not set properly.'
        else:
            self.IncludeType[self.IncludeHeaderType].append(value)

    DictIncludeHeader = property(GetToDictIncludeHeader, SetToDictIncludeHeader)

    @property
    def UpdateIncludeHeader(self):
        for StrKeyIncludeH in self.IncludeType['key-list']:
            self.IncludeHeaderType = StrKeyIncludeH
            for StrHeader in self.DictIncludeHeader:
                if StrHeader is not None:
                    self.ParseIncludeHeader = StrHeader
                if self.ParseIncludeHeader is not None:
                    self.IncludeHeaderFormat = self.ParseIncludeHeader
                if self.IncludeHeaderFormat == False:
                    self.VarDefIncludeHeader = self.ParseIncludeHeader

        return

    def GetSkeletonTag(self):
        IsSearch = re.compile(self.RegExpTagDetection.format(self.SkeletonTagVar))
        valueReturn = False
        if len(IsSearch.findall(self.VarDefSkeleton)) > 0:
            valueReturn = True
        if self.IsDisabledCCITagSkeletonWarning and valueReturn == False:
            raise CCITagSkeletonWarning, self.SkeletonTagVar
        return valueReturn

    def SetSkeletonTag(self, value):
        if value not in self.ListTag:
            raise CCItagRegistrationWarning, value
        if value not in self.DictOperation.keys():
            raise CCITagDictWarning, value
        self.SkeletonTagVar = value

    @property
    def CurrentSkeletonTag(self):
        return self.SkeletonTagVar

    IsSkeletonTag = property(GetSkeletonTag, SetSkeletonTag)

    def GetModSkeleton(self):
        return self.ModSkeletonVar

    def SetModSkeleton(self, value):
        if value == None:
            value = str()
        StrSkelChg = str(self.VarDefSkeleton)
        self.ModSkeletonVar = StrSkelChg.replace(self.CurrentSkeletonTag, value)
        return

    SkeletonChange = property(GetModSkeleton, SetModSkeleton)

    @property
    def UpdateSkeleton(self):
        self.VarDefSkeleton = self.SkeletonChange

    def GetTypeDict(self):
        return self.TypeDictVar

    def SetTypeDict(self, value):
        if value not in self.ListTypeDict:
            raise CCITypeDictWarning, value
        if value in self.ListTypeDict:
            self.TypeDictVar = value

    TypeDict = property(GetTypeDict, SetTypeDict)

    def GetIndexTypeDict(self):
        return self.IndexTypeDictVar

    def SetIndexTypeDict(self, value):
        self.IndexTypeDictVar = value

    IndexTypeDict = property(GetIndexTypeDict, SetIndexTypeDict)

    @property
    def QueryValueTypeDict(self):
        TypeDict = getattr(self, self.TypeDict)
        return TypeDict[self.IndexTypeDict]

    def GetValueTypeDict(self):
        return getattr(self, self.TypeDict)[self.IndexTypeDict]

    def SetValueTypeDict(self, value):
        getattr(self, self.TypeDict)[self.IndexTypeDict] = value

    AddValueTypeDict = property(GetValueTypeDict, SetValueTypeDict)

    def GetNpType(self):
        return self.NpTypeVar

    def SetNpType(self, value):
        self.NpTypeVar = value

    FNpType = property(GetNpType, SetNpType)

    def GetDims(self):
        return self.DimsVar

    def SetDims(self, value):
        self.DimsVar = value

    FDims = property(GetDims, SetDims)

    def GetCName(self):
        return self.CNameVar

    def SetCName(self, value):
        self.CNameVar = value

    FCName = property(GetCName, SetCName)

    def GetCCodeVar(self):
        return self.CCodeVar

    def SetCCodeVar(self, value):
        self.CCodeVar = value

    FCCode = property(GetCCodeVar, SetCCodeVar)

    def GetModNameVar(self):
        return self.ModNameVar

    def SetModNameVar(self, value):
        self.ModNameVar = value

    FModName = property(GetModNameVar, SetModNameVar)

    def GetUniqueName(self):
        return self.UniqueNameVar

    def SetUniqueName(self, value):
        self.UniqueNameVar = value

    FUniqueName = property(GetUniqueName, SetUniqueName)
    _TYPE_CONV_DICT = {float: 'double', 
       int: 'long', 
       str: 'str'}
    _RETURN_FUNC_DICT = {float: 'PyFloat_FromDouble', 
       int: 'PyLong_FromLong', 
       str: 'PyString_FromString'}
    _TYPE_PARSE_SPEC_DICT = {float: 'd', 
       int: 'i', 
       str: 's'}
    _NP_TYPE_CONV_DICT = {np.uint8: 'npy_uint8', 
       np.uint16: 'npy_uint16', 
       np.uint32: 'npy_uint32', 
       np.uint64: 'npy_uint64', 
       np.int8: 'npy_int8', 
       np.int16: 'npy_int16', 
       np.int32: 'npy_int32', 
       np.int64: 'npy_int64', 
       np.float32: 'npy_float32', 
       np.float64: 'npy_float64'}
    _TYPE_PARSE_PY_BUILD = {'s': {'py_type': str, 'c_type': 'char *'}, 
       's#': {'py_type': str, 'c_type': 'char *'}, 
       'z': {'py_type': str, 'c_type': 'char *'}, 
       'z#': {'py_type': str, 'c_type': 'char *'}, 
       'u': {'py_type': unicode, 'c_type': 'Py_UNICODE *'}, 
       'u#': {'py_type': unicode, 'c_type': 'Py_UNICODE *'}, 
       'i': {'py_type': int, 'c_type': 'int'}, 
       'b': {'py_type': int, 'c_type': 'char'}, 
       'h': {'py_type': int, 'c_type': 'short int'}, 
       'l': {'py_type': int, 'c_type': 'long int'}, 
       'B': {'py_type': int, 'c_type': 'unsigned char'}, 
       'H': {'py_type': int, 'c_type': 'unsigned short int'}, 
       'I': {'py_type': int, 'c_type': 'unsigned int'}, 
       'k': {'py_type': int, 'c_type': 'unsigned long'}, 
       'L': {'py_type': long, 'c_type': 'PY_LONG_LONG'}, 
       'K': {'py_type': long, 'c_type': 'unsigned PY_LONG_LONG'}, 
       'n': {'py_type': int, 'c_type': 'Py_ssize_t'}, 
       'c': {'py_type': str, 'c_type': 'char'}, 
       'd': {'py_type': float, 'c_type': 'double'}, 
       'f': {'py_type': float, 'c_type': 'float'}, 
       'D': {'py_type': complex, 'c_type': 'Py_complex *'}, 
       'O': {'py_type': object, 'c_type': 'PyObject *'}, 
       'S': {'py_type': object, 'c_type': 'PyObject *'}, 
       'N': {'py_type': object, 'c_type': 'PyObject *'}, 
       'O&': {'py_type': object, 'c_type': 'Any'}, 
       '(items)': {'py_type': None, 'c_type': None}, 
       '[items]': {'py_type': None, 'c_type': None}, 
       '{items}': {'py_type': dict, 'c_type': None}}

    def GenerateCode(self):
        for ItemIndex in self.DictOperation.keys():
            self.IsSkeletonTag = ItemIndex
            getattr(self, self.DictOperation[ItemIndex])()
            self.UpdateSkeleton

    def _gen_name(self):
        self.SkeletonChange = self.FUniqueName

    def _gen_function(self):
        self.SkeletonChange = self.VarDefFunction

    def _gen_include_header(self):
        self.UpdateIncludeHeader
        StrHeaderAdd = '\n'
        for Item in self.VarDefIncludeHeader:
            StrHeaderAdd += ('{}\n').format(Item)

        self.SkeletonChange = StrHeaderAdd

    def _gen_support_code(self):
        self.SkeletonChange = self._string_or_path(self.support_code, self.support_code_path)

    def _gen_code(self):
        self.SkeletonChange = self._string_or_path(self.FCCode, self.code_path)

    def _gen_var_decls(self):
        StrTagValue = str()
        str_list = []
        self.TypeDict = '_TYPE_CONV_DICT'
        for py_type, self.FCName in self.py_types:
            self.IndexTypeDict = py_type
            str_list.append(('{0} {1};').format(self.QueryValueTypeDict, self.FCName))

        for self.FNpType, self.FDims, self.FCName in self.np_types:
            str_list.append(('PyArrayObject *py_{0};').format(self.FCName))

        self.TypeDict = '_TYPE_CONV_DICT'
        if self.return_type is not None:
            self.IndexTypeDict = self.return_type
            str_list.append(('{0} return_val;').format(self.QueryValueTypeDict))
        self.SkeletonChange = ('\n').join(str_list)
        return

    def _gen_parse_arg_types(self):
        StrTagValue = str()
        str_list = []
        self.TypeDict = '_TYPE_PARSE_SPEC_DICT'
        for py_type, self.FCName in self.py_types:
            self.IndexTypeDict = py_type
            str_list.append(self.QueryValueTypeDict)

        for self.FNpType, self.FDims, self.FCName in self.np_types:
            str_list.append('O')

        self.SkeletonChange = ('').join(str_list)

    def _gen_parse_arg_list(self):
        StrTagValue = str()
        str_list = []
        for py_type, self.FCName in self.py_types:
            str_list.append(('&{0}').format(self.FCName))

        for self.FNpType, self.FDims, self.FCName in self.np_types:
            str_list.append(('&py_{0}').format(self.FCName))

        self.SkeletonChange = (', ').join(str_list)

    def _gen_numpy_array_macros(self):
        StrTagValue = str()
        str_list = []
        for self.FNpType, self.FDims, self.FCName in self.np_types:
            str_list.append(_gen_numpy_array_index_macro())
            s = ('#define {0}_shape(i) (py_{0}->dimensions[(i)])').format(self.FCName)
            str_list.append(s)
            s = ('#define {0}_ndim (py_arr->nd)').format(self.FCName)
            str_list.append(s)

        self.SkeletonChange = ('\n').join(str_list)

    def _gen_numpy_array_index_macro(self):
        StrTagValue = str()
        self.TypeDict = '_NP_TYPE_CONV_DICT'
        self.IndexTypeDict = self.FNpType
        arg_list = (', ').join([ ('x{0}').format(i) for i in range(self.FDims) ])
        strides = ''
        for i in range(self.FDims):
            strides += (' + (x{0}) * py_{1}->strides[{0}]').format(i, self.FCName)

        return ('#define {0}({1}) *({2} *)((py_{0}->data {3}))').format(self.FCName, arg_list, self.QueryValueTypeDict, strides)

    def _gen_return_val(self):
        StrTagValue = str()
        if self.return_type is None:
            StrTagValue = 'Py_RETURN_NONE;'
        else:
            self.TypeDict = '_RETURN_FUNC_DICT'
            self.IndexTypeDict = self.return_type
            StrTagValue = ('return {0}(return_val);').format(self.QueryValueTypeDict)
        self.SkeletonChange = StrTagValue
        return

    def SetNpFloat128(self):
        try:
            self.TypeDict = '_NP_TYPE_CONV_DICT'
            self.IndexTypeDict = np.float128
            self.AddValueTypeDict = 'npy_float128'
        except AttributeError:
            raise CCITypeSupportWarning, 'np.float128 not supported in your Numpy module...'

    def SetTempDirCompilation(self):
        self.TemporaryFile = NamedTemporaryFile(mode='w+', suffix='', prefix='np_inline-', dir='/tmp/', delete=True)
        self._PATH = os.path.expanduser(('{}').format(self._PATH))
        if not os.path.exists(self._PATH):
            os.makedirs(self._PATH)

    def SetSystemTypeLib(self):
        self.ContextOS = 'lib'

    def __init__(self, *args, **kargs):
        self.__dict__.update(kargs)
        try:
            for FuncLoader in self.__Loader__:
                getattr(self, FuncLoader)()

        except CCITypeSupportWarning:
            print 'System and/or Numpy version is not supporting the 128bit operation mode.'

    def _mod_path(self):
        StrValue = str(self.ContextLibOs)
        return os.path.join(self._PATH, StrValue.format(self.FModName))

    def _import():
        mod = imp.load_dynamic(self.FModName, _mod_path(self.FModName))
        self._FUNCS[mod_name] = getattr(mod, self.VarDefFunction)

    def inline(self):
        try:
            return self._FUNCS[self.FUniqueName](*self.args)
        except:
            pass

        try:
            _import(self.FUniqueName)
            return self._FUNCS[self.FUniqueName](*self.args)
        except:
            pass

        with _COMP_LOCK:
            self.GenerateCode()
            self._build_install_module()
            _import(self.FUniqueName)
        return self._FUNCS[self.FUniqueName](*self.args)

    def inline_debug(self):
        """Same as inline, but the types of each argument are checked, and 
      the code is recompiled the first time this function is called. """
        ListCheckArg = [
         'args', 'py_types', 'np_types']
        for IterAttr in ListCheckArg:
            assert getattr(np, 'iterable')(getattr(self, IterAttr))
            print '<!>Assert 1<!>'

        assert self.FCCode is not None or self.code_path is not None
        print '<!>Assert 2<!>'
        assert not (self.FCCode is not None and self.code_path is not None)
        print '<!>Assert 3<!>'
        assert not (self.support_code is not None and self.support_code_path is not None)
        print '<!>Assert 4<!>'
        if self.code_path is not None:
            assert os.path.exists(self.code_path)
            print '<!>Assert 5<!>'
        if self.support_code_path is not None:
            assert os.path.exists(self.support_code_path)
            print '<!>Assert 6<!>'
        for py_obj, (py_type, c_name) in zip(self.args[:len(self.py_types)], self.py_types):
            assert isinstance(py_obj, py_type), ('Type err: {0}').format(c_name)
            print '<!>Assert 7<!>'
            assert py_type in (int, float), ('Bad type: {0}').format(py_type)
            print '<!>Assert 8<!>'

        for np_obj, (np_type, ndim, c_name) in zip(self.args[len(self.py_types):], self.np_types):
            assert np_obj.dtype == np_type, ('Type err: {0}').format(c_name)
            print '<!>Assert 9<!>'
            assert np_obj.ndim == ndim, ('Bad dims: {0}').format(c_name)
            print '<!>Assert 10<!>'

        assert self.return_type in (None, int, float)
        print '<!>Assert 11<!>'
        if self.FUniqueName not in self._FUNCS and os.path.exists(self._mod_path()):
            os.unlink(_mod_path())
        return self.inline()

    def _string_or_path(self, code_str, code_path):
        """Return either code_str if it is not None, or the contents in 
      code_path.
      """
        ReturnInformation = None
        if code_str is not None:
            ReturnInformation = code_str
        if code_path is not None:
            FH = open(code_path, 'r+')
            ReturnInformation = FH.read()
            FH.close()
        return ReturnInformation

    def _build_install_module(self):
        curpath = os.getcwd()
        mod_name_c = ('{0}.c').format(self.FModName)
        try:
            FH = open(os.path.join(self._PATH, mod_name_c), 'wb')
            FH.write(self.VarDefSkeleton)
            FH.close()
            if 'include_dirs' not in self.extension_kwargs:
                self.extension_kwargs['include_dirs'] = []
            self.extension_kwargs['include_dirs'].append(np.get_include())
            os.chdir(self._PATH)
            ext = Extension(self.FModName, [mod_name_c], **self.extension_kwargs)
            setup(ext_modules=[ext], script_args=['clean'])
            setup(ext_modules=[ext], script_args=[
             'install', ('--install-lib={0}').format(self._PATH)])
        finally:
            os.chdir(curpath)


BoolTestDictManagerAdd = True
BoolTestSkeletonMod = True
BoolTestSkeletonTag = True
BoolTestSkeletonAdd = True
BoolTestCodeGeneration = True
BoolTestCodeCompilation = True
if __name__.__eq__('__main__'):
    Acode = CCodeInline()
    BInlineCode = 'printf( "Program #%i: Hello world.\\n", i ) ;'
    BCode = CCodeInline(args=(1,), py_types=((int, 'i'),))
    if BoolTestDictManagerAdd:
        Acode.TypeDict = '_RETURN_FUNC_DICT'
        Acode.IndexTypeDict = list
        Acode.AddValueTypeDict = 'PyList_FromCSV'
    if BoolTestSkeletonMod:
        Acode.SkeletonIndex = 0
        Acode.AddSkeleton
        print Acode.VarDefSkeleton
        if BoolTestSkeletonTag:
            Acode.IsSkeletonTag = '__INCLUDE_HEADER__'
            print ('Current tag: {}').format(Acode.CurrentSkeletonTag)
            print ('Is Tag:{} is present inside Skeleton: {}').format(Acode.CurrentSkeletonTag, Acode.IsSkeletonTag)
            Acode.SkeletonChange = '#include <Python.h>'
            Acode.UpdateSkeleton
            print 'Showing Skeleton-0 modification'
            print Acode.VarDefSkeleton
        if BoolTestSkeletonAdd:
            Acode.SkeletonIndex = 1
            Acode.AddSkeleton
            Acode.IsSkeletonTag = '__INCLUDE_HEADER__'
            Acode.SkeletonChange = '\n#include <Python.h>\n#include <numpy/arrayobject.h>'
            Acode.UpdateSkeleton
            print 'Showing Skeleton-1 modification'
            print Acode.VarDefSkeleton
            Acode.SkeletonIndex = 0
            print 'Back to Skeleton-0\nShowing Skeleton-0 Code.'
            print Acode.VarDefSkeleton
    if BoolTestCodeGeneration:
        print 'Start Parsing example with BoolTestCodeGeneration'
        BCode.SkeletonIndex = 1
        BCode.AddSkeleton
        BCode.FCCode = BInlineCode
        BCode.FUniqueName = 'hello_world_example'
        BCode.GenerateCode()
        print BCode.VarDefSkeleton
        if BoolTestCodeCompilation:
            BCode.SkeletonIndex = 1
            BCode.AddSkeleton
            BCode.FUniqueName = 'hello_world_example'
            BCode.IncludeHeaderType = 'internal'
            BCode.DictIncludeHeader = 'stdlib.h'
            BCode.UpdateIncludeHeader
            BCode.GenerateCode()