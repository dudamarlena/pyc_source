# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/util/vtkVariant.py
# Compiled at: 2018-11-28 17:07:58
"""
Utility functions to mimic the template support functions for vtkVariant
"""
import vtk, sys
_variant_type_map = {'void': vtk.VTK_VOID, 
   'char': vtk.VTK_CHAR, 
   'unsigned char': vtk.VTK_UNSIGNED_CHAR, 
   'signed char': vtk.VTK_SIGNED_CHAR, 
   'short': vtk.VTK_SHORT, 
   'unsigned short': vtk.VTK_UNSIGNED_SHORT, 
   'int': vtk.VTK_INT, 
   'unsigned int': vtk.VTK_UNSIGNED_INT, 
   'long': vtk.VTK_LONG, 
   'unsigned long': vtk.VTK_UNSIGNED_LONG, 
   'long long': vtk.VTK_LONG_LONG, 
   'unsigned long long': vtk.VTK_UNSIGNED_LONG_LONG, 
   'float': vtk.VTK_FLOAT, 
   'double': vtk.VTK_DOUBLE, 
   'string': vtk.VTK_STRING, 
   'unicode string': vtk.VTK_UNICODE_STRING, 
   'vtkObjectBase': vtk.VTK_OBJECT, 
   'vtkObject': vtk.VTK_OBJECT}
_variant_method_map = {vtk.VTK_VOID: '', 
   vtk.VTK_CHAR: 'ToChar', 
   vtk.VTK_UNSIGNED_CHAR: 'ToUnsignedChar', 
   vtk.VTK_SIGNED_CHAR: 'ToSignedChar', 
   vtk.VTK_SHORT: 'ToShort', 
   vtk.VTK_UNSIGNED_SHORT: 'ToUnsignedShort', 
   vtk.VTK_INT: 'ToInt', 
   vtk.VTK_UNSIGNED_INT: 'ToUnsignedInt', 
   vtk.VTK_LONG: 'ToLong', 
   vtk.VTK_UNSIGNED_LONG: 'ToUnsignedLong', 
   vtk.VTK_LONG_LONG: 'ToLongLong', 
   vtk.VTK_UNSIGNED_LONG_LONG: 'ToUnsignedLongLong', 
   vtk.VTK_FLOAT: 'ToFloat', 
   vtk.VTK_DOUBLE: 'ToDouble', 
   vtk.VTK_STRING: 'ToString', 
   vtk.VTK_UNICODE_STRING: 'ToUnicodeString', 
   vtk.VTK_OBJECT: 'ToVTKObject'}
_variant_check_map = {vtk.VTK_VOID: 'IsValid', 
   vtk.VTK_CHAR: 'IsChar', 
   vtk.VTK_UNSIGNED_CHAR: 'IsUnsignedChar', 
   vtk.VTK_SIGNED_CHAR: 'IsSignedChar', 
   vtk.VTK_SHORT: 'IsShort', 
   vtk.VTK_UNSIGNED_SHORT: 'IsUnsignedShort', 
   vtk.VTK_INT: 'IsInt', 
   vtk.VTK_UNSIGNED_INT: 'IsUnsignedInt', 
   vtk.VTK_LONG: 'IsLong', 
   vtk.VTK_UNSIGNED_LONG: 'IsUnsignedLong', 
   vtk.VTK_LONG_LONG: 'IsLongLong', 
   vtk.VTK_UNSIGNED_LONG_LONG: 'IsUnsignedLongLong', 
   vtk.VTK_FLOAT: 'IsFloat', 
   vtk.VTK_DOUBLE: 'IsDouble', 
   vtk.VTK_STRING: 'IsString', 
   vtk.VTK_UNICODE_STRING: 'IsUnicodeString', 
   vtk.VTK_OBJECT: 'IsVTKObject'}

def vtkVariantCreate(v, t):
    """
    Create a vtkVariant of the specified type, where the type is in the
    following format: 'int', 'unsigned int', etc. for numeric types,
    and 'string' or 'unicode string' for strings.  You can also use an
    integer VTK type constant for the type.
    """
    if not issubclass(type(t), int):
        t = _variant_type_map[t]
    return vtk.vtkVariant(v, t)


