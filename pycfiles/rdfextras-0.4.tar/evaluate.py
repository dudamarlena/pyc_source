# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/rdfextras/sparql/evaluate.py
# Compiled at: 2012-07-13 08:11:28
import rdflib
from rdfextras.sparql import operators
from rdfextras.sparql.query import SessionBNode
from rdflib.namespace import RDF
from rdflib.term import URIRef, Variable, BNode, Literal, Identifier
from rdflib.term import XSDToPython
from rdfextras.sparql import _questChar
from rdfextras.sparql import SPARQLError
from rdfextras.sparql.components import IRIRef
from rdfextras.sparql.components import BinaryOperator, BuiltinFunctionCall, EqualityOperator, FunctionCall, GreaterThanOperator, GreaterThanOrEqualOperator, LessThanOperator, LessThanOrEqualOperator, ListRedirect, LogicalNegation, NotEqualOperator, NumericNegative, ParsedAdditiveExpressionList, ParsedCollection, ParsedConditionalAndExpressionList, ParsedConstrainedTriples, ParsedDatatypedLiteral, ParsedREGEXInvocation, ParsedRelationalExpressionList, ParsedString, QName, QNamePrefix, RDFTerm, UnaryOperator, FUNCTION_NAMES

class Unbound:
    """
    A class to encapsulate a query variable. This class should be used in
    conjunction with :class:`rdfextras.sparql.graph.BasicGraphPattern`.
    """

    def __init__(self, name):
        """
        :param name: the name of the variable (without the '?' character)
        :type name: unicode or string
        """
        if isinstance(name, basestring):
            self.name = _questChar + name
            self.origName = name
        else:
            raise SPARQLError('illegal argument, variable name must be a string or unicode')

    def __repr__(self):
        retval = '?%s' % self.origName
        return retval

    def __str__(self):
        return self.__repr__()


DEBUG = False
BinaryOperatorMapping = {LessThanOperator: 'operators.lt(%s,%s)%s', 
   EqualityOperator: 'operators.eq(%s,%s)%s', 
   NotEqualOperator: 'operators.neq(%s,%s)%s', 
   LessThanOrEqualOperator: 'operators.le(%s,%s)%s', 
   GreaterThanOperator: 'operators.gt(%s,%s)%s', 
   GreaterThanOrEqualOperator: 'operators.ge(%s,%s)%s'}
UnaryOperatorMapping = {LogicalNegation: 'not(%s)', 
   NumericNegative: '-(%s)'}
CAMEL_CASE_BUILTINS = {'isuri': 'operators.isURI', 
   'isiri': 'operators.isIRI', 
   'isblank': 'operators.isBlank', 
   'isliteral': 'operators.isLiteral'}

class Resolver:
    supportedSchemas = [
     None]

    def normalize(self, uriRef, baseUri):
        return baseUri + uriRef


class BNodeRef(BNode):
    """
    An explicit reference to a persistent BNode in the data set.
    This use of the syntax "_:x" to reference a named BNode is
    technically in violation of the SPARQL spec, but is also
    very useful.  If an undistinguished variable is desired,
    then an actual variable can be used as a trivial workaround.

    Support for these can be disabled by disabling the
    'EVAL_OPTION_ALLOW_BNODE_REF' evaulation option.

    Also known as special 'session' BNodes.  I.e., BNodes at
    the query side which refer to BNodes in persistence
    """
    pass


