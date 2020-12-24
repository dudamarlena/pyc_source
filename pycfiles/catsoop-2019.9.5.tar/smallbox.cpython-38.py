# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/smallbox/smallbox.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 2646 bytes
import collections.abc
defaults = {'csq_soln':'', 
 'csq_check_function':lambda sub, soln: sub.strip() == soln.strip(), 
 'csq_npoints':1, 
 'csq_msg_function':lambda sub, soln: '', 
 'csq_show_check':False}

def escape(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def total_points(**info):
    return info['csq_npoints']


def handle_submission(submissions, **info):
    check = info['csq_check_function']
    sub = submissions[info['csq_name']]
    soln = info['csq_soln']
    check_result = check(sub, soln)
    if isinstance(check_result, collections.abc.Mapping):
        score = check_result['score']
        msg = check_result['msg']
    else:
        if isinstance(check_result, collections.abc.Sequence):
            score, msg = check_result
        else:
            score = check_result
            mfunc = info['csq_msg_function']
            try:
                msg = mfunc(sub, soln)
            except:
                try:
                    msg = mfunc(sub)
                except:
                    msg = ''

            else:
                percent = float(score)
                if info['csq_show_check']:
                    if percent == 1.0:
                        response = '<img src="%s" />' % info['cs_check_image']
                    elif percent == 0.0:
                        response = '<img src="%s" />' % info['cs_cross_image']
                    else:
                        response = ''
                else:
                    response = ''
                response += msg
                return {'score':percent,  'msg':response}


def render_html(last_log, **info):
    if last_log is None:
        last_log = {}
    out = '<input type="text"'
    if info.get('csq_size', None) is not None:
        out += ' size="%s"' % info['csq_size']
    out += ' value="%s"' % escape(last_log.get(info['csq_name'], ''))
    out += ' name="%s"' % info['csq_name']
    out += ' id="%s"' % info['csq_name']
    return out + ' />'


def answer_display(**info):
    out = 'Solution: %s' % info['csq_soln']
    return out