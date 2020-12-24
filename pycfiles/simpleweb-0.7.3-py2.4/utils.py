# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/utils.py
# Compiled at: 2007-01-10 11:07:05
import sys
ENV_KEY_FLUP_SESSION = 'com.saddi.service.session'
ENV_KEY_AUTH_MIDDLEWARE = 'simpleweb.middleware.auth.user'

def doctor_system_path(sys):
    sys.path.insert(0, '.')


def from_import(m, try_class=True):
    """
        Given a module string 'a.b.c' will do:

        from a.b import c and return c to the caller
        """
    if m.find('.') < 0:
        return __import__(m)
    else:
        (package, module) = m.rsplit('.', 1)
        try:
            r = __import__(m, {}, {}, [module])
        except ImportError:
            if not try_class:
                raise
            else:
                _module = from_import(package, try_class=False)
                try:
                    return getattr(_module, module)
                except AttributeError:
                    raise ImportError("Failed to import '%s'. '%s' not found in '%s'" % (m, module, package))

        else:
            return r


def get_functions(m):
    """
        Given a module 'm', will return a generator of
        all the function objects in the module. Given a class,
        will return a generator of all the actual functions
        attached to the methods of the class.
        """
    m = from_import(m)
    objs = vars(m)
    for fn in objs.values():
        if hasattr(fn, 'func_name'):
            yield fn
        elif hasattr(fn, 'im_func'):
            yield fn.im_func


def get_methods_dict(m, list_of_methods):
    """
        Given a module/class object m and a list of methods ['A', 'B', 'func']
        will return a dict like: {'A':m.A, 'B':m.B, 'func':m.func}.

        If any of m.A, m.B or m.func doesn't exist, the dictionary won't include it
        """
    funcs = get_functions(m)
    method_dict = {}
    for f in funcs:
        if f.func_name in list_of_methods:
            method_dict[f.func_name] = f

    return method_dict


def optional_dependency_err(subsystem, dependency):
    msg_err('Cannot initialize %s. %s must be properly installed first.' % (subsystem, dependency))
    sys.exit()


def msg_info(msg):
    sys.stdout.write('=> %s\n' % msg)


def msg_err(msg):
    sys.stderr.write('!! %s\n' % msg)


def msg_warn(msg):
    sys.stderr.write('** %s\n' % msg)