# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/_ext/helpers.py
# Compiled at: 2017-07-29 15:15:55
import os, sys
PROJECTS = [
 ('common', 'SteelScript Common', '..'),
 ('netprofiler', 'SteelScript NetProfiler', '../../steelscript-netprofiler'),
 ('netshark', 'SteelScript NetShark', '../../steelscript-netshark'),
 ('appresponse', 'SteelScript AppResponse', '../../steelscript-appresponse'),
 ('wireshark', 'SteelScript WireShark', '../../steelscript-wireshark'),
 ('steelhead', 'SteelScript SteelHead', '../../steelscript-steelhead'),
 ('scc', 'SteelScript SteelCentral Controller', '../../steelscript-scc'),
 ('appfwk', 'SteelScript Application Framework', '../../steelscript-appfwk'),
 ('cmdline', 'SteelScript Command Line', '../../steelscript-cmdline'),
 ('vmconfig', 'SteelScript VM', '../../steelscript-vm-config'),
 ('reschema', 'reschema', '../../reschema'),
 ('sleepwalker', 'sleepwalker', '../../sleepwalker')]

def create_symlinks():
    for proj, title, path in PROJECTS:
        if proj == 'common':
            continue
        try:
            os.unlink(proj)
        except OSError:
            pass

        src = ('{path}/docs').format(path=path)
        if not os.path.exists(src):
            raise Exception('Could not find related project source tree: %s' % src)
        os.symlink(src, proj)


def write_toc_templates():
    if not os.path.exists('_templates'):
        os.mkdir('_templates')
    for proj, title, path in PROJECTS:
        tocfile = '%s_toc.html' % proj
        template_tocfile = '_templates/%s' % tocfile
        if not os.path.exists(template_tocfile):
            with open(template_tocfile, 'w') as (f):
                f.write(('{{%- if display_toc %}}\n  <h3><a href="{{{{ pathto(\'{proj}/overview.html\', 1) }}}}">{{{{ _(\'{title}\') }}}}</a></h3>\n  {{{{ toc }}}}\n{{%- endif %}}').format(proj=proj, title=title))


def setup_html_sidebards(html_sidebars):
    for proj, title, path in PROJECTS:
        tocfile = '%s_toc.html' % proj
        html_sidebars['%s/*' % proj] = [
         tocfile, 'relations.html', 'sourcelink.html',
         'searchbox.html', 'license.html']


def setup_sys_path():
    for proj, title, path in PROJECTS:
        if not os.path.exists(path):
            raise Exception('Could not find related project source tree: %s' % path)
        sys.path.insert(0, os.path.abspath(path))