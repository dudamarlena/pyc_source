# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/mount.py
# Compiled at: 2018-07-29 08:43:40
import os, six, docker_emperor.logger as logger
__all__ = [
 'run']

def run(root, *args, **kwargs):
    name = args[0].strip() if args else None
    if name:
        if name in root.project['mounting']:
            root.project.config['mounting'] = name
            logger.success('Mounting <b>%s</b> selected.' % root.mounting.name)
        else:
            logger.error('Mounting <b>%s</b> unknow.' % name)
            exit(1)
    else:

        def select_mounting_name():
            logger.ask(('Please select the <b>{}</b> mounting to work on').format(root.project.name))
            for i, m in enumerate(root.project['mounting']):
                logger.choice(('<b>{}</b>] {}').format(i + 1, m.name))

            mi = six.moves.input(': ')
            try:
                if mi == '0':
                    raise Exception
                return root.project['mounting'][(int(mi) - 1)].name
            except Exception as e:
                logger.error('<b>%s</b> is not a valid choice' % mi)
                return select_mounting_name()

        root.project.config['mounting'] = select_mounting_name()
        logger.success('Mounting <b>%s</b> selected.' % root.mounting.name)
    return