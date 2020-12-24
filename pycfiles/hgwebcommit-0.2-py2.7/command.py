# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/actions/command.py
# Compiled at: 2011-10-28 19:16:45
from flask import render_template, request, redirect, url_for, flash
from flaskext.babel import gettext
from hgwebcommit import app
from hgwebcommit.actions.base import BaseAction
from hgwebcommit.utils import exec_command, get_repo
from hgwebcommit.forms import ConfirmForm

class ExecuteCommandAction(BaseAction):
    """
    execute shell command action
    """

    def __init__(self, name, label, command, encoding=None, params=None):
        super(ExecuteCommandAction, self).__init__(name, label, params)
        self.command = command
        self.encoding = encoding or 'utf-8'

    def run(self, *args, **kwargs):
        repo = get_repo()
        form = ConfirmForm(request.form, prefix='action-', csrf_enabled=False)
        if form.validate():
            output = exec_command(self.command)
            app.logger.info('exec_command - %s [%s]' % (self.name, (' ').join(self.command)))
            if self.encoding:
                output = output.decode(self.encoding)
            if output:
                flash_message = output
            else:
                flash_message = gettext('"%(label)s" was executed.', label=self.label)
            flash(flash_message)
            return
        else:
            message = gettext('Execute "%(label)s"', label=self.label)
            form = ConfirmForm(None, confirm=1, prefix='action-', csrf_enabled=False)
            return render_template('actions/command.html', message=message, repository=repo, form=form, action_name=self.name)