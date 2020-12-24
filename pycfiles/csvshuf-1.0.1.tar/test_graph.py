# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ae/bzr/csvsee/tests/test_graph.py
# Compiled at: 2010-09-15 01:54:20
__doc__ = 'Unit tests for the csvsee.graph module\n'
import os, sys
from csvsee import graph, utils
from nose.tools import assert_raises
from . import data_dir, temp_filename

class TestGraph:

    @classmethod
    def setup_class(cls):
        cls.png_file = temp_filename('png')
        cls.csv_file = os.path.join(data_dir, 'response_time.csv')

    @classmethod
    def teardown_class(cls):
        os.unlink(cls.png_file)

    def test_graph_default(self):
        """Test the `Graph` class with default settings.
        """
        g = graph.Graph(self.csv_file)
        g['title'] = 'Default settings'
        g.generate()
        g.save(self.png_file)
        assert os.path.isfile(self.png_file)
        g.show()

    def test_graph_peak(self):
        """Test graphing of peak values.
        """
        g = graph.Graph(self.csv_file)
        g['peak'] = 3
        g['title'] = 'Peak values'
        g['ylabel'] = 'Response time'
        g['ymax'] = 2000
        g['truncate'] = 10
        g.generate()
        g.save(self.png_file)
        assert os.path.isfile(self.png_file)

    def test_graph_top(self):
        """Test graphing of top average values.
        """
        g = graph.Graph(self.csv_file)
        g['top'] = 3
        g['title'] = 'Top values'
        g['ylabel'] = 'Response time'
        g['ymax'] = 2000
        g['truncate'] = 10
        g.generate()
        g.save(self.png_file)
        assert os.path.isfile(self.png_file)

    def test_bad_extension(self):
        """Test saving to a filename with an unknown extension.
        """
        bad_ext = self.png_file + '.foo'
        g = graph.Graph(self.csv_file)
        assert_raises(ValueError, g.save, bad_ext)

    def test_bad_columns(self):
        """Test the use of bad column names.
        """
        g = graph.Graph(self.csv_file)
        g['x'] = 'Nonexistent column'
        assert_raises(utils.NoMatch, g.generate)