def convertTerm(term, queryProlog):
    """
    Utility function  for converting parsed Triple components into Unbound
    """
    if isinstance(term, Variable):
        if hasattr(queryProlog, 'variableBindings') and term in queryProlog.variableBindings:
            rt = queryProlog.variableBindings.get(term, term)
            return isinstance(rt, BNode) and BNodeRef(rt) or rt
        return term
    elif isinstance(term, BNodeRef):
        return term
    if isinstance(term, BNode):
        return term
    else:
        if isinstance(term, QName):
            if not term.prefix:
                if queryProlog is None:
                    return URIRef(term.localname)
                else:
                    if queryProlog.baseDeclaration and '' in queryProlog.prefixBindings and queryProlog.prefixBindings['']:
                        base = URIRef(Resolver().normalize(queryProlog.prefixBindings[''], queryProlog.baseDeclaration))
                    elif queryProlog.baseDeclaration:
                        base = queryProlog.baseDeclaration
                    else:
                        base = queryProlog.prefixBindings['']
                    return URIRef(Resolver().normalize(term.localname, base))

            else:
                if term.prefix == '_':
                    import warnings
                    warnings.warn('The verbatim interpretation of explicit bnode' + 'identifiers is contrary to (current) DAWG stance', SyntaxWarning)
                    return SessionBNode(term.localname)
                else:
                    return URIRef(Resolver().normalize(term.localname, queryProlog.prefixBindings[term.prefix]))

        elif isinstance(term, QNamePrefix):
            if queryProlog is None:
                return URIRef(term)
            else:
                if queryProlog.baseDeclaration is None:
                    return URIRef(term)
                return URIRef(Resolver().normalize(term, queryProlog.baseDeclaration))

        else:
            if isinstance(term, ParsedString):
                return Literal(term)
            else:
                if isinstance(term, ParsedDatatypedLiteral):
                    dT = term.dataType
                    if isinstance(dT, QName):
                        dT = convertTerm(dT, queryProlog)
                    return Literal(term.value, datatype=dT)
                if isinstance(term, IRIRef) and queryProlog.baseDeclaration:
                    return URIRef(Resolver().normalize(term, queryProlog.baseDeclaration))
                return term

        return


def unRollCollection(collection, queryProlog):
    nestedComplexTerms = []
    listStart = convertTerm(collection.identifier, queryProlog)
    if not collection._list:
        return
        yield (
         listStart, RDF.rest, RDF.nil)
    else:
        if len(collection._list) == 1:
            singleItem = collection._list[0]
            if isinstance(singleItem, RDFTerm):
                nestedComplexTerms.append(singleItem)
                yield (listStart, RDF.first,
                 convertTerm(singleItem.identifier, queryProlog))
            else:
                yield (
                 listStart, RDF.first, convertTerm(singleItem, queryProlog))
            yield (listStart, RDF.rest, RDF.nil)
        else:
            singleItem = collection._list[0]
            if isinstance(singleItem, Identifier):
                singleItem = singleItem
            else:
                singleItem = singleItem.identifier
            yield (listStart, RDF.first, convertTerm(singleItem, queryProlog))
            prevLink = listStart
            for colObj in collection._list[1:]:
                linkNode = convertTerm(BNode(), queryProlog)
                if isinstance(colObj, RDFTerm):
                    nestedComplexTerms.append(colObj)
                    yield (linkNode, RDF.first,
                     convertTerm(colObj.identifier, queryProlog))
                else:
                    yield (
                     linkNode, RDF.first, convertTerm(colObj, queryProlog))
                yield (prevLink, RDF.rest, linkNode)
                prevLink = linkNode

            yield (prevLink, RDF.rest, RDF.nil)
        for additionalItem in nestedComplexTerms:
            for item in unRollRDFTerm(additionalItem, queryProlog):
                yield item


def unRollRDFTerm(item, queryProlog):
    nestedComplexTerms = []
    for propVal in item.propVals:
        for propObj in propVal.objects:
            if isinstance(propObj, RDFTerm):
                nestedComplexTerms.append(propObj)
                yield (
                 convertTerm(item.identifier, queryProlog),
                 convertTerm(propVal.property, queryProlog),
                 convertTerm(propObj.identifier, queryProlog))
            else:
                yield (
                 convertTerm(item.identifier, queryProlog),
                 convertTerm(propVal.property, queryProlog),
                 convertTerm(propObj, queryProlog))

    if isinstance(item, ParsedCollection):
        for rt in unRollCollection(item, queryProlog):
            yield rt

    for additionalItem in nestedComplexTerms:
        for item in unRollRDFTerm(additionalItem, queryProlog):
            yield item


