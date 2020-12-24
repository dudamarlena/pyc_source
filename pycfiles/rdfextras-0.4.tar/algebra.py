# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/rdfextras/sparql/algebra.py
# Compiled at: 2012-07-13 08:11:28
"""
An implementation of the W3C SPARQL Algebra on top of sparql-p's expansion trees

See: http://www.w3.org/TR/rdf-sparql-query/#sparqlAlgebra

For each symbol in a SPARQL abstract query, we define an operator for evaluation.
The SPARQL algebra operators of the same name are used to evaluate SPARQL abstract
query nodes as described in the section "Evaluation Semantics".

We define eval(D(G), graph pattern) as the evaluation of a graph pattern with respect
to a dataset D having active graph G. The active graph is initially the default graph.
"""
import unittest
from rdflib.graph import ConjunctiveGraph
from rdflib.graph import Graph
from rdflib.graph import ReadOnlyGraphAggregate
from rdflib import plugin
from rdflib.term import URIRef
from rdflib.term import Variable
from rdflib.store import Store
from rdfextras.sparql import DESCRIBE
from rdfextras.sparql import graph
from rdfextras.sparql import SPARQLError
from rdfextras.sparql import query as sparql_query
from rdfextras.sparql.components import ASCENDING_ORDER
from rdfextras.sparql.components import AskQuery
from rdfextras.sparql.components import DescribeQuery
from rdfextras.sparql.components import GraphPattern
from rdfextras.sparql.components import NamedGraph
from rdfextras.sparql.components import ParsedAlternativeGraphPattern
from rdfextras.sparql.components import ParsedGraphGraphPattern
from rdfextras.sparql.components import ParsedGroupGraphPattern
from rdfextras.sparql.components import ParsedOptionalGraphPattern
from rdfextras.sparql.components import Prolog
from rdfextras.sparql.components import SelectQuery
from rdfextras.sparql.evaluate import convertTerm
from rdfextras.sparql.evaluate import createSPARQLPConstraint
from rdfextras.sparql.evaluate import unRollTripleItems
from rdfextras.sparql.graph import BasicGraphPattern
from rdfextras.sparql.query import _variablesToArray
import logging
log = logging.getLogger(__name__)
DAWG_DATASET_COMPLIANCE = False

def ReduceGraphPattern(graphPattern, prolog):
    """
    Takes parsed graph pattern and converts it into a BGP operator

    Replace all basic graph patterns by BGP(list of triple patterns)

    """
    if isinstance(graphPattern.triples[0], list) and len(graphPattern.triples) == 1:
        graphPattern.triples = graphPattern.triples[0]
    items = []
    for triple in graphPattern.triples:
        bgp = BasicGraphPattern(list(unRollTripleItems(triple, prolog)), prolog)
        items.append(bgp)

    if len(items) == 1:
        assert isinstance(items[0], BasicGraphPattern), repr(items)
        bgp = items[0]
        return bgp
    if len(items) > 1:
        constraints = [ b.constraints for b in items if b.constraints ]
        constraints = reduce(lambda x, y: x + y, constraints, [])

        def mergeBGPs(left, right):
            if isinstance(left, BasicGraphPattern):
                left = left.patterns
            if isinstance(right, BasicGraphPattern):
                right = right.patterns
            return left + right

        bgp = BasicGraphPattern(reduce(mergeBGPs, items), prolog)
        bgp.addConstraints(constraints)
        return bgp
    raise


