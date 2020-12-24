# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/YamlParser.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 5903 bytes
"""Submodule for all the YAML-based management structures.

For specific information about the structures, see original Java implementation
--it is used as the authoritative implementation, available in util.management.

Note that the YAML dictionary-based fields are listed in the _fields attribute
and this is what is used on the load & dump YAML procedures.

For more information of the internal magic, see "MgrObject.py" file.

BLACK MAGIC WARNING! The NAME of the module (like "contractmgr") and the NAME
of the class (like "Contract") are used in order to obtain the YAML tag, which
will (hopefully) match the Java generated name, which comes from the Java
package name (like "!!util.management.contractmgr.Contract"). This is syntactic
sugar, but should be taken into account for cross-language correctness.
"""
from collections import namedtuple
from functools import partial
from yaml import Loader, load, dump
from dataclay.util.YamlIgnores import IGNORE_CLASSES, IGNORE_PREFIXES
from .ids import _uuid
import info.VersionInfo as VersionInfo
import management.accountmgr.Account as Account
import management.classmgr.AccessedImplementation as AccessedImplementation
import management.classmgr.AccessedProperty as AccessedProperty
import management.classmgr.Implementation as Implementation
import management.classmgr.MetaClass as MetaClass
import management.classmgr.Operation as Operation
import management.classmgr.Property as Property
import management.classmgr.Type as Type
import management.classmgr.UserType as UserType
import management.classmgr.java.JavaImplementation as JavaImplementation
import management.classmgr.python.PythonClassInfo as PythonClassInfo
import management.classmgr.python.PythonImplementation as PythonImplementation
import management.contractmgr.Contract as Contract
import management.datacontractmgr.DataContract as DataContract
import management.datasetmgr.DataSet as DataSet
import management.interfacemgr.Interface as Interface
import management.metadataservice.ExecutionEnvironment as ExecutionEnvironment
import management.metadataservice.MetaDataInfo as MetaDataInfo
import management.metadataservice.StorageLocation as StorageLocation
import management.metadataservice.DataClayInstance as DataClayInstance
import management.namespacemgr.Namespace as Namespace
import management.sessionmgr.SessionContract as SessionContract
import management.sessionmgr.SessionDataContract as SessionDataContract
import management.sessionmgr.SessionImplementation as SessionImplementation
import management.sessionmgr.SessionInfo as SessionInfo
import management.sessionmgr.SessionInterface as SessionInterface
import management.sessionmgr.SessionOperation as SessionOperation
import management.sessionmgr.SessionProperty as SessionProperty
import management.stubs.ImplementationStubInfo as ImplementationStubInfo
import management.stubs.PropertyStubInfo as PropertyStubInfo
import management.stubs.StubInfo as StubInfo
from dataclay.communication.grpc.messages.common.common_messages_pb2 import Langs

def trivial_constructor(loader, node):
    """Constructor used to "ignore" certain types.

    The behaviour is always to build a mapping. This is a harmless behaviour
    (at least, is expected to be). dataClay uses this for all want-to-ignore
    types, without losing semantics. If problems arise from this, this method
    could avoid them by returning None.

    For aesthetic reasons, a namedtuple instance is returned (which will be
    built tailored to the input, which may or may not be an expected behaviour)
    and its name will be used from the tag.
    """
    name = node.tag.rsplit('.', 1)[(-1)]
    contents = loader.construct_mapping(node)
    return (namedtuple(name, contents.keys()))(**contents)


def tuple_constructor(loader, node):
    """ Constructor for a Java Tuple represented in YAML, which is is a simple two-element python tuple.
    :param loader: 
    :param node:
    :returns: None
    :rtype: None
    """
    d = loader.construct_mapping(node)
    return (d['first'], d['second'])


def feature_constructor(loader, node):
    """Feature (Java enum) is parsed as a String."""
    s = loader.construct_scalar(node)
    return hash(s)


def lonely_equal_constructor(loader, node):
    """Solve/monkey-patch a very old bug.
    https://bitbucket.org/xi/pyyaml/issues/49/plain-equal-sign-as-node-content-results
    """
    s = loader.construct_scalar(node)
    return s


def lang_constructor(loader, node):
    """Language is parsed as a GRPC enum."""
    s = loader.construct_scalar(node)
    return Langs.Value(s)


Loader.add_constructor('tag:yaml.org,2002:value', lonely_equal_constructor)
Loader.add_constructor('tag:yaml.org,2002:es.bsc.dataclay.util.structs.Tuple', tuple_constructor)
Loader.add_constructor('tag:yaml.org,2002:es.bsc.dataclay.util.management.classmgr.features.Feature$FeatureType', feature_constructor)
Loader.add_constructor('tag:yaml.org,2002:es.bsc.dataclay.communication.grpc.messages.common.CommonMessages$Langs', lang_constructor)
for prefix in IGNORE_PREFIXES:
    yaml_tag_prefix = 'tag:yaml.org,2002:%s' % prefix
    Loader.add_multi_constructor(yaml_tag_prefix, lambda loader, _, node: trivial_constructor(loader, node))

for class_tag in IGNORE_CLASSES:
    yaml_class_tag = 'tag:yaml.org,2002:%s' % class_tag
    Loader.add_constructor(yaml_class_tag, trivial_constructor)

dataclay_yaml_load = partial(load, Loader=Loader)
dataclay_yaml_dump = dump