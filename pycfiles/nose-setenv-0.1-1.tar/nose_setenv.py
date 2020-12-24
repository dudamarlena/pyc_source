# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mahmoud/code/nose-setenv/nose_setenv/nose_setenv.py
# Compiled at: 2012-02-15 01:10:15
from __future__ import unicode_literals
import ast, os, nose
from nose.plugins import Plugin

class SetEnvironmentVariables(Plugin):
    """
    This plugin is used to set environment variables to seamlessly integrate
    in the nosetests architecture.

    """
    enabled = True
    name = b'env-setter'

    def options(self, parser, env):
        super(SetEnvironmentVariables, self).options(parser, env=env)
        parser.add_option(b'--set-env-variables', dest=b'set_env_variables', default=None, help=b'The environment variables to set/override')
        return

    def configure(self, options, conf):
        super(SetEnvironmentVariables, self).configure(options, conf)
        if not options.set_env_variables:
            return
        env_variables_to_override = ast.literal_eval(options.set_env_variables)
        for env_key, env_val in env_variables_to_override.iteritems():
            os.environ[env_key] = env_val


if __name__ == b'__main__':
    nose.main(addplugins=[SetEnvironmentVariables()])