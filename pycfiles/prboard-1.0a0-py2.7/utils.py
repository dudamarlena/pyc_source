# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\prboard\utils.py
# Compiled at: 2016-04-23 11:15:18
import constants, settings, logging
log = logging.getLogger('')
colors = constants.Colors

def parse_pr_filters(filter_str):
    """
    Function to parse PR filter specified.
        "By PR Number ---->  num:123"
        "By PR Labels ---->  labels:label1;label2;label3"
        "By PR Title  ---->  title:pr_title   (wilcard match)"
        "By PR Title  ---->  etitle:pr_title  (exact match)"
        "By PR All    ---->  num:123,labels:label1;label2;label3,title:pr_title"

    Args:
        filter_str (str): Filter String to be parsed

    Returns:
        filters (list): List of filter objects

    """
    filter_mappings = constants.FILTER_COMMAND_MAPPING
    filts = filter(lambda x: x != '', filter_str.split(','))
    filter_objects = []
    for f in filts:
        try:
            cmd, value = f.split(':')
            if ';' in value:
                value = value.split(';')
            filter_class = filter_mappings[cmd]
            filter_objects.append(filter_class(filter_value=value))
        except (ValueError, KeyError):
            continue

    return filter_objects


def overload_settings_from_file():
    if not settings.PRBOARD_SETTINGS_FILE:
        return
    try:
        with open(settings.PRBOARD_SETTINGS_FILE, 'r') as (settings_file):
            for line in settings_file.read().splitlines():
                try:
                    config_name, config_value = line.split('=')
                    if config_name == 'PRBOARD_SETTINGS_FILE':
                        continue
                    setattr(settings, config_name, config_value)
                except ValueError:
                    continue

    except IOError as e:
        log.warning(('Unable to access settings file={}, error={}').format(settings.PRBOARD_SETTINGS_FILE, e.message))


class PrintPR(object):

    def __init__(self, pr, repo, detailed_mode=False, labels=[]):
        self.pr = pr
        self.repo = repo
        self.prnum = pr.number
        self.title = pr.title
        self.comments = pr.comments
        self.state = pr.state
        self.detailed_mode = detailed_mode
        self.html_url = pr.html_url
        self.milestone = colors.ENDC + colors.OKBLUE + pr.milestone + colors.ENDC if pr.milestone else colors.FAIL + 'No Milestone' + colors.ENDC
        self.assignee = colors.OKBLUE + pr.assignee + colors.ENDC if pr.assignee else colors.FAIL + 'Not Assigned' + colors.ENDC
        self.labels = colors.OKBLUE + (':').join(labels) + colors.ENDC if labels else colors.FAIL + 'No Labels' + colors.ENDC

    def print_output(self):
        if self.detailed_mode:
            self.print_detailed_output()
        else:
            self.print_summary()

    def print_summary(self):
        colors = constants.Colors
        print colors.BOLD + str(self.prnum).ljust(6) + ' ' + self.title[:50].ljust(50) + ' ' + colors.FAIL + str(self.comments) + (' comment(s) {}').format(self.html_url) + colors.ENDC + self.html_url

    def print_detailed_output(self):
        hindent = 4
        bindent = 11
        pr_header = ('{} {} (mile={},assigne={},lables={}) {}').format(str(self.prnum).ljust(6), self.title[:100], self.milestone, self.assignee, self.labels, self.html_url)
        print_header(pr_header, sep='', indent=hindent)
        if self.comments:
            for comment in self.pr.get_issue_comments():
                prefix = bindent * ' ' + colors.BOLD + ('{}@@{}:::').format(comment.user.login, str(comment.updated_at)).ljust(40) + colors.ENDC
                print prefix + comment.body + (' {}').format(comment.html_url)

        else:
            print bindent * ' ' + 'No comments'


def print_header(text, sep='=', indent=0):
    """

    Args:
        text:
        sep:

    Returns:

    """
    if sep:
        print sep * len(text)
    print indent * ' ' + colors.HEADER + text + colors.ENDC
    if sep:
        print sep * len(text)