# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/ask/models/stata_functions.py
# Compiled at: 2014-08-27 19:26:12
from django.template.defaultfilters import slugify

def statify_label(text):
    text = slugify(text)
    for i in ['\n', '-']:
        text = text.replace(i, ' ')

    return text[:80]


def label_variable(question):
    return 'label variable %(var)s `"%(lab)s"\' \nnote %(var)s: `"%(full)s"\' ' % {'var': question.variable_name, 
       'lab': statify_label(question.text), 
       'full': (' ').join(question.text.splitlines())}


def label_choices(question):
    choicestring = (' ').join([ '%s `"%s"\' ' % (s, l) for s, l in question.choices() ])
    return 'label define %s %s ' % (question.variable_name, choicestring)


def label_choices_checkboxes(question):
    choicestring = (' ').join([ '%s `"%s"\' ' % (s, l) for s, l in question.choices() ])
    labelsstring = 'label define %s %s ' % (question.variable_name, choicestring)
    optionsstring = '\n    tostring %s, replace\n    split %s, p(",") destring gen(%s__ticked_)\n    foreach v of varlist `r(varlist)\' {\n        label variable `v\' `"%s"\'\n    }\n    ' % tuple([question.variable_name] * 4)
    return ('\n').join([labelsstring, optionsstring])


def set_format_time(question):
    """Times are exported as a CSV string of h:m:s and seconds since 00:00.

    Here we output stata syntax to split that string, and save and label the
    resulting 2 variables. """
    synt = '\n    tostring %(var)s, replace\n    split %(var)s, p(",") destring gen(%(var)s_split)\n    label variable %(var)s_split1 "%(lab)s as a string"\n    label variable %(var)s_split2 "%(lab)s as seconds since 00:00"\n    destring %(var)s_split2, replace\n    ' % {'var': question.variable_name, 'lab': statify_label(question.text)}
    return synt


def set_format_date(question):
    return '\ntostring %s, replace\ngen __tmpdate = date(%s,"YMD#")\ndrop %s\nrename __tmpdate %s\nformat %s %%td\n    ' % tuple([question.variable_name] * 5)


def set_format_datetime(question):
    return '\ngen double __%s = clock(%s,"YMD#hms#")\ndrop %s\nrename __%s %s\nformat %s %%tc\n    ' % tuple([question.variable_name] * 6)