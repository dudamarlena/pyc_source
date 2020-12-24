# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/bigbox/bigbox.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1554 bytes
smbox, _ = csm_tutor.question('smallbox')
defaults = dict(smbox['defaults'])
defaults.update({'csq_rows':10,  'csq_cols':60})

def escape(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


total_points = smbox['total_points']
answer_display = smbox['answer_display']
handle_submission = smbox['handle_submission']

def render_html(last_log, **info):
    if last_log is None:
        last_log = {}
    rows = info['csq_rows']
    cols = info['csq_cols']
    out = '<textarea rows="%d" cols="%d"' % (rows, cols)
    out += ' name="%s"' % info['csq_name']
    out += ' id="%s"' % info['csq_name']
    out += '>%s</textarea><br>' % escape(last_log.get(info['csq_name'], ''))
    return out