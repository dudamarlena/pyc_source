# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/publickey/sshconfig.py
# Compiled at: 2014-10-30 23:20:51
import sys, codecs, jinja2, publickey.yamldata as yd
template = jinja2.Template("{% for id, x in items %}\nHost {{ id }}\n  {% if x.title %}# {{ x.title }}{% endif %}\n  HostName {{ x.hostname }}\n  Port {{ x.port|default(22) }}\n  User {{ x.user|default('ubuntu') }}\n  IdentityFile {{ x.identityfile|default('~/.ssh/id_rsa') }}\n{% endfor %}\nServerAliveInterval 120\n")

def generate(config):
    doc = yd.load(config.filepath)
    items = sorted(yd.filter_by_tags(doc, config.tags), key=lambda x: (
     yd.first_tag(x[1]), x[0]))
    text = template.render(items=items)
    codecs.getwriter('utf-8')(sys.stdout).write(text)