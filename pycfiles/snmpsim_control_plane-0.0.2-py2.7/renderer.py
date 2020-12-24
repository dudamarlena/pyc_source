# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim_control_plane/management/exporters/renderer.py
# Compiled at: 2020-01-01 13:42:52
import os, stat, tempfile, jinja2

def render_configuration(dst_file, template, context):
    if os.path.exists(dst_file):
        os.unlink(dst_file)
    if not context:
        return
    search_path = [
     os.path.join(os.path.dirname(__file__), 'templates')]
    if os.path.sep in template:
        search_path.insert(0, os.path.dirname(template))
        template = os.path.basename(template)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(search_path), trim_blocks=True, lstrip_blocks=True)
    tmpl = env.get_template(template)
    text = tmpl.render(context=context)
    with tempfile.NamedTemporaryFile(dir=os.path.dirname(dst_file), mode='w', delete=False) as (fp):
        fp.write(text)
    os.rename(fp.name, dst_file)
    os.chmod(dst_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)