def ReduceToAlgebra(left, right):
    """

    Converts a parsed Group Graph Pattern into an expression in the algebra by recursive
    folding / reduction (via functional programming) of the GGP as a list of Basic
    Triple Patterns or "Graph Pattern Blocks"

    12.2.1 Converting Graph Patterns

    .. sourcecode:: text

        [20] GroupGraphPattern ::= '{' TriplesBlock? ( ( GraphPatternNotTriples | Filter )
             '.'? TriplesBlock? )* '}'
        [22] GraphPatternNotTriples ::= OptionalGraphPattern | GroupOrUnionGraphPattern |
             GraphGraphPattern
        [26] Filter ::= 'FILTER' Constraint
        [27] Constraint ::= BrackettedExpression | BuiltInCall | FunctionCall
        [56] BrackettedExpression  ::= '(' ConditionalOrExpression ')'

        ( GraphPatternNotTriples | Filter ) '.'? TriplesBlock?
           nonTripleGraphPattern     filter         triples

    """
    prolog = ReduceToAlgebra.prolog
    if isinstance(right, AlgebraExpression) or isinstance(right, ParsedGroupGraphPattern):
        right = reduce(ReduceToAlgebra, right, None)
        log.debug(right)
    if not isinstance(right, GraphPattern):
        raise AssertionError(type(right))
        if right.triples:
            if right.nonTripleGraphPattern:
                if isinstance(right.nonTripleGraphPattern, ParsedGraphGraphPattern):
                    right = Join(ReduceGraphPattern(right, prolog), GraphExpression(right.nonTripleGraphPattern.name, reduce(ReduceToAlgebra, right.nonTripleGraphPattern.graphPatterns, None)))
                elif isinstance(right.nonTripleGraphPattern, ParsedOptionalGraphPattern):
                    if left:
                        if not isinstance(left, (Join, BasicGraphPattern)):
                            raise AssertionError(repr(left))
                            rightTriples = ReduceGraphPattern(right, prolog)
                            LJright = LeftJoin(left, reduce(ReduceToAlgebra, right.nonTripleGraphPattern.graphPatterns, None))
                            return Join(LJright, rightTriples)
                        else:
                            rightTriples = ReduceGraphPattern(right, prolog)
                            return Join(reduce(ReduceToAlgebra, right.nonTripleGraphPattern.graphPatterns, None), rightTriples)

                    elif isinstance(right.nonTripleGraphPattern, ParsedAlternativeGraphPattern):
                        unionList = [ reduce(ReduceToAlgebra, i.graphPatterns, None) for i in right.nonTripleGraphPattern.alternativePatterns
                                    ]
                        right = Join(reduce(Union, unionList), ReduceGraphPattern(right, prolog))
                    else:
                        raise Exception(right)
                elif isinstance(left, BasicGraphPattern) and left.constraints:
                    if right.filter:
                        if not left.patterns:
                            filter2 = createSPARQLPConstraint(right.filter, prolog)
                            right = ReduceGraphPattern(right, prolog)
                            right.addConstraints(left.constraints)
                            right.addConstraint(filter2)
                            return right
                        left.addConstraint(createSPARQLPConstraint(right.filter, prolog))
                    right = ReduceGraphPattern(right, prolog)
                elif right.filter:
                    filter = createSPARQLPConstraint(right.filter, prolog)
                    right = ReduceGraphPattern(right, prolog)
                    right.addConstraint(filter)
                else:
                    right = ReduceGraphPattern(right, prolog)
            elif right.nonTripleGraphPattern is None:
                if right.filter:
                    if isinstance(left, BasicGraphPattern):
                        left.addConstraint(createSPARQLPConstraint(right.filter, prolog))
                        return left
                    pattern = BasicGraphPattern()
                    pattern.addConstraint(createSPARQLPConstraint(right.filter, prolog))
                    if left is None:
                        return pattern
                    right = pattern
                else:
                    raise Exception(right)
            elif right.nonTripleGraphPattern:
                if isinstance(right.nonTripleGraphPattern, ParsedGraphGraphPattern):
                    right = GraphExpression(right.nonTripleGraphPattern.name, reduce(ReduceToAlgebra, right.nonTripleGraphPattern.graphPatterns, None))
                elif isinstance(right.nonTripleGraphPattern, ParsedOptionalGraphPattern):
                    if left:
                        return LeftJoin(left, reduce(ReduceToAlgebra, right.nonTripleGraphPattern.graphPatterns, None))
                    else:
                        return reduce(ReduceToAlgebra, right.nonTripleGraphPattern.graphPatterns, None)

                elif isinstance(right.nonTripleGraphPattern, ParsedAlternativeGraphPattern):
                    unionList = map(lambda i: reduce(ReduceToAlgebra, i.graphPatterns, None), right.nonTripleGraphPattern.alternativePatterns)
                    right = reduce(Union, unionList)
                else:
                    raise Exception(right)
        return left or right
    else:
        return Join(left, right)
        return


def RenderSPARQLAlgebra(parsedSPARQL, nsMappings=None):
    global prolog
    nsMappings = nsMappings and nsMappings or {}
    prolog = parsedSPARQL.prolog
    if prolog is not None:
        prolog.DEBUG = False
    else:
        prolog = Prolog(None, [])
        prolog.DEBUG = False
    return reduce(ReduceToAlgebra, parsedSPARQL.query.whereClause.parsedGraphPattern.graphPatterns, None)


def LoadGraph(dtSet, dataSetBase, graph):
    try:
        from Ft.Lib.Uri import UriResolverBase as Resolver
        from Ft.Lib.Uri import GetScheme, OsPathToUri
    except:

        def OsPathToUri(path):
            return path

        def GetScheme(uri):
            return

        class Resolver:
            supportedSchemas = [
             None]

            def resolve(self, uriRef, baseUri):
                return uriRef

    if dataSetBase is not None:
        res = Resolver()
        scheme = GetScheme(dtSet) or GetScheme(dataSetBase)
        if scheme not in res.supportedSchemes:
            dataSetBase = OsPathToUri(dataSetBase)
        source = Resolver().resolve(str(dtSet), dataSetBase)
    else:
        source = dtSet
    try:
        graph.parse(source)
    except:
        try:
            source = Resolver().resolve(str(dtSet), dataSetBase)
            graph.parse(source, format='n3')
        except:
            raise
            graph.parse(dtSet, format='rdfa')

    return


