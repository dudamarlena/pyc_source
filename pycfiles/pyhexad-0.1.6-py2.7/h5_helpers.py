# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5_helpers.py
# Compiled at: 2014-12-08 16:25:59
import h5py

def is_h5_location_handle(loc):
    """
    Returns if 'loc' is a valid location handle.
    Only HDF5 file or group handles are valid location handles.

    """
    return isinstance(loc, (h5py.File, h5py.Group))


def resolvable(loc, path):
    """
    Returns if (loc, path) can be resolved to an HDF5 object.
    """
    if not isinstance(path, str):
        raise TypeError("'path' must be a string.")
    if is_h5_location_handle(loc) and path in loc:
        try:
            obj = loc.get(path, getclass=True)
            return True
        except KeyError:
            return False


def path_is_valid_wrt_loc(loc, path):
    """ Returns a tuple with the path_validity and the link type.

    Returns if 'path' is valid with respect to location 'loc'.
    The first return value (bool) indicates the validity.
    If the path is valid wrt. location, the second return value
    is the type of link or None, if the path is '/'.
    If the path is invalid wrt. location, the second argument is
    always none.

    """
    if is_h5_location_handle(loc) and isinstance(path, str) and path in loc:
        if path != '/':
            try:
                link_type = loc.get(path, getlink=True)
                known_link_type = True
            except:
                known_link_type = False
                link_type = None

            return (
             known_link_type, link_type)
        else:
            return (
             True, None)

    else:
        return (
         False, None)
    return


def path_is_available_for_obj(loc, path, obj_type):
    """
    Returns if a given path is available for the creation of a new HDF5 object
    of a certain class.

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        the path for the new HDF5 object.
    obj_type: h5py.[Dataset, Dtatype, Group]

    """
    if not is_h5_location_handle(loc):
        return False
    if not isinstance(path, str):
        return False
    if obj_type not in (h5py.Dataset, h5py.Datatype, h5py.Group):
        return False
    if path == '' or path[(-1)] == '/':
        return False
    if path == '/' and obj_type == h5py.Group:
        return False
    if path == '/' and obj_type != h5py.Group:
        return False
    is_absolute = False
    if path[0] == '/':
        is_absolute = True
        path = path[1:]
    a = path.split('/')
    ppath = ''
    if is_absolute:
        ppath = '/'
    for i in range(len(a)):
        ppath += a[i]
        if ppath not in loc:
            return True
        if len(a) == 1 or i == len(a) - 1:
            if resolvable(loc, ppath):
                cur_type = loc.get(ppath, getclass=True)
                if cur_type != obj_type:
                    return False
                if obj_type == h5py.Group:
                    return True
                return False
            else:
                return False
        elif resolvable(loc, ppath):
            if loc.get(ppath, getclass=True) != h5py.Group:
                return False
        else:
            return False
        ppath += '/'


def is_object(filename, path):
    """
    Check if there is an object at 'path' in 'filename'.
    """
    if not (isinstance(filename, str) and isinstance(path, str)):
        raise TypeError('String expected.')
    ret = False
    try:
        with h5py.File(filename, 'r') as (f):
            cls = f.get(path, getclass=True)
            ret = cls == h5py.Dataset or cls == h5py.Group
    except Exception:
        pass

    return ret


def object_has_attribute(filename, path, attr):
    """
    Check if an HDF5 object has an HDF5 attribute with name 'attr'.
    """
    if not (isinstance(filename, str) and isinstance(path, str) and isinstance(attr, str)):
        raise TypeError('String expected.')
    ret = False
    try:
        with h5py.File(filename, 'r') as (f):
            ret = attr in f[path].attrs
    except Exception:
        pass

    return ret