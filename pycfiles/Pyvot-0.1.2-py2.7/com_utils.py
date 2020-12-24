# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build-py2\bdist.egg\xl\_impl\com_utils.py
# Compiled at: 2011-11-21 15:27:19
import win32com.client as win32, pythoncom, pywintypes
from pywintypes import com_error
import winerror
from win32com.client import constants
import datetime, sys
_running_python3 = sys.version_info.major > 2

def ensure_excel_dispatch_support():
    """Ensure that early-bound dispatch support is generated for Excel typelib, version 1.7
    
    This may attempt to write to the site-packages directory"""
    try:
        win32.gencache.EnsureModule('{00020813-0000-0000-C000-000000000046}', 0, 1, 7)
    except Exception as e:
        raise Exception('Failed to verify / generate Excel COM wrappers. Check that you have write access to site-packages.' + 'See the original exception (in args[1]) for more info', e)


def marshal_to_excel_value--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'v'
                6  LOAD_GLOBAL           1  'list'
                9  CALL_FUNCTION_2       2  None
               12  JUMP_IF_TRUE_OR_POP    27  'to 27'
               15  LOAD_GLOBAL           0  'isinstance'
               18  LOAD_FAST             0  'v'
               21  LOAD_GLOBAL           2  'tuple'
               24  CALL_FUNCTION_2       2  None
             27_0  COME_FROM            12  '12'
               27  UNARY_NOT        
               28  POP_JUMP_IF_TRUE     40  'to 40'
               31  LOAD_ASSERT              AssertionError
               34  LOAD_CONST               'marshal_to_excel_value only handles scalars'
               37  RAISE_VARARGS_2       2  None

 L.  36        40  LOAD_GLOBAL           0  'isinstance'
               43  LOAD_FAST             0  'v'
               46  LOAD_GLOBAL           4  'datetime'
               49  LOAD_ATTR             4  'datetime'
               52  CALL_FUNCTION_2       2  None
               55  POP_JUMP_IF_FALSE    68  'to 68'

 L.  37        58  LOAD_GLOBAL           5  '_datetime_to_com_time'
               61  LOAD_FAST             0  'v'
               64  CALL_FUNCTION_1       1  None
               67  RETURN_END_IF    
             68_0  COME_FROM            55  '55'

 L.  39        68  LOAD_FAST             0  'v'
               71  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 68


_com_time_type = type(pywintypes.Time(0))

def unmarshal_from_excel_value--- This code section failed: ---

 L.  43         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'v'
                6  LOAD_GLOBAL           1  'list'
                9  CALL_FUNCTION_2       2  None
               12  JUMP_IF_TRUE_OR_POP    27  'to 27'
               15  LOAD_GLOBAL           0  'isinstance'
               18  LOAD_FAST             0  'v'
               21  LOAD_GLOBAL           2  'tuple'
               24  CALL_FUNCTION_2       2  None
             27_0  COME_FROM            12  '12'
               27  UNARY_NOT        
               28  POP_JUMP_IF_TRUE     40  'to 40'
               31  LOAD_ASSERT              AssertionError
               34  LOAD_CONST               'unmarshal_from_excel_value only handles scalars'
               37  RAISE_VARARGS_2       2  None

 L.  45        40  LOAD_GLOBAL           0  'isinstance'
               43  LOAD_FAST             0  'v'
               46  LOAD_GLOBAL           4  '_com_time_type'
               49  CALL_FUNCTION_2       2  None
               52  POP_JUMP_IF_FALSE    65  'to 65'

 L.  46        55  LOAD_GLOBAL           5  '_com_time_to_datetime'
               58  LOAD_FAST             0  'v'
               61  CALL_FUNCTION_1       1  None
               64  RETURN_END_IF    
             65_0  COME_FROM            52  '52'

 L.  48        65  LOAD_FAST             0  'v'
               68  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 65


