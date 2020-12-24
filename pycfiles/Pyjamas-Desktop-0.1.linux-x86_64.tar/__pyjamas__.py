# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/__pyjamas__.py
# Compiled at: 2008-09-03 16:46:52
""" This module interfaces between PyWebkitGTK and the Pyjamas API,
    to get applications kick-started.
"""
from traceback import print_stack
main_frame = None

def set_main_frame(frame):
    global main_frame
    main_frame = frame
    import DOM
    DOM.init()


def get_main_frame():
    return main_frame


def doc():
    return main_frame.get_gdom_document()


def wnd():
    """ try to avoid using this function until a bug in pywebkitgtk
        has been tracked down
    """
    return main_frame.get_dom_window()


def JS(code):
    """ try to avoid using this function, it will only give you grief
        right now...
    """
    ctx = main_frame.gjs_get_global_context()
    try:
        return ctx.eval(code)
    except:
        print 'code', code
        print_stack()


pygwt_moduleNames = []

def pygwt_processMetas():
    global pygwt_moduleNames
    import DOM
    metas = doc().get_elements_by_tag_name('meta')
    for i in range(metas.props.length):
        meta = metas.item(i)
        name = DOM.getAttribute(meta, 'name')
        if name == 'pygwt:module':
            content = DOM.getAttribute(meta, 'content')
            if content:
                pygwt_moduleNames.append(content)

    return pygwt_moduleNames