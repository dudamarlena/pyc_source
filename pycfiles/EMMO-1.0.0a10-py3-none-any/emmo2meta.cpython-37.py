# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/friisj/Private/prosjekter/EMMC/EMMO-python/demo/horizontal/emmo2meta.py
# Compiled at: 2020-04-08 15:07:41
# Size of source mod 2**32: 16101 bytes
"""Module for representing an EMMO-based ontology, as a collection of
DLite metadata entities.

Entities in the ontology are mapped to DLite as follows:
  - owl class (except EMMO property, see below) -> metadata entities
  - owl `hasProperty` restrictions are interpreted. The "object"
    entity of the relation is added as a SOFT property to the
    "subject" entity.
  - all other owl restriction -> entity + relation(s)
  - owl object property -> relations
  - owl class construct -> entity + relation(s)

TODO:
  - map restriction cardinality to collection diminsions
"""
import sys, re
from inspect import isclass
import dlite
from dlite import Instance, Dimension, Property
from emmo import get_ontology
from emmo.utils import asstring
import owlready2
if sys.version_info >= (3, 7):
    odict = dict
else:
    from collections import OrderedDict as odict

class EMMO2Meta:
    __doc__ = 'A class for representing EMMO or an EMMO-based ontology as a\n    collection of metadata entities using DLite.\n\n    Parameters\n    ----------\n    ontology : string\n        URI or path to the ontology to represent.  Defaults to EMMO.\n    classes : sequence\n        The classes to include.  May be given either as a sequence of\n        strings or a sequence of owlready2 classes.  The default is to\n        include all of the ontology.\n    version : string\n        Default version for classes lacking a `version` annotation.\n    collid : string\n        Set an explicit id to the generated collection.\n\n    Notes\n    -----\n    The collection UUID is accessable via the `coll.uuid` attribute.\n    Use the `collid` argument to provide a human readable id to make\n    it easier to later retrieve it from a storage (without having\n    to remember its UUID).\n    '

    def __init__(self, ontology=None, classes=None, version='0.1', collid=None):
        if ontology is None:
            self.onto = get_ontology()
            self.onto.load()
        else:
            if isinstance(ontology, str):
                self.onto = get_ontology(ontology)
                self.onto.load()
            else:
                self.onto = ontology
        self.version = version
        self.iri = self.onto.base_iri
        self.namespace = self.onto.base_iri.rstrip('#')
        self.coll = dlite.Collection(collid)
        if classes is None:
            classes = self.onto.classes()
        else:
            if isinstance(classes, str):
                classes = [
                 classes]
        for cls in classes:
            self.add_class(cls)

    def is_dlite_property(self, cls, r):
        """Returns true if restriction `r` should be converted into a dlite
        property of class `cls`."""
        if isinstance(r, owlready2.Restriction):
            if isclass(r.property):
                if issubclass(r.property, emmo.semiotical):
                    if isinstance(r.value, owlready2.ThingClass):
                        return True
            if isinstance(r.value, (bool, int, float, str)):
                return True
        return False

    def get_dlite_unit(self, cls, r):
        """Returns a string with the unit corresponding to restriction `r`
        of class `cls` or None if `r` has no unit."""
        c = r.value
        if isinstance(c, owlready2.ThingClass):
            pass

    def get_dlite_dimensions(self, cls, r):
        """Returns a list with dimension names corresponding to restriction
        `r` of class `cls` or None if `r` has no dimensions."""
        pass

    def get_subclasses(self, cls):
        """Returns a generator yielding all subclasses of owl class `cls`."""
        yield cls
        for subcls in cls.subclasses():
            yield from self.get_subclasses(subcls)

    def get_uri(self, name, version=None):
        """Returns uri (namespace/version/name)."""
        if version is None:
            version = self.version
        return '%s/%s/%s' % (self.namespace, version, name)

    def get_uuid(self, uri=None):
        """Returns a UUID corresponding to `uri`.  If `uri` is None,
        a random UUID is returned."""
        return dlite.get_uuid(uri)

    def get_label(self, entity):
        """Returns a label for entity."""
        if hasattr(entity, 'label'):
            return entity.label.first()
        name = repr(entity)
        label, n = re.subn('emmo(-[a-z]+)?\\.', '', name)
        return label

    def find_label(self, inst):
        """Returns label for class instance `inst` already added to the
        collection."""
        if hasattr(inst, 'uuid'):
            uuid = inst.uuid
        else:
            uuid = dlite.get_uuid(inst)
        rel = self.coll.find_first(p='_has-uuid', o=uuid)
        if not rel:
            raise ValueError('no class instance with UUID: %s' % uuid)
        return rel.s

    def add(self, entity):
        """Adds owl entity to collection and returns a reference to the
        new metadata."""
        if entity == owlready2.Thing:
            raise ValueError('invalid entity: %s' % entity)
        else:
            if isinstance(entity, owlready2.ThingClass):
                return self.add_class(entity)
            if isinstance(entity, owlready2.Restriction):
                return self.add_restriction(entity)
            if isinstance(entity, owlready2.ClassConstruct):
                return self.add_class_construct(entity)
            raise ValueError('invalid entity: %s' % entity)

    def add_class(self, cls):
        """Adds owl class `cls` to collection and returns a reference to
        the new metadata."""
        if isinstance(cls, str):
            cls = self.onto[cls]
        label = cls.label.first()
        if not self.coll.has(label):
            uri = self.get_uri(label)
            dims, props = self.get_properties(cls)
            e = Instance(uri, dims, props, self.get_description(cls))
            self.coll.add(label, e)
            for r in cls.is_a:
                if r is owlready2.Thing:
                    continue
                if isinstance(r, owlready2.ThingClass):
                    self.coll.add_relation(label, 'is_a', r.label.first())
                    self.add_class(r)
                elif isinstance(r, owlready2.Restriction):
                    if isinstance(r.value, owlready2.ThingClass) and isinstance(r.value, self.onto.Property) and issubclass(r.property, self.onto.hasProperty):
                        self.add_class(r.value)
                    else:
                        self.add_restriction(r)
                elif isinstance(r, owlready2.ClassConstruct):
                    self.add_class_construct(r)
                else:
                    raise TypeError('Unexpected is_a member: %s' % type(r))

        return self.coll.get(label)

    def get_properties(self, cls):
        """Returns two lists with the dlite dimensions and properties
        correspinding to owl class `cls`."""
        dims = []
        props = []
        dimindices = {}
        propnames = set()
        types = dict(Integer='int', Real='double', String='string')

        def get_dim(r, name, descr=None):
            """Returns dimension index corresponding to dimension name `name`
            for property `r.value`."""
            t = owlready2.class_construct._restriction_type_2_label[r.type]
            if (t in ('some', 'only', 'min') or t) in ('max', 'exactly'):
                if r.cardinality > 1:
                    if name not in dimindices:
                        dimindices[name] = len(dims)
                        dims.append(Dimension(name, descr))
                    return [
                     dimindices[name]]
            return []

        for c in cls.mro():
            if not isinstance(c, owlready2.ThingClass):
                continue
            for r in c.is_a:
                if isinstance(r, owlready2.Restriction):
                    if isinstance(r.property, owlready2.Inverse) or issubclass(r.property, self.onto.hasProperty) and isinstance(r.value, owlready2.ThingClass) and isinstance(r.value, self.onto.Property):
                        name = self.get_label(r.value)
                        if name in propnames:
                            continue
                        propnames.add(name)
                        if isinstance(r.value, (self.onto.DescriptiveProperty,
                         self.onto.QualitativeProperty,
                         self.onto.SubjectiveProperty)):
                            ptype = 'string'
                        else:
                            ptype = 'double'
                    d = []
                    d.extend(get_dim(r, 'n_%ss' % name, 'Number of %s.' % name))
                    unit = None
                    for r2 in [r] + r.value.is_a:
                        if isinstance(r2, owlready2.Restriction):
                            if issubclass(r2.property, self.onto.hasType):
                                typelabel = self.get_label(r2.value)
                                ptype = types[typelabel]
                                d.extend(get_dim(r2, '%s_length' % name, 'Length of %s' % name))
                            elif issubclass(r2.property, self.onto.hasUnit):
                                unit = self.get_label(r2.value)

                    descr = self.get_description(r.value)
                    props.append(Property(name, type=ptype, dims=d, unit=unit,
                      description=descr))

        return (
         dims, props)

    def add_restriction(self, r):
        """Adds owl restriction `r` to collection and returns a reference
        to it."""
        rtype = owlready2.class_construct._restriction_type_2_label[r.type]
        cardinality = r.cardinality if r.cardinality else 0
        e = self.add_restriction_entity()
        inst = e()
        inst.type = rtype
        inst.cardinality = cardinality
        label = inst.uuid
        self.coll.add(label, inst)
        if isinstance(r.value, (bool, int, float, str)):
            self.coll.add_relation(label, asstring(r.property), str(r.value))
        else:
            if isclass(r.value) and issubclass(r.value, (bool, int, float, str)):
                self.coll.add_relation(label, asstring(r.property), r.value.__name__)
            else:
                vlabel = self.get_label(r.value)
                self.coll.add_relation(label, asstring(r.property), vlabel)
                if not self.coll.has(vlabel):
                    self.add(r.value)
        return inst

    def add_restriction_entity(self):
        """Adds restriction metadata to collection and returns a reference
        to it."""
        uri = self.get_uri('Restriction')
        if not self.coll.has('Restriction'):
            props = [Property('type', type='string', description='Type of restriction.  Valid values for `type` are: "only", "some", "exact", "min" and "max".'),
             Property('cardinality', type='int', description='The cardinality.  Unused for "only" and "some" restrictions.')]
            e = Instance(uri, [], props, 'Class restriction.  For each instance of a class restriction there should be a relation\n\n    (r.label, r.property, r.value.label)\n\nwhere `r.label` is the label associated with the restriction, `r.property` is a relation and `r.value.label` is the label of the value of the restriction.')
            self.coll.add('Restriction', e)
        return self.coll.get('Restriction')

    def add_class_construct(self, c):
        """Adds owl class construct `c` to collection and returns a reference
        to it."""
        ctype = c.__class__.__name__
        e = self.add_class_construct_entity()
        inst = e()
        label = inst.uuid
        inst.type = ctype
        if isinstance(c, owlready2.LogicalClassConstruct):
            args = c.Classes
        else:
            args = [
             c.Class]
        for arg in args:
            self.coll.add_relation(label, 'has_argument', self.get_label(arg))

        self.coll.add(label, inst)
        return inst

    def add_class_construct_entity(self):
        """Adds class construct metadata to collection and returns a reference
        to it."""
        uri = self.get_uri('ClassConstruct')
        if not self.coll.has('ClassConstruct'):
            props = [Property('type', type='string', description='Type of class construct.  Valid values for `type` are: "not", "inverse", "and" or "or".')]
            e = Instance(uri, [], props, 'Class construct.  For each instance of a class construct there should be one or more relations of type\n\n    (c.label, "has_argument", c.value.label)\n\nwhere `c.label` is the label associated with the class construct, `c.value.label` is the label of an argument.')
            self.coll.add('ClassConstruct', e)
        return self.coll.get('ClassConstruct')

    def get_description(self, cls):
        """Returns description for OWL class `cls` by combining its
        annotations."""
        if isinstance(cls, str):
            cls = onto[cls]
        else:
            descr = []
            annotations = cls.get_annotations()
            if 'definition' in annotations:
                descr.extend(annotations['definition'])
            if 'elucication' in annotations:
                if annotations['elucidation']:
                    for e in annotations['elucidation']:
                        descr.extend(['', 'ELUCIDATION:', e])

            if 'axiom' in annotations:
                if annotations['axiom']:
                    for e in annotations['axiom']:
                        descr.extend(['', 'AXIOM:', e])

            if 'comment' in annotations:
                if annotations['comment']:
                    for e in annotations['comment']:
                        descr.extend(['', 'COMMENT:', e])

            if 'example' in annotations and annotations['example']:
                for e in annotations['example']:
                    descr.extend(['', 'EXAMPLE:', e])

        return '\n'.join(descr).strip()

    def save(self, *args, **kw):
        """Saves collection to storage."""
        (self.coll.save)(*args, **kw)


def main():
    e = EMMO2Meta()
    e.save('json', 'emmo2meta.json', 'mode=w')
    return e


if __name__ == '__main__':
    e = main()
    coll = e.coll
    onto = e.onto