# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/fileupload/fileupload.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 4226 bytes
import os, json, base64, mimetypes
from urllib.parse import urlencode
tutor.qtype_inherit('smallbox')
base, _ = tutor.question('smallbox')
always_rerender = True
defaults.update({'csq_soln_filename':'solution.txt', 
 'csq_allow_save':False, 
 'csq_soln_type':'string', 
 'csq_extract_data':True})

def handle_submission(submissions, **info):
    o = {'score':None, 
     'msg':'',  'rerender':True}
    name = info['csq_name']
    ll = submissions.get(name, None)
    if ll is not None:
        fname, _ = ll
        if info['csq_extract_data']:
            submissions[name] = info['csm_loader'].get_file_data(info, submissions, name)
        o.update((base['handle_submission'])(submissions, **info))
    return o


def render_html(last_log, **info):
    name = info['csq_name']
    out = '<input type="file" style="display: none" id=%s name="%s" />' % (
     name,
     name)
    out += '<button class="btn btn-catsoop" id="%s_select_button">Select File</button>&nbsp;<tt><span id="%s_selected_file">No file selected</span></tt>' % (
     name, name)
    out += '<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ndocument.getElementById(\'%s_select_button\').addEventListener(\'click\', function (){\n    document.getElementById("%s").click();\n});\ndocument.getElementById(\'%s\').addEventListener(\'change\', function (){\n    document.getElementById(\'%s_selected_file\').innerText = document.getElementById(\'%s\').value;\n});\n// @license-end</script>' % (
     name, name, name, name, name)
    ll = last_log.get(name, None)
    if ll is not None:
        try:
            fname, loc = ll
            loc = os.path.basename(loc)
            if info['csm_cslog'].ENCRYPT_KEY is not None:
                seed = info['cs_path_info'][0] if info['cs_path_info'] else info['cs_path_info']
                _path = [info['csm_cslog']._e(i, repr(seed)) for i in info['cs_path_info']]
            else:
                _path = info['cs_path_info']
            qstring = urlencode({'path':json.dumps(_path),  'fname':loc})
            safe_fname = fname.replace('<', '').replace('>', '').replace('"', '').replace("'", '')
            out += '<br/>'
            out += '<a href="%s/_util/get_upload?%s" download="%s">Download Most Recent Submission</a>' % (
             info['cs_url_root'], qstring, safe_fname)
        except:
            pass

    return out


def answer_display(**info):
    name = info['csq_soln_filename']
    if info['csq_soln_type'] == 'string':
        data = csm_thirdparty.data_uri.DataURI.make('text/plain', None, True, info['csq_soln'])
    else:
        data = csm_thirdparty.data_uri.DataURI.from_file(info['csq_soln'])
        ext = mimetypes.guess_extension(data.mimetype) or '.txt'
        name = name.rsplit('.', 1) + ext
    return '<a href="%s" download="%s">Download Solution</a>' % (data, name)