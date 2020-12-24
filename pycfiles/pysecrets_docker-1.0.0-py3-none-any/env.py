# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/env.py
# Compiled at: 2019-04-10 23:34:56
import os
from .helper import HOME
from .env_helper import append_line_if_not_exists, load_var_value_from_shell_script

class EnvSecret(object):
    """
    Allow to load secret information from environment variable.
    """
    pysecret_file = '.bashrc_pysecret'
    pysecret_script = os.path.join(HOME, pysecret_file)
    bashrc_script = os.path.join(HOME, '.bashrc')
    bash_profile_script = os.path.join(HOME, '.bash_profile')
    zshrc_script = os.path.join(HOME, '.zshrc')
    config_fish_script = os.path.join(HOME, '.config', 'fish', 'config.fish')

    def export_cmd_text(self, var, value):
        """
        create ``export VAR="VALUE"`` command text
        """
        return ('export {var}="{value}"').format(var=var, value=value)

    def set(self, var, value, temp=False):
        """
        Set value.

        :type var: str
        :param var:

        :type value: str
        :param value:

        :type temp: bool
        :param temp: if True, then will not write ``export var="value"`` to pysecret file.

        :return: None
        """
        os.environ[var] = str(value)
        if temp is False:
            append_line_if_not_exists(self.pysecret_script, self.export_cmd_text(var, value))

    @property
    def environ(self):
        return os.environ

    def get(self, var):
        """
        Get value.

        :type var: str
        :param var:

        :rtype: str
        :return:
        """
        return self.environ[var]

    def unset(self, var):
        raise NotImplementedError('not implemented yet!')

    @property
    def source_pysecret_command(self):
        return ('source ~/{}').format(self.pysecret_file)

    def apply_source_pysecret_to_bashrc(self):
        append_line_if_not_exists(self.bashrc_script, self.source_pysecret_command)

    def apply_source_pysecret_to_bash_profile(self):
        append_line_if_not_exists(self.bash_profile_script, self.source_pysecret_command)

    def apply_source_pysecret_to_zshrc(self):
        append_line_if_not_exists(self.zshrc_script, self.source_pysecret_command)

    def apply_source_pysecret_to_config_fish(self):
        append_line_if_not_exists(self.config_fish_script, self.source_pysecret_command)

    def load_pysecret_script(self):
        environ = load_var_value_from_shell_script(self.pysecret_script)
        for key, value in environ.items():
            os.environ[key] = value