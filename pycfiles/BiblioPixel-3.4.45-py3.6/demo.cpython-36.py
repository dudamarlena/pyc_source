# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/demo.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2437 bytes
"""
Run a bibliopixel demo
"""
DESCRIPTION = '\nFor the list of possible demos, type\n\n.. code-block:: bash\n\n    bp demo list\n\n'
import random
from ..main import project_flags, demo_table
from ..project import project
from ..util import log
DEMO_OPTS = ', '.join(sorted(demo_table.DEMO_TABLE.keys()))

def make_runnable_animation(demo, args):
    if callable(demo):
        return demo(args).run
    else:
        if 'driver' in demo:
            if not demo['driver'].get('num'):
                if 'layout' in demo:
                    if demo['layout']['typename'] == 'cube':
                        demo['driver']['num'] = args.width * args.height * args.depth
                else:
                    demo['driver']['num'] = args.width * args.height
        if 'layout' in demo:
            layout = demo['layout']
            if 'width' in layout:
                layout['width'] = layout['width'] or args.width
            if 'x' in layout:
                layout['x'] = layout['x'] or args.width
            if 'height' in layout:
                layout['height'] = layout['height'] or args.height
            if 'y' in layout:
                layout['y'] = layout['y'] or args.height
            if 'z' in layout:
                layout['z'] = layout['z'] or args.depth
        project = project_flags.make_project(args, demo)
        return project.animation


def usage():
    log.printer('Available demos are: {}'.format(DEMO_OPTS))


def run(args):
    if args.name == 'list':
        usage()
        return
    else:
        args.simpixel = args.simpixel or True
        if not args.name:
            usage()
            args.name = random.choice(list(demo_table.DEMO_TABLE))
            log.printer('Randomly selected', args.name)
        try:
            demo = demo_table.DEMO_TABLE[args.name]
        except KeyError:
            raise KeyError('Unknown demo %s' % args.name)

    animation = make_runnable_animation(demo, args)
    animation.layout.start()
    animation.start()


def add_arguments(parser):
    parser.set_defaults(run=run)
    project_flags.add_arguments(parser)
    parser.add_argument('name',
      nargs='?', default='', help=('Name of demo to run. Options are: {}'.format(DEMO_OPTS)))
    parser.add_argument('--width',
      default=16, type=int, help='X dimension of display')
    parser.add_argument('--height',
      default=16, type=int, help='Y dimension of display')
    parser.add_argument('--depth',
      default=16, type=int, help='Z dimension of display. Only used for Cube demos.')