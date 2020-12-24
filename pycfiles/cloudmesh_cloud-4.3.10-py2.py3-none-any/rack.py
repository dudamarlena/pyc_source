# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/system/rack.py
# Compiled at: 2017-04-23 10:30:41
import json, subprocess, textwrap
from jinja2 import Template
from cloudmesh_client.common.util import path_expand

class Rack(object):

    def __init__(self, servers):
        self.template_string = None
        self.servers = servers
        self.diag = None
        self.data = None
        return

    def set_template(self, template):
        if template is None:
            self.template_string = 'rackdiag {' + '\n              // Change order of rack-number as ascending\n              ascending;\n\n              // define height of rack\n              20U;\n\n              // define description of rack\n              description = "Comet Cluster Virtualization Rack";\n\n              // define rack units\n              1: UPS [2U];   // define height of unit\n              3: Network [color=green]\n              {% for x in range (0, 10) %}\n              {{x+4}}: Server [' + (' ').join(['{{server[x]["label"]}}', '{{server[x]["numbered"]}}', '{{server[x]["fontsize"]}}', '{{server[x]["shape"]}}', '{{server[x]["textcolor"]}}', '{{server[x]["color"]}}']) + ']' + '{% endfor %}' + '\n}'
        else:
            self.template_string = template
        self.generate_rack(self.servers)
        return

    def generate_rack(self, servers):
        empty = {'color': 'color="white" ', 
           'label': '', 
           'numbered': '', 
           'fontsize': '', 
           'shape': '', 
           'textcolor': ''}
        self.data = []
        for server in range(0, servers):
            self.data.append(dict(empty))

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def dump(self):
        content = self.diag
        result = []
        counter = 1
        for line in content.split('\n'):
            result.append(('{0:>5}: {1}').format(counter, line))
            counter += 1

        return ('\n').join(result)

    def set(self, server, **kwargs):
        for attribute in kwargs:
            comma = ' '
            if attribute is not 'color':
                comma = ', '
            self.data[(server - 1)][attribute] = ('{}="{}"{}').format(attribute, kwargs[attribute], comma)

    def set_color(self, server, color):
        self.set(server, color=color)

    def set_label(self, server, label):
        self.set(server, label=label)

    def set_numbering(self, server, numbering):
        self.set(server, numbering=numbering)

    def set_fontsize(self, server, fontsize):
        self.set(server, fontsize=fontsize)

    def set_textcolorl(self, server, textcolorl):
        self.set(server, textcolorl=textcolorl)

    def set_shape(self, server, shape):
        self.set(server, shape=shape)

    def render(self):
        template = Template(textwrap.dedent(self.template_string))
        self.diag = template.render(server=self.data)
        return self.diag

    def diagram(self, name):
        with open(('{}.diag').format(path_expand(name)), 'w') as (f):
            f.write(self.diag)

    def svg(self, name):
        self.diagram(name)
        cmd = ['rackdiag', '-T', 'svg', ('{}.diag').format(path_expand(name))]
        subprocess.Popen(cmd).wait()

    def view(self, name):
        cmd = [
         'open', ('{}.svg').format(path_expand(name))]
        subprocess.Popen(cmd)


if __name__ == '__main__':
    rack = Rack(10)
    rack.set_template(None)
    rack.set(10, color='blue')
    rack.set(9, color='green')
    rack.set(8, textcolor='red')
    rack.set(7, textsize='24')
    rack.set(7, shape='cloud')
    rack.set(6, numbered='1')
    result = rack.render()
    name = '~/.cloudmesh/c'
    rack.svg(name)
    rack.view(name)