# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/unit/test_query_signature_analyze.py
# Compiled at: 2020-01-07 01:20:05
# Size of source mod 2**32: 13411 bytes
from unittest import TestCase
from django_query_profiler.query_profiler_storage import QuerySignature, QuerySignatureAnalyzeResult, StackTraceElement
from django_query_profiler.query_profiler_storage.django_stack_trace_analyze import _parse_sql_for_tables_and_eq

class QuerySignatureAnalyzeTest(TestCase):
    __doc__ = ' Contains Test cases from real django queries executed, with django_stack_trace '

    def test_filter_exists(self):
        query_without_params = '\n            SELECT (1) AS a FROM company_health_enrollment\n            WHERE (company_health_enrollment.lineOfCoverage = %s AND company_health_enrollment.company_id = %s\n                AND company_health_enrollment.isActive = %s AND company_health_enrollment.isEnrollmentComplete = %s)\n            LIMIT 1\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['company_health_enrollment'])
        self.assertEqual(where_equality_key, '')
        django_stack_trace = (
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'has_results', None),
         StackTraceElement('django.db.models.sql.query', 'has_results', None),
         StackTraceElement('django.db.models.query', 'exists', None))
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_filter_first(self):
        query_without_params = '\n            SELECT employee_health_enrollment.id, employee_health_enrollment.employee_id,\n                   employee_health_enrollment.createdAt, employee_health_enrollment.version_id,\n                   employee_health_enrollment.premiumsMap, employee_health_enrollment.progress\n            FROM employee_health_enrollment\n            WHERE (employee_health_enrollment.employee_id = %s AND employee_health_enrollment.type = %s\n                AND employee_health_enrollment.isActive = %s AND employee_health_enrollment.coverage_type = %s)\n            ORDER BY employee_health_enrollment.id ASC LIMIT 1\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_health_enrollment'])
        self.assertEqual(where_equality_key, '')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
         StackTraceElement('django.db.models.query', 'iterator', None),
         StackTraceElement('django.db.models.query', '_fetch_all', None),
         StackTraceElement('django.db.models.query', '__iter__', None),
         StackTraceElement('django.db.models.query', '__getitem__', None),
         StackTraceElement('django.db.models.query', 'first', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_filter(self):
        query_without_params = '\n            SELECT company_rate_version.id, company_rate_version.planId, company_rate_version.companyHealthEnrollmentId,\n                   company_rate_version.companyId, company_rate_version.quoteParams\n            FROM company_rate_version\n            WHERE (company_rate_version.companyId IN (%s) AND company_rate_version.lineOfCoverage = %s\n                  AND company_rate_version.planId IN (%s))\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['company_rate_version'])
        self.assertEqual(where_equality_key, '')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
         StackTraceElement('django.db.models.query', 'iterator', None),
         StackTraceElement('django.db.models.query', '_fetch_all', None),
         StackTraceElement('django.db.models.query', '__iter__', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_filter_with_join(self):
        query_without_params = '\n            SELECT (1) AS a\n            FROM change_request\n                INNER JOIN employment_type_change\n                    ON ( change_request.employmentTypeChange_id = employment_type_change.id )\n            WHERE (change_request.employee_id = %s AND change_request.isApplied = %s\n                AND employment_type_change.employmentType = %s)\n            LIMIT 1\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['change_request', 'employment_type_change'])
        self.assertEqual(where_equality_key, '')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'has_results', None),
         StackTraceElement('django.db.models.sql.query', 'has_results', None),
         StackTraceElement('django.db.models.query', 'exists', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_get(self):
        query_without_params = '\n            SELECT register_company_employee.id, register_company_employee.version_id,\n                   register_company_employee.user_id, register_company_employee.company_id,\n                   register_company_employee.isHighlyCompensated, register_company_employee.middleInitial\n            FROM register_company_employee\n            WHERE register_company_employee.id = %s\n            LIMIT 21\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['register_company_employee'])
        self.assertEqual(where_equality_key, 'register_company_employee.id')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
         StackTraceElement('django.db.models.query', 'iterator', None),
         StackTraceElement('django.db.models.query', '_fetch_all', None),
         StackTraceElement('django.db.models.query', '__len__', None),
         StackTraceElement('django.db.models.query', 'get', None),
         StackTraceElement('django.db.models.manager', 'manager_method', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.GET)

    def test_prefetch_related(self):
        query_without_params = '\n            SELECT employee_employment.id, employee_employment.version_id, employee_employment.isActive,\n                   employee_employment.fullTimeStartDate_is_set, employee_employment.fullTimeEndDate_is_set\n            FROM employee_employment\n            WHERE employee_employment.employee_id = %s\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_employment'])
        self.assertEqual(where_equality_key, 'employee_employment.employee_id')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
         StackTraceElement('django.db.models.query', 'iterator', None),
         StackTraceElement('django.db.models.query', '_fetch_all', None),
         StackTraceElement('django.db.models.query', '__iter__', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED)

    def test_select_related(self):
        query_without_params = '\n            SELECT employee_settings.id, employee_settings.employee_id, employee_settings.groupID,\n                   employee_settings.dentalGroupID, employee_settings.visionGroupID,\n                   employee_settings.dentalCompanyHealthCarrier_id_is_set\n            FROM employee_settings\n            WHERE employee_settings.employee_id = %s\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_settings'])
        self.assertEqual(where_equality_key, 'employee_settings.employee_id')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
         StackTraceElement('django.db.models.query', 'iterator', None),
         StackTraceElement('django.db.models.query', '_fetch_all', None),
         StackTraceElement('django.db.models.query', '__len__', None),
         StackTraceElement('django.db.models.query', 'get', None),
         StackTraceElement('django.db.models.manager', 'manager_method', None),
         StackTraceElement('django.db.models.fields.related_descriptors', 'get_object', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED)

    def test_prefetch_related_2(self):
        query_without_params = '\n            SELECT employee_health_enrollment.id, employee_health_enrollment.employee_id,\n                    employee_health_enrollment.progress\n             FROM employee_health_enrollment\n             WHERE employee_health_enrollment.employee_id = %s\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_health_enrollment'])
        self.assertEqual(where_equality_key, 'employee_health_enrollment.employee_id')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
         StackTraceElement('django.db.models.query', 'iterator', None),
         StackTraceElement('django.db.models.query', '_fetch_all', None),
         StackTraceElement('django.db.models.query', '__iter__', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED)

    def test_select_related_2(self):
        query_without_params = '\n            SELECT carrier.id, carrier.carrierID, carrier.name, carrier.displayName, carrier.state,\n                   carrier.newHireApprovalProcessingDays\n            FROM carrier WHERE carrier.id = %s\n            LIMIT 21\n        '
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['carrier'])
        self.assertEqual(where_equality_key, 'carrier.id')
        django_stack_trace = [
         StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
         StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
         StackTraceElement('django.db.models.query', 'iterator', None),
         StackTraceElement('django.db.models.query', '_fetch_all', None),
         StackTraceElement('django.db.models.query', '__len__', None),
         StackTraceElement('django.db.models.query', 'get', None),
         StackTraceElement('django.db.models.fields.related_descriptors', 'get_object', None)]
        query_signature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED)