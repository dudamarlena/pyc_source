# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/multiexpression/multiexpression.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 5018 bytes
expression, _ = csm_tutor.question('expression')
defaults = dict(expression['defaults'])
defaults['csq_expressions'] = [('$x = ~$', ['2', '3']), ('$y = ~$', ['sqrt(2)'])]
defaults['csq_combine_results'] = lambda results: sum((any(i) for i in results)) / len(results)
total_points = expression['total_points']

def get_parsed_reps(submissions, **info):
    parser = expression['_get_parser'](info)
    funcs = dict(expression['default_funcs'])
    funcs.update(info.get('csq_funcs', {}))
    parsed = []
    for ix, (prompt, solutions) in enumerate(info['csq_expressions']):
        osub = sub = submissions.get('__%s_%04d' % (info['csq_name'], ix), '')
        fprompt = csm_language.source_transform_string(info, prompt)
        try:
            sub = parser.parse(sub)
            parsed.append('%s<br/><displaymath>%s</displaymath>' % (
             fprompt, expression['tree2tex'](info, funcs, sub)[0]))
        except:
            parsed.append('%s<br/><center><font color="red">Error: could not parse your expression <code>%s</code></font></center>' % (
             fprompt, repr(osub)))

    else:
        msg = '<div class="question">Your expressions were parsed as:<hr/>'
        msg += '<hr />'.join(parsed)
        return msg + '</div>'


checktext = 'Check Syntax'

def handle_check(submissions, **info):
    return get_parsed_reps(submissions, **info)


def handle_submission(submissions, **info):
    results = []
    parsed = []
    for ix, (prompt, solutions) in enumerate(info['csq_expressions']):
        sub = submissions.get('__%s_%04d' % (info['csq_name'], ix), '')
        this_question = []
        if not isinstance(solutions, list):
            solutions = [
             solutions]
        for soln in solutions:
            spoof = dict(info)
            spoof['csq_soln'] = [soln]
            this_question.append((expression['handle_submission'])({info['csq_name']: sub}, **spoof).get('score', 0.0))
        else:
            results.append(this_question)

    else:
        msg = get_parsed_reps(submissions, **info)
        score = info['csq_combine_results'](results)
        if isinstance(score, (list, tuple)):
            score, extra_msg = score
            msg = '%s<hr/>%s' % (msg, extra_msg)
        return {'score':score,  'msg':msg}


def escape(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def render_html(submissions, **info):
    submissions = submissions or {}
    out = '<table border="0">'
    for ix, (prompt, _) in enumerate(info['csq_expressions']):
        qbox_name = '__%s_%04d' % (info['csq_name'], ix)
        out += '<tr><td align="right">'
        out += csm_language.source_transform_string(info, prompt)
        out += '</td><td>'
        out += '<input type="text"'
        if info.get('csq_size', None) is not None:
            out += ' size="%s"' % info['csq_size']
        out += ' value="%s"' % escape(submissions.get(qbox_name, ''))
        out += ' name="%s"' % qbox_name
        out += ' id="%s"' % qbox_name
        out += ' /></td></tr>'
    else:
        return out + '</table>'


def answer_display(**info):
    custom_answer = info.get('csq_custom_answer_display', None)
    if custom_answer is not None:
        return custom_answer
    parser = expression['_get_parser'](info)
    out = ''
    funcs = dict(expression['default_funcs'])
    funcs.update(info.get('csq_funcs', {}))
    parsed = []
    for ix, (prompt, solutions) in enumerate(info['csq_expressions']):
        fprompt = csm_language.source_transform_string(info, prompt)
        if not isinstance(solutions, list):
            solutions = [
             solutions]
        for soln in solutions:
            try:
                soln = parser.parse(soln)
                parsed.append('%s<br/><displaymath>%s</displaymath>' % (
                 fprompt, expression['tree2tex'](info, funcs, soln)[0]))
            except:
                parsed.append('%s<br/><center><font color="red">Error: could not parse expression <code>%s</code></font></center>' % (
                 fprompt, repr(soln)))

        else:
            return '<hr/>'.join(parsed)