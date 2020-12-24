# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/docker-droplet/docker_droplet/tests/test_template.py
# Compiled at: 2020-02-14 12:39:23
# Size of source mod 2**32: 661 bytes
import unittest, pathlib
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

class TestTemplate(unittest.TestCase):

    def test_loader(self) -> None:
        directory = pathlib.Path('docker_droplet/terraform/').absolute()
        templateLoader = FileSystemLoader(searchpath=directory)
        templateEnv = Environment(loader=templateLoader)
        try:
            templateEnv.get_template('providers.jinja2')
            templateEnv.get_template('digitalocean.jinja2')
        except TemplateNotFound:
            self.fail('Jinja templates not found')


if __name__ == '__main__':
    unittest.main()