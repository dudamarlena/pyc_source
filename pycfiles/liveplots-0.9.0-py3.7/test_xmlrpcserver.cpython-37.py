# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/liveplots/tests/test_xmlrpcserver.py
# Compiled at: 2019-11-08 08:17:51
# Size of source mod 2**32: 2982 bytes
from __future__ import absolute_import
from nose import SkipTest
from nose.tools import assert_equal
from liveplots.xmlrpcserver import rpc_plot
import six.moves.xmlrpc_client
from numpy import random

class TestRTplot:

    def setUp(self):
        port = rpc_plot(persist=0)
        self.r_tplot = six.moves.xmlrpc_client.ServerProxy('http://localhost:%s' % port)

    def test___init__(self):
        port = rpc_plot(persist=0)
        assert isinstance(port, int)

    def test_clearFig(self):
        assert_equal(0, self.r_tplot.clearFig())

    def test_close_plot(self):
        assert_equal(0, self.r_tplot.close_plot())

    def test_histogram(self):
        data = random.normal(0, 1, 1000).tolist()
        self.r_tplot.histogram(data, ['test'], 'test histogram')
        self.r_tplot.close_plot()

    def test_multiple_histogram(self):
        data = random.normal(0, 1, 1000).tolist()
        data2 = random.normal(3, 1, 1000).tolist()
        self.r_tplot.histogram([data, data2], ['test', 'test2'], 'Multiple histograms')
        self.r_tplot.close_plot()

    def test_multiple_histogram_multiplot(self):
        data = random.normal(0, 1, 1000).tolist()
        data2 = random.normal(3, 1, 1000).tolist()
        self.r_tplot.histogram([data, data2], ['test', 'test2'], 'Multiple histograms', 1)
        self.r_tplot.close_plot()

    def test_lines(self):
        data = [random.normal(0, 1, 1000).tolist() for i in range(4)]
        self.r_tplot.lines(data, [], ['a', 'b', 'c', 'd'], 'Test Lines', 'lines', 0)
        self.r_tplot.close_plot()

    def test_lines_multiplot(self):
        data = [random.normal(0, 1, 1000).tolist() for i in range(4)]
        self.r_tplot.lines(data, [], ['a', 'b', 'c', 'd'], 'test Lines - panel', 'lines', 1)
        self.r_tplot.close_plot()

    def test_scatter(self):
        data = random.normal(0, 1, 1000).tolist()
        data2 = random.normal(0, 2, 1000).tolist()
        self.r_tplot.scatter(data, data2, ['d1', 'd2'], 'test scatter')
        self.r_tplot.close_plot()

    @SkipTest
    def test_lines_and_dots(self):
        data = random.normal(0, 1, 1000).tolist()
        data2 = random.normal(0, 2, 1000).tolist()
        self.r_tplot.lines([data, data2], [], ['d1', 'd2'], 'Test different styles', ['lines', 'boxes'], 0)
        self.r_tplot.close_plot()


class TestStartServer:

    def test_start_server(self):
        raise SkipTest