def TopEvaluate(query, dataset, passedBindings=None, DEBUG=False, exportTree=False, dataSetBase=None, extensionFunctions={}, dSCompliance=False, loadContexts=False):
    """
    The outcome of executing a SPARQL is defined by a series of steps, starting
    from the SPARQL query as a string, turning that string into an abstract
    syntax form, then turning the abstract syntax into a SPARQL abstract query
    comprising operators from the SPARQL algebra. This abstract query is then
    evaluated on an RDF dataset.
    """
    if not passedBindings:
        passedBindings = {}
    if query.prolog:
        query.prolog.DEBUG = DEBUG
        prolog = query.prolog
    else:
        prolog = Prolog(None, [])
        prolog.DEBUG = False
    prolog.answerList = []
    prolog.eagerLimit = None
    prolog.extensionFunctions.update(extensionFunctions)
    ReduceToAlgebra.prolog = prolog
    query.prolog.rightMostBGPs = set()
    DAWG_DATASET_COMPLIANCE = dSCompliance
    if query.query.dataSets:
        graphs = []
        for dtSet in query.query.dataSets:
            if isinstance(dtSet, NamedGraph):
                if loadContexts:
                    newGraph = Graph(dataset.store, dtSet)
                    LoadGraph(dtSet, dataSetBase, newGraph)
                    graphs.append(newGraph)
                else:
                    continue
            else:
                if DAWG_DATASET_COMPLIANCE:
                    assert isinstance(dataset, ConjunctiveGraph)
                    memGraph = dataset.default_context
                elif loadContexts:
                    memGraph = dataset.get_context(dtSet)
                else:
                    memStore = plugin.get('IOMemory', Store)()
                    memGraph = Graph(memStore)
                    LoadGraph(dtSet, dataSetBase, memGraph)
                if memGraph.identifier not in [ g.identifier for g in graphs ]:
                    graphs.append(memGraph)

        tripleStore = graph.SPARQLGraph(ReadOnlyGraphAggregate(graphs, store=dataset.store), dSCompliance=DAWG_DATASET_COMPLIANCE)
    else:
        tripleStore = graph.SPARQLGraph(dataset, dSCompliance=DAWG_DATASET_COMPLIANCE)
    if isinstance(query.query, SelectQuery) and query.query.variables:
        query.query.variables = [ convertTerm(item, query.prolog) for item in query.query.variables ]
    else:
        query.query.variables = []
    if query.query.whereClause.parsedGraphPattern is None:
        query.query.whereClause.parsedGraphPattern = BasicGraphPattern([])
        query.query.whereClause.parsedGraphPattern.graphPatterns = ()
    expr = reduce(ReduceToAlgebra, query.query.whereClause.parsedGraphPattern.graphPatterns, None)
    limit = None
    offset = 0
    if isinstance(query.query, SelectQuery) and query.query.solutionModifier.limitClause is not None:
        limit = int(query.query.solutionModifier.limitClause)
    if isinstance(query.query, SelectQuery) and query.query.solutionModifier.offsetClause is not None:
        offset = int(query.query.solutionModifier.offsetClause)
    else:
        offset = 0
    if limit is not None and offset == 0:
        query.prolog.eagerLimit = limit
        for x in expr.fetchTerminalExpression():
            query.prolog.rightMostBGPs.add(x)

        if query.prolog.DEBUG:
            log.debug('Setting up for an eager limit evaluation (size: %s)' % query.prolog.eagerLimit)
    if DEBUG:
        log.debug('## Full SPARQL Algebra expression ##')
        log.debug(expr)
        log.debug('###################################')
    if isinstance(expr, BasicGraphPattern):
        retval = None
        bindings = sparql_query._createInitialBindings(expr)
        if passedBindings:
            bindings.update(passedBindings)
        top = sparql_query._SPARQLNode(None, bindings, expr.patterns, tripleStore, expr=expr)
        top.topLevelExpand(expr.constraints, query.prolog)
        result = sparql_query.Query(top, tripleStore)
    elif expr is None and isinstance(query.query, DescribeQuery):
        bindings = {}
        top = sparql_query._SPARQLNode(None, bindings, (), tripleStore, expr=expr)
        top.topLevelExpand((), query.prolog)
        result = sparql_query.Query(top, tripleStore)
    else:
        assert isinstance(expr, AlgebraExpression), repr(expr)
        if DEBUG:
            log.debug('## Full SPARQL Algebra expression ##')
            log.debug(expr)
            log.debug('###################################')
        result = expr.evaluate(tripleStore, passedBindings, query.prolog)
        if isinstance(result, BasicGraphPattern):
            bindings = sparql_query._createInitialBindings(result)
            if passedBindings:
                bindings.update(passedBindings)
            top = sparql_query._SPARQLNode(None, bindings, result.patterns, result.tripleStore, expr=result)
            top.topLevelExpand(result.constraints, query.prolog)
            result = sparql_query.Query(top, tripleStore)
        assert isinstance(result, sparql_query.Query), repr(result)
    if exportTree:
        from rdfextras.sparql.Visualization import ExportExpansionNode
        if result.top:
            ExportExpansionNode(result.top, fname='out.svg', verbose=True)
        else:
            ExportExpansionNode(result.parent1.top, fname='out1.svg', verbose=True)
            ExportExpansionNode(result.parent2.top, fname='out2.svg', verbose=True)
    if result == None:
        msg = 'Errors in the patterns, no valid query object generated; '
        raise SPARQLError(msg)
    if isinstance(query.query, AskQuery):
        return result.ask()
    else:
        if isinstance(query.query, SelectQuery):
            orderBy = None
            orderAsc = None
            if query.query.solutionModifier.orderClause:
                orderBy = []
                orderAsc = []
                for orderCond in query.query.solutionModifier.orderClause:
                    if isinstance(orderCond, Variable):
                        orderBy.append(orderCond)
                        orderAsc.append(ASCENDING_ORDER)
                    else:
                        order_expr = orderCond.expression.reduce()
                        assert isinstance(order_expr, Variable), 'Support for ORDER BY with anything other than a variable is not supported: %s' % order_expr
                        orderBy.append(order_expr)
                        orderAsc.append(orderCond.order == ASCENDING_ORDER)

            if query.query.recurClause is not None:
                recursive_pattern = query.query.recurClause.parsedGraphPattern
                if recursive_pattern is None:
                    recursive_expr = expr
                else:
                    recursive_expr = reduce(ReduceToAlgebra, recursive_pattern.graphPatterns, None)

                def get_recursive_results(recursive_bindings_update, select):
                    recursive_bindings = result.top.bindings.copy()
                    recursive_bindings.update(recursive_bindings_update)
                    if isinstance(recursive_expr, BasicGraphPattern):
                        recursive_top = sparql_query._SPARQLNode(None, recursive_bindings, recursive_expr.patterns, tripleStore, expr=recursive_expr)
                        recursive_top.topLevelExpand(recursive_expr.constraints, query.prolog)
                        recursive_result = sparql_query.Query(recursive_top, tripleStore)
                    else:
                        recursive_result = recursive_expr.evaluate(tripleStore, recursive_bindings, query.prolog)
                    return recursive_result.top.returnResult(select)

                recursive_maps = query.query.recurClause.maps
                result.set_recursive(get_recursive_results, recursive_maps)
            topUnionBindings = []
            selection = result.select(query.query.variables, query.query.distinct, limit, orderBy, orderAsc, offset)
            selectionF = sparql_query._variablesToArray(query.query.variables, 'selection')
            if result.get_recursive_results is not None:
                selectionF.append(result.map_from)
            vars = result._getAllVariables()
            if result.parent1 != None and result.parent2 != None:
                topUnionBindings = reduce(lambda x, y: x + y, [ root.returnResult(selectionF) for root in fetchUnionBranchesRoots(result)
                                                              ])
            elif limit == 0 or limit is not None or offset is not None and offset > 0:
                if prolog.answerList:
                    topUnionBindings = prolog.answerList
                    vars = prolog.answerList[0].keys()
                else:
                    topUnionBindings = []
            else:
                topUnionBindings = result.top.returnResult(selectionF)
            if result.get_recursive_results is not None:
                topUnionBindings.extend(result._recur(topUnionBindings, selectionF))
                selectionF.pop()
            return (selection,
             _variablesToArray(query.query.variables, 'selection'),
             vars,
             orderBy, query.query.distinct,
             topUnionBindings)
        else:
            if isinstance(query.query, DescribeQuery):

                def create_result(vars, binding, graph):
                    return (
                     graph.n3(), [], vars, limit, offset, [])

                import rdflib
                extensionFunctions = {rdflib.term.URIRef('http://www.w3.org/TR/rdf-sparql-query/#describe'): create_result}
                if query.query.solutionModifier.limitClause is not None:
                    limit = int(query.query.solutionModifier.limitClause)
                else:
                    limit = None
                if query.query.solutionModifier.offsetClause is not None:
                    offset = int(query.query.solutionModifier.offsetClause)
                else:
                    offset = 0
                if result.parent1 != None and result.parent2 != None:
                    rt = (r for r in reduce(lambda x, y: x + y, [ root.returnResult(selectionF) for root in fetchUnionBranchesRoots(result)
                                                                ]))
                else:
                    if limit is not None or offset != 0:
                        raise NotImplemented('Solution modifiers cannot be used with DESCRIBE')
                    else:
                        rt = result.top.returnResult(None)
                    rtGraph = Graph(namespace_manager=dataset.namespace_manager)
                    for binding in rt:
                        if binding:
                            g = extensionFunctions[DESCRIBE](query.query.describeVars, binding, tripleStore.graph)
                            return g

                rtGraph.bind('', 'http://rdflib.net/store#')
                rtGraph.bind('rdfg', 'http://www.w3.org/2004/03/trix/rdfg-1/')
                rtGraph.add((URIRef('http://rdflib.net/store#' + tripleStore.graph.identifier),
                 rdflib.RDF.type,
                 URIRef('http://rdflib.net/store#Store')))
                return rtGraph
            if query.query.solutionModifier.limitClause is not None:
                limit = int(query.query.solutionModifier.limitClause)
            else:
                limit = None
            if query.query.solutionModifier.offsetClause is not None:
                offset = int(query.query.solutionModifier.offsetClause)
            else:
                offset = 0
            if result.parent1 != None and result.parent2 != None:
                rt = (r for r in reduce(lambda x, y: x + y, [ root.returnResult(selectionF) for root in fetchUnionBranchesRoots(result)
                                                            ]))
            else:
                if limit is not None or offset != 0:
                    raise NotImplemented('Solution modifiers cannot be used with CONSTRUCT')
                else:
                    rt = result.top.returnResult(None)
                rtGraph = Graph(namespace_manager=dataset.namespace_manager)
                for binding in rt:
                    for s, p, o, func in ReduceGraphPattern(query.query.triples, prolog).patterns:
                        s, p, o = map(lambda x: isinstance(x, Variable) and binding.get(x) or x, [s, p, o])
                        if not [ i for i in [s, p, o] if isinstance(i, Variable) ]:
                            rtGraph.add((s, p, o))

            return rtGraph

        return


