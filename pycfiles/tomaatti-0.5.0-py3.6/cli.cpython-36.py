# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/cli.py
# Compiled at: 2018-10-05 03:47:17
# Size of source mod 2**32: 2070 bytes


def script_entry_point():
    from argparse import ArgumentParser
    from tomaatti import I3Integration, Tomaatti, ScreenOverlay
    argument_parser = ArgumentParser(description='Pomodoro timer for i3')
    argument_parser.add_argument('--screen-overlay', action='store_true', help='Show a full screen overlay (experimental)')
    argument_parser.add_argument('--blur-overlay', action='store_true', help='Blur the background of the screen overlay (experimental)')
    parsed_arguments = argument_parser.parse_args()
    if parsed_arguments.screen_overlay:
        if ScreenOverlay.is_coposite_manager_running():
            print('Showing screen overlay')
            overlay = ScreenOverlay()
            overlay.show_overlay('This is an experimental feature of Tomaatti')
        else:
            print('Composite manager is not running!')
        return
    app = Tomaatti()
    app.initialize()
    if I3Integration.get_clicked_button() == I3Integration.RIGHT_MOUSE_BUTTON:
        app.switch_mode()
    else:
        if I3Integration.get_clicked_button() == I3Integration.LEFT_MOUSE_BUTTON:
            app.toggle_timer()
    app.check_state()
    print(app.current_label)


if __name__ == '__main__':
    script_entry_point()