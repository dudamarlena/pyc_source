# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_util/test_cli.py
# Compiled at: 2014-09-26 04:50:19
"""

  cli tests
  ~~~~~~~~~

  tests for canteen's data structures utilities.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
from canteen.util import cli
from canteen import FrameworkTest

class CLIToolsTests(FrameworkTest):
    """ Tests for `cli.Tool` """

    def test_construct(self):
        """ Test construction of a simple CLI tool """

        class Sample(cli.Tool):
            """ sample CLI tool """

            def execute(arguments):
                """ execution flow """
                pass

        assert isinstance(Sample.__dict__['execute'], staticmethod), 'by default tool execution methods should be static'
        return Sample

    def test_construct_subtool(self):
        """ Test construction of a CLI tool with subtools """

        class Sample(cli.Tool):
            """ sample CLI tool """

            class Subsample(cli.Tool):
                """ sub-sample CLI tool """

                @classmethod
                def execute(cls, arguments):
                    """ sample """
                    pass

        assert isinstance(Sample.Subsample.__dict__['execute'], classmethod), "classmethods should be allowed as tool execution flows, instead got '%s'" % repr(Sample.Subsample.execute)
        return Sample

    def test_construct_arguments(self):
        """ Test construction of a CLI tool with arguments without short options """

        class Sample(cli.Tool):
            """ sample CLI tool """
            arguments = (
             (
              '--debug', {'action': 'store_true'}),)

            class Subsample(cli.Tool):
                """ sub-sample CLI tool """

                def execute(arguments):
                    """ sample """
                    pass

        return Sample

    def test_construct_arguments_with_short(self):
        """ Test construction of a CLI tool with arguments with short options """

        class Sample(cli.Tool):
            """ sample CLI tool """
            arguments = (
             (
              '--debug', '-d', {'action': 'store_true'}),)

            class Subsample(cli.Tool):
                """ sub-sample CLI tool """

                def execute(arguments):
                    """ sample """
                    pass

        return Sample

    def test_initialize_clitool(self):
        """ Test initializing a CLI tool in various contexts without safe mode """
        self.test_construct()(autorun=False, safe=False)
        self.test_construct_subtool()(autorun=False, safe=False)
        self.test_construct_arguments()(autorun=False, safe=False)
        self.test_construct_arguments_with_short()(autorun=False, safe=False)

    def test_initialize_clitool_safe(self):
        """ Test initializing a CLI tool in various contexts with safe mode """
        self.test_construct()(autorun=False, safe=True)
        self.test_construct_subtool()(autorun=False, safe=True)
        self.test_construct_arguments()(autorun=False, safe=True)
        self.test_construct_arguments_with_short()(autorun=False, safe=True)