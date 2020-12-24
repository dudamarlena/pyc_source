# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-audiofield/audiofield/tasks.py
# Compiled at: 2016-03-01 06:04:56
from celery.utils.log import get_task_logger
from celery.decorators import task
import subprocess, os
from uuid import uuid1
logger = get_task_logger(__name__)
DELAY_TASK = 5

@task()
def audio_convert_task(conv):
    """Convert audio files"""
    logger.info('[audio_convert_task] Received a request to convert audio file in %dsecs' % DELAY_TASK)
    run_convert_task.apply_async((conv,), countdown=DELAY_TASK)
    return True


@task()
def run_convert_task(conv):
    """
    Exec the audio convert
    This version use Bash to convert the audio as calling Sox directly fails
    """
    filebash = '/tmp/bash-%s.sh' % str(uuid1())
    logger.warning('Convert audio file :> %s' % str(conv))
    logger.warning('Filebash :> %s' % filebash)
    filename = conv.split(' ')[1].strip()
    if os.path.isfile(filename):
        logger.debug('File exists!')
    else:
        logger.error("Error: File don't exist!")
        return False
    with open(filebash, 'w') as (mfile):
        mfile.write('#!/bin/bash\n')
        mfile.write(conv)
        mfile.write('\n')
    cmd = [
     'bash',
     filebash]
    response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = response.communicate()
    if error:
        logger.error('Error conversion : %s ' % error)
    return response


@task()
def old_run_convert_task(conv):
    """Exec the audio convert"""
    logger.warning('Convert audio file :> %s' % str(conv))
    filename = conv.split(' ')[1].strip()
    if os.path.isfile(filename):
        logger.debug('File exists!')
    else:
        logger.error("Error: File don't exist!")
    response = subprocess.Popen(conv.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = response.communicate()
    if error:
        logger.error('Conv :')
        logger.error(conv.split(' '))
        logger.error('Error conversion2 : %s ' % error)
    return response