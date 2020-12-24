# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sanic_jinja/__init__.py
# Compiled at: 2019-02-22 00:36:09
# Size of source mod 2**32: 806 bytes
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape
import functools

def generate_template(app=None, package_name=None, package_path='templates'):
    if not app or not package_name:
        raise Exception('app or package_name is None.')
    env = Environment(loader=PackageLoader(package_name=package_name, package_path=package_path), autoescape=(select_autoescape(['html', 'xml', 'tpl'])))

    def template(env, tpl, **kwargs):
        """
        render template
        :param tpl:
        :param kwargs:
        :return:
        """
        if not env:
            raise Exception("template doesn't init.")
        templ = env.get_template(tpl)
        return html(templ.render(kwargs))

    return functools.partial(template, env)