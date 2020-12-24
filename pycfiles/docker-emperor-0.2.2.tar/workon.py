# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/workon.py
# Compiled at: 2018-07-18 08:56:40
import os, six, docker_emperor.logger as logger
__all__ = [
 'run']

def run(root, *args, **kwargs):
    project = None
    project_name = args[0] if len(args) else None
    if project_name:
        project = root.projects.get(project_name)
        if not project:
            logger.warning('Project <b>%s</b> unknow.' % project_name)
    if not project:

        def select_project():
            logger.ask('Select the project to work on')
            for i, p in enumerate(root.projects.items()):
                key, value = p
                logger.choice(('<b>{}]</b> {}').format(i + 1, key))

            pi = six.moves.input(': ')
            try:
                if pi == '0':
                    raise Exception
                return root.projects.items()[(int(pi) - 1)]
            except Exception as e:
                logger.error(('{} is not a valid choice').format(pi))
                return select_project()

        project_name, project = select_project()
    if project:
        workdir = project.get('workdir')
        if workdir and os.path.isdir(workdir):
            logger.success('Workon the project <b>%s</b> in <b>%s</b>' % (project_name, workdir))
            os.chdir(workdir)
            shell = os.environ.get('SHELL', '/bin/sh')
            os.execl(shell, shell)
            return
    return