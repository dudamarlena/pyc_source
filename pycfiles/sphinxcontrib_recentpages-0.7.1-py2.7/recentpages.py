# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sphinxcontrib/recentpages.py
# Compiled at: 2012-12-17 09:49:43
"""
    sphinxcontrib.recentpages
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Build recent update pages list.

    :copyright: Copyright 2012 by Sho Shimauchi.
    :license: BSD, see LICENSE for details.
"""
from sphinx.util.compat import Directive
from docutils import nodes
import os, datetime, re

def setup(app):
    app.add_node(recentpages, html=(
     visit_html_recentpages, depart_recentpages))
    app.add_config_value('recentpages_sidebar', True, 'html')
    app.add_config_value('recentpages_sidebar_pages', 5, 'html')
    app.add_directive('recentpages', RecentpagesDirective)
    app.connect('env-updated', generate_template)
    app.connect('html-page-context', generate_recentpages_html)


class recentpages(nodes.General, nodes.Element):
    """Node for recentpages extention.
    """
    pass


class RecentpagesDirective(Directive):
    """
    Directive to display recent update pages list.
    """
    has_content = True
    option_spec = {'num': int}

    def run(self):
        env = self.state.document.settings.env
        env.note_reread()
        docpath = self.state.document.current_source
        srcdir = env.srcdir
        pagename = docpath.replace(srcdir, '').lstrip('/').rpartition('.')[0]
        num = self.options.get('num', -1)
        res = recentpages('')
        res['pagename'] = pagename
        res['num'] = num
        return [
         res]


def visit_html_recentpages(self, node):
    """visitor method for recentpages node
    """
    builder = self.builder
    env = self.builder.env
    file_list = _get_file_list_ordered_by_mtime(env)
    n = node['num']
    num = len(file_list) if n < 0 else n
    html_content = []
    for docname, mtime, title in file_list:
        pagename = node['pagename']
        relative_uri = builder.get_relative_uri(pagename, docname)
        html_content.append('%s - ' % datetime.datetime.fromtimestamp(mtime))
        html_content.append('<a href="%s">' % relative_uri)
        html_content.append('%s</a><br />' % title)
        num -= 1
        if num <= 0:
            break

    self.body += html_content
    raise nodes.SkipNode


def depart_recentpages(self, node):
    pass


def generate_recentpages_html(app, pagename, templatename, context, doctree):
    """generate recentpage sidebar parts.
    """
    if not app.builder.config.recentpages_sidebar:
        return
    context['recentpages_sidebar'] = True
    builder = app.builder
    env = app.builder.env
    num = app.builder.config.recentpages_sidebar_pages
    file_list = _get_file_list_ordered_by_mtime(env)
    html_content = []
    current_mday = ''
    for docname, mtime, title in file_list:
        relative_uri = builder.get_relative_uri(pagename, docname)
        mday = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        if current_mday != mday:
            current_mday = mday
            html_content.append('<b>%s</b><br />' % current_mday)
        html_content.append('<div style="margin-left:16px">')
        html_content.append('<a href="%s">' % relative_uri)
        html_content.append('%s</a><br />' % title)
        html_content.append('</div>')
        num -= 1
        if num <= 0:
            break

    context['recentpages_content'] = ('').join(html_content)


explicit_title_re = re.compile('^<(.*?)>(.+?)\\s*(?<!\\x00)<(.*?)>$', re.DOTALL)

def _get_file_list_ordered_by_mtime(env):
    res = []
    for docname in env.found_docs:
        abspath = env.doc2path(docname)
        mtime = os.path.getmtime(abspath)
        title = env.titles[docname]
        m = explicit_title_re.match(unicode(title))
        if m:
            title = m.group(2)
        else:
            title = None
        res.append((docname, mtime, title))

    res = list(set(res))
    res.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
    return res


def generate_template(app, env):
    """Generate recentpages.html template on update.
    This template is used in sidebar.
    """
    if not app.builder.config.recentpages_sidebar:
        return
    templates_path = app.builder.config.templates_path
    if len(templates_path) == 0:
        app.builder.warn('no templates directory')
        return
    srcdir = app.builder.srcdir
    template_dir = os.path.join(app.builder.srcdir, templates_path[0])
    if not os.path.exists(template_dir):
        app.builder.warn('%s does not exist' % (template_dir,))
        return
    target_path = os.path.join(template_dir, 'recentpages.html')
    if os.path.exists(target_path):
        return
    if not os.access(template_dir, os.W_OK):
        app.builder.warn('%s is not writable' % (template_dir,))
        return
    contents = '{#\n    recentpages.html\n    ~~~~~~~~~~~~~~~~\n\n    Sphinx sidebar template: recentpages\n\n    :copyright: Copyright 2012 by Sho Shimauchi.\n    :license: BSD, see LICENSE for details.\n#}\n{%- if recentpages_sidebar %}\n<h3>Recentpages</h3>\n{{ recentpages_content }}\n{%- endif %}\n'
    op = open(target_path, 'w')
    try:
        op.write(contents)
    finally:
        op.close()