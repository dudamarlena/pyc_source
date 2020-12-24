# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/rpc/preprocessors/press_static_assets/press_static_asset_preprocessor.py
# Compiled at: 2019-02-12 10:52:56
# Size of source mod 2**32: 2593 bytes
import pystache, yaml
from mercury.common.exceptions import MercuryUserError
from mercury.rpc.preprocessors import preprocessor

def __asset_list_hax(assets):
    """Converts any lists to a string so they can be properly rendered by pystache
    """
    for k, v in list(assets.items()):
        if isinstance(v, dict):
            __asset_list_hax(v)
        if isinstance(v, list):
            assets[k] = '[%s]' % ', '.join(v)


@preprocessor.preprocessor('press_static_assets', 'Uses user supplied assets to render press configuration templates')
def press_static_assets(target, instruction):
    """Uses a mercury_id indexed asset store which is supplied, in it's entirety, within the instruction
    :param target: A target containing a mercury_id
    :param instruction: A dictionary containing two fields, template and assets
        template is a string containing a yaml formatted press configuration mustache template
        assets is a dictionary indexed by mercury_id. Each value contains render information
        relevant to the template. If the asset data does not contain data for the target mercury_id
        a MercuryUserException exception is raised

        Note, this is throw away code. The mercury_assets backend will take over the functionality provided
        herein.
    :return: exec_press capability contract
    """
    template = '\n'.join(instruction.get('template'))
    asset_db = instruction.get('assets')
    if not template:
        if asset_db:
            raise MercuryUserError('Contract is incomplete')
    render_data = asset_db.get(target['mercury_id'])
    if not render_data:
        raise MercuryUserError('Assets supplied do not cover target')
    __asset_list_hax(render_data)
    rendered = (pystache.render)(template, **render_data)
    configuration = yaml.load(rendered)
    return {'method':'press', 
     'kwargs':{'configuration': configuration}}