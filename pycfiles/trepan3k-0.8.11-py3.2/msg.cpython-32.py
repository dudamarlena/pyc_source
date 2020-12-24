# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/bwprocessor/msg.py
# Compiled at: 2015-04-06 04:35:06
""" Common I/O routines"""

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

        def __init__(self):
            self.response = {'errs': [],  'msg': []}


    import pprint
    demo = Demo()
    msg(demo, 'hi')
    pp = pprint.PrettyPrinter()
    pp.pprint(demo.response)