class AlgebraExpression(object):
    """
    For each symbol in a SPARQL abstract query, we define an operator for
    evaluation. The SPARQL algebra operators of the same name are used
    to evaluate SPARQL abstract query nodes as described in the section
    "Evaluation Semantics".
    """

    def __repr__(self):
        return '%s(%s,%s)' % (self.__class__.__name__, self.left, self.right)

    def evaluate(self, tripleStore, initialBindings, prolog):
        """
        12.5 Evaluation Semantics

        We define eval(D(G), graph pattern) as the evaluation of a graph pattern
        with respect to a dataset D having active graph G. The active graph is
        initially the default graph.
        """
        raise Exception(repr(self))


class EmptyGraphPatternExpression(AlgebraExpression):
    """
    A placeholder for evaluating empty graph patterns - which
    should result in an empty multiset of solution bindings
    """

    def __repr__(self):
        return 'EmptyGraphPatternExpression(..)'

    def evaluate(self, tripleStore, initialBindings, prolog):
        if prolog.DEBUG:
            log.debug('eval(%s,%s,%s)' % (self, initialBindings, tripleStore.graph))
        empty = sparql_query._SPARQLNode(None, {}, [], tripleStore)
        empty.bound = False
        return sparql_query.Query(empty, tripleStore)


def fetchUnionBranchesRoots(node):
    for parent in [node.parent1, node.parent2]:
        if parent.parent1:
            for branch_root in fetchUnionBranchesRoots(parent):
                yield branch_root

        else:
            yield parent.top


