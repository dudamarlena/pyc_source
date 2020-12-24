# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chambeca/my_programs/Building/EQcorrscan/eqcorrscan/doc/_ext/obspydoc.py
# Compiled at: 2019-05-12 15:35:51
# Size of source mod 2**32: 1292 bytes
import re
from docutils import nodes

def post_process_html(app, pagename, templatename, context, doctree):
    try:
        context['body'] = context['body'].replace('&#8211;', '<span class="dash" />')
    except:
        pass

    return doctree and doctree.has_name('citations') or None
    body = re.sub('<td><table class="first last docutils citation" frame="void" id="(?P<tag>[A-Za-z0-9]+)" rules="none">\n<colgroup><col class="label" /><col /></colgroup>\n<tbody valign="top">\n<tr><td class="label">(?P<content>\\[[A-Za-z0-9]+\\])</td><td></td></tr>\n</tbody>\n</table>\n</td>', '<td id="\\g<tag>"><span class="label label-default">\\g<content></span></td>', context['body'])
    context['body'] = body


def make_images_responsive(app, doctree):
    """
    Add Bootstrap img-responsive class to images.
    """
    for fig in doctree.traverse(condition=(nodes.figure)):
        if 'thumbnail' in fig['classes']:
            continue
        for img in fig.traverse(condition=(nodes.image)):
            img['classes'].append('img-responsive')


def setup(app):
    app.connect('html-page-context', post_process_html)
    app.connect('doctree-read', make_images_responsive)