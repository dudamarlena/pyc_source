# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/all_pixel_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1210 bytes
"""
Test the all_pixel
"""
from ..drivers import ledtype
from ..util import log
from bibliopixel.animation.tests import StripChannelTest
from bibliopixel.layout.strip import Strip
from bibliopixel.drivers.serial import Serial
from bibliopixel.project.types import ledtype
DESCRIPTION = '\nEquivalent to\n\n.. code-block:: bash\n\n    bp --num=10 --loglevel=debug --animation=strip_test --driver=serial       --fail_on_exception --layout=strip --ledtype=<argument>\n\n'
LEDTYPES = '\nBiblioPixel currently understands the following types of LED strips:\n\n' + ', '.join(sorted(ledtype.LEDTYPE.__members__.keys()))
LEDTYPE_HELP = 'The type of the LED strip that is connected to your AllPixel\n' + LEDTYPES
NO_LED_ERROR = 'ERROR: No ledtype provided\n' + LEDTYPES

def run(args):
    if not args.ledtype:
        log.error(NO_LED_ERROR)
        return -1
    log.set_log_level('DEBUG')
    driver = Serial(ledtype=(ledtype.make(args.ledtype)), num=10)
    layout = Strip([driver])
    animation = StripChannelTest(layout)
    animation._set_runner(None)
    animation.start()


def add_arguments(args):
    args.set_defaults(run=run)
    args.add_argument('ledtype', help=LEDTYPE_HELP, nargs='?')