def fetchChildren(node):
    if isinstance(node, sparql_query._SPARQLNode):
        yield [ c for c in node.children ]
    elif isinstance(node, sparql_query.Query):
        if node.parent1 is None:
            for c in fetchChildren(node.top):
                yield c

        else:
            for parent in [node.parent1, node.parent2]:
                for c in fetchChildren(parent):
                    yield c

    return


def walktree(top, depthfirst=True, leavesOnly=True, optProxies=False):
    if isinstance(top, sparql_query._SPARQLNode) and top.clash:
        return
    if not depthfirst and (not leavesOnly or not top.children):
        proxies = False
        for optChild in reduce(lambda x, y: x + y, [ list(sparql_query._fetchBoundLeaves(o)) for o in top.optionalTrees
                                                   ], []):
            proxies = True
            yield optChild

        if not proxies:
            yield top
    children = reduce(lambda x, y: x + y, list(fetchChildren(top)))
    for child in children:
        if child.children:
            for newtop in walktree(child, depthfirst, leavesOnly, optProxies):
                yield newtop

        else:
            proxies = False
            for optChild in reduce(lambda x, y: x + y, [ list(sparql_query._fetchBoundLeaves(o)) for o in child.optionalTrees
                                                       ], []):
                proxies = True
                yield optChild

            if not proxies:
                yield child

    if depthfirst and (not leavesOnly or not children):
        proxies = False
        for optChild in reduce(lambda x, y: x + y, [ list(sparql_query._fetchBoundLeaves(o)) for o in top.optionalTrees
                                                   ], []):
            proxies = True
            yield optChild

        if not proxies:
            yield top


def print_tree(node, padding=' '):
    print padding[:-1] + repr(node)
    padding = padding + ' '
    count = 0
    for child in node.children:
        count += 1
        print padding + '|'
        if child.children:
            if count == len(node.children):
                print_tree(child, padding + ' ')
            else:
                print_tree(child, padding + '|')
        else:
            print padding + '+-' + repr(child) + ' ' + repr(dict([ (k, v) for k, v in child.bindings.items() if v
                                                                 ]))
            optCount = 0
            for optTree in child.optionalTrees:
                optCount += 1
                print padding + '||'
                if optTree.children:
                    if optCount == len(child.optionalTrees):
                        print_tree(optTree, padding + ' ')
                    else:
                        print_tree(optTree, padding + '||')
                else:
                    print padding + '+=' + repr(optTree)

    count = 0
    for optTree in node.optionalTrees:
        count += 1
        print padding + '||'
        if optTree.children:
            if count == len(node.optionalTrees):
                print_tree(optTree, padding + ' ')
            else:
                print_tree(optTree, padding + '||')
        else:
            print padding + '+=' + repr(optTree)


