# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ucsmquery.py
# Compiled at: 2011-11-02 12:56:16
from pyucsm import *
import getopt
from inspect import getargspec
import sys
IGNORE = [
 'set_auth', 'login', 'logout', 'refresh']
CONN_CLS = UcsmConnection
ONLY_DN = False
HIERARCHY = False

def gener_descr(func, name):
    args = getargspec(func)[0]
    args = args[args[0] == 'self':]
    templ = 'Method:\t\t%(name)s'
    if args:
        templ += '\nArguments:\t%(args)s'
    if func.func_doc:
        templ += '\nDocumentation:\t%(doc)s'
    return templ % {'name': name, 'args': (', ').join(args), 'doc': func.func_doc}


def get_possible_opts(cls):
    return list(set('%s=' % arg for attr_name, attr in cls.__dict__.items() if attr_name not in IGNORE and attr_name[0] != '_' and hasattr(attr, 'func_name') for arg in getargspec(attr)[0][1:]))


def create_doc(cls):
    descr = ('\n\n').join(gener_descr(attr, attr_name) for attr_name, attr in cls.__dict__.items() if attr_name not in IGNORE and attr_name[0] != '_' and hasattr(attr, 'func_name'))
    return descr


def print_help(func_name):
    global CONN_CLS
    cls = CONN_CLS
    try:
        print gener_descr(getattr(cls, func_name))
    except AttributeError:
        return usage()


def usage():
    print 'Usage: ucsmquery.py host[:port] [options] command [arguments].\n\nOptions:\n    -l login -- UCSM login\n    -p pass  -- password\n\nCommands:\n\n%s\n\nArguments for UCSM query must be used as long options. Sample:\n\nucsmquery.py 192.168.0.1 -l admin -p 12345  resolve_dn --dn=sys/chassis-2/blade-5\n' % create_doc(UcsmConnection)


def wrong_command(command=None):
    print 'Command not found or incorrect arguments.'


def print_objects(objects, only_dn=False, hierarchy=False):
    if only_dn:
        for obj in objects:
            try:
                print '%s: %s' % (obj.ucs_class, obj.dn)
            except AttributeError:
                print '%s object has no DN' % obj.ucs_class

            if hierarchy:
                print
                print_objects(obj.children, only_dn, hierarchy)

    else:
        newline = False
        for obj in objects:
            if newline:
                print
            print obj.pretty_str()
            if hierarchy:
                if len(obj.children):
                    print
                print_objects(obj.children, only_dn, hierarchy)
            newline = True


def print_objects_glob(objects):
    global HIERARCHY
    global ONLY_DN
    print_objects(objects, ONLY_DN, HIERARCHY)


def serialize_print(data):
    if isinstance(data, list):
        if len(data) and isinstance(data[0], UcsmObject):
            print_objects_glob(data)
        else:
            for elem in data:
                serialize_print(elem)

    if isinstance(data, UcsmObject):
        print_objects_glob([data])
    if isinstance(data, dict):
        for key, val in data.items():
            print '%s:'
            serialize_print(val)

    if isinstance(data, basestring):
        print data


def kwargs_to_ucsm_object(cls_, **kwargs):
    obj = UcsmObject(cls_)
    for key, val in kwargs:
        setattr(obj, key, val)

    return obj


def parse_opt_val(string):
    try:
        if string.startswith('{') or string.startswith('obj('):
            raise Exception
        return eval(string, {'obj': kwargs_to_ucsm_object, 'UcsmObject': UcsmObject})
    except Exception:
        return string


def kwargs_from_opts(opts):
    kwargs = {}
    for opt, val in opts.items():
        kwargs[opt] = parse_opt_val(val)

    return kwargs


def perform(host, login, password, command, args=list(), opts=dict(), port=80):
    client = CONN_CLS(host, port)
    try:
        try:
            client.login(login, password)
            reply = getattr(client, command)(*args, **kwargs_from_opts(opts))
            serialize_print(reply)
        except (KeyError, AttributeError):
            wrong_command()
        except UcsmError as e:
            print 'Error: %s' % e

    finally:
        client.logout()


def import_class(path):
    mod, cls = path.rsplit('.', 1)
    return getattr(__import__(mod, fromlist=[cls]), cls)


def main():
    global CONN_CLS
    global HIERARCHY
    global ONLY_DN
    global quiet
    try:
        argv = sys.argv[1:]
        opts, args = getopt.gnu_getopt(argv, 'l:p:P:dqcr', get_possible_opts(CONN_CLS))
    except getopt.GetoptError as e:
        usage()
        print e
        exit()

    login = 'admin'
    password = 'nbv12345'
    comm_opts = {}
    quiet = False
    for opt, val in opts:
        if opt == '-l':
            login = val
        elif opt == '-p':
            password = val
        elif opt == '-d':
            import pyucsm
            pyucsm.set_debug(True)
        elif opt[:2] == '--':
            comm_opts[opt[2:]] = val
        elif opt == '-q':
            ONLY_DN = True
        elif opt == '-r':
            HIERARCHY = True
        elif opt == '-c':
            CONN_CLS = import_class(val)

    if len(args) >= 2:
        if args[0] == 'help':
            print_help(args[1])
            exit(0)
        port = 80
        host = args[0]
        colon = args[0].find(':')
        if colon >= 0:
            host = args[0][:colon]
            port = int(args[0][colon + 1:])
        perform(host, login, password, args[1], args=args[2:], opts=comm_opts, port=port)
    else:
        usage()


if __name__ == '__main__':
    main()