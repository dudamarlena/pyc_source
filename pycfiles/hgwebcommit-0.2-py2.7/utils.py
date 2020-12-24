# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/utils.py
# Compiled at: 2011-10-28 19:16:45


def gethostname():
    import socket
    return socket.gethostname()


def exec_command(command):
    from subprocess import Popen, PIPE
    p = Popen(command, stdout=PIPE)
    return p.stdout.read()


def get_repo():
    from hgwebcommit import app
    from hgwebcommit.repository import get_repository
    return get_repository(path=app.config['HGWEBCOMMIT_REPOSITORY'], encoding=app.config['HGWEBCOMMIT_ENCODING'])


def operation_repo(repo, operation, files, commit_message=None):
    from flaskext.babel import gettext as _
    from hgwebcommit import app
    if operation == 'commit':
        repo.commit(files, commit_message)
        app.logger.info('commit - %s [%s]' % (commit_message, (', ').join(files)))
        return _('commited.')
    if operation == 'revert':
        repo.revert(files)
        app.logger.info('reverted - [%s]' % (', ').join(files))
        return _('reverted.')
    if operation == 'remove':
        repo.remove(files)
        app.logger.info('removed - [%s]' % (', ').join(files))
        return _('removed.')
    from flask import abort
    abort(400)