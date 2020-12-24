# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dsikora/www/docker-drupal-new/docker_console/bash_completion/__init__.py
# Compiled at: 2017-08-04 05:48:43
import os
from ..utils.aliases import __all__ as available_aliases

def get_available_commands():
    from docker_console.__main__ import build_arrays
    from copy import deepcopy
    build_arrays_cpy = deepcopy(build_arrays)
    del build_arrays_cpy['build-in-docker']
    return (' {0} ').format(('\n').join(build_arrays_cpy.keys()))


def get_commands_completion_functions():
    return '\n_docker_console_init() {\n\tcase "$cur" in\n\t\t-*)\n\t\t\tCOMPREPLY=( $( compgen -W "-f --force-replace-conf" -- "$cur" ) )\n\t\t\t;;\n\tesac\n}\n\n_docker_console_shell() {\n\tcase "$cur" in\n\t\t-*)\n\t\t\tCOMPREPLY=( $( compgen -W "-s --docker-shell-run -c --docker-container" -- "$cur" ) )\n\t\t\t;;\n\tesac\n}\n\n_docker_console_drush() {\n\tcase "$cur" in\n\t\t-*)\n\t\t\tCOMPREPLY=( $( compgen -W "-e --drush-eval-run" -- "$cur" ) )\n\t\t\t;;\n\tesac\n}\n'


def get_aliases():
    return (' {0} ').format(('\n').join('@%s' % alias for alias in available_aliases[:]))


def get_boolean_options():
    return '\n        -y\n    '


def get_options_with_args():
    return '\n        -p --docker-run-path\n        -s --docker-shell-run\n        -c --docker-container\n    '


def setup_autocomplete():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'bash_completion', 'template.sh'), 'rt') as (f):
            content = f.read()
            content = content.replace('{{commands_completion_functions}}', get_commands_completion_functions())
            content = content.replace('{{commands}}', get_available_commands())
            content = content.replace('{{global_aliases}}', get_aliases())
            content = content.replace('{{global_boolean_options}}', get_boolean_options())
            content = content.replace('{{global_options_with_args}}', get_options_with_args())
            with open('/tmp/bash_completion.tmp', 'wt') as (outf):
                outf.write(content)
            os.system('sudo mv /tmp/bash_completion.tmp /usr/share/bash-completion/completions/docker-console')
            os.system('sudo ln -sf /usr/share/bash-completion/completions/docker-console /usr/share/bash-completion/completions/dcon')
    except:
        pass