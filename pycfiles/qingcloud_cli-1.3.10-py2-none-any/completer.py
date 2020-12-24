# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/completer.py
# Compiled at: 2016-03-23 04:23:11
import sys
from .driver import get_valid_actions

def return_choices(choices):
    print ('\n').join(choices)
    sys.exit(0)


def return_no_choices():
    sys.exit(0)


def complete(cmdline, point):
    service_names = ('iaas', 'qs')
    service_name = None
    words = cmdline[0:point].split()
    if not words:
        return
    else:
        current_word = words[(-1)]
        non_options = [ w for w in words if not w.startswith('-') ]
        for w in non_options:
            if w in service_names:
                service_name = w

        if service_name:
            action_names = get_valid_actions(service_name)
            if current_word != service_name:
                action_names = [ act for act in action_names if act.startswith(current_word) ]
                if current_word in action_names and len(action_names) == 1:
                    return_no_choices()
            return_choices(action_names)
        else:
            closed_services = [ s for s in service_names if s.startswith(current_word) ]
            if not closed_services:
                closed_services = service_names
            return_choices(closed_services)
        return


if __name__ == '__main__':
    if len(sys.argv) == 3:
        complete(sys.argv[1], int(sys.argv[2]))
    else:
        print 'usage: %s <cmdline> <point>' % sys.argv[0]