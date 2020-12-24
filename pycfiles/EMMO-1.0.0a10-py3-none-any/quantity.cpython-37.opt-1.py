# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/quantity.py
# Compiled at: 2020-04-11 02:20:29
# Size of source mod 2**32: 4778 bytes
"""A module for working with EMMO-based quantities and units."""
import owlready2

def isquantity(q):
    """Return true if `q` is an EMMO Quantity."""
    o = q.namespace.ontology
    return isinstance(q, owlready2.ThingClass) and issubclass(q, q.namespace.world[(f"{o.Quantity.iri}")])


def _deepest_class(classes):
    """Return the class in `classes` that is the descendant of all the
    other classes.  Return None if no such class exists."""
    print('===', classes)
    for cls in classes:
        print('  ', cls, all((issubclass(cls, c) for c in classes)))
        if all((issubclass(cls, c) for c in classes)):
            return cls


def physics_dimension_of_quantity(q):
    """Return the physics dimension of quantity `q`.

    None is returned if `q` is not a quantity or don't have a physics dimension.
    """
    dim = []
    o = q.namespace.ontology
    w = q.namespace.world
    b = owlready2.base
    for s1, p1, o1 in o.get_triples(s=(q.storid), p=(b.rdfs_subclassof)):
        for s2, p2, o2 in o.get_triples(s=o1, p=(b.rdf_type), o=(b.owl_restriction)):
            for s3, p3, o3 in o.get_triples(s=o1, p=(b.owl_onproperty), o=(o.hasReferenceUnit)):
                for s4, p4, o4 in o.get_triples(s=o1, p=(b.ONLY)):
                    for s5, p5, o5 in o.get_triples(s=o4,
                      p=(b.owl_onproperty),
                      o=(o.hasPhysicsDimension)):
                        for s6, p6, o6 in o.get_triples(s=o4, p=(b.ONLY)):
                            dim.append(w[w._unabbreviate(o6)])

    if dim:
        return dim[0]


def physics_dimension_of_unit(u):
    """Return the physics dimension of unit `u`.

    None is returned if `u` is not a unit or don't have a physics dimension.
    """
    dim = []
    o = u.namespace.ontology
    w = u.namespace.world
    b = owlready2.base
    for s1, p1, o1 in o.get_triples(s=(u.storid), p=(b.rdfs_subclassof)):
        for s2, p2, o2 in o.get_triples(s=o1, p=(b.rdf_type), o=(b.owl_restriction)):
            for s3, p3, o3 in o.get_triples(s=o1, p=(b.owl_onproperty), o=(o.hasPhysicsDimension)):
                for s4, p4, o4 in o.get_triples(s=o1, p=(b.ONLY)):
                    try:
                        dim.append(w[w._unabbreviate(o4)])
                    except KeyError:
                        pass

    if dim:
        return dim[0]


def get_units(q):
    """Returns a list with all possible units for quantity `q`.

    An empty list is returned if `q` is not a quantity.
    """
    o = q.namespace.ontology
    dim = physics_dimension_of_quantity(q)
    if dim is None:
        return
    return [u for u in o.ReferenceUnit.descendants() if physics_dimension_of_unit(u) is dim]


def get_units_sparql(q):
    """Returns a list with all possible units for quantity `q`.

    An empty list is returned if `q` is not a quantity.
    """
    g = q.namespace.world.as_rdflib_graph()
    o = q.namespace.ontology
    w = q.namespace.world
    query = f"\n        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n        PREFIX owl: <http://www.w3.org/2002/07/owl#>\n        SELECT ?unit\n        WHERE {{\n            <{q.iri}> rdfs:subClassOf [\n                a owl:Restriction;\n                owl:onProperty <{o.hasReferenceUnit.iri}>;\n                owl:allValuesFrom [\n                    a owl:Restriction;\n                    owl:onProperty <{o.hasPhysicsDimension.iri}>;\n                    owl:allValuesFrom ?dim\n                ]\n            ] .\n            ?unit rdfs:subClassOf+ <{o.ReferenceUnit.iri}>;\n                rdfs:subClassOf [\n                    a owl:Restriction;\n                    owl:onProperty <{o.hasPhysicsDimension.iri}>;\n                    owl:allValuesFrom ?dim\n                ] .\n        }}\n        "
    return [r[0] for r in g.query_owlready(query)]


class Quantity(object):
    __doc__ = 'A class offering extra attributes and methods for a quantity.'

    def __new__(cls, q):
        for k, v in cls.__dict__.items():
            setattr(q, k, v)

        return q