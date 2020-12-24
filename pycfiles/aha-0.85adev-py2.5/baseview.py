# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/controller/baseview.py
# Compiled at: 2010-10-22 05:14:42
""" GAEO View package """
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