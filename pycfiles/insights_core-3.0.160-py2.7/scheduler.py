# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/scheduler.py
# Compiled at: 2019-05-16 13:41:33
from .. import parser, get_active_lines, Parser
import re
from insights.specs import Specs

@parser(Specs.scheduler)
class Scheduler(Parser):

    def parse_content(self, content):
        active_scheduler_regex = re.compile('\\[.*]')
        result = {}
        for line in get_active_lines(content):
            for sched in line.split():
                active_scheduler = active_scheduler_regex.search(sched)
                if active_scheduler:
                    result[self.file_path.split('/')[3]] = active_scheduler.group()

        self.data = result