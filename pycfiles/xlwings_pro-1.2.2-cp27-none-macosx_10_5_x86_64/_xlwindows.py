# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <xlwings_pro-1.2.2>/xlwings/_xlwindows.py
# Compiled at: 2020-03-09 05:37:56
import os, sys
cwd = os.getcwd()
if not hasattr(sys, 'frozen'):
    os.chdir(sys.exec_prefix)
import win32api
os.chdir(cwd)
from warnings import warn
import datetime as dt, numbers, types
from ctypes import oledll, PyDLL, py_object, byref, POINTER, windll
import pywintypes, pythoncom
from win32com.client import Dispatch, CDispatch, DispatchEx
import win32timezone, win32gui, win32process
from comtypes import IUnknown
from comtypes.automation import IDispatch
from .constants import ColorIndex, UpdateLinks, InsertShiftDirection, InsertFormatOrigin, DeleteShiftDirection
from .utils import rgb_to_int, int_to_rgb, get_duplicates, np_datetime_to_datetime, col_name
try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None

from . import PY3
time_types = (
 dt.date, dt.datetime, pywintypes.TimeType)
if np:
    time_types = time_types + (np.datetime64,)
N_COM_ATTEMPTS = 0
BOOK_CALLER = None
missing = object()

class COMRetryMethodWrapper(object):

    def __init__(self, method):
        self.__method = method

    def __call__(self, *args, **kwargs):
        n_attempt = 1
        while True:
            try:
                v = self.__method(*args, **kwargs)
                t = type(v)
                if t is CDispatch:
                    return COMRetryObjectWrapper(v)
                if t is types.MethodType:
                    return COMRetryMethodWrapper(v)
                return v
            except pywintypes.com_error as e:
                if (not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS) and e.hresult == -2147418111:
                    n_attempt += 1
                    continue
                else:
                    raise
            except AttributeError as e:
                if not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS:
                    n_attempt += 1
                    continue
                else:
                    raise


class ExcelBusyError(Exception):

    def __init__(self):
        super(ExcelBusyError, self).__init__('Excel application is not responding')


class COMRetryObjectWrapper(object):

    def __init__(self, inner):
        object.__setattr__(self, '_inner', inner)

    def __setattr__(self, key, value):
        n_attempt = 1
        while True:
            try:
                return setattr(self._inner, key, value)
            except pywintypes.com_error as e:
                if (not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS) and e.hresult in (-2147418111,
                                                                                        -2147352567):
                    n_attempt += 1
                    continue
                else:
                    raise
            except AttributeError as e:
                if not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS:
                    n_attempt += 1
                    continue
                else:
                    raise

    def __getattr__(self, item):
        n_attempt = 1
        while True:
            try:
                v = getattr(self._inner, item)
                t = type(v)
                if t is CDispatch:
                    return COMRetryObjectWrapper(v)
                if t is types.MethodType:
                    return COMRetryMethodWrapper(v)
                return v
            except pywintypes.com_error as e:
                if (not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS) and e.hresult == -2147418111:
                    n_attempt += 1
                    continue
                else:
                    raise
            except AttributeError as e:
                try:
                    self._oleobj_.GetIDsOfNames(0, item)
                except pythoncom.ole_error as e:
                    if e.hresult != -2147418111:
                        raise

                if not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS:
                    n_attempt += 1
                    continue
                else:
                    raise ExcelBusyError()

    def __call__(self, *args, **kwargs):
        n_attempt = 1
        for i in range(N_COM_ATTEMPTS + 1):
            try:
                v = self._inner(*args, **kwargs)
                t = type(v)
                if t is CDispatch:
                    return COMRetryObjectWrapper(v)
                if t is types.MethodType:
                    return COMRetryMethodWrapper(v)
                return v
            except pywintypes.com_error as e:
                if (not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS) and e.hresult == -2147418111:
                    n_attempt += 1
                    continue
                else:
                    raise
            except AttributeError as e:
                if not N_COM_ATTEMPTS or n_attempt < N_COM_ATTEMPTS:
                    n_attempt += 1
                    continue
                else:
                    raise

    def __iter__(self):
        for v in self._inner:
            t = type(v)
            if t is CDispatch:
                yield COMRetryObjectWrapper(v)
            else:
                yield v


OBJID_NATIVEOM = -16

def accessible_object_from_window(hwnd):
    ptr = POINTER(IDispatch)()
    res = oledll.oleacc.AccessibleObjectFromWindow(hwnd, OBJID_NATIVEOM, byref(IDispatch._iid_), byref(ptr))
    return ptr


def comtypes_to_pywin(ptr, interface=None):
    _PyCom_PyObjectFromIUnknown = PyDLL(pythoncom.__file__).PyCom_PyObjectFromIUnknown
    _PyCom_PyObjectFromIUnknown.restype = py_object
    if interface is None:
        interface = IUnknown
    return _PyCom_PyObjectFromIUnknown(ptr, byref(interface._iid_), True)


