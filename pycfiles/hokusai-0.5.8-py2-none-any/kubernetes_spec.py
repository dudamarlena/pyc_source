# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/services/kubernetes_spec.py
# Compiled at: 2020-04-09 11:50:23
import os, yaml
from tempfile import NamedTemporaryFile
from hokusai.lib.config import config
from hokusai.lib.config_loader import ConfigLoader
from hokusai.lib.template_renderer import TemplateRenderer
from hokusai.lib.exceptions import HokusaiError
from hokusai.services.ecr import ECR

class KubernetesSpec(object):

    def __init__(self, kubernetes_yaml):
        self.kubernetes_yaml = kubernetes_yaml
        self.ecr = ECR()

    def to_string(self):
        template_config = {'project_name': config.project_name, 
           'project_repo': self.ecr.project_repo}
        if config.template_config_files:
            for template_config_file in config.template_config_files:
                config_loader = ConfigLoader(template_config_file)
                template_config.update(config_loader.load())

        rendered_template = TemplateRenderer(self.kubernetes_yaml, template_config).render()
        if os.environ.get('DEBUG'):
            print rendered_template
        return rendered_template

    def to_file(self):
        f = NamedTemporaryFile(delete=False)
        f.write(self.to_string())
        f.close()
        return f.name

    def to_list(self):
        return list(yaml.safe_load_all(self.to_string()))