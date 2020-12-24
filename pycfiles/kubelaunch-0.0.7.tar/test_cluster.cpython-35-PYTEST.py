# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jasonkuruzovich/githubdesktop/0_class/kubelaunch-cli/kubelaunch/notebooks/clusters/test_cluster.py
# Compiled at: 2017-12-25 23:44:08
# Size of source mod 2**32: 844 bytes
"""Tests for our `kubel cluster` subcommand."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from subprocess import PIPE, Popen as popen
from unittest import TestCase
import os

class TestCluster(TestCase):

    def test_returns_not_line(self):
        output = popen(['kubel', 'cluster', 'login', '--dry-run'], stdout=PIPE).communicate()[0]
        lines = output.decode('UTF-8').split('\n')
        print(lines)
        self.assertTrue(len(lines) > 1 and len(lines) < 7)

    def test_returns_adding_config(self):
        output = popen(['kubel', 'cluster', 'login', '--dry-run'], stdout=PIPE).communicate()[0]
        self.assertTrue('gcloud init' in output.decode('UTF-8'))