def is_hwnd_xl_app(hwnd):
    try:
        child_hwnd = win32gui.FindWindowEx(hwnd, 0, 'XLDESK', None)
        child_hwnd = win32gui.FindWindowEx(child_hwnd, 0, 'EXCEL7', None)
        ptr = accessible_object_from_window(child_hwnd)
        return True
    except WindowsError:
        return False
    except pywintypes.error:
        return False

    return


def get_xl_app_from_hwnd(hwnd):
    pythoncom.CoInitialize()
    child_hwnd = win32gui.FindWindowEx(hwnd, 0, 'XLDESK', None)
    child_hwnd = win32gui.FindWindowEx(child_hwnd, 0, 'EXCEL7', None)
    ptr = accessible_object_from_window(child_hwnd)
    p = comtypes_to_pywin(ptr, interface=IDispatch)
    disp = COMRetryObjectWrapper(Dispatch(p))
    return disp.Application


def get_excel_hwnds():
    pythoncom.CoInitialize()
    hwnd = windll.user32.GetTopWindow(None)
    pids = set()
    while hwnd:
        try:
            child_hwnd = win32gui.FindWindowEx(hwnd, 0, 'XLDESK', None)
            if child_hwnd:
                child_hwnd = win32gui.FindWindowEx(child_hwnd, 0, 'EXCEL7', None)
            if child_hwnd:
                pid = win32process.GetWindowThreadProcessId(hwnd)[1]
                if pid not in pids:
                    pids.add(pid)
                    yield hwnd
        except pywintypes.error:
            pass

        hwnd = windll.user32.GetWindow(hwnd, 2)

    return


def get_xl_apps():
    for hwnd in get_excel_hwnds():
        try:
            yield get_xl_app_from_hwnd(hwnd)
        except ExcelBusyError:
            pass
        except WindowsError:
            pass


def is_range_instance(xl_range):
    pyid = getattr(xl_range, '_oleobj_', None)
    if pyid is None:
        return False
    else:
        return xl_range._oleobj_.GetTypeInfo().GetTypeAttr().iid == pywintypes.IID('{00020846-0000-0000-C000-000000000046}')


class Apps(object):

    def keys(self):
        k = []
        for hwnd in get_excel_hwnds():
            k.append(App(xl=hwnd).pid)

        return k

    def __iter__(self):
        for hwnd in get_excel_hwnds():
            yield App(xl=hwnd)

    def __len__(self):
        return len(list(get_excel_hwnds()))

    def __getitem__(self, pid):
        for hwnd in get_excel_hwnds():
            app = App(xl=hwnd)
            if app.pid == pid:
                return app

        raise KeyError('Could not find an Excel instance with this PID.')


class App(object):

    def __init__(self, spec=None, add_book=True, xl=None):
        if spec is not None:
            warn('spec is ignored on Windows.')
        if xl is None:
            self._xl = COMRetryObjectWrapper(DispatchEx('Excel.Application'))
            if add_book:
                self._xl.Workbooks.Add()
            self._hwnd = None
        elif isinstance(xl, int):
            self._xl = None
            self._hwnd = xl
        else:
            self._xl = xl
            self._hwnd = None
        return

    @property
    def xl(self):
        if self._xl is None:
            self._xl = get_xl_app_from_hwnd(self._hwnd)
        return self._xl

    api = xl

    @property
    def selection(self):
        try:
            _ = self.xl.Selection.Address
            return Range(xl=self.xl.Selection)
        except pywintypes.com_error:
            return

        return

    def activate(self, steal_focus=False):
        hwnd = windll.user32.GetForegroundWindow()
        if steal_focus or is_hwnd_xl_app(hwnd):
            windll.user32.SetForegroundWindow(self.xl.Hwnd)
        else:
            windll.user32.SetWindowPos(self.xl.Hwnd, hwnd, 0, 0, 0, 0, 19)

    @property
    def visible(self):
        return self.xl.Visible

    @visible.setter
    def visible(self, visible):
        self.xl.Visible = visible

    def quit(self):
        self.xl.DisplayAlerts = False
        self.xl.Quit()

    def kill(self):
        import win32api
        PROCESS_TERMINATE = 1
        handle = win32api.OpenProcess(PROCESS_TERMINATE, False, self.pid)
        win32api.TerminateProcess(handle, -1)
        win32api.CloseHandle(handle)

    @property
    def screen_updating(self):
        return self.xl.ScreenUpdating

    @screen_updating.setter
    def screen_updating(self, value):
        self.xl.ScreenUpdating = value

    @property
    def display_alerts(self):
        return self.xl.DisplayAlerts

    @display_alerts.setter
    def display_alerts(self, value):
        self.xl.DisplayAlerts = value

    @property
    def calculation(self):
        return calculation_i2s[self.xl.Calculation]

    @calculation.setter
    def calculation(self, value):
        self.xl.Calculation = calculation_s2i[value]

    def calculate(self):
        self.xl.Calculate()

    @property
    def version(self):
        return self.xl.Version

    @property
    def books(self):
        return Books(xl=self.xl.Workbooks)

    @property
    def hwnd(self):
        if self._hwnd is None:
            self._hwnd = self._xl.Hwnd
        return self._hwnd

    @property
    def pid(self):
        return win32process.GetWindowThreadProcessId(self.hwnd)[1]

    def range(self, arg1, arg2=None):
        if isinstance(arg1, Range):
            xl1 = arg1.xl
        else:
            xl1 = self.xl.Range(arg1)
        if arg2 is None:
            return Range(xl=xl1)
        else:
            if isinstance(arg2, Range):
                xl2 = arg2.xl
            else:
                xl2 = self.xl.Range(arg2)
            return Range(xl=self.xl.Range(xl1, xl2))

    def run(self, macro, args):
        return self.xl.Run(macro, *args)