def unRollTripleItems(items, queryProlog):
    """
    Takes a list of Triples (nested lists or ParsedConstrainedTriples)
    and (recursively) returns a generator over all the contained triple
    patterns
    """
    if isinstance(items, RDFTerm):
        for item in unRollRDFTerm(items, queryProlog):
            yield item

    elif isinstance(items, ParsedConstrainedTriples):
        assert isinstance(items.triples, list)
        for item in items.triples:
            if isinstance(item, RDFTerm):
                for i in unRollRDFTerm(item, queryProlog):
                    yield i

            else:
                for i in unRollTripleItems(item, queryProlog):
                    yield item

    else:
        for item in items:
            if isinstance(item, RDFTerm):
                for i in unRollRDFTerm(item, queryProlog):
                    yield i

            else:
                for i in unRollTripleItems(item, queryProlog):
                    yield item


def mapToOperator(expr, prolog, combinationArg=None, constraint=False):
    """
    Reduces certain expressions (operator expressions, function calls, terms,
    and combinator expressions) into strings of their Python equivalent
    """
    if prolog.DEBUG:
        print 'mapToOperator:\n\texpr=%s,\n\ttype=%s,\n\tconstr=%s.\n' % (
         expr, type(expr), constraint)
    combinationInvokation = combinationArg and '(%s)' % combinationArg or ''
    if isinstance(expr, ListRedirect):
        expr = expr.reduce()
    if isinstance(expr, UnaryOperator):
        return UnaryOperatorMapping[type(expr)] % mapToOperator(expr.argument, prolog, combinationArg, constraint=constraint)
    if isinstance(expr, BinaryOperator):
        return BinaryOperatorMapping[type(expr)] % (
         mapToOperator(expr.left, prolog, combinationArg, constraint=constraint),
         mapToOperator(expr.right, prolog, combinationArg, constraint=constraint),
         combinationInvokation)
    if isinstance(expr, (Variable, Unbound)):
        if constraint:
            return 'operators.EBV(rdflib.Variable("%s"))%s' % (
             expr.n3(), combinationInvokation)
        else:
            return '"?%s"' % expr

    else:
        if isinstance(expr, ParsedREGEXInvocation):
            return 'operators.regex(%s, %s%s)%s' % (
             mapToOperator(expr.arg1, prolog, combinationArg, constraint=constraint),
             mapToOperator(expr.arg2, prolog, combinationArg, constraint=constraint),
             expr.arg3 and ',"' + str(expr.arg3) + '"' or '',
             combinationInvokation)
        if isinstance(expr, BuiltinFunctionCall):
            normBuiltInName = FUNCTION_NAMES[expr.name].lower()
            normBuiltInName = CAMEL_CASE_BUILTINS.get(normBuiltInName, 'operators.' + normBuiltInName)
            return '%s(%s)%s' % (
             normBuiltInName,
             (',').join([ mapToOperator(i, prolog, combinationArg, constraint=constraint) for i in expr.arguments
             ]),
             combinationInvokation)
        if isinstance(expr, ParsedDatatypedLiteral):
            lit = Literal(expr.value, datatype=convertTerm(expr.dataType, prolog))
            if constraint:
                return 'operators.EBV(%r)%s' % (lit, combinationInvokation)
            return repr(lit)
        else:
            if isinstance(expr, (Literal, URIRef)):
                return repr(expr)
            if isinstance(expr, QName):
                if expr[:2] == '_:':
                    return repr(BNode(expr[2:]))
                else:
                    return "'%s'" % convertTerm(expr, prolog)

            else:
                if isinstance(expr, basestring):
                    return "'%s'" % convertTerm(expr, prolog)
                if isinstance(expr, ParsedAdditiveExpressionList):
                    return 'Literal(%s)' % operators.addOperator([ mapToOperator(item, prolog, combinationArg='i', constraint=constraint) for item in expr
                                                                 ], combinationArg)
                if isinstance(expr, FunctionCall):
                    if isinstance(expr.name, QName):
                        fUri = convertTerm(expr.name, prolog)
                    if fUri in XSDToPython:
                        return "operators.XSDCast(%s, '%s')%s" % (
                         mapToOperator(expr.arguments[0], prolog, combinationArg='i', constraint=constraint),
                         fUri,
                         combinationInvokation)
                    if fUri not in prolog.extensionFunctions:
                        import warnings
                        warnings.warn('Use of unregistered extension function: %s' % fUri, UserWarning, 1)
                    else:
                        raise NotImplemented('Extension Mechanism hook not yet completely hooked up..')
                else:
                    if isinstance(expr, ListRedirect):
                        expr = expr.reduce()
                        if expr.pyBooleanOperator:
                            return expr.pyBooleanOperator.join([ mapToOperator(i, prolog, constraint=constraint) for i in expr
                                                               ])
                    raise Exception('What do i do with %s (a %s)?' % (
                     expr, type(expr).__name__))


