# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_result.py
# Compiled at: 2019-11-28 13:06:29
from __future__ import absolute_import, division, print_function, unicode_literals
import glob, logging, sys, tempfile, unittest
sys.dont_write_bytecode = True
from benchexec.result import *
from benchexec.result import _PROP_CALL, _PROP_LABEL, _PROP_AUTOMATON, _PROP_DEREF, _PROP_FREE, _PROP_MEMTRACK, _PROP_MEMCLEANUP, _PROP_TERMINATION, _PROP_SAT, _SCORE_CORRECT_FALSE, _SCORE_CORRECT_TRUE, _SCORE_WRONG_TRUE, _SCORE_WRONG_FALSE, _PROP_OVERFLOW, _PROP_DEADLOCK, _PROP_MEMSAFETY, _MEMSAFETY_SUBPROPERTIES, _VALID_RESULTS_PER_PROPERTY

class TestResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        logging.disable(logging.CRITICAL)

    def setUp(self):
        self.addTypeEqualityFunc(Property, lambda a, b, msg=None: self.assertEqual(a.__dict__, b.__dict__, msg))
        return

    def expected_result(self, result, subcategory=None):
        return {b'dummy.prp': ExpectedResult(result, subcategory)}

    prop_call = Property(b'dummy.prp', True, True, _PROP_CALL, [])
    prop_deadlock = Property(b'dummy.prp', True, True, _PROP_DEADLOCK, [])
    prop_memcleanup = Property(b'dummy.prp', True, True, _PROP_MEMCLEANUP, [])
    prop_memsafety = Property(b'dummy.prp', True, True, _PROP_MEMSAFETY, list(_MEMSAFETY_SUBPROPERTIES))
    prop_overflow = Property(b'dummy.prp', True, True, _PROP_OVERFLOW, [])
    prop_termination = Property(b'dummy.prp', True, True, _PROP_TERMINATION, [])
    prop_sat = Property(b'dummy.prp', True, False, _PROP_SAT, [])

    def test_Property_from_names(self):
        for prop in _VALID_RESULTS_PER_PROPERTY.keys():
            self.assertEqual(Property(None, True, prop != _PROP_SAT, prop, None), Property.create_from_names([prop]))

        self.assertEqual(Property(None, True, True, _PROP_MEMSAFETY, list(_MEMSAFETY_SUBPROPERTIES)), Property.create_from_names(_MEMSAFETY_SUBPROPERTIES))
        self.assertEqual(Property(None, False, False, b'test prop', None), Property.create_from_names([b'test prop']))
        property_test_sets = [
         [
          b'test prop 1', b'test prop 2'],
         [
          _PROP_CALL, _PROP_TERMINATION],
         [
          _PROP_DEREF, _PROP_FREE]]
        for test_props in property_test_sets:
            self.assertEqual(Property(None, False, False, b'unknown property', list(test_props)), Property.create_from_names(test_props))

        return

    def test_Property_from_standard_file(self):
        property_files = glob.glob(os.path.join(os.path.dirname(__file__), b'../doc/properties/*.prp'))
        for property_file in property_files:
            name = os.path.splitext(os.path.basename(property_file))[0]
            is_svcomp = name not in {_PROP_SAT, _PROP_AUTOMATON}
            subproperties = [_PROP_FREE, _PROP_DEREF, _PROP_MEMTRACK] if name == _PROP_MEMSAFETY else None
            self.assertEqual(Property(property_file, True, is_svcomp, name, subproperties), Property.create(property_file, allow_unknown=False))

        return

    def _test_Property_from_file(self, content, is_svcomp):
        with tempfile.NamedTemporaryFile(mode=b'wt', prefix=b'BenchExec_test_result', suffix=b'.prp') as (temp_file):
            temp_file.write(content)
            temp_file.flush()
            filename = temp_file.name
            with self.assertRaisesRegex(BenchExecException, b'known property', msg=b'for property file with content\n' + content):
                Property.create(filename, allow_unknown=False)
            self.assertEqual(Property(filename=filename, is_well_known=False, is_svcomp=is_svcomp, name=os.path.splitext(os.path.basename(filename))[0], subproperties=None), Property.create(filename, allow_unknown=True), msg=b'different result for property file with content\n' + content)
        return

    def test_Property_from_non_standard_file(self):
        self._test_Property_from_file(b'test property', False)
        self._test_Property_from_file(b'CHECK( init(main()), LTL(G p) )', True)
        self._test_Property_from_file(b'CHECK( init(main()), LTL(G p) )\n\nCHECK( init(main()), LTL(F end) )', True)
        self._test_Property_from_file(b'CHECK( init(main()), LTL(G valid-free) )\nCHECK( init(main()), LTL(G valid-deref) )', True)
        self._test_Property_from_file(b'CHECK( init(main()), LTL(G valid-free) and LTL(G valid-deref) )', True)

    def test_Property_names(self):
        self.assertEqual(list(_MEMSAFETY_SUBPROPERTIES), self.prop_memsafety.names)
        self.assertEqual([_PROP_CALL], list(self.prop_call.names))
        self.assertEqual([_PROP_SAT], list(self.prop_sat.names))
        self.assertEqual([b'test'], Property(None, False, False, b'test', None).names)
        self.assertEqual([
         b'a', b'b'], Property(None, False, False, b'test', [b'a', b'b']).names)
        return

    def test_Property_max_score_not_available(self):
        self.assertEqual(0, self.prop_call.max_score(ExpectedResult(None, None)))
        self.assertEqual(0, self.prop_call.max_score(None))
        return

    def test_Property_max_score_smt(self):
        self.assertEqual(0, self.prop_sat.max_score(ExpectedResult(True, None)))
        self.assertEqual(0, self.prop_sat.max_score(ExpectedResult(False, None)))
        return

    def test_Property_max_score_svcomp(self):
        self.assertEqual(_SCORE_CORRECT_TRUE, self.prop_call.max_score(ExpectedResult(True, None)))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_call.max_score(ExpectedResult(False, None)))
        self.assertEqual(_SCORE_CORRECT_TRUE, self.prop_memsafety.max_score(ExpectedResult(True, None)))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_memsafety.max_score(ExpectedResult(False, None)))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_memsafety.max_score(ExpectedResult(False, _PROP_FREE)))
        return

    def test_Property_compute_score_not_available(self):
        self.assertEqual(0, self.prop_call.compute_score(CATEGORY_MISSING, RESULT_TRUE_PROP))
        self.assertEqual(0, self.prop_call.compute_score(CATEGORY_ERROR, RESULT_TRUE_PROP))
        self.assertEqual(0, self.prop_call.compute_score(CATEGORY_UNKNOWN, RESULT_TRUE_PROP))

    def test_Property_compute_score_smt(self):
        self.assertEqual(0, self.prop_sat.compute_score(CATEGORY_CORRECT, RESULT_SAT))
        self.assertEqual(0, self.prop_sat.compute_score(CATEGORY_WRONG, RESULT_SAT))

    def test_Property_compute_score_svcomp(self):
        self.assertEqual(_SCORE_CORRECT_TRUE, self.prop_call.compute_score(CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_call.compute_score(CATEGORY_CORRECT, RESULT_FALSE_REACH))
        self.assertEqual(_SCORE_CORRECT_TRUE, self.prop_memsafety.compute_score(CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_memsafety.compute_score(CATEGORY_CORRECT, RESULT_FALSE_MEMTRACK))
        self.assertEqual(_SCORE_CORRECT_TRUE, self.prop_termination.compute_score(CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_termination.compute_score(CATEGORY_CORRECT, RESULT_FALSE_TERMINATION))
        self.assertEqual(_SCORE_CORRECT_TRUE, self.prop_overflow.compute_score(CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_overflow.compute_score(CATEGORY_CORRECT, RESULT_FALSE_OVERFLOW))
        self.assertEqual(_SCORE_CORRECT_TRUE, self.prop_deadlock.compute_score(CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, self.prop_deadlock.compute_score(CATEGORY_CORRECT, RESULT_FALSE_DEADLOCK))
        self.assertEqual(_SCORE_WRONG_FALSE, self.prop_call.compute_score(CATEGORY_WRONG, RESULT_FALSE_REACH))
        self.assertEqual(_SCORE_WRONG_TRUE, self.prop_call.compute_score(CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, self.prop_memsafety.compute_score(CATEGORY_WRONG, RESULT_FALSE_MEMTRACK))
        self.assertEqual(_SCORE_WRONG_TRUE, self.prop_memsafety.compute_score(CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, self.prop_memsafety.compute_score(CATEGORY_WRONG, RESULT_FALSE_DEREF))
        self.assertEqual(_SCORE_WRONG_FALSE, self.prop_termination.compute_score(CATEGORY_WRONG, RESULT_FALSE_TERMINATION))
        self.assertEqual(_SCORE_WRONG_TRUE, self.prop_termination.compute_score(CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, self.prop_overflow.compute_score(CATEGORY_WRONG, RESULT_FALSE_OVERFLOW))
        self.assertEqual(_SCORE_WRONG_TRUE, self.prop_overflow.compute_score(CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, self.prop_deadlock.compute_score(CATEGORY_WRONG, RESULT_FALSE_OVERFLOW))
        self.assertEqual(_SCORE_WRONG_TRUE, self.prop_deadlock.compute_score(CATEGORY_WRONG, RESULT_TRUE_PROP))

    def test_score_for_task_no_score_available(self):
        self.assertEqual(0, score_for_task([_PROP_CALL], CATEGORY_MISSING, RESULT_TRUE_PROP))
        self.assertEqual(0, score_for_task([_PROP_CALL], CATEGORY_ERROR, RESULT_TRUE_PROP))
        self.assertEqual(0, score_for_task([_PROP_CALL], CATEGORY_UNKNOWN, RESULT_TRUE_PROP))

    def test_score_for_task_smt(self):
        self.assertEqual(None, score_for_task([_PROP_SAT], CATEGORY_CORRECT, RESULT_SAT))
        self.assertEqual(None, score_for_task([_PROP_SAT], CATEGORY_WRONG, RESULT_SAT))
        return

    def test_score_for_task_svcomp(self):
        self.assertEqual(_SCORE_CORRECT_TRUE, score_for_task([_PROP_CALL], CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, score_for_task([_PROP_CALL], CATEGORY_CORRECT, RESULT_FALSE_REACH))
        self.assertEqual(_SCORE_CORRECT_TRUE, score_for_task([
         _PROP_DEREF, _PROP_FREE, _PROP_MEMTRACK], CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, score_for_task([
         _PROP_DEREF, _PROP_FREE, _PROP_MEMTRACK], CATEGORY_CORRECT, RESULT_FALSE_MEMTRACK))
        self.assertEqual(_SCORE_CORRECT_TRUE, score_for_task([_PROP_TERMINATION], CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, score_for_task([
         _PROP_TERMINATION], CATEGORY_CORRECT, RESULT_FALSE_TERMINATION))
        self.assertEqual(_SCORE_CORRECT_TRUE, score_for_task([_PROP_OVERFLOW], CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, score_for_task([_PROP_OVERFLOW], CATEGORY_CORRECT, RESULT_FALSE_OVERFLOW))
        self.assertEqual(_SCORE_CORRECT_TRUE, score_for_task([_PROP_DEADLOCK], CATEGORY_CORRECT, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_CORRECT_FALSE, score_for_task([_PROP_DEADLOCK], CATEGORY_CORRECT, RESULT_FALSE_DEADLOCK))
        self.assertEqual(_SCORE_WRONG_FALSE, score_for_task([_PROP_CALL], CATEGORY_WRONG, RESULT_FALSE_REACH))
        self.assertEqual(_SCORE_WRONG_TRUE, score_for_task([_PROP_CALL], CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, score_for_task([
         _PROP_DEREF, _PROP_FREE, _PROP_MEMTRACK], CATEGORY_WRONG, RESULT_FALSE_MEMTRACK))
        self.assertEqual(_SCORE_WRONG_TRUE, score_for_task([
         _PROP_DEREF, _PROP_FREE, _PROP_MEMTRACK], CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, score_for_task([
         _PROP_DEREF, _PROP_FREE, _PROP_MEMTRACK], CATEGORY_WRONG, RESULT_FALSE_DEREF))
        self.assertEqual(_SCORE_WRONG_FALSE, score_for_task([
         _PROP_TERMINATION], CATEGORY_WRONG, RESULT_FALSE_TERMINATION))
        self.assertEqual(_SCORE_WRONG_TRUE, score_for_task([_PROP_TERMINATION], CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, score_for_task([_PROP_OVERFLOW], CATEGORY_WRONG, RESULT_FALSE_OVERFLOW))
        self.assertEqual(_SCORE_WRONG_TRUE, score_for_task([_PROP_OVERFLOW], CATEGORY_WRONG, RESULT_TRUE_PROP))
        self.assertEqual(_SCORE_WRONG_FALSE, score_for_task([_PROP_DEADLOCK], CATEGORY_WRONG, RESULT_FALSE_OVERFLOW))
        self.assertEqual(_SCORE_WRONG_TRUE, score_for_task([_PROP_DEADLOCK], CATEGORY_WRONG, RESULT_TRUE_PROP))

    def test_result_classification(self):
        self.assertEqual(RESULT_CLASS_TRUE, get_result_classification(RESULT_TRUE_PROP))
        self.assertEqual(RESULT_CLASS_TRUE, get_result_classification(RESULT_SAT))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_REACH))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_DEREF))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_FREE))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_MEMTRACK))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_TERMINATION))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_UNSAT))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_WITNESS_CONFIRMED))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_OVERFLOW))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_PROP))
        self.assertEqual(RESULT_CLASS_FALSE, get_result_classification(RESULT_FALSE_PROP + b'(test)'))
        self.assertEqual(RESULT_CLASS_OTHER, get_result_classification(RESULT_DONE))
        self.assertEqual(RESULT_CLASS_OTHER, get_result_classification(RESULT_UNKNOWN))
        self.assertEqual(RESULT_CLASS_OTHER, get_result_classification(b'KILLED'))
        self.assertEqual(RESULT_CLASS_OTHER, get_result_classification(b'TIMEOUT'))
        self.assertEqual(RESULT_CLASS_OTHER, get_result_classification(b''))

    def test_expected_results_of_file_SVCOMP(self):
        self.assertEqual({_PROP_CALL: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-unreach-call.c'))
        self.assertEqual({_PROP_CALL: ExpectedResult(False, None)}, expected_results_of_file(b'test_false-unreach-call.c'))
        self.assertEqual({_PROP_LABEL: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-unreach-label.c'))
        self.assertEqual({_PROP_LABEL: ExpectedResult(False, None)}, expected_results_of_file(b'test_false-unreach-label.c'))
        self.assertEqual({_PROP_DEADLOCK: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-no-deadlock.c'))
        self.assertEqual({_PROP_DEADLOCK: ExpectedResult(False, None)}, expected_results_of_file(b'test_false-no-deadlock.c'))
        self.assertEqual({_PROP_OVERFLOW: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-no-overflow.c'))
        self.assertEqual({_PROP_OVERFLOW: ExpectedResult(False, None)}, expected_results_of_file(b'test_false-no-overflow.c'))
        self.assertEqual({_PROP_TERMINATION: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-termination.c'))
        self.assertEqual({_PROP_TERMINATION: ExpectedResult(False, None)}, expected_results_of_file(b'test_false-termination.c'))
        self.assertEqual({_PROP_MEMCLEANUP: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-valid-memcleanup.c'))
        self.assertEqual({_PROP_MEMCLEANUP: ExpectedResult(False, None)}, expected_results_of_file(b'test_false-valid-memcleanup.c'))
        return

    def test_expected_results_of_file_SVCOMP_memsafety(self):
        self.assertEqual({_PROP_MEMSAFETY: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-valid-memsafety.c'))
        self.assertEqual({_PROP_DEREF: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-valid-deref.c'))
        self.assertEqual({_PROP_MEMSAFETY: ExpectedResult(False, _PROP_DEREF)}, expected_results_of_file(b'test_false-valid-deref.c'))
        self.assertEqual({_PROP_FREE: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-valid-free.c'))
        self.assertEqual({_PROP_MEMSAFETY: ExpectedResult(False, _PROP_FREE)}, expected_results_of_file(b'test_false-valid-free.c'))
        self.assertEqual({_PROP_MEMTRACK: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-valid-memtrack.c'))
        self.assertEqual({_PROP_MEMSAFETY: ExpectedResult(False, _PROP_MEMTRACK)}, expected_results_of_file(b'test_false-valid-memtrack.c'))
        return

    def test_expected_results_of_file_no_SVCOMP(self):
        self.assertEqual({_PROP_SAT: ExpectedResult(True, None)}, expected_results_of_file(b'test_sat.c'))
        self.assertEqual({_PROP_SAT: ExpectedResult(False, None)}, expected_results_of_file(b'test_unsat.c'))
        return

    def test_expected_results_of_file_several_properties(self):
        self.assertEqual({_PROP_CALL: ExpectedResult(True, None), 
           _PROP_TERMINATION: ExpectedResult(False, None), 
           _PROP_OVERFLOW: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-no-overflow_true-unreach-call_false-termination.c'))
        self.assertEqual({_PROP_MEMSAFETY: ExpectedResult(True, None), 
           _PROP_MEMCLEANUP: ExpectedResult(False, None)}, expected_results_of_file(b'test_true-valid-memsafety_false-valid-memcleanup.c'))
        self.assertEqual({_PROP_MEMSAFETY: ExpectedResult(False, b'valid-memtrack'), 
           _PROP_MEMCLEANUP: ExpectedResult(False, None), 
           _PROP_CALL: ExpectedResult(True, None)}, expected_results_of_file(b'test_true-unreach-call_false-valid-memtrack_false-valid-memcleanup.c'))
        return

    def test_result_category_true(self):
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False, b'valid-memtrack'), RESULT_TRUE_PROP, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [self.prop_memcleanup]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, [self.prop_memcleanup]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_SAT, [self.prop_sat]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False), RESULT_SAT, [self.prop_sat]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [self.prop_overflow]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, [self.prop_overflow]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, [self.prop_deadlock]))
        test_prop = Property(b'dummy.prp', False, True, b'test prop', None)
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [test_prop]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, [test_prop]))
        test_prop = Property(b'dummy.prp', False, True, b'test prop', [b'a', b'b', b'c'])
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, [test_prop]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False, b'a'), RESULT_TRUE_PROP, [test_prop]))
        return

    def test_result_category_false(self):
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_REACH, [self.prop_call]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_REACH, [self.prop_call]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_DEREF, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_FREE, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_MEMTRACK, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False, b'valid-deref'), RESULT_FALSE_DEREF, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False, b'valid-free'), RESULT_FALSE_FREE, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False, b'valid-memtrack'), RESULT_FALSE_MEMTRACK, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False, b'valid-deref'), RESULT_FALSE_FREE, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False, b'valid-free'), RESULT_FALSE_MEMTRACK, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(False, b'valid-memtrack'), RESULT_FALSE_DEREF, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_TERMINATION, [
         self.prop_termination]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_TERMINATION, [
         self.prop_termination]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_UNSAT, [self.prop_sat]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_UNSAT, [self.prop_sat]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_OVERFLOW, [self.prop_overflow]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_OVERFLOW, [self.prop_overflow]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_DEADLOCK, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_DEADLOCK, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [self.prop_overflow]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_PROP, [self.prop_overflow]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_PROP, [self.prop_deadlock]))
        test_prop = Property(b'dummy.prp', False, True, b'test prop', None)
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [test_prop]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_PROP, [test_prop]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False), RESULT_FALSE_PROP + b'(a)', [test_prop]))
        test_prop = Property(b'dummy.prp', False, True, b'test prop', [b'a', b'b', b'c'])
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [test_prop]))
        self.assertEqual(CATEGORY_WRONG, get_result_category(self.expected_result(True), RESULT_FALSE_PROP + b'(a)', [test_prop]))
        self.assertEqual(CATEGORY_CORRECT, get_result_category(self.expected_result(False, b'a'), RESULT_FALSE_PROP + b'(a)', [test_prop]))
        return

    def test_result_category_different_false_result(self):
        expected_result_false = self.expected_result(False)
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_DEREF, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_TERMINATION, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_UNSAT, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_OVERFLOW, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_REACH, [self.prop_termination]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_DEREF, [self.prop_termination]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_UNSAT, [self.prop_termination]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_OVERFLOW, [self.prop_termination]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_REACH, [self.prop_sat]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_DEREF, [self.prop_sat]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_TERMINATION, [self.prop_sat]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_OVERFLOW, [self.prop_sat]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [self.prop_sat]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_PROP, [self.prop_sat]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_REACH, [self.prop_overflow]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_DEREF, [self.prop_overflow]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_TERMINATION, [self.prop_overflow]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_UNSAT, [self.prop_overflow]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_REACH, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_DEREF, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_FALSE_TERMINATION, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_false, RESULT_UNSAT, [self.prop_deadlock]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(True), RESULT_FALSE_OVERFLOW, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(True), RESULT_FALSE_REACH, [self.prop_termination]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(True), RESULT_FALSE_PROP, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(False, b'valid-deref'), RESULT_FALSE_PROP, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(False, b'valid-free'), RESULT_FALSE_PROP, [
         self.prop_memsafety]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(False, b'valid-memtrack'), RESULT_FALSE_PROP, [
         self.prop_memsafety]))
        test_prop = Property(b'dummy.prp', False, True, b'test prop', [b'a', b'b', b'c'])
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(False, b'a'), RESULT_FALSE_PROP, [test_prop]))

    def test_result_category_different_true_result(self):
        expected_result_true = self.expected_result(True)
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_true, RESULT_SAT, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(expected_result_true, RESULT_TRUE_PROP, [self.prop_sat]))

    def test_result_category_no_property(self):
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(False, b'valid-memtrack.c'), RESULT_TRUE_PROP, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(True), RESULT_SAT, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(False), RESULT_SAT, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(True), RESULT_TRUE_PROP, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(False), RESULT_TRUE_PROP, []))

    def test_result_category_no_expected_result(self):
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_TRUE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_FALSE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_TRUE_PROP, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_FALSE_FREE, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_TRUE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_FALSE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_SAT, [self.prop_sat]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_UNSAT, [self.prop_sat]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_TRUE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_FALSE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_TRUE_PROP, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_FALSE_FREE, [self.prop_memsafety]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_TRUE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_FALSE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_SAT, [self.prop_sat]))
        self.assertEqual(CATEGORY_MISSING, get_result_category({}, RESULT_UNSAT, [self.prop_sat]))
        return

    def test_result_category_different_property(self):

        def other_expected_result(result, subcategory=None):
            return {b'different-file.prp': ExpectedResult(result, subcategory)}

        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(True), RESULT_TRUE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(False), RESULT_TRUE_PROP, [self.prop_termination]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(True), RESULT_TRUE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(False, b'valid-memtrack'), RESULT_TRUE_PROP, [
         self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(True), RESULT_TRUE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(False), RESULT_TRUE_PROP, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(True), RESULT_SAT, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(other_expected_result(False), RESULT_SAT, [self.prop_call]))
        return

    def test_result_category_other(self):
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(True), RESULT_DONE, [self.prop_call]))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(True), RESULT_DONE, []))
        self.assertEqual(CATEGORY_MISSING, get_result_category(self.expected_result(None), RESULT_DONE, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(True), RESULT_UNKNOWN, [self.prop_call]))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(True), RESULT_UNKNOWN, []))
        self.assertEqual(CATEGORY_UNKNOWN, get_result_category(self.expected_result(None), RESULT_UNKNOWN, [self.prop_call]))
        self.assertEqual(CATEGORY_ERROR, get_result_category(self.expected_result(True), b'KILLED', [self.prop_call]))
        self.assertEqual(CATEGORY_ERROR, get_result_category(self.expected_result(True), b'TIMEOUT', [self.prop_call]))
        self.assertEqual(CATEGORY_ERROR, get_result_category(self.expected_result(True), b'', [self.prop_call]))
        return