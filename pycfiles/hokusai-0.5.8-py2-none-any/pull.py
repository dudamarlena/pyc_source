# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/commands/pull.py
# Compiled at: 2019-10-09 12:07:43
import os
from hokusai.lib.command import command
from hokusai.lib.config import config
from hokusai.services.ecr import ECR
from hokusai.lib.common import print_green, shout
from hokusai.lib.exceptions import HokusaiError

@command()
def pull(tag, local_tag):
    ecr = ECR()
    if not ecr.project_repo_exists():
        raise HokusaiError('ECR repo %s does not exist... did you run `hokusai setup` for this project?' % config.project_name)
    shout(ecr.get_login(), mask=('^(docker login -u) .+ (-p) .+ (.+)$', '\\1 ****** \\2 ***** \\3'))
    shout('docker pull %s:%s' % (ecr.project_repo, tag))
    shout('docker tag %s:%s hokusai_%s:%s' % (ecr.project_repo, tag, config.project_name, local_tag))
    print_green('Pulled %s:%s to hokusai_%s:%s' % (ecr.project_repo, tag, config.project_name, local_tag), newline_after=True)