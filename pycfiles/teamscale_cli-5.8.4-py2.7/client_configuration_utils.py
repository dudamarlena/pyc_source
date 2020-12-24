# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/teamscale_precommit_client/client_configuration_utils.py
# Compiled at: 2020-04-21 02:31:18
from teamscale_client.teamscale_client_config import TeamscaleClientConfig

def get_teamscale_client_configuration(config_file):
    """Gets a Teamscale client configuration from the provided config file or a config file in the user's home dir
    or both combined. This allows users to separate their credentials (e.g. in their home dir) from the project specific
    configurations (e.g. in the repository roots).
    """
    local_teamscale_config = None
    teamscale_config_in_home_dir = None
    try:
        local_teamscale_config = TeamscaleClientConfig.from_config_file(config_file)
    except RuntimeError:
        pass

    try:
        teamscale_config_in_home_dir = TeamscaleClientConfig.from_config_file_in_home_dir()
    except RuntimeError:
        pass

    if local_teamscale_config:
        if not teamscale_config_in_home_dir:
            _require_sufficient_configuration(local_teamscale_config)
            return local_teamscale_config
        else:
            teamscale_config_in_home_dir.overwrite_with(local_teamscale_config)
            _require_sufficient_configuration(teamscale_config_in_home_dir)
            return teamscale_config_in_home_dir

    elif not teamscale_config_in_home_dir:
        raise RuntimeError('No valid configuration found.')
    else:
        _require_sufficient_configuration(teamscale_config_in_home_dir)
        return teamscale_config_in_home_dir
    return


def _require_sufficient_configuration(configuration):
    """Ensures the provided configuration is sufficient for precommit analysis."""
    if not configuration.is_sufficient(require_project_id=True):
        raise RuntimeError('Not all necessary parameters specified in configuration file %s' % configuration.config_file)