def vtkVariantExtract(v, t=None):
    """
    Extract the specified value type from the vtkVariant, where the type is
    in the following format: 'int', 'unsigned int', etc. for numeric types,
    and 'string' or 'unicode string' for strings.  You can also use an
    integer VTK type constant for the type.  Set the type to 'None" to
    extract the value in its native type.
    """
    v = vtk.vtkVariant(v)
    if t == None:
        t = v.GetType()
    elif not issubclass(type(t), int):
        t = _variant_type_map[t]
    if getattr(v, _variant_check_map[t])():
        return getattr(v, _variant_method_map[t])()
    else:
        return
        return


def vtkVariantCast(v, t):
    """
    Cast the vtkVariant to the specified value type, where the type is
    in the following format: 'int', 'unsigned int', etc. for numeric types,
    and 'string' or 'unicode string' for strings.  You can also use an
    integer VTK type constant for the type.
    """
    if not issubclass(type(t), int):
        t = _variant_type_map[t]
    v = vtk.vtkVariant(v, t)
    if v.IsValid():
        return getattr(v, _variant_method_map[t])()
    else:
        return
        return


def vtkVariantStrictWeakOrder(s1, s2):
    """
    Compare variants by type first, and then by value.  When called from
    within a Python 2 interpreter, the return values are -1, 0, 1 like the
    cmp() method, for compatibility with the Python 2 list sort() method.
    This is in contrast with the Python 3 version of this method (and the
    VTK C++ version), which return true or false.
    """
    s1 = vtk.vtkVariant(s1)
    s2 = vtk.vtkVariant(s2)
    t1 = s1.GetType()
    t2 = s2.GetType()

    def vcmp(x, y):
        if sys.hexversion >= 50331648:
            return x < y
        else:
            return cmp(x, y)

    if t1 != t2:
        return vcmp(t1, t2)
    v1 = s1.IsValid()
    v2 = s2.IsValid()
    if not v1 or not v2:
        return vcmp(v1, v2)
    r1 = getattr(s1, _variant_method_map[t1])()
    r2 = getattr(s2, _variant_method_map[t2])()
    if t1 == vtk.VTK_OBJECT:
        c1 = r1.GetClassName()
        c2 = r2.GetClassName()
        if c1 != c2:
            return vcmp(c1, c2)
        return vcmp(r1.__this__, r2.__this__)
    return vcmp(r1, r2)


if sys.hexversion >= 50331648:

    class vtkVariantStrictWeakOrderKey:
        """A key method (class, actually) for use with sort()"""

        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return vtkVariantStrictWeakOrder(self.obj, other)


else:

    class vtkVariantStrictWeakOrderKey:
        """A key method (class, actually) for use with sort()"""

        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return vtkVariantStrictWeakOrder(self.obj, other) < 0

        def __gt__(self, other):
            return vtkVariantStrictWeakOrder(self.obj, other) > 0

        def __eq__(self, other):
            return vtkVariantStrictWeakOrder(self.obj, other) == 0

        def __le__(self, other):
            return vtkVariantStrictWeakOrder(self.obj, other) <= 0

        def __ge__(self, other):
            return vtkVariantStrictWeakOrder(self.obj, other) >= 0

        def __ne__(self, other):
            return vtkVariantStrictWeakOrder(self.obj, other) != 0


def vtkVariantStrictEquality(s1, s2):
    """
    Check two variants for strict equality of type and value.
    """
    s1 = vtk.vtkVariant(s1)
    s2 = vtk.vtkVariant(s2)
    t1 = s1.GetType()
    t2 = s2.GetType()
    if t1 != t2:
        return False
    v1 = s1.IsValid()
    v2 = s2.IsValid()
    if not v1 and not v2:
        return True
    if v1 != v2:
        return False
    r1 = getattr(s1, _variant_method_map[t1])()
    r2 = getattr(s2, _variant_method_map[t2])()
    return r1 == r2


def vtkVariantLessThan(s1, s2):
    """
    Return true if s1 < s2.
    """
    return vtk.vtkVariant(s1) < vtk.vtkVariant(s2)


def vtkVariantEqual(s1, s2):
    """
    Return true if s1 == s2.
    """
    return vtk.vtkVariant(s1) == vtk.vtkVariant(s2)