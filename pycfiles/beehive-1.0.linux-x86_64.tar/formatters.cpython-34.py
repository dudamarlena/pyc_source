# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/formatters.py
# Compiled at: 2014-10-30 08:03:31
# Size of source mod 2**32: 3343 bytes
import sys
from beehive.formatter.base import StreamOpener
from beehive.textutil import compute_words_maxsize
from beehive.formatter.plain import PlainFormatter
from beehive.formatter.pretty import PrettyFormatter
from beehive.formatter.json import JSONFormatter, PrettyJSONFormatter
from beehive.formatter.null import NullFormatter
from beehive.formatter.html import HTMLFormatter
from beehive.formatter.progress import ScenarioProgressFormatter, StepProgressFormatter, ScenarioStepProgressFormatter
from beehive.formatter.rerun import RerunFormatter
from beehive.formatter.tags import TagsFormatter, TagsLocationFormatter
from beehive.formatter.steps import StepsFormatter, StepsDocFormatter, StepsUsageFormatter
from beehive.formatter.sphinx_steps import SphinxStepsFormatter
formatters = {}

def register_as(formatter_class, name):
    """
    Register formatter class with given name.

    :param formatter_class:  Formatter class to register.
    :param name:  Name for this formatter (as identifier).
    """
    formatters[name] = formatter_class


def register(formatter_class):
    register_as(formatter_class, formatter_class.name)


def list_formatters(stream):
    """
    Writes a list of the available formatters and their description to stream.

    :param stream:  Output stream to use.
    """
    formatter_names = sorted(formatters)
    column_size = compute_words_maxsize(formatter_names)
    schema = '  %-' + str(column_size) + 's  %s\n'
    for name in formatter_names:
        stream.write(schema % (name, formatters[name].description))


def get_formatter(config, stream_openers):
    default_stream_opener = StreamOpener(stream=sys.stdout)
    formatter_list = []
    for i, name in enumerate(config.format):
        stream_opener = default_stream_opener
        if i < len(stream_openers):
            stream_opener = stream_openers[i]
        formatter_list.append(formatters[name](stream_opener, config))

    return formatter_list


def setup_formatters():
    formatters['plain'] = PlainFormatter
    formatters['pretty'] = PrettyFormatter
    formatters['json'] = JSONFormatter
    formatters['json.pretty'] = PrettyJSONFormatter
    formatters['null'] = NullFormatter
    formatters['progress'] = ScenarioProgressFormatter
    formatters['progress2'] = StepProgressFormatter
    formatters['progress3'] = ScenarioStepProgressFormatter
    formatters['rerun'] = RerunFormatter
    formatters['tags'] = TagsFormatter
    formatters['tags.location'] = TagsLocationFormatter
    formatters['steps'] = StepsFormatter
    formatters['steps.doc'] = StepsDocFormatter
    formatters['steps.usage'] = StepsUsageFormatter
    formatters['sphinx.steps'] = SphinxStepsFormatter
    formatters['html'] = HTMLFormatter


setup_formatters()