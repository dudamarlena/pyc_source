# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/test/test_oozie2png.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 5404 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.oozie2png import convert_oozie_to_dot, convert_oozie_to_png
from vipe.common.utils import read_as_string
from vipe.graphviz.importance_score_map import DetailLevel
from vipe.graphviz.simplified_dot_graph.graph import SimplifiedDotGraph

class TestEndToEndGenerateImages:
    __doc__ = "Integration-like end-to-end tests.\n\n    The tests check if the whole processing path: from reading Oozie XML to\n    generating image file works at all. It's not checked whether a reasonable\n    output is generated.\n    "

    def test_complex_workflow(self):
        self._TestEndToEndGenerateImages__convert_to_images('../../examples/complex_workflow/workflow.xml')

    def test_iis_preprocessing_main_workflow(self):
        self._TestEndToEndGenerateImages__convert_to_images('../../examples/iis_workflows/preprocessing-main.xml')

    def test_iis_primary_main_workflow(self):
        self._TestEndToEndGenerateImages__convert_to_images('../../examples/iis_workflows/primary-main.xml')

    def test_iis_primary_processing_workflow(self):
        self._TestEndToEndGenerateImages__convert_to_images('../../examples/iis_workflows/primary-processing.xml')

    @staticmethod
    def __convert_to_images(oozie_file_path):
        oozie_xml = read_as_string(__name__, oozie_file_path)
        vertical_orientation = False
        show_input_ports = True
        show_output_ports = True
        for detail_level in DetailLevel:
            TestEndToEndGenerateImages._TestEndToEndGenerateImages__convert_to_image(oozie_file_path, oozie_xml, detail_level, show_input_ports, show_output_ports, vertical_orientation)

        detail_level = DetailLevel.highest
        show_input_ports = False
        show_output_ports = False
        TestEndToEndGenerateImages._TestEndToEndGenerateImages__convert_to_image(oozie_file_path, oozie_xml, detail_level, show_input_ports, show_output_ports, vertical_orientation)
        vertical_orientation = True
        TestEndToEndGenerateImages._TestEndToEndGenerateImages__convert_to_image(oozie_file_path, oozie_xml, detail_level, show_input_ports, show_output_ports, vertical_orientation)

    @staticmethod
    def __convert_to_image(oozie_file_path, oozie_xml, detail_level, show_input_ports, show_output_ports, vertical_orientation):
        try:
            convert_oozie_to_png(oozie_xml, detail_level, show_input_ports, show_output_ports, vertical_orientation)
        except:
            print('Error while processing file "{}" with detail_level="{}", show_input_ports="{}", show_output_ports="{}", vertical_orientation="{}"'.format(oozie_file_path, detail_level, show_input_ports, show_output_ports, vertical_orientation))
            raise


class TestEndToEndGenerateDot:
    __doc__ = 'Integration-like end-to-end tests of creating dot files.\n\n    The tests check if most of the processing path: from reading Oozie XML to\n    generating dot file works as expected.\n    '

    def test_complex_worfklow(self):
        oozie_xml_path = '../../examples/complex_workflow/workflow.xml'
        for path, detail_level in [
         (
          'data/complex-0_lowest_detail.dot', DetailLevel.lowest),
         (
          'data/complex-1_low_detail.dot', DetailLevel.low),
         (
          'data/complex-2_medium_detail.dot', DetailLevel.medium),
         (
          'data/complex-3_high_detail.dot', DetailLevel.high),
         (
          'data/complex-4_very_high_detail.dot', DetailLevel.very_high),
         (
          'data/complex-5_highest_detail.dot', DetailLevel.highest)]:
            self._TestEndToEndGenerateDot__check(path, oozie_xml_path, detail_level, True, True)

    @staticmethod
    def __check(expected_dot_path, oozie_xml_path, detail_level, show_input_ports=False, show_output_ports=False):
        actual_oozie_xml = read_as_string(__name__, oozie_xml_path)
        actual_dot = convert_oozie_to_dot(actual_oozie_xml, detail_level, show_input_ports, show_output_ports, True)
        actual = SimplifiedDotGraph.from_dot(actual_dot)
        expected_dot = read_as_string(__name__, expected_dot_path)
        expected = SimplifiedDotGraph.from_dot(expected_dot)
        @py_assert1 = expected == actual
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, actual)) % {'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual'}
            @py_format5 = (@pytest_ar._format_assertmsg('Problem when analyzing file "{}", namely: {} != {}'.format(expected_dot_path, expected, actual)) + '\n>assert %(py4)s') % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None