def _com_time_to_datetime--- This code section failed: ---

 L.  51         0  LOAD_GLOBAL           0  '_running_python3'
                3  POP_JUMP_IF_FALSE   109  'to 109'

 L.  55         6  LOAD_FAST             0  'pytime'
                9  LOAD_ATTR             1  'tzinfo'
               12  LOAD_CONST               None
               15  COMPARE_OP            9  is-not
               18  POP_JUMP_IF_TRUE     27  'to 27'
               21  LOAD_ASSERT              AssertionError
               24  RAISE_VARARGS_1       1  None

 L.  56        27  LOAD_GLOBAL           4  'datetime'
               30  LOAD_ATTR             4  'datetime'
               33  LOAD_CONST               'month'
               36  LOAD_FAST             0  'pytime'
               39  LOAD_ATTR             5  'month'
               42  LOAD_CONST               'day'
               45  LOAD_FAST             0  'pytime'
               48  LOAD_ATTR             6  'day'
               51  LOAD_CONST               'year'
               54  LOAD_FAST             0  'pytime'
               57  LOAD_ATTR             7  'year'
               60  LOAD_CONST               'hour'

 L.  57        63  LOAD_FAST             0  'pytime'
               66  LOAD_ATTR             8  'hour'
               69  LOAD_CONST               'minute'
               72  LOAD_FAST             0  'pytime'
               75  LOAD_ATTR             9  'minute'
               78  LOAD_CONST               'second'
               81  LOAD_FAST             0  'pytime'
               84  LOAD_ATTR            10  'second'
               87  LOAD_CONST               'microsecond'

 L.  58        90  LOAD_FAST             0  'pytime'
               93  LOAD_ATTR            11  'microsecond'
               96  LOAD_CONST               'tzinfo'
               99  LOAD_FAST             0  'pytime'
              102  LOAD_ATTR             1  'tzinfo'
              105  CALL_FUNCTION_2048  2048  None
              108  RETURN_END_IF    
            109_0  COME_FROM             3  '3'

 L.  60       109  LOAD_FAST             0  'pytime'
              112  LOAD_ATTR            12  'msec'
              115  LOAD_CONST               0
              118  COMPARE_OP            2  ==
              121  POP_JUMP_IF_TRUE    133  'to 133'
              124  LOAD_ASSERT              AssertionError
              127  LOAD_CONST               'fractional seconds not yet handled'
              130  RAISE_VARARGS_2       2  None

 L.  61       133  LOAD_GLOBAL           4  'datetime'
              136  LOAD_ATTR             4  'datetime'
              139  LOAD_CONST               'month'
              142  LOAD_FAST             0  'pytime'
              145  LOAD_ATTR             5  'month'
              148  LOAD_CONST               'day'
              151  LOAD_FAST             0  'pytime'
              154  LOAD_ATTR             6  'day'
              157  LOAD_CONST               'year'
              160  LOAD_FAST             0  'pytime'
              163  LOAD_ATTR             7  'year'
              166  LOAD_CONST               'hour'

 L.  62       169  LOAD_FAST             0  'pytime'
              172  LOAD_ATTR             8  'hour'
              175  LOAD_CONST               'minute'
              178  LOAD_FAST             0  'pytime'
              181  LOAD_ATTR             9  'minute'
              184  LOAD_CONST               'second'
              187  LOAD_FAST             0  'pytime'
              190  LOAD_ATTR            10  'second'
              193  CALL_FUNCTION_1536  1536  None
              196  RETURN_VALUE     
              197  LOAD_CONST               None
              200  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 197


def _datetime_to_com_time--- This code section failed: ---

 L.  65         0  LOAD_GLOBAL           0  '_running_python3'
                3  POP_JUMP_IF_FALSE    52  'to 52'

 L.  70         6  LOAD_FAST             0  'dt'
                9  LOAD_ATTR             1  'tzinfo'
               12  LOAD_CONST               None
               15  COMPARE_OP            8  is
               18  POP_JUMP_IF_FALSE    48  'to 48'

 L.  71        21  LOAD_FAST             0  'dt'
               24  LOAD_ATTR             3  'replace'
               27  LOAD_CONST               'tzinfo'
               30  LOAD_GLOBAL           4  'datetime'
               33  LOAD_ATTR             5  'timezone'
               36  LOAD_ATTR             6  'utc'
               39  CALL_FUNCTION_256   256  None
               42  STORE_FAST            0  'dt'
               45  JUMP_FORWARD          0  'to 48'
             48_0  COME_FROM            45  '45'

 L.  72        48  LOAD_FAST             0  'dt'
               51  RETURN_VALUE     
             52_0  COME_FROM             3  '3'

 L.  74        52  LOAD_FAST             0  'dt'
               55  LOAD_ATTR             7  'microsecond'
               58  LOAD_CONST               0
               61  COMPARE_OP            2  ==
               64  POP_JUMP_IF_TRUE     76  'to 76'
               67  LOAD_ASSERT              AssertionError
               70  LOAD_CONST               'fractional seconds not yet handled'
               73  RAISE_VARARGS_2       2  None

 L.  75        76  LOAD_GLOBAL           9  'pywintypes'
               79  LOAD_ATTR            10  'Time'
               82  LOAD_FAST             0  'dt'
               85  LOAD_ATTR            11  'timetuple'
               88  CALL_FUNCTION_0       0  None
               91  CALL_FUNCTION_1       1  None
               94  RETURN_VALUE     
               95  LOAD_CONST               None
               98  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 95


def enum_running_monikers():
    try:
        r = pythoncom.GetRunningObjectTable()
        for moniker in r:
            yield moniker

    except com_error as e:
        if e.args[0] == winerror.E_ACCESSDENIED:
            raise Exception('Access to the running object table was denied. This may be due to a high-privilege registered object')


def get_running_xlWorkbook_for_filename(filename):
    wbPartialMatch = None
    filename = filename.lower()
    context = pythoncom.CreateBindCtx(0)
    for moniker in enum_running_monikers():
        name = moniker.GetDisplayName(context, None).lower()
        if filename == name:
            obj = pythoncom.GetRunningObjectTable().GetObject(moniker)
            wb = win32.Dispatch(obj.QueryInterface(pythoncom.IID_IDispatch))
            return wb
        if name.endswith('\\' + filename):
            obj = pythoncom.GetRunningObjectTable().GetObject(moniker)
            wbPartialMatch = win32.Dispatch(obj.QueryInterface(pythoncom.IID_IDispatch))

    return wbPartialMatch


def open_xlWorkbook(filename):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = True
    return excel.Workbooks.Open(filename)


def get_open_xlWorkbooks():
    IID_Workbook = pythoncom.pywintypes.IID('{000208DA-0000-0000-C000-000000000046}')
    l = []
    for moniker in enum_running_monikers():
        obj = pythoncom.GetRunningObjectTable().GetObject(moniker)
        try:
            wb = win32.Dispatch(obj.QueryInterface(pythoncom.IID_IDispatch))
            if getattr(wb, 'CLSID', None) == IID_Workbook:
                l.append(wb)
        except com_error:
            pass

    return l