# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/seleniumtesting/main.py
# Compiled at: 2018-04-25 12:34:24
# Size of source mod 2**32: 1447 bytes
import unittest
from collections import defaultdict
from edw.seleniumtesting import common
from edw.seleniumtesting import util

def run(base_url, suite, resolution=(1024, 768), verbosity=1, browser='chrome', browser_path=None, browser_args=tuple(), extra_args={}):
    browser = util.get_browser(browser, browser_path, browser_args)
    (browser.set_window_size)(*resolution)
    test_runner = unittest.TextTestRunner(verbosity=verbosity,
      resultclass=(common.BrowserTestResult))
    test_suite = suite(browser, base_url, extra_args)
    test_runner.run(test_suite)
    browser.quit()


def run_cli():
    parser = util.build_cli_arguments()
    args = parser.parse_args()
    if args.help_test is not None:
        return print(util.ARG_TESTS[args.help_test].__doc__)
    extra_args = defaultdict(dict)
    for group, key, value in args.extra_arg:
        extra_args[group][key] = value

    for test_name in args.test:
        util.validate_test_name(test_name)
        suite = util.ARG_TESTS[test_name]
        run(base_url=(args.url), suite=suite,
          resolution=(
         args.screenwidth, args.screenheight),
          verbosity=(args.verbose),
          browser=(args.browser),
          browser_path=(args.browserpath),
          browser_args=(tuple(args.browserargs)),
          extra_args=extra_args)


if __name__ == '__main__':
    run_cli()