def _ExpandJoin(node, expression, tripleStore, prolog, optionalTree=False):
    """
    Traverses to the leaves of expansion trees to implement the Join
    operator
    """
    if prolog.DEBUG:
        print_tree(node)
        log.debug('-------------------')
    currExpr = expression
    for node in walktree(node):
        if node.clash:
            continue
        if not len(node.children) == 0:
            raise AssertionError
            if prolog.DEBUG:
                log.debug('Performing Join(%s,..)' % node)
            if isinstance(currExpr, AlgebraExpression):
                if prolog.DEBUG:
                    log.debug('passing on bindings to %s\n:%s' % (currExpr, node.bindings.copy()))
                expression = currExpr.evaluate(tripleStore, node.bindings.copy(), prolog)
            else:
                expression = currExpr
            if isinstance(expression, BasicGraphPattern):
                tS = tripleStore
                if hasattr(expression, 'tripleStore'):
                    if prolog.DEBUG:
                        log.debug('has tripleStore: %s ' % expression.tripleStore)
                    tS = expression.tripleStore
                if prolog.DEBUG:
                    log.debug('Evaluated left node and traversed to leaf, expanding with %s' % expression)
                    log.debug(node.tripleStore.graph)
                    log.debug('expressions bindings: %s' % sparql_query._createInitialBindings(expression))
                    log.debug('node bindings: %s' % node.bindings)
                exprBindings = sparql_query._createInitialBindings(expression)
                exprBindings.update(node.bindings)
                descendantOptionals = node.optionalTrees and [ o for o in node.optionalTrees if list(sparql_query._fetchBoundLeaves(o)) ]
                top = descendantOptionals or node
            else:
                if prolog.DEBUG:
                    log.debug('descendant optionals: %s' % descendantOptionals)
                top = None
            child = None
            if not node.clash and not descendantOptionals:
                child = sparql_query._SPARQLNode(top, exprBindings, expression.patterns, tS, expr=node.expr)
                child.topLevelExpand(expression.constraints, prolog)
                if prolog.DEBUG:
                    log.debug('Has compatible bindings and no valid optional expansions')
                    log.debug('Newly bound descendants: ')
                    for c in sparql_query._fetchBoundLeaves(child):
                        log.debug('\t%s %s' % (c, c.bound))
                        log.debug(c.bindings)

        else:
            if not isinstance(expression, sparql_query.Query):
                raise AssertionError
                child = expression.top or list(fetchUnionBranchesRoots(expression))
            else:
                child = expression.top
            if isinstance(child, sparql_query._SPARQLNode):
                if node.clash == False and child is not None:
                    node.children.append(child)
                    if prolog.DEBUG:
                        log.debug('Adding %s to %s (a UNION branch)' % (child, node))
            else:
                assert isinstance(child, list)
                for newChild in child:
                    node.children.append(newChild)
                    if prolog.DEBUG:
                        log.debug('Adding %s to %s' % (child, node))

            if prolog.DEBUG:
                print_tree(node)
                log.debug('-------------------')
            for optTree in node.optionalTrees:
                for validLeaf in sparql_query._fetchBoundLeaves(optTree):
                    _ExpandJoin(validLeaf, expression, tripleStore, prolog, optionalTree=True)

    return


class NonSymmetricBinaryOperator(AlgebraExpression):

    def fetchTerminalExpression(self):
        if isinstance(self.right, BasicGraphPattern):
            yield self.right
        else:
            for i in self.right.fetchTerminalExpression():
                yield i


class Join(NonSymmetricBinaryOperator):
    """
    .. sourcecode:: text

        [[(P1 AND P2)]](D,G) = [[P1]](D,G) compat [[P2]](D,G)

        Join(Ω1, Ω2) = { merge(μ1, μ2) | μ1 in Ω1 and μ2 in Ω2, and μ1 and μ2 are                          compatible }

    Pseudocode implementation:

    Evaluate BGP1
    Traverse to leaves (expand and expandOption leaves) of BGP1, set 'rest' to
    triple patterns in BGP2 (filling out bindings).
    Trigger another round of expand / expandOptions (from the leaves)
    """

    def __init__(self, BGP1, BGP2):
        self.left = BGP1
        self.right = BGP2

    def evaluate(self, tripleStore, initialBindings, prolog):
        if prolog.DEBUG:
            log.debug('eval(%s,%s,%s)' % (self, initialBindings, tripleStore.graph))
        if isinstance(self.left, AlgebraExpression):
            left = self.left.evaluate(tripleStore, initialBindings, prolog)
        else:
            left = self.left
        if isinstance(left, BasicGraphPattern):
            bindings = sparql_query._createInitialBindings(left)
            if initialBindings:
                bindings.update(initialBindings)
            if hasattr(left, 'tripleStore'):
                lTS = left.tripleStore
            else:
                lTS = tripleStore
            top = sparql_query._SPARQLNode(None, bindings, left.patterns, lTS, expr=left)
            top.topLevelExpand(left.constraints, prolog)
            _ExpandJoin(top, self.right, tripleStore, prolog)
            return sparql_query.Query(top, tripleStore)
        else:
            assert isinstance(left, sparql_query.Query), repr(left)
            if left.parent1 and left.parent2:
                for union_root in fetchUnionBranchesRoots(left):
                    _ExpandJoin(union_root, self.right, tripleStore, prolog)

            else:
                for b in sparql_query._fetchBoundLeaves(left.top):
                    _ExpandJoin(b, self.right, tripleStore, prolog)

            return left
            return


