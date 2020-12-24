# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddmonitoring/run.py
# Compiled at: 2019-12-01 10:12:02
# Size of source mod 2**32: 3325 bytes
import logging, sys, os, json, asyncio
from cliff.command import Command
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.screen import Screen
from asciimatics.renderers import FigletText, ColourImageFile
from asciimatics.effects import Print
from apscheduler.schedulers.background import BackgroundScheduler
import ddmonitoring.utils.start as start
from ddmonitoring.app.metrics_model import MetricsModel
from ddmonitoring.app.view import MonitorFrame
from ddmonitoring.utils.constants import DATA_INTERVAL_SHORT, DATA_INTERVAL_LONG

class Run(Command):
    __doc__ = '[Datadog Take Home Project] - Command to run the monitoring utility'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Run, self).get_parser(prog_name)
        parser.add_argument('input_file', nargs='?')
        return parser

    def take_action(self, parsed_args):
        user_data = {}
        if not parsed_args.input_file:
            self.log.warning('Please provide path to json input file as argument before running.                See ddmonitoring run --help for more instructions')
            return
        with open(parsed_args.input_file) as (input_file):
            user_data = json.load(input_file)
        if not start.validate_input(user_data, self.log):
            return
        scheduler = BackgroundScheduler()
        logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
        logging.getLogger('apscheduler').propagate = False
        model = MetricsModel(check_data=user_data, logger=(self.log))
        self.log.info('Making initial requests...')
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(start.populate_metrics_data(model, user_data))
        except KeyboardInterrupt:
            sys.exit(0)

        model.make_global_metrics(DATA_INTERVAL_SHORT)
        model.make_global_metrics(DATA_INTERVAL_LONG)
        start.setup_background_jobs(scheduler, model)
        scheduler.start()

        def display_ui(screen):
            if screen.width < 132 or screen.height < 30:
                effects = [
                 Print(screen, ColourImageFile(screen, (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dd.png')), (int(screen.height // 3 * 2.5)), uni=(screen.unicode_aware),
                   dither=(screen.unicode_aware)), 0),
                 Print(screen, (FigletText('Resize to 132x30+')),
                   y=(screen.height - 6))]
            else:
                effects = [MonitorFrame(screen, model)]
            screen.play([Scene(effects, -1)], stop_on_resize=True)

        while 1:
            try:
                Screen.wrapper(display_ui, catch_interrupt=False)
            except ResizeScreenError:
                pass
            except (KeyboardInterrupt, StopApplication):
                sys.exit(0)