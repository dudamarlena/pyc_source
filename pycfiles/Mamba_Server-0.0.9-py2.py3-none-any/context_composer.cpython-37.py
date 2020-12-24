# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/context_composer.py
# Compiled at: 2020-05-13 09:17:59
# Size of source mod 2**32: 2434 bytes
import os, json, time
from mamba_server.context import Context
from mamba_server.utils.misc import get_component, get_components
from mamba_server.components.gui.load_screen.interface import LoadScreenInterface
from mamba_server.components.gui.main_window.interface import MainWindowInterface
from mamba_server.components.gui.plugins.interface import GuiPluginInterface

def execute(launch_file, mamba_dir):
    context = Context()
    context.set('mamba_dir', mamba_dir)
    with open(launch_file) as (f):
        launch_config = json.load(f)
        if 'load_screen' in launch_config:
            load_screen = get_component(launch_config['load_screen']['component'], 'mamba_server.components.gui.load_screen', LoadScreenInterface, context)
            load_screen.show()
            min_load_screen_time = None
            if 'min_seconds' in launch_config['load_screen']:
                min_load_screen_time = launch_config['load_screen']['min_seconds'] * 1000
                start_time = time.time()
        if 'app' in launch_config:
            main_window = get_component(launch_config['app']['component'], 'mamba_server.components.gui.main_window', MainWindowInterface, context)
            context.set('main_window', main_window)
        if 'gui_plugins' in launch_config:
            gui_plugins = get_components(launch_config['gui_plugins'], 'mamba_server.components.gui.plugins', GuiPluginInterface, context)
            context.set('gui_plugins', gui_plugins)
        if 'load_screen' in launch_config:
            if min_load_screen_time is not None:
                load_screen.after(min_load_screen_time - (time.time() - start_time), load_screen.close)
                load_screen.start_event_loop()
        if 'app' in launch_config:
            context.get('main_window').show()
            context.get('main_window').start_event_loop()


if __name__ == '__main__':
    execute(os.path.join('launch', 'default_qt.launch.json'))