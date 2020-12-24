# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pytest_gui_status\status_gui\utils_gui.py
# Compiled at: 2016-01-13 15:25:21
import jinja2, os

def render_template(app, tmpl_name, tmpl_params):
    with open(os.path.join(app.template_path, tmpl_name)) as (f_tmpl):
        tmpl_content = f_tmpl.read()
    return jinja2.Template(tmpl_content).render(tmpl_params)