def createSPARQLPConstraint(filter, prolog):
    """
    Takes an instance of either ParsedExpressionFilter or ParsedFunctionFilter
    and converts it to a sparql-p operator by composing a python string of
    lambda functions and SPARQL operators.
    This string is then evaluated to return the actual function for sparql-p
    """
    reducedFilter = isinstance(filter.filter, ListRedirect) and filter.filter.reduce() or filter.filter
    if prolog.DEBUG:
        print 'createSPARQLPConstraint reducedFilter=%s, type=%s' % (
         reducedFilter, type(reducedFilter))
    if isinstance(reducedFilter, (ListRedirect,
     BinaryOperator,
     UnaryOperator,
     BuiltinFunctionCall,
     ParsedREGEXInvocation)):
        if isinstance(reducedFilter, UnaryOperator) and isinstance(reducedFilter.argument, Variable):
            const = True
        else:
            const = False
    else:
        const = True
    if prolog.DEBUG:
        print 'createSPARQLPConst: reducedFilterType = %s, constraint = %s' % (
         type(reducedFilter), const)
    if isinstance(reducedFilter, ParsedConditionalAndExpressionList):
        combinationLambda = 'lambda i: %s' % (' or ').join([ '%s' % mapToOperator(expr, prolog, combinationArg='i', constraint=const) for expr in reducedFilter
                                                           ])
        if prolog.DEBUG:
            print 'a. sparql-p operator(s): %s' % combinationLambda
        return eval(combinationLambda)
    else:
        if isinstance(reducedFilter, ParsedRelationalExpressionList):
            combinationLambda = 'lambda i: %s' % (' and ').join([ '%s' % mapToOperator(expr, prolog, combinationArg='i', constraint=const) for expr in reducedFilter
                                                                ])
            if prolog.DEBUG:
                print 'b. sparql-p operator(s): %s' % combinationLambda
            return eval(combinationLambda)
        if isinstance(reducedFilter, BuiltinFunctionCall):
            rt = mapToOperator(reducedFilter, prolog, constraint=const)
            if prolog.DEBUG:
                print 'c. sparql-p operator(s): %s' % rt
            return eval(rt)
        if isinstance(reducedFilter, (
         ParsedAdditiveExpressionList, UnaryOperator, FunctionCall)):
            rt = 'lambda i: %s' % mapToOperator(reducedFilter, prolog, combinationArg='i', constraint=const)
            if prolog.DEBUG:
                print 'd. sparql-p operator(s): %s' % rt
            return eval(rt)
        if isinstance(reducedFilter, Variable):
            rt = 'operators.EBV(rdflib.Variable("%s"))' % reducedFilter.n3()
            if prolog.DEBUG:
                print 'e. sparql-p operator(s): %s' % rt
            return eval(rt)
        if reducedFilter == 'true' or reducedFilter == 'false':

            def trueFn(arg):
                return True

            def falseFn(arg):
                return False

            return reducedFilter == 'true' and trueFn or falseFn
        rt = mapToOperator(reducedFilter, prolog, constraint=const)
        if prolog.DEBUG:
            print 'f. sparql-p operator(s): %s' % rt
        return eval(rt)


def isTriplePattern(nestedTriples):
    """
    Determines (recursively) if the BasicGraphPattern contains any Triple
    Patterns returning a boolean flag indicating if it does or not
    """
    if isinstance(nestedTriples, list):
        for i in nestedTriples:
            if isTriplePattern(i):
                return True
            return False

    elif isinstance(nestedTriples, ParsedConstrainedTriples):
        if nestedTriples.triples:
            return isTriplePattern(nestedTriples.triples)
        else:
            return False

    else:
        if isinstance(nestedTriples, ParsedConstrainedTriples) and not nestedTriples.triples:
            return isTriplePattern(nestedTriples.triples)
        else:
            return True