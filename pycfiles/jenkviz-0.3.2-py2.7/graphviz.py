# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jenkviz/graphviz.py
# Compiled at: 2012-01-25 11:58:04
__author__ = 'Benoit Delbosc'
__copyright__ = 'Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>'
from commands import getstatusoutput
from datetime import timedelta

def graphviz(roots, svg_file):
    """Create a fpath svg from build tree."""
    root = roots[0]
    dot_file = svg_file.replace('.svg', '.dot')
    out = open(dot_file, 'w+')
    out.write('digraph g {\ngraph [rankdir=LR];\nnode [fontsize="16" shape="record"];\ninfo [label="start: %s|stop: %s|elapsed: %s|duration: %s|number of builds: %s|throughput: %.2f%%"];\n' % (root.extra['start'], root.extra['stop'], root.extra['elapsed'], timedelta(seconds=root.extra['duration']),
     root.extra['count'], root.extra['throughput']))
    visited = []
    for root in roots:
        _graphviz_recurse(root, out, visited)

    out.write('}\n')
    out.close()
    _make_svg(dot_file, svg_file)


def _graphviz_recurse(parent, out, visited):
    if parent.url in visited:
        return
    visited.append(parent.url)
    out.write('%s [label="%s #%s|%s %s|%s" color=%s URL="%s"]\n' % (
     parent.getId(), parent.name, parent.build_number, str(parent.start_t)[11:], parent.host, parent.duration,
     parent.color(), parent.full_url()))
    if parent.trigger:
        out.write('%s [color=orange style=filled]\n%s -> %s\n' % (
         parent.trigger, parent.trigger, parent.getId()))
    if not parent.children:
        return
    out.write('%s -> {' % parent.getId())
    for build in parent.children:
        if parent.url in build.get_upstream():
            out.write(build.getId() + ';')

    out.write('}\n')
    for build in parent.children:
        if parent.url not in build.get_upstream():
            out.write('%s -> %s [color=orange]\n' % (parent.getId(), build.getId()))

    for build in parent.children:
        _graphviz_recurse(build, out, visited)


def _make_svg(dot_file, svg_file):
    cmd = 'dot -Tsvg %s -o %s' % (dot_file, svg_file)
    ret, output = getstatusoutput(cmd)
    if ret != 0:
        raise RuntimeError('Failed to run dot cmd: ' + cmd + '\n' + str(output))