class Books(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    @property
    def active(self):
        return Book(self.xl.Application.ActiveWorkbook)

    def __call__(self, name_or_index):
        try:
            return Book(xl=self.xl(name_or_index))
        except pywintypes.com_error:
            raise KeyError(name_or_index)

    def __len__(self):
        return self.xl.Count

    def add(self):
        return Book(xl=self.xl.Add())

    def open(self, fullname, update_links=None, read_only=None, format=None, password=None, write_res_password=None, ignore_read_only_recommended=None, origin=None, delimiter=None, editable=None, notify=None, converter=None, add_to_mru=None, local=None, corrupt_load=None):
        if update_links:
            update_links = UpdateLinks.xlUpdateLinksAlways
        return Book(xl=self.xl.Open(fullname, update_links, read_only, format, password, write_res_password, ignore_read_only_recommended, origin, delimiter, editable, notify, converter, add_to_mru, local, corrupt_load))

    def __iter__(self):
        for xl in self.xl:
            yield Book(xl=xl)


class Book(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    @property
    def name(self):
        return self.xl.Name

    @property
    def sheets(self):
        return Sheets(xl=self.xl.Worksheets)

    @property
    def app(self):
        return App(xl=self.xl.Application)

    def close(self):
        self.xl.Close(SaveChanges=False)

    def save(self, path=None):
        saved_path = self.xl.Path
        if saved_path != '' and path is None:
            self.xl.Save()
        elif saved_path != '' and path is not None and os.path.split(path)[0] == '':
            path = os.path.join(os.getcwd(), path)
            self.xl.SaveAs(os.path.realpath(path))
        elif saved_path == '' and path is None:
            path = os.path.join(os.getcwd(), self.xl.Name + '.xlsx')
            alerts_state = self.xl.Application.DisplayAlerts
            self.xl.Application.DisplayAlerts = False
            self.xl.SaveAs(os.path.realpath(path))
            self.xl.Application.DisplayAlerts = alerts_state
        elif path:
            alerts_state = self.xl.Application.DisplayAlerts
            self.xl.Application.DisplayAlerts = False
            self.xl.SaveAs(os.path.realpath(path))
            self.xl.Application.DisplayAlerts = alerts_state
        return

    @property
    def fullname(self):
        return self.xl.FullName

    @property
    def names(self):
        return Names(xl=self.xl.Names)

    def activate(self):
        self.xl.Activate()


class Sheets(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    @property
    def active(self):
        return Sheet(self.xl.Parent.ActiveSheet)

    def __call__(self, name_or_index):
        return Sheet(xl=self.xl(name_or_index))

    def __len__(self):
        return self.xl.Count

    def __iter__(self):
        for xl in self.xl:
            yield Sheet(xl=xl)

    def add(self, before=None, after=None):
        if before:
            return Sheet(xl=self.xl.Add(Before=before.xl))
        else:
            if after:
                count = self.xl.Count
                new_sheet_index = after.xl.Index + 1
                if new_sheet_index > count:
                    xl_sheet = self.xl.Add(Before=after.xl)
                    self.xl(self.xl.Count).Move(Before=self.xl(self.xl.Count - 1))
                    self.xl(self.xl.Count).Activate()
                else:
                    xl_sheet = self.xl.Add(Before=self.xl(after.xl.Index + 1))
                return Sheet(xl=xl_sheet)
            return Sheet(xl=self.xl.Add())


class Sheet(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    @property
    def name(self):
        return self.xl.Name

    @name.setter
    def name(self, value):
        self.xl.Name = value

    @property
    def names(self):
        return Names(xl=self.xl.Names)

    @property
    def book(self):
        return Book(xl=self.xl.Parent)

    @property
    def index(self):
        return self.xl.Index

    def range(self, arg1, arg2=None):
        if isinstance(arg1, Range):
            xl1 = arg1.xl
        elif isinstance(arg1, tuple):
            if len(arg1) == 4:
                row, col, nrows, ncols = arg1
                return Range(xl=(self.xl, row, col, nrows, ncols))
            if 0 in arg1:
                raise IndexError('Attempted to access 0-based Range. xlwings/Excel Ranges are 1-based.')
            xl1 = self.xl.Cells(arg1[0], arg1[1])
        elif isinstance(arg1, numbers.Number) and isinstance(arg2, numbers.Number):
            xl1 = self.xl.Cells(arg1, arg2)
            arg2 = None
        else:
            xl1 = self.xl.Range(arg1)
        if arg2 is None:
            return Range(xl=xl1)
        else:
            if isinstance(arg2, Range):
                xl2 = arg2.xl
            elif isinstance(arg2, tuple):
                if 0 in arg2:
                    raise IndexError('Attempted to access 0-based Range. xlwings/Excel Ranges are 1-based.')
                xl2 = self.xl.Cells(arg2[0], arg2[1])
            else:
                xl2 = self.xl.Range(arg2)
            return Range(xl=self.xl.Range(xl1, xl2))

    @property
    def cells(self):
        return Range(xl=self.xl.Cells)

    def activate(self):
        return self.xl.Activate()

    def select(self):
        return self.xl.Select()

    def clear_contents(self):
        self.xl.Cells.ClearContents()

    def clear(self):
        self.xl.Cells.Clear()

    def autofit(self, axis=None):
        if axis == 'rows' or axis == 'r':
            self.xl.Rows.AutoFit()
        elif axis == 'columns' or axis == 'c':
            self.xl.Columns.AutoFit()
        elif axis is None:
            self.xl.Rows.AutoFit()
            self.xl.Columns.AutoFit()
        return

    def delete(self):
        app = self.xl.Parent.Application
        alerts_state = app.DisplayAlerts
        app.DisplayAlerts = False
        self.xl.Delete()
        app.DisplayAlerts = alerts_state

    @property
    def charts(self):
        return Charts(xl=self.xl.ChartObjects())

    @property
    def shapes(self):
        return Shapes(xl=self.xl.Shapes)

    @property
    def pictures(self):
        return Pictures(xl=self.xl.Pictures())

    @property
    def used_range(self):
        return Range(xl=self.xl.UsedRange)


class Range(object):

    def __init__(self, xl):
        if isinstance(xl, tuple):
            self._coords = xl
            self._xl = missing
        else:
            self._coords = missing
            self._xl = xl

    @property
    def xl(self):
        if self._xl is missing:
            xl_sheet, row, col, nrows, ncols = self._coords
            if nrows and ncols:
                self._xl = xl_sheet.Range(xl_sheet.Cells(row, col), xl_sheet.Cells(row + nrows - 1, col + ncols - 1))
            else:
                self._xl = None
        return self._xl

    @property
    def coords(self):
        if self._coords is missing:
            self._coords = (self.xl.Worksheet,
             self.xl.Row,
             self.xl.Column,
             self.xl.Rows.Count,
             self.xl.Columns.Count)
        return self._coords

    @property
    def api(self):
        return self.xl

    @property
    def sheet(self):
        return Sheet(xl=self.coords[0])

    def __len__(self):
        return self.xl and self.xl.Count or 0

    @property
    def row(self):
        return self.coords[1]

    @property
    def column(self):
        return self.coords[2]

    @property
    def shape(self):
        return (self.coords[3], self.coords[4])

    @property
    def raw_value(self):
        if self.xl is not None:
            return self.xl.Value
        else:
            return
            return

    @raw_value.setter
    def raw_value(self, data):
        if self.xl is not None:
            self.xl.Value = data
        return

    def clear_contents(self):
        if self.xl is not None:
            self.xl.ClearContents()
        return

    def clear(self):
        if self.xl is not None:
            self.xl.Clear()
        return

    @property
    def formula(self):
        if self.xl is not None:
            return self.xl.Formula
        else:
            return
            return

    @formula.setter
    def formula(self, value):
        if self.xl is not None:
            self.xl.Formula = value
        return

    def end(self, direction):
        direction = directions_s2i.get(direction, direction)
        return Range(xl=self.xl.End(direction))

    @property
    def formula_array(self):
        if self.xl is not None:
            return self.xl.FormulaArray
        else:
            return
            return

    @formula_array.setter
    def formula_array(self, value):
        if self.xl is not None:
            self.xl.FormulaArray = value
        return

    @property
    def column_width(self):
        if self.xl is not None:
            return self.xl.ColumnWidth
        else:
            return 0
            return

    @column_width.setter
    def column_width(self, value):
        if self.xl is not None:
            self.xl.ColumnWidth = value
        return

    @property
    def row_height(self):
        if self.xl is not None:
            return self.xl.RowHeight
        else:
            return 0
            return

    @row_height.setter
    def row_height(self, value):
        if self.xl is not None:
            self.xl.RowHeight = value
        return

    @property
    def width(self):
        if self.xl is not None:
            return self.xl.Width
        else:
            return 0
            return

    @property
    def height(self):
        if self.xl is not None:
            return self.xl.Height
        else:
            return 0
            return

    @property
    def left(self):
        if self.xl is not None:
            return self.xl.Left
        else:
            return 0
            return

    @property
    def top(self):
        if self.xl is not None:
            return self.xl.Top
        else:
            return 0
            return

    @property
    def number_format(self):
        if self.xl is not None:
            return self.xl.NumberFormat
        else:
            return ''
            return

    @number_format.setter
    def number_format(self, value):
        if self.xl is not None:
            self.xl.NumberFormat = value
        return

    def get_address(self, row_absolute, col_absolute, external):
        if self.xl is not None:
            return self.xl.GetAddress(row_absolute, col_absolute, 1, external)
        else:
            raise NotImplemented()
            return

    @property
    def address(self):
        if self.xl is not None:
            return self.xl.Address
        else:
            _, row, col, nrows, ncols = self.coords
            return '$%s$%s{%sx%s}' % (col_name(col), str(row), nrows, ncols)
            return

    @property
    def current_region(self):
        if self.xl is not None:
            return Range(xl=self.xl.CurrentRegion)
        else:
            return self
            return

    def autofit(self, axis=None):
        if self.xl is not None:
            if axis == 'rows' or axis == 'r':
                self.xl.Rows.AutoFit()
            elif axis == 'columns' or axis == 'c':
                self.xl.Columns.AutoFit()
            elif axis is None:
                self.xl.Columns.AutoFit()
                self.xl.Rows.AutoFit()
        return

    def insert(self, shift=None, copy_origin=None):
        shifts = {'down': InsertShiftDirection.xlShiftDown, 'right': InsertShiftDirection.xlShiftToRight, 
           None: None}
        copy_origins = {'format_from_left_or_above': InsertFormatOrigin.xlFormatFromLeftOrAbove, 'format_from_right_or_below': InsertFormatOrigin.xlFormatFromRightOrBelow}
        self.xl.Insert(Shift=shifts[shift], CopyOrigin=copy_origins[copy_origin])
        return

    def delete(self, shift=None):
        shifts = {'up': DeleteShiftDirection.xlShiftUp, 'left': DeleteShiftDirection.xlShiftToLeft, None: None}
        self.xl.Delete(Shift=shifts[shift])
        return

    def copy(self, destination=None):
        self.xl.Copy(Destination=destination.api if destination else None)
        return

    def paste(self, paste=None, operation=None, skip_blanks=False, transpose=False):
        pastes = {'all': -4104, 
           None: -4104, 
           'all_except_borders': 7, 
           'all_merging_conditional_formats': 14, 
           'all_using_source_theme': 13, 
           'column_widths': 8, 
           'comments': -4144, 
           'formats': -4122, 
           'formulas': -4123, 
           'formulas_and_number_formats': 11, 
           'validation': 6, 
           'values': -4163, 
           'values_and_number_formats': 12}
        operations = {'add': 2, 
           'divide': 5, 
           'multiply': 4, 
           None: -4142, 
           'subtract': 3}
        self.xl.PasteSpecial(Paste=pastes[paste], Operation=operations[operation], SkipBlanks=skip_blanks, Transpose=transpose)
        return

    @property
    def hyperlink(self):
        if self.xl is not None:
            try:
                return self.xl.Hyperlinks(1).Address
            except pywintypes.com_error:
                raise Exception("The cell doesn't seem to contain a hyperlink!")

        else:
            return ''
        return

    def add_hyperlink(self, address, text_to_display, screen_tip):
        if self.xl is not None:
            link = self.xl.Hyperlinks.Add(Anchor=self.xl, Address=address)
            link.TextToDisplay = text_to_display
            link.ScreenTip = screen_tip
        return

    @property
    def color(self):
        if self.xl is not None:
            if self.xl.Interior.ColorIndex == ColorIndex.xlColorIndexNone:
                return
            else:
                return int_to_rgb(self.xl.Interior.Color)

        else:
            return
        return

    @color.setter
    def color(self, color_or_rgb):
        if self.xl is not None:
            if color_or_rgb is None:
                self.xl.Interior.ColorIndex = ColorIndex.xlColorIndexNone
            elif isinstance(color_or_rgb, int):
                self.xl.Interior.Color = color_or_rgb
            else:
                self.xl.Interior.Color = rgb_to_int(color_or_rgb)
        return

    @property
    def name(self):
        if self.xl is not None:
            try:
                name = Name(xl=self.xl.Name)
            except pywintypes.com_error:
                name = None

            return name
        return
        return

    @name.setter
    def name(self, value):
        if self.xl is not None:
            self.xl.Name = value
        return

    def __call__(self, *args):
        if self.xl is not None:
            if len(args) == 0:
                raise ValueError('Invalid arguments')
            return Range(xl=self.xl(*args))
        else:
            raise NotImplemented()
            return

    @property
    def rows(self):
        return Range(xl=self.xl.Rows)

    @property
    def columns(self):
        return Range(xl=self.xl.Columns)

    def select(self):
        return self.xl.Select()

    @property
    def merge_area(self):
        return Range(xl=self.xl.MergeArea)

    @property
    def merge_cells(self):
        return self.xl.MergeCells

    def merge(self, across):
        self.xl.Merge(across)

    def unmerge(self):
        self.xl.UnMerge()


def clean_value_data(data, datetime_builder, empty_as, number_builder):
    if number_builder is not None:
        return [ [ _com_time_to_datetime(c, datetime_builder) if isinstance(c, time_types) else number_builder(c) if type(c) == float else empty_as if c is None or isinstance(c, int) and c in (-2146826281,
                                                                                                                                                                                                 -2146826246,
                                                                                                                                                                                                 -2146826259,
                                                                                                                                                                                                 -2146826288,
                                                                                                                                                                                                 -2146826252,
                                                                                                                                                                                                 -2146826265,
                                                                                                                                                                                                 -2146826273) else c for c in row ] for row in data
               ]
    else:
        return [ [ _com_time_to_datetime(c, datetime_builder) if isinstance(c, time_types) else empty_as if c is None or isinstance(c, int) and c in (-2146826281,
                                                                                                                                                      -2146826246,
                                                                                                                                                      -2146826259,
                                                                                                                                                      -2146826288,
                                                                                                                                                      -2146826252,
                                                                                                                                                      -2146826265,
                                                                                                                                                      -2146826273) else c for c in row ] for row in data
               ]
        return


def _com_time_to_datetime(com_time, datetime_builder):
    """
    This function is a modified version from Pyvot (https://pypi.python.org/pypi/Pyvot)
    and subject to the following copyright:

    Copyright (c) Microsoft Corporation.

    This source code is subject to terms and conditions of the Apache License, Version 2.0. A
    copy of the license can be found in the LICENSE.txt file at the root of this distribution. If
    you cannot locate the Apache License, Version 2.0, please send an email to
    vspython@microsoft.com. By using this source code in any fashion, you are agreeing to be bound
    by the terms of the Apache License, Version 2.0.

    You must not remove this notice, or any other, from this software.

    """
    if PY3:
        return datetime_builder(month=com_time.month, day=com_time.day, year=com_time.year, hour=com_time.hour, minute=com_time.minute, second=com_time.second, microsecond=com_time.microsecond, tzinfo=None)
    else:
        assert com_time.msec == 0, 'fractional seconds not yet handled'
        return datetime_builder(month=com_time.month, day=com_time.day, year=com_time.year, hour=com_time.hour, minute=com_time.minute, second=com_time.second)
        return


def _datetime_to_com_time(dt_time):
    """
    This function is a modified version from Pyvot (https://pypi.python.org/pypi/Pyvot)
    and subject to the following copyright:

    Copyright (c) Microsoft Corporation.

    This source code is subject to terms and conditions of the Apache License, Version 2.0. A
    copy of the license can be found in the LICENSE.txt file at the root of this distribution. If
    you cannot locate the Apache License, Version 2.0, please send an email to
    vspython@microsoft.com. By using this source code in any fashion, you are agreeing to be bound
    by the terms of the Apache License, Version 2.0.

    You must not remove this notice, or any other, from this software.

    """
    if pd and isinstance(dt_time, type(pd.NaT)):
        return
    else:
        if np:
            if type(dt_time) is np.datetime64:
                dt_time = np_datetime_to_datetime(dt_time)
        if type(dt_time) is dt.date:
            dt_time = dt.datetime(dt_time.year, dt_time.month, dt_time.day, tzinfo=win32timezone.TimeZoneInfo.utc())
        if PY3:
            if pd and isinstance(dt_time, pd.Timestamp):
                dt_time = dt_time.to_pydatetime()
            dt_time = dt_time.replace(tzinfo=None)
            dt_time = dt_time.replace(tzinfo=win32timezone.TimeZoneInfo.utc())
            return dt_time
        assert dt_time.microsecond == 0, 'fractional seconds not yet handled'
        return pywintypes.Time(dt_time.timetuple())
        return


def prepare_xl_data_element(x):
    if isinstance(x, time_types):
        return _datetime_to_com_time(x)
    else:
        if np and isinstance(x, (np.floating, float)) and np.isnan(x):
            return ''
        else:
            if np and isinstance(x, np.number):
                return float(x)
            if x is None:
                return ''
            return x

        return


class Shape(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    @property
    def name(self):
        return self.xl.Name

    @property
    def parent(self):
        return Sheet(xl=self.xl.Parent)

    @property
    def type(self):
        return shape_types_i2s[self.xl.Type]

    @property
    def left(self):
        return self.xl.Left

    @left.setter
    def left(self, value):
        self.xl.Left = value

    @property
    def top(self):
        return self.xl.Top

    @top.setter
    def top(self, value):
        self.xl.Top = value

    @property
    def width(self):
        return self.xl.Width

    @width.setter
    def width(self, value):
        self.xl.Width = value

    @property
    def height(self):
        return self.xl.Height

    @height.setter
    def height(self, value):
        self.xl.Height = value

    def delete(self):
        self.xl.Delete()

    @name.setter
    def name(self, value):
        self.xl.Name = value

    @property
    def index(self):
        return self.xl.Index

    def activate(self):
        self.xl.Activate()


class Collection(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    def __call__(self, key):
        try:
            return self._wrap(xl=self.xl.Item(key))
        except pywintypes.com_error:
            raise KeyError(key)

    def __len__(self):
        return self.xl.Count

    def __iter__(self):
        for xl in self.xl:
            yield self._wrap(xl=xl)

    def __contains__(self, key):
        try:
            self.xl.Item(key)
            return True
        except pywintypes.com_error:
            return False


class Shapes(Collection):
    _wrap = Shape


class Chart(object):

    def __init__(self, xl_obj=None, xl=None):
        self.xl = xl_obj.Chart if xl is None else xl
        self.xl_obj = xl_obj
        return

    @property
    def api(self):
        return (self.xl_obj, self.xl)

    @property
    def name(self):
        if self.xl_obj is None:
            return self.xl.Name
        else:
            return self.xl_obj.Name
            return

    @name.setter
    def name(self, value):
        if self.xl_obj is None:
            self.xl.Name = value
        else:
            self.xl_obj.Name = value
        return

    @property
    def parent(self):
        if self.xl_obj is None:
            return Book(xl=self.xl.Parent)
        else:
            return Sheet(xl=self.xl_obj.Parent)
            return

    def set_source_data(self, rng):
        self.xl.SetSourceData(rng.xl)

    @property
    def chart_type(self):
        return chart_types_i2s[self.xl.ChartType]

    @chart_type.setter
    def chart_type(self, chart_type):
        self.xl.ChartType = chart_types_s2i[chart_type]

    @property
    def left(self):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        return self.xl_obj.Left

    @left.setter
    def left(self, value):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        self.xl_obj.Left = value
        return

    @property
    def top(self):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        return self.xl_obj.Top

    @top.setter
    def top(self, value):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        self.xl_obj.Top = value
        return

    @property
    def width(self):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        return self.xl_obj.Width

    @width.setter
    def width(self, value):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        self.xl_obj.Width = value
        return

    @property
    def height(self):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        return self.xl_obj.Height

    @height.setter
    def height(self, value):
        if self.xl_obj is None:
            raise Exception('This chart is not embedded.')
        self.xl_obj.Height = value
        return

    def delete(self):
        self.xl_obj.Delete()


class Charts(Collection):

    def _wrap(self, xl):
        return Chart(xl_obj=xl)

    def add(self, left, top, width, height):
        return Chart(xl_obj=self.xl.Add(left, top, width, height))


class Picture(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    @property
    def name(self):
        return self.xl.Name

    @name.setter
    def name(self, value):
        self.xl.Name = value

    @property
    def parent(self):
        return Sheet(xl=self.xl.Parent)

    @property
    def left(self):
        return self.xl.Left

    @left.setter
    def left(self, value):
        self.xl.Left = value

    @property
    def top(self):
        return self.xl.Top

    @top.setter
    def top(self, value):
        self.xl.Top = value

    @property
    def width(self):
        return self.xl.Width

    @width.setter
    def width(self, value):
        self.xl.Width = value

    @property
    def height(self):
        return self.xl.Height

    @height.setter
    def height(self, value):
        self.xl.Height = value

    def delete(self):
        self.xl.Delete()


class Pictures(Collection):
    _wrap = Picture

    @property
    def parent(self):
        return Sheet(xl=self.xl.Parent)

    def add(self, filename, link_to_file, save_with_document, left, top, width, height):
        return Picture(xl=self.xl.Parent.Shapes.AddPicture(Filename=filename, LinkToFile=link_to_file, SaveWithDocument=save_with_document, Left=left, Top=top, Width=width, Height=height).DrawingObject)


class Names(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    def __call__(self, name_or_index):
        return Name(xl=self.xl(name_or_index))

    def contains(self, name_or_index):
        try:
            self.xl(name_or_index)
        except pywintypes.com_error as e:
            if e.hresult == -2147352567:
                return False
            raise

        return True

    def __len__(self):
        return self.xl.Count

    def add(self, name, refers_to):
        return Name(xl=self.xl.Add(name, refers_to))


class Name(object):

    def __init__(self, xl):
        self.xl = xl

    @property
    def api(self):
        return self.xl

    def delete(self):
        self.xl.Delete()

    @property
    def name(self):
        return self.xl.Name

    @name.setter
    def name(self, value):
        self.xl.Name = value

    @property
    def refers_to(self):
        return self.xl.RefersTo

    @refers_to.setter
    def refers_to(self, value):
        self.xl.RefersTo = value

    @property
    def refers_to_range(self):
        return Range(xl=self.xl.RefersToRange)


chart_types_s2i = {'3d_area': -4098, 
   '3d_area_stacked': 78, 
   '3d_area_stacked_100': 79, 
   '3d_bar_clustered': 60, 
   '3d_bar_stacked': 61, 
   '3d_bar_stacked_100': 62, 
   '3d_column': -4100, 
   '3d_column_clustered': 54, 
   '3d_column_stacked': 55, 
   '3d_column_stacked_100': 56, 
   '3d_line': -4101, 
   '3d_pie': -4102, 
   '3d_pie_exploded': 70, 
   'area': 1, 
   'area_stacked': 76, 
   'area_stacked_100': 77, 
   'bar_clustered': 57, 
   'bar_of_pie': 71, 
   'bar_stacked': 58, 
   'bar_stacked_100': 59, 
   'bubble': 15, 
   'bubble_3d_effect': 87, 
   'column_clustered': 51, 
   'column_stacked': 52, 
   'column_stacked_100': 53, 
   'cone_bar_clustered': 102, 
   'cone_bar_stacked': 103, 
   'cone_bar_stacked_100': 104, 
   'cone_col': 105, 
   'cone_col_clustered': 99, 
   'cone_col_stacked': 100, 
   'cone_col_stacked_100': 101, 
   'cylinder_bar_clustered': 95, 
   'cylinder_bar_stacked': 96, 
   'cylinder_bar_stacked_100': 97, 
   'cylinder_col': 98, 
   'cylinder_col_clustered': 92, 
   'cylinder_col_stacked': 93, 
   'cylinder_col_stacked_100': 94, 
   'doughnut': -4120, 
   'doughnut_exploded': 80, 
   'line': 4, 
   'line_markers': 65, 
   'line_markers_stacked': 66, 
   'line_markers_stacked_100': 67, 
   'line_stacked': 63, 
   'line_stacked_100': 64, 
   'pie': 5, 
   'pie_exploded': 69, 
   'pie_of_pie': 68, 
   'pyramid_bar_clustered': 109, 
   'pyramid_bar_stacked': 110, 
   'pyramid_bar_stacked_100': 111, 
   'pyramid_col': 112, 
   'pyramid_col_clustered': 106, 
   'pyramid_col_stacked': 107, 
   'pyramid_col_stacked_100': 108, 
   'radar': -4151, 
   'radar_filled': 82, 
   'radar_markers': 81, 
   'stock_hlc': 88, 
   'stock_ohlc': 89, 
   'stock_vhlc': 90, 
   'stock_vohlc': 91, 
   'surface': 83, 
   'surface_top_view': 85, 
   'surface_top_view_wireframe': 86, 
   'surface_wireframe': 84, 
   'xy_scatter': -4169, 
   'xy_scatter_lines': 74, 
   'xy_scatter_lines_no_markers': 75, 
   'xy_scatter_smooth': 72, 
   'xy_scatter_smooth_no_markers': 73}
chart_types_i2s = {v:k for k, v in chart_types_s2i.items()}
directions_s2i = {'d': -4121, 
   'down': -4121, 
   'l': -4159, 
   'left': -4159, 
   'r': -4161, 
   'right': -4161, 
   'u': -4162, 
   'up': -4162}
directions_i2s = {-4121: 'down', 
   -4159: 'left', 
   -4161: 'right', 
   -4162: 'up'}
calculation_s2i = {'automatic': -4105, 
   'manual': -4135, 
   'semiautomatic': 2}
calculation_i2s = {v:k for k, v in calculation_s2i.items()}
shape_types_s2i = {'auto_shape': 1, 
   'callout': 2, 
   'canvas': 20, 
   'chart': 3, 
   'comment': 4, 
   'content_app': 27, 
   'diagram': 21, 
   'embedded_ole_object': 7, 
   'form_control': 8, 
   'free_form': 5, 
   'group': 6, 
   'igx_graphic': 24, 
   'ink': 22, 
   'ink_comment': 23, 
   'line': 9, 
   'linked_ole_object': 10, 
   'linked_picture': 11, 
   'media': 16, 
   'ole_control_object': 12, 
   'picture': 13, 
   'placeholder': 14, 
   'script_anchor': 18, 
   'shape_type_mixed': -2, 
   'table': 19, 
   'text_box': 17, 
   'text_effect': 15, 
   'web_video': 26}
shape_types_i2s = {v:k for k, v in shape_types_s2i.items()}