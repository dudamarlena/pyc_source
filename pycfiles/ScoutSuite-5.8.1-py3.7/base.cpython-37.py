# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/resources/base.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 913 bytes
"""This module provides implementations for Resources and CompositeResources for OCI."""
import abc
from ScoutSuite.providers.base.resources.base import Resources, CompositeResources

class OracleResources(Resources, metaclass=abc.ABCMeta):
    __doc__ = 'This is the base class for Aliyun resources.'


class OracleCompositeResources(OracleResources, CompositeResources, metaclass=abc.ABCMeta):
    __doc__ = "This class represents a collection of composite Resources (resources that include nested resources referred as\n    their children). Classes extending OracleCompositeResources have to define a '_children' attribute which consists of\n    a list of tuples describing the children. The tuples are expected to respect the following format:\n    (<child_class>, <child_name>). 'child_name' is used to indicate the name under which the child resources will be\n    stored in the parent object.\n    "