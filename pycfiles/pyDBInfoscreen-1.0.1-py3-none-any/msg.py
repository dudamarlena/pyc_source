# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/bwprocessor/msg.py
# Compiled at: 2013-03-08 17:08:25
__doc__ = ' Common I/O routines'

def errmsg(proc_obj, message, opts={}):
    response = proc_obj.response
    if 'set_name' in opts:
        response['name'] = 'error'
    return response['errs'].append(message)


def msg(proc_obj, message, opts={}):
    response = proc_obj.response
    return response['msg'].append(message)


if __name__ == '__main__':

    class Demo:
        __module__ = __name__

        def __init__(self):
            self.response = {'errs': [], 'msg': []}


    import pprint
    demo = Demo()
    msg(demo, 'hi')
    pp = pprint.PrettyPrinter()
    pp.pprint(demo.response)