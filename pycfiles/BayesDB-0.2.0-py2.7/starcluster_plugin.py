# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/starcluster_plugin.py
# Compiled at: 2015-02-12 15:25:14
import os
from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log
project_name = 'bayesdb'
repo_url = 'https://github.com/mit-probabilistic-computing-project/%s.git' % project_name
get_repo_dir = lambda user: os.path.join('/home', user, project_name)
get_setup_script = lambda user: os.path.join(get_repo_dir(user), 'setup.py')

class bayesdbSetup(ClusterSetup):

    def __init__(self):
        pass

    def run(self, nodes, master, user, user_shell, volumes):
        repo_dir = get_repo_dir(user)
        setup_script = get_setup_script(user)
        for node in nodes:
            log.info('Installing %s as root on %s' % (project_name, node.alias))
            cmd_strs = [
             'pip install pyparsing==2.0.1',
             'pip install patsy',
             'pip install statsmodels',
             'rm -rf %s' % repo_dir,
             'git clone %s %s' % (repo_url, repo_dir),
             'python %s develop' % setup_script,
             'chown -R %s %s' % (user, repo_dir)]
            for cmd_str in cmd_strs:
                node.ssh.execute(cmd_str + ' >out 2>err')

        for node in nodes:
            log.info('Setting up %s as %s on %s' % (project_name, user, node.alias))
            cmd_strs = [
             'mkdir -p ~/.matplotlib',
             'echo backend: Agg > ~/.matplotlib/matplotlibrc']
            for cmd_str in cmd_strs:
                node.shell(user=user, command=cmd_str)