def _ExpandLeftJoin(node, expression, tripleStore, prolog, optionalTree=False):
    """
    Traverses to the leaves of expansion trees to implement the LeftJoin
    operator
    """
    currExpr = expression
    if prolog.DEBUG:
        log.debug('DFS and LeftJoin expansion of ')
        print_tree(node)
        log.debug('---------------------')
        log.debug(node.bindings)
    for node in walktree(node, optProxies=True):
        if node.clash:
            continue
        assert len(node.children) == 0
        if prolog.DEBUG:
            log.debug('Performing LeftJoin(%s,..)' % node)
        if isinstance(currExpr, AlgebraExpression):
            if prolog.DEBUG:
                log.debug('evaluating B in LeftJoin(A,B)')
                log.debug('passing on bindings to %s\n:%s' % (
                 currExpr, node.bindings.copy()))
            expression = currExpr.evaluate(tripleStore, node.bindings.copy(), prolog)
        else:
            expression = currExpr
        if isinstance(expression, BasicGraphPattern):
            rightBindings = sparql_query._createInitialBindings(expression)
            rightBindings.update(node.bindings)
            optTree = sparql_query._SPARQLNode(None, rightBindings, expression.patterns, tripleStore, expr=expression)
            if prolog.DEBUG:
                log.debug('evaluating B in LeftJoin(A,B) - a BGP: %s' % expression)
                log.debug('Passing on bindings %s' % rightBindings)
            optTree.topLevelExpand(expression.constraints, prolog)
            for proxy in sparql_query._fetchBoundLeaves(optTree):
                proxy.priorLeftJoin = True

        else:
            if prolog.DEBUG:
                log.debug('Attaching previously evaluated node: %s' % expression.top)
            if not isinstance(expression, sparql_query.Query):
                raise AssertionError
                optTree = expression.top or list(fetchUnionBranchesRoots(expression))
            else:
                optTree = expression.top
            if prolog.DEBUG:
                log.debug('Optional tree: %s' % optTree)
            if isinstance(optTree, sparql_query._SPARQLNode):
                if optTree.clash == False and optTree is not None:
                    node.optionalTrees.append(optTree)
                    if prolog.DEBUG:
                        log.debug('Adding %s to %s (a UNION branch)' % (
                         optTree, node.optionalTrees))
            else:
                assert isinstance(optTree, list)
                for newChild in optTree:
                    node.optionalTrees.append(newChild)
                    if prolog.DEBUG:
                        log.debug('Adding %s to %s' % (newChild, node.optionalTrees))

        if prolog.DEBUG:
            log.debug('DFS after LeftJoin expansion ')
            print_tree(node)
            log.debug('---------------------')

    return


class LeftJoin(NonSymmetricBinaryOperator):
    """
    .. code-block:: text

        Let Ω1 and Ω2 be multisets of solution mappings and F a filter. We define:
        LeftJoin(Ω1, Ω2, expr) =
            Filter(expr, Join(Ω1, Ω2)) set-union Diff(Ω1, Ω2, expr)

        LeftJoin(Ω1, Ω2, expr) =
        { merge(μ1, μ2) | μ1 in Ω1 and μ2 in Ω2, and
                          μ1 and μ2 are compatible, and
                          expr(merge(μ1, μ2)) is true }
        set-union
        { μ1 | μ1 in Ω1 and μ2 in Ω2, and
               μ1 and μ2 are not compatible }
        set-union
        { μ1 | μ1 in Ω1and μ2 in Ω2, and μ1 and μ2 are compatible and
               expr(merge(μ1, μ2)) is false }

    """

    def __init__(self, BGP1, BGP2, expr=None):
        self.left = BGP1
        self.right = BGP2

    def evaluate(self, tripleStore, initialBindings, prolog):
        if prolog.DEBUG:
            log.debug('eval(%s,%s,%s)' % (self, initialBindings, tripleStore.graph))
        if isinstance(self.left, AlgebraExpression):
            left = self.left.evaluate(tripleStore, initialBindings, prolog)
        else:
            left = self.left
        if isinstance(left, BasicGraphPattern):
            bindings = sparql_query._createInitialBindings(left)
            if initialBindings:
                bindings.update(initialBindings)
            if hasattr(left, 'tripleStore'):
                tripleStore = left.tripleStore
            top = sparql_query._SPARQLNode(None, bindings, left.patterns, tripleStore, expr=left)
            top.topLevelExpand(left.constraints, prolog)
            for b in sparql_query._fetchBoundLeaves(top):
                _ExpandLeftJoin(b, self.right, tripleStore, prolog)

            return sparql_query.Query(top, tripleStore)
        else:
            assert isinstance(left, sparql_query.Query), repr(left)
            if left.parent1 and left.parent2:
                for union_root in fetchUnionBranchesRoots(left):
                    _ExpandLeftJoin(union_root, self.right, tripleStore, prolog)

            else:
                for b in sparql_query._fetchBoundLeaves(left.top):
                    _ExpandLeftJoin(b, self.right, tripleStore, prolog)

            return left
            return


