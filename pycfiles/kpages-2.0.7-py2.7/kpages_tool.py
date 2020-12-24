# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kpages/kpages_tool.py
# Compiled at: 2019-03-25 08:05:34
"""
    author comger@gmail.com
"""
import tornado.ioloop
from optparse import OptionParser
from kpages import LogicContext, run_test, pro_test, run_doc, reflesh_config, set_default_encoding

def _get_opt():
    parser = OptionParser('%prog [options]', version='%prog v0.9')
    parser.add_option('--config', dest='config', default='setting.py', help='config for app')
    parser.add_option('--test', dest='test', default=None, help='utest module')
    parser.add_option('--doc', dest='doc', default=None, help='doc all router api to markdown')
    parser.add_option('--pro', dest='pro', default=None, help='profile for method')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        set_default_encoding()
        opts, args = _get_opt()
        reflesh_config(opts.config)
        if opts.test is not None:
            m = opts.test
            if m == 'all':
                m = None
            with LogicContext():
                run_test(m)
        elif opts.pro is not None:
            with LogicContext():
                pro_test(opts.pro)
        elif opts.doc is not None:
            with LogicContext():
                run_doc(opts.doc)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print 'exit tool '