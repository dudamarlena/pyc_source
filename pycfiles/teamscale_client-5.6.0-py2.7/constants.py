# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/teamscale_client/constants.py
# Compiled at: 2020-03-30 02:50:39
"""This module contains multiple constants collections typically used when
communicating metrics and findings with Teamscale."""
from __future__ import absolute_import
from __future__ import unicode_literals

class Assessment:
    """Constants to be used as assessment levels."""
    RED = b'RED'
    YELLOW = b'YELLOW'


class AssessmentMetricColors:
    """Constants used for colors in assessment metrics. """
    RED = b'RED'
    YELLOW = b'YELLOW'
    GREEN = b'GREEN'


class Enablement:
    """The enablement describes which rating a finding should receive."""
    RED = b'RED'
    YELLOW = b'YELLOW'
    AUTO = b'AUTO'
    OFF = b'OFF'


class MetricAggregation:
    """Class that contains valid aggregation strategies."""
    SUM = b'SUM'
    MAX = b'MAX'
    MIN = b'MIN'


class MetricValueType:
    """Metric value types."""
    NUMERIC = b'NUMERIC'
    TIMESTAMP = b'TIMESTAMP'
    ASSESSMENT = b'ASSESSMENT'


class MetricProperties:
    """Possible properties used in metric definitions."""
    SIZE_METRIC = b'SIZE_METRIC'
    RATIO_METRIC = b'RATIO_METRIC'
    QUALITY_NEUTRAL = b'QUALITY_NEUTRAL'
    LOW_IS_BAD = b'LOW_IS_BAD'


class CoverageFormats:
    """Possible coverage formats that Teamscale can interpret."""
    CTC = b'CTC'
    COBERTURA = b'COBERTURA'
    GCOV = b'GCOV'
    LCOV = b'LCOV'
    XR_BABOON = b'XR_BABOON'
    JACOCO = b'JACOCO'
    DOT_COVER = b'DOT_COVER'
    MS_COVERAGE = b'MS_COVERAGE'
    ROSLYN = b'ROSLYN'
    BULLSEYE = b'BULLSEYE'
    SIMPLE = b'SIMPLE'
    OPEN_COVER = b'OPEN_COVER'
    IEC_COVERAGE = b'IEC_COVERAGE'
    LLVM = b'LLVM'
    CLOVER = b'CLOVER'
    XCODE = b'XCODE'
    TESTWISE_COVERAGE = b'TESTWISE_COVERAGE'
    SAP_COVERAGE = b'SAP_COVERAGE'
    ISTANBUL = b'ISTANBUL'


class ReportFormats:
    """Report formats that Teamscale understands."""
    PCLINT = b'PCLINT'
    CLANG = b'CLANG'
    ASTREE = b'ASTREE'
    FXCOP = b'FXCOP'
    SPCOP = b'SPCOP'
    CS_COMPILER_WARNING = b'CS_COMPILER_WARNING'
    PYLINT = b'PYLINT'
    FINDBUGS = b'FINDBUGS'


class UnitTestReportFormats:
    """Reports for unit test results that Teamscale understands."""
    JUNIT = b'JUNIT'
    XUNIT = b'XUNIT'


class ConnectorType:
    """Connector types."""
    TFS = b'Azure DevOps TFVC (TFS)'
    FILE_SYSTEM = b'File System'
    MULTI_VERSION_FILE_SYSTEM = b'Multi-Version File System'
    GIT = b'Git'
    SVN = b'Subversion'
    GERRIT = b'Gerrit'


class TaskStatus:
    """Different statuses a task in Teamscale can have"""
    OPEN = b'OPEN'
    RESOLVED = b'RESOLVED'
    VERIFIED = b'VERIFIED'
    DISCARDED = b'DISCARDED'


class TaskResolution:
    """Different resolutions used in tasks"""
    NONE = b'NONE'
    FIXED = b'FIXED'
    INFEASIBLE = b'INFEASIBLE'
    TOO_MUCH_EFFORT = b'TOO_MUCH_EFFORT'