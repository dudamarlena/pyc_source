# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allegro_franz/util.py
# Compiled at: 2011-04-12 03:29:54
__author__ = 'Cosmin Basca'
from franz.openrdf.model.value import URI as fURIRef
from franz.openrdf.model.value import BNode as fBNode
from franz.openrdf.model.literal import Literal as fLiteral
from surf.rdf import BNode, Literal, URIRef, Namespace

def toRdfLib(term):
    if type(term) is fURIRef:
        return URIRef(term.getURI())
    elif type(term) is fLiteral:
        try:
            if term.getDatatype() is None:
                return Literal(term.getLabel(), lang=term.getLanguage())
            else:
                dtype = term.getDatatype().getURI()
                if dtype.startswith('<') and dtype.endswith('>'):
                    dtype = dtype.strip('<>')
                    dtype = URIRef(dtype)
                else:
                    dtype = URIRef(dtype)
                return Literal(term.getLabel(), lang=term.getLanguage(), datatype=dtype)
        except Exception, e:
            print e

    elif type(term) is fBNode:
        return BNode(term.getID())
    elif type(term) in [list, tuple]:
        return map(toRdfLib, term)
    return term


def toSesame(term, factory):
    if type(term) in (URIRef, Namespace):
        return factory.createURI(unicode(term))
    elif type(term) is Literal:
        return factory.createLiteral(unicode(term), datatype=term.datatype, language=term.language)
    elif type(term) is BNode:
        return factory.createBNode(unicode(term))
    elif type(term) in [list, tuple]:
        return map(lambda item: toSesame(item, factory), term)
    return term


def toStatement((s, p, o), factory, context=None):
    return factory.createStatement(s, p, o, context)


def toTuple(statement):
    return (
     statement.getSubject(), statement.getPredicate(), statement.getObject(), statement.getContext())