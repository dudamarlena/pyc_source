# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/test/test_schevo_tests.py
# Compiled at: 2008-01-19 12:32:25
"""Test Schevo's unit tests against restricted databases with
allow-all-operation policies.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from base import class_with_policy
from schevo.test.test_bank import BaseBank
from schevo.test.test_calculated_field_unicode import BaseCalculatedUnicode
from schevo.test.test_change import BaseChangeset, BaseDistributor
from schevo.test.test_database_namespace import BaseDatabaseNamespaces
from schevo.test.test_default_values import BaseDefaultValues
from schevo.test.test_entity_extent import BaseEntityExtent
from schevo.test.test_entity_subclass import BaseHiddenBases, BaseSameNameSubclasses, BaseSubclassTransactionCorrectness
from schevo.test.test_extent_name_override import BaseOverride
from schevo.test.test_extent_without_fields import BaseExtentWithoutFields
from schevo.test.test_extentmethod import BaseExtentMethod
from schevo.test.test_field_entity import BaseEntity
from schevo.test.test_field_entitylist import BaseFieldEntityList
from schevo.test.test_field_entityset import BaseFieldEntitySet
from schevo.test.test_field_entitysetset import BaseFieldEntitySetSet
from schevo.test.test_field_maps import BaseFieldMaps
from schevo.test.test_icon import BaseFsIconMap
from schevo.test.test_label import BaseDecoration
from schevo.test.test_links import BaseLinks
from schevo.test.test_on_delete import BaseOnDelete, BaseOnDeleteKeyRelax
from schevo.test.test_populate import BasePopulateSimple, BasePopulateComplex, BasePopulateHidden
from schevo.test.test_query import BaseQuery
from schevo.test.test_relax_index import BaseRelaxIndex
from schevo.test.test_schema import BaseSchema
from schevo.test.test_transaction import BaseTransaction
from schevo.test.test_transaction_before_after import BaseTransactionBeforeAfter
from schevo.test.test_transaction_field_reorder import BaseTransactionFieldReorder
from schevo.test.test_transaction_require_changes import BaseTransactionRequireChanges
from schevo.test.test_view import BaseView
TestBank = class_with_policy(BaseBank)
TestCalculatedUnicode = class_with_policy(BaseCalculatedUnicode)
TestChangeset = class_with_policy(BaseChangeset)
TestDistributor = class_with_policy(BaseDistributor)
TestDatabaseNamespaces = class_with_policy(BaseDatabaseNamespaces)
TestDefaultValues = class_with_policy(BaseDefaultValues)
TestEntityExtent = class_with_policy(BaseEntityExtent)
TestHiddenBases = class_with_policy(BaseHiddenBases)
TestSameNameSubclasses = class_with_policy(BaseSameNameSubclasses)
TestSubclassTransactionCorrectness = class_with_policy(BaseSubclassTransactionCorrectness)
TestOverride = class_with_policy(BaseOverride)
TestExtentWithoutFields = class_with_policy(BaseExtentWithoutFields)
TestExtentMethod = class_with_policy(BaseExtentMethod)
TestEntity = class_with_policy(BaseEntity)
TestEntity.test_convert = lambda self: None
TestFieldEntityList = class_with_policy(BaseFieldEntityList)
TestFieldEntitySet = class_with_policy(BaseFieldEntitySet)
TestFieldEntitySetSet = class_with_policy(BaseFieldEntitySetSet)
TestFieldMaps = class_with_policy(BaseFieldMaps)
TestFsIconMap = class_with_policy(BaseFsIconMap)
TestDecoration = class_with_policy(BaseDecoration)
TestLinks = class_with_policy(BaseLinks)
TestOnDelete = class_with_policy(BaseOnDelete)
TestOnDeleteKeyRelax = class_with_policy(BaseOnDeleteKeyRelax)
TestOnDelete.internal_cascade_complex_1 = lambda self: None
TestOnDelete.internal_cascade_complex_2 = lambda self: None
TestPopulateSimple = class_with_policy(BasePopulateSimple)
TestPopulateComplex = class_with_policy(BasePopulateComplex)
TestPopulateHidden = class_with_policy(BasePopulateHidden)
TestPopulateSimple.test_datalist_simple = lambda self: None
TestPopulateComplex.test_datalist_complex = lambda self: None
TestQuery = class_with_policy(BaseQuery)
TestRelaxIndex = class_with_policy(BaseRelaxIndex)
TestSchema = class_with_policy(BaseSchema)
TestTransaction = class_with_policy(BaseTransaction)
TestTransaction.internal_update_entities_1 = lambda self, expected: None
TestTransaction.test_create_simple = lambda self: None
TestTransaction.test_extra_fields = lambda self: None
TestTransaction.test_update_simple = lambda self: None
TestTransaction.test_callable_wrapper = lambda self: None
TestTransactionBeforeAfter = class_with_policy(BaseTransactionBeforeAfter)
TestTransactionFieldReorder = class_with_policy(BaseTransactionFieldReorder)
TestTransactionRequireChanges = class_with_policy(BaseTransactionRequireChanges)
TestView = class_with_policy(BaseView)
optimize.bind_all(sys.modules[__name__])