class Union(AlgebraExpression):
    """
    II. [[(P1 UNION P2)]](D,G) = [[P1]](D,G) OR [[P2]](D,G)

    Union(Ω1, Ω2) = { μ | μ in Ω1 or μ in Ω2 }

    """

    def __init__(self, BGP1, BGP2):
        self.left = BGP1
        self.right = BGP2

    def fetchTerminalExpression(self):
        for item in [self.left, self.right]:
            if isinstance(item, BasicGraphPattern):
                yield item
            else:
                for i in item.fetchTerminalExpression():
                    yield i

    def evaluate(self, tripleStore, initialBindings, prolog):
        if prolog.DEBUG:
            log.debug('eval(%s,%s,%s)' % (self, initialBindings, tripleStore.graph))
        if isinstance(self.left, AlgebraExpression):
            left = self.left.evaluate(tripleStore, initialBindings, prolog)
        else:
            left = self.left
        if isinstance(left, BasicGraphPattern):
            bindings = sparql_query._createInitialBindings(left)
            if initialBindings:
                bindings.update(initialBindings)
            top = sparql_query._SPARQLNode(None, bindings, left.patterns, tripleStore, expr=left)
            top.topLevelExpand(left.constraints, prolog)
            top = sparql_query.Query(top, tripleStore)
        else:
            assert isinstance(left, sparql_query.Query), repr(left)
            top = left
        if isinstance(self.right, AlgebraExpression):
            right = self.right.evaluate(tripleStore, initialBindings, prolog)
        else:
            right = self.right
        tS = tripleStore
        if isinstance(right, BasicGraphPattern):
            if hasattr(right, 'tripleStore'):
                tS = right.tripleStore
            rightBindings = sparql_query._createInitialBindings(right)
            if initialBindings:
                rightBindings.update(initialBindings)
            rightNode = sparql_query._SPARQLNode(None, rightBindings, right.patterns, tS, expr=right)
            rightNode.topLevelExpand(right.constraints, prolog)
        else:
            assert isinstance(right, sparql_query.Query), repr(right)
            rightNode = right.top
        return top + sparql_query.Query(rightNode, tS)


class GraphExpression(AlgebraExpression):
    """
    .. sourcecode:: text

        [24] GraphGraphPattern ::=  'GRAPH'  VarOrIRIref  GroupGraphPattern
        eval(D(G), Graph(IRI,P)) = eval(D(D[i]), P)
        eval(D(G), Graph(var,P)) =
            multiset-union over IRI i in D : Join( eval(D(D[i]), P) , Omega(?v->i) )

    """

    def __init__(self, iriOrVar, GGP):
        self.iriOrVar = iriOrVar
        self.GGP = GGP

    def __repr__(self):
        return 'Graph(%s,%s)' % (self.iriOrVar, self.GGP)

    def fetchTerminalExpression(self):
        if isinstance(self.GGP, BasicGraphPattern):
            yield self.GGP
        else:
            for i in self.GGP.fetchTerminalExpression():
                yield i

    def evaluate(self, tripleStore, initialBindings, prolog):
        """
        The GRAPH keyword is used to make the active graph one of all of the
        named graphs in the dataset for part of the query.
        """
        if prolog.DEBUG:
            log.debug('eval(%s,%s,%s)' % (self, initialBindings, tripleStore.graph))
        if isinstance(self.iriOrVar, Variable):
            if self.iriOrVar in initialBindings:
                if prolog.DEBUG:
                    log.debug('Passing on unified graph name: %s' % initialBindings[self.iriOrVar])
                tripleStore = graph.SPARQLGraph(Graph(tripleStore.graph.store, initialBindings[self.iriOrVar]), dSCompliance=DAWG_DATASET_COMPLIANCE)
            else:
                if prolog.DEBUG:
                    log.debug('Setting up BGP to return additional bindings for %s' % self.iriOrVar)
                tripleStore = graph.SPARQLGraph(tripleStore.graph, graphVariable=self.iriOrVar, dSCompliance=DAWG_DATASET_COMPLIANCE)
        else:
            graphName = self.iriOrVar
            graphName = convertTerm(graphName, prolog)
            if isinstance(tripleStore.graph, ReadOnlyGraphAggregate):
                targetGraph = [ g for g in tripleStore.graph.graphs if g.identifier == graphName ]
                targetGraph = targetGraph[0]
            else:
                targetGraph = Graph(tripleStore.graph.store, graphName)
            tripleStore = graph.SPARQLGraph(targetGraph, dSCompliance=DAWG_DATASET_COMPLIANCE)
        if isinstance(self.GGP, AlgebraExpression):
            return self.GGP.evaluate(tripleStore, initialBindings, prolog)
        else:
            assert isinstance(self.GGP, BasicGraphPattern), repr(self.GGP)
            self.GGP.tripleStore = tripleStore
            return self.GGP


if __name__ == '__main__':
    unittest.main()