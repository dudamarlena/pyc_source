# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/actions/commit.py
# Compiled at: 2011-10-28 19:16:45
from flask import render_template, request, redirect, url_for, flash
from flaskext.babel import gettext
from hgwebcommit import app
from hgwebcommit.actions.base import BaseAction
from hgwebcommit.utils import get_repo, operation_repo
from hgwebcommit.forms import ConfirmForm

class CommitAction(BaseAction):
    """
    commit action
    """

    def __init__(self, name, label, files, commit_message, params=None):
        super(CommitAction, self).__init__(name, label, params)
        self.files = files
        self.commit_message = commit_message

    def run(self, *args, **kwargs):
        repo = get_repo()
        form = ConfirmForm(request.form, prefix='action-', csrf_enabled=False)
        if form.validate():
            output = operation_repo(repo, 'commit', self.files, self.commit_message)
            app.logger.info('commit_action - %s [%s]' % (self.name, (', ').join(self.files)))
            flash_message = gettext('"%(label)s" was executed.', label=self.label)
            flash(flash_message)
            return
        else:
            message = gettext('Execute "%(label)s"', label=self.label)
            form = ConfirmForm(None, confirm=1, prefix='action-', csrf_enabled=False)
            return render_template('actions/commit.html', message=message, repository=repo, form=form, action_name=self.name)