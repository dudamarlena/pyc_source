# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/controller/baseview.py
# Compiled at: 2010-10-22 05:14:42
__doc__ = ' GAEO View package '
import os
from aha import Config

class BaseView(object):

    def __init__(self, controller, **args):
        self.__config = Config()
        self.__controller = controller
        self.rendered = False
        self.__tpldir = os.path.join(self.__config.template_dir, controller.params['controller'])

    def render(self, content, hdrs={}, **opts):
        nothing = opts.get('nothing', False)
        if not nothing:
            r = self.__controller.response
            if hdrs:
                for (k, v) in hdrs.items():
                    r.headers[k] = v

            r.out.write(content)
        self.rendered = True