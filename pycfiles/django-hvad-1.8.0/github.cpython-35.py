# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/spectras/projects/hvad/django-hvad/docs/_ext/github.py
# Compiled at: 2017-02-18 14:03:18
# Size of source mod 2**32: 1128 bytes
from docutils import nodes
from docutils.parsers.rst.roles import set_classes
ISSUE_URL = 'https://github.com/{owner}/{repo}/issues/{num}'

def github_issue_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    try:
        issuenum = int(text)
        if issuenum <= 0:
            raise ValueError()
    except ValueError:
        msg = inliner.reporter.error('Issuse number must be a strictly positive integer. Number "%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return ([prb], [msg])

    ref = ISSUE_URL.format(owner=inliner.document.settings.env.config['github_owner'], repo=inliner.document.settings.env.config['github_repo'], num=issuenum)
    set_classes(options)
    node = nodes.reference(rawtext, '#%d' % issuenum, refuri=ref, **options)
    return ([node], [])


def setup(app):
    app.add_config_value('github_owner', None, 'html')
    app.add_config_value('github_repo', None, 'html')
    app.add_role('issue', github_issue_role)