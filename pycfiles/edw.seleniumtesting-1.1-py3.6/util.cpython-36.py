# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/seleniumtesting/util.py
# Compiled at: 2018-04-25 12:33:40
# Size of source mod 2**32: 3147 bytes
from functools import partial
import argparse
from pkg_resources import iter_entry_points
from selenium import webdriver
DRIVERS = {'chrome':(
  webdriver.Chrome, webdriver.ChromeOptions), 
 'firefox':(
  webdriver.Firefox, webdriver.FirefoxOptions), 
 'phantomjs':(
  webdriver.PhantomJS, None), 
 'edge':(
  webdriver.Edge, None), 
 'ie':(
  webdriver.Ie, None), 
 'safari':(
  webdriver.Safari, None)}
MSG_UNKNOWN_TEST = 'Unknown test "{}"! Known tests: "{known_tests}"'
ARG_TESTS = {}
for entry_point in iter_entry_points(group='edw.seleniumtesting', name=None):
    ARG_TESTS[entry_point.name] = entry_point.load()

def get_browser(name, path=None, args=tuple()):
    browser, opts = DRIVERS[name]
    if opts:
        if args:
            options = opts()
            for arg in args:
                options.add_argument(arg)

            browser = partial(browser, options=options)
    if path:
        return browser(executable_path=path)
    else:
        return browser()


def validate_test_name(test_name):
    assert test_name in ARG_TESTS, MSG_UNKNOWN_TEST.format(test_name,
      known_tests=(', '.join(ARG_TESTS.keys())))


def build_cli_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run tests on websites.\nThe given browser webdriver must be in your $PATH\nor given via the --browserpath option.\n\nE.g.: chrome: chromedriver, firefox: geckodriver, edge: MicrosoftWebDriver.exe.')
    parser.add_argument('url',
      type=str, help='Site url, eg: https://digital-agenda-data.eu.')
    parser.add_argument('test',
      nargs='*', type=str, default=(ARG_TESTS.keys()), help=('Test names, one or more of: "{}". Default: all'.format(', '.join(ARG_TESTS.keys()))))
    parser.add_argument('-v', '--verbose', action='count', default=1)
    parser.add_argument('-B',
      '--browser', default='chrome', help=('Browser to use, known: "{}". Default: chrome'.format(', '.join(DRIVERS.keys()))))
    parser.add_argument('-P',
      '--browserpath', default=None, help='Custom path to browser executable.')
    parser.add_argument('-A',
      '--browserargs', nargs='*', default=[], help='Call browser with arguments. Only Chrome and Firefox supported.')
    parser.add_argument('-sw',
      '--screenwidth', default=1024, help='Screen width. Default: 1024.')
    parser.add_argument('-sh',
      '--screenheight', default=768, help='Screen height. Default: 768.')
    parser.add_argument('-ea',
      '--extra-arg', nargs='+', action='append', default=[], metavar='group key value', help="Extra arguments passed to suite.\nYou can use this to pass in user credentials or \nany other dynamic data that can't live with the test code.")
    parser.add_argument('--help-test',
      default=None, help='Shows the docstring of the specified test suite.')
    return parser