# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/richtext/richtext.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 2433 bytes
tutor.qtype_inherit('bigbox')
_base_render_html = render_html
_base_handle_submit = handle_submission
defaults.update({'csq_soln':'',  'csq_npoints':1,  'csq_show_check':False})

def markdownify(context, text):
    return context['csm_language']._md(text)


def richtext_format(context, text, msg='Preview:'):
    out = '</br>%s<br/>' % msg
    out += '<div style="background-color: #eeeeee;padding:10px; border-radius:10px;">'
    out += markdownify(context, text)
    out = out.replace('<script', '&lt;script')
    out = out.replace('</script', '&lt;script')
    out += '<script type="text/javascript">catsoop.render_all_math(document.getElementById("cs_qdiv_%s"), true);</script>' % context['csq_name']
    out += '</div>'
    return out


checktext = 'Preview'

def handle_check(submission, **info):
    last = submission.get(info['csq_name'])
    return richtext_format(info, last)


def handle_submission(submissions, **info):
    o = _base_handle_submit(submissions, **info)
    o['msg'] = o.get('msg', '') + richtext_format(info,
      (submissions[info['csq_name']]), msg='Submitted:')
    return o


def render_html(last_log, **info):
    out = _base_render_html(last_log, **info)
    help_url = '/'.join([info['cs_url_root'], '_qtype', 'richtext', 'formatting.html'])
    out += '<a onClick="window.open(\'%s\', \'_blank\', \'\');" style="cursor:pointer; cursor:hand;">Formatting Help</a>' % help_url
    return out


def answer_display(**info):
    out = '<b>Solution:</b><br/>&nbsp;<br/> %s' % info['csq_soln']
    return out