# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jinja\__init__.py
# Compiled at: 2007-10-21 19:31:50
"""
    jinja
    ~~~~~

    Jinja is a `sandboxed`_ template engine written in pure Python. It
    provides a `Django`_ like non-XML syntax and compiles templates into
    executable python code. It's basically a combination of Django templates
    and python code.

    Nutshell
    --------

    Here a small example of a Jinja template::

        {% extends 'base.html' %}
        {% block title %}Memberlist{% endblock %}
        {% block content %}
          <ul>
          {% for user in users %}
            <li><a href="{{ user.url|e }}">{{ user.username|e }}</a></li>
          {% endfor %}
          </ul>
        {% endblock %}

    Philosophy
    ----------

    Application logic is for the controller but don't try to make the life
    for the template designer too hard by giving him too few functionality.

    For more informations visit the new `jinja webpage`_ and `documentation`_.

    Note
    ----

    This is the Jinja 1.0 release which is completely incompatible with the
    old "pre 1.0" branch. The old branch will still receive security updates
    and bugfixes but the 1.0 branch will be the only version that receives
    support.

    If you have an application that uses Jinja 0.9 and won't be updated in
    the near future the best idea is to ship a Jinja 0.9 checkout together
    with the application.

    The `Jinja tip`_ is installable via `easy_install` with ``easy_install
    Jinja==dev``.

    .. _sandboxed: http://en.wikipedia.org/wiki/Sandbox_(computer_security)
    .. _Django: http://www.djangoproject.com/
    .. _jinja webpage: http://jinja.pocoo.org/
    .. _documentation: http://jinja.pocoo.org/documentation/index.html
    .. _Jinja tip: http://dev.pocoo.org/hg/jinja-main/archive/tip.tar.gz#egg=Jinja-dev

    :copyright: 2007 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from jinja.environment import Environment
from jinja.datastructure import Markup
from jinja.plugin import jinja_plugin_factory as template_plugin_factory
from jinja.loaders import FileSystemLoader, PackageLoader, DictLoader, ChoiceLoader, FunctionLoader, MemcachedFileSystemLoader
from jinja.utils import from_string
__all__ = [
 'Environment', 'Markup', 'FileSystemLoader', 'PackageLoader',
 'DictLoader', 'ChoiceLoader', 'FunctionLoader',
 'MemcachedFileSystemLoader', 'from_string']
__version__ = '1.2'