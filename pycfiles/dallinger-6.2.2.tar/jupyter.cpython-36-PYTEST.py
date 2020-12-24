# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/jupyter.py
# Compiled at: 2020-04-27 20:27:30
# Size of source mod 2**32: 1386 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from ipywidgets import widgets
from jinja2 import Template
from traitlets import observe, Unicode
from dallinger.config import get_config
header_template = Template('\n<h2>{{ name }}</h2>\n<div>Status: {{ status }}</div>\n{% if app_id %}<div>App ID: {{ app_id }}</div>{% endif %}\n')
config_template = Template('\n<table style="min-width: 50%">\n{% for k, v in config %}\n<tr>\n<th>{{ k }}</th>\n<td>{{ v }}</td>\n</tr>\n{% endfor %}\n</table>\n')

class ExperimentWidget(widgets.VBox):
    status = Unicode('Unknown')

    def __init__(self, exp):
        self.exp = exp
        super(ExperimentWidget, self).__init__()
        self.render()

    @property
    def config_tab(self):
        config = get_config()
        if config.ready:
            config_items = list(config.as_dict().items())
            config_items.sort()
            config_tab = widgets.HTML(config_template.render(config=config_items))
        else:
            config_tab = widgets.HTML('Not loaded.')
        return config_tab

    @observe('status')
    def render(self, change=None):
        header = widgets.HTML(header_template.render(name=(self.exp.task),
          status=(self.status),
          app_id=(self.exp.app_id)))
        tabs = widgets.Tab(children=[self.config_tab])
        tabs.set_title(0, 'Configuration')
        self.children = [header, tabs]