# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phenry/.config/i3/fluidspaces/src/fluidspaces/__main__.py
# Compiled at: 2017-10-25 04:10:39
# Size of source mod 2**32: 4082 bytes
"""Navigator for i3wm "named containers".

Create i3 workspaces with custom names on the fly, navigate between them based
on their their name or position, and move containers between them.
"""
import argparse, sys
from fluidspaces import i3Commands, MenuCommands, Workspaces, __version__

def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.set_defaults(action='go_to')
    send_actions = parser.add_mutually_exclusive_group(required=False)
    send_actions.add_argument('-b', '--bring-to', dest='action',
      action='store_const',
      const='bring_to',
      help='bring focused container with you to workspace')
    send_actions.add_argument('-s', '--send-to', dest='action',
      action='store_const',
      const='send_to',
      help='send focused container away to workspace')
    parser.add_argument('-m', '--menu', choices=[
     'dmenu', 'rofi'],
      default='dmenu',
      help='program used to render the menu (default: %(default)s)')
    parser.add_argument('-t', '--toggle', action='store_true',
      help='skip menu & choose workspace 2 (default: %(default)s)')
    parser.add_argument('-V', '--version', action='version',
      version=__version__)
    args = parser.parse_args()
    wps = Workspaces()
    wps.import_wps(i3Commands.get_wps_str())
    wps.export_wps()
    wps.import_wps(i3Commands.get_wps_str())
    if args.toggle:
        chosen_plain_name = '2:'
    else:
        prompts = {'go_to':'Go to workspace: ', 
         'send_to':'Send container to workspace: ', 
         'bring_to':'Bring container to workspace: '}
        menus = {'dmenu':[
          'dmenu'], 
         'rofi':[
          'rofi', '-dmenu', '-p', prompts[args.action]]}
        chosen_plain_name = MenuCommands.menu(menus[args.menu], wps.choices_str)
        if chosen_plain_name is None:
            sys.exit(0)
        chosen_wp = wps.get_wp(chosen_plain_name)
        if chosen_wp is None:
            chosen_wp_is_new = True
            chosen_i3_name = chosen_plain_name
        else:
            chosen_wp_is_new = False
            chosen_i3_name = chosen_wp.i3_name
        if args.action == 'send_to':
            i3Commands.send_to_wp(chosen_i3_name)
        else:
            if args.action == 'bring_to':
                i3Commands.send_to_wp(chosen_i3_name)
                i3Commands.go_to_wp(chosen_i3_name)
                if chosen_wp_is_new:
                    wps.import_wps(i3Commands.get_wps_str())
                wps.promote_wp(chosen_i3_name)
                wps.export_wps()
            elif args.action == 'go_to':
                i3Commands.go_to_wp(chosen_i3_name)
                if chosen_wp_is_new:
                    wps.import_wps(i3Commands.get_wps_str())
                wps.promote_wp(chosen_i3_name)
                wps.export_wps()


if __name__ == '__main__':
    main()