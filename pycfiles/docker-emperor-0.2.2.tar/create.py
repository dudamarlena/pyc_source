# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/create.py
# Compiled at: 2019-06-13 09:31:55
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    name = args[0].strip() if args else None
    if name:
        args = list(args)
        args.pop(0)
        mounting = root.project['mounting'].get(name)
        if mounting:
            logger.success('Prepare mounting <b>%s</b> to be created.' % mounting.name)
        else:
            logger.error('Mounting <b>%s</b> unknow.' % name)
            exit(1)
    else:
        mounting = root.mounting
    if not mounting.is_localhost:
        root.run_command('remove', internal=True, *args)
        logger.cmd('Create machine <b>%s</b>' % (mounting.docker_machine_name,))
        logger.cmd('With driver <b>%s</b>' % (mounting.get_machine_driver(),))
        cmd = root.bash(mounting.docker_machine_bin, 'create', '--driver', mounting.get_machine_driver(), mounting.docker_machine_name, is_system=True, *args)
    else:
        logger.warning(mounting.LOCAL_MACHINE_WARNING)
    return