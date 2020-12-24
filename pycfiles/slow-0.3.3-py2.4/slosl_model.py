# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/slosl_model.py
# Compiled at: 2006-01-10 04:15:14
import re, operator, os
from itertools import *
__all__ = ('RankingFunction', 'SloslStatement', 'SLOSL_NAMESPACE_URI')
SLOSL_NAMESPACE_URI = 'http://www.dvs1.informatik.tu-darmstadt.de/research/OverML/slosl'
SLOSL_NAMESPACE_DICT = {'slosl': SLOSL_NAMESPACE_URI}
from StringIO import StringIO
from lxml import etree
from lxml.etree import ElementTree, Element, SubElement
from xpathmodel import XPathModel, XPathModelHelper, result_filter, autoconstruct, get_first
from mathml.lmathdom import MathDOM
from slow.schema import SCHEMAS
__statements_tag = '{%s}statements' % SLOSL_NAMESPACE_URI

def buildStatements():
    return Element(__statements_tag)


__statement_tag = '{%s}statement' % SLOSL_NAMESPACE_URI

def buildStatement(statements=None):
    if statements:
        element = SubElement(statements, __statement_tag)
    else:
        element = Element(__statement_tag)
    SubElement(element, '{%s}buckets' % SLOSL_NAMESPACE_URI)
    return element


EMPTY_MODEL = Element(__statements_tag)
SLOSL_RNG_SCHEMA = SCHEMAS['slosl']

def _build_named_attribute(name, *args):
    return XPathModelHelper._build_referenced_access(('{%s}%s' % (SLOSL_NAMESPACE_URI, name)), 'name', *args)


def _build_slosl_tree_node(name, *args):
    return XPathModelHelper._build_tree_node(('{%s}%s' % (SLOSL_NAMESPACE_URI, name)), *args)


class SloslElement(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = SLOSL_NAMESPACE_URI


class SloslStatements(SloslElement):
    __module__ = __name__
    DEFAULT_ROOT_NAME = 'statements'
    DOCUMENT_SCHEMA = SLOSL_RNG_SCHEMA.copy(start='slosl_statements')
    _get_names = './{%(DEFAULT_NAMESPACE)s}statement/@name'

    def _get_statements(self):
        """./{%(DEFAULT_NAMESPACE)s}statement"""
        pass

    def _get_statement(self, _xpath_result, name):
        """./{%(DEFAULT_NAMESPACE)s}statement[@name = $name]"""
        if _xpath_result:
            node = _xpath_result[0]
        else:
            node = SubElement(self, '{%s}statement' % SLOSL_NAMESPACE_URI, name=name)
        return node

    def _set_statement(self, _xpath_result, name, statement):
        """./{%(DEFAULT_NAMESPACE)s}statement[@name = $name]"""
        if statement.tag != '{%s}statement' % SLOSL_NAMESPACE_URI:
            raise ValueError, 'Invalid statement element.'
        for old_node in _xpath_result:
            self.remove(old_node)

        self.append(statement)

    def _del_statement(self, name):
        """./{%(DEFAULT_NAMESPACE)s}statement[@name = $name]"""
        pass

    def _strip(self):
        for statement in self.statements:
            if not statement.name:
                self.remove(statement)
            else:
                statement._strip()


class RankingFunction(SloslElement):
    __module__ = __name__
    DEFAULT_ROOT_NAME = 'ranked'
    FUNCTIONS = {'lowest': 2, 'highest': 2, 'closest': 3, 'furthest': 3}
    _get_function = 'string(./@function)'

    def _set_function(self, name):
        arg_count = self.FUNCTIONS[name]
        self.set('function', name)
        while len(self) < arg_count:
            SubElement(self, '{%s}parameter' % SLOSL_NAMESPACE_URI)

        while len(self) > arg_count:
            del self[-1]

    _get_name, _set_name = _get_function, _set_function
    _get_parameterCount = 'count(./{%(DEFAULT_NAMESPACE)s}parameter)'

    def _get_parameters(self, _xpath_result):
        """./{%(DEFAULT_NAMESPACE)s}parameter/*"""
        return _xpath_result

    def function_parameter_count(self):
        return self.FUNCTIONS[self.get('function')]

    @get_first
    def _get_parameter(self, i):
        """./{%(DEFAULT_NAMESPACE)s}parameter[$i+1]/*"""
        pass

    def _set_parameter(self, _xpath_result, i, value_node):
        """./{%(DEFAULT_NAMESPACE)s}parameter[$i+1]"""
        arg_count = self.FUNCTIONS[self.get('function')]
        if _xpath_result:
            parent = _xpath_result[0]
        elif i < arg_count:
            while len(self) <= i:
                parent = SubElement(self, '{%s}parameter' % SLOSL_NAMESPACE_URI)

        else:
            raise IndexError, 'Maximum %s parameters allowed.' % arg_count
        parent.clear()
        parent.append(value_node)


class SloslStatement(SloslElement):
    __module__ = __name__
    DEFAULT_ROOT_NAME = 'statement'
    DOCUMENT_SCHEMA = SLOSL_RNG_SCHEMA.copy(start='slosl_statement')
    (_get_where, _set_where, _del_where) = _build_slosl_tree_node('where')
    (_get_having, _set_having, _del_having) = _build_slosl_tree_node('having')
    (_get_select, _set_select, _del_select, _get_selects, _del_selects) = _build_named_attribute('select')
    (_get_with, _set_with, _del_with, _get_withs, _del_withs) = _build_named_attribute('with')
    (_get_foreach, _set_foreach, _del_foreach, _get_foreachs, _del_foreachs) = _build_named_attribute('foreach', '/{%s}buckets' % SLOSL_NAMESPACE_URI)
    _get_view = 'string(./@name)'

    def _set_view(self, name):
        self.set('name', name)

    _get_name, _set_name = _get_view, _set_view
    _attr_selected = 'bool#./@selected'

    def _set_parent(self, _xpath_result, parent):
        """./{%(DEFAULT_NAMESPACE)s}parent[string(.) = normalize-space($parent)]"""
        if not _xpath_result:
            node = SubElement(self, '{%s}parent' % SLOSL_NAMESPACE_URI)
            node.text = parent.strip()

    def _get_parents(self, _xpath_result):
        """./{%(DEFAULT_NAMESPACE)s}parent/text()"""
        return map(unicode, _xpath_result)

    def _set_parents(self, parent_list):
        parent_list = [ name.strip() for name in parent_list ]
        parent_tag = '{%s}parent' % SLOSL_NAMESPACE_URI
        for child in self[:]:
            if child.tag == parent_tag:
                name = child.text
                try:
                    parent_list.remove(name)
                except ValueError:
                    self.remove(child)

        for name in parent_list:
            child = SubElement(self, parent_tag)
            child.text = name

    _del_parents = './{%(DEFAULT_NAMESPACE)s}parent'

    @get_first
    @autoconstruct('.', '{%s}ranked' % SLOSL_NAMESPACE_URI)
    def _get_ranked(self):
        """./{%(DEFAULT_NAMESPACE)s}ranked"""
        pass

    _del_ranked = './{%(DEFAULT_NAMESPACE)s}ranked'

    @result_filter(bool)
    def _get_bucket(self):
        """./{%(DEFAULT_NAMESPACE)s}buckets[@inherit = 'true'] or not(./{%(DEFAULT_NAMESPACE)s}buckets)"""
        pass

    @autoconstruct('.', '{%(DEFAULT_NAMESPACE)s}buckets')
    def _set_bucket(self, _xpath_result, value):
        """./{%(DEFAULT_NAMESPACE)s}buckets"""
        node = _xpath_result[0]
        if value:
            str_val = 'true'
            node.clear()
        else:
            str_val = 'false'
        node.set('inherit', str_val)


ns = etree.Namespace(SLOSL_NAMESPACE_URI)
ns[None] = SloslElement
ns['statements'] = SloslStatements
ns['statement'] = SloslStatement
ns['ranked'] = RankingFunction
if __name__ == '__main__':
    from mathml import MATHML_NAMESPACE_URI
    slosl_xml = '\n  <slosl:statements xmlns:slosl="%s" xmlns:m="%s">\n    <slosl:statement name="chord_last_neighbour" selected="true">\n      <slosl:select name="id"><m:ci>node.id</m:ci></slosl:select>\n      <slosl:select name="local_dist"><m:ci>node.local_dist</m:ci></slosl:select>\n      <slosl:parent>chord_neighbours</slosl:parent>\n      <slosl:ranked function="highest">\n        <slosl:parameter><m:cn type="integer">1</m:cn></slosl:parameter>\n        <slosl:parameter><m:ci>node.local_dist</m:ci></slosl:parameter>\n      </slosl:ranked>\n      <slosl:where>\n        <m:apply><m:eq/><m:ci>node.side</m:ci><m:cn type="integer">1</m:cn></m:apply>\n      </slosl:where>\n      <slosl:buckets inherit="true"/>\n    </slosl:statement>\n\n    <slosl:statement name="chord_fingertable" selected="true">\n      <slosl:select name="id"><m:ci>node.id</m:ci></slosl:select>\n      <slosl:parent>db</slosl:parent>\n      <slosl:ranked function="highest">\n        <slosl:parameter><m:cn type="integer">1</m:cn></slosl:parameter>\n        <slosl:parameter><m:ci>node.id</m:ci></slosl:parameter>\n      </slosl:ranked>\n      <slosl:with name="log_k"><m:cn type="integer">160</m:cn></slosl:with>\n      <slosl:with name="max_id">\n        <m:apply><m:power/><m:cn type="integer">2</m:cn><m:ci>log_k</m:ci></m:apply>\n      </slosl:with>\n      <slosl:where>\n        <m:apply><m:and/><m:apply><m:eq/><m:ci>node.knows_chord</m:ci><m:true/></m:apply><m:apply><m:eq/><m:ci>node.alive</m:ci><m:true/></m:apply></m:apply>\n      </slosl:where>\n      <slosl:having>\n        <m:apply><m:in/><m:ci>node.id</m:ci><m:list><m:apply><m:power/><m:cn type="integer">2</m:cn><m:ci>i</m:ci></m:apply><m:apply><m:power/><m:cn>2</m:cn><m:apply><m:plus/><m:ci>i</m:ci><m:cn type="integer">1</m:cn></m:apply></m:apply></m:list></m:apply>\n      </slosl:having>\n      <slosl:buckets>\n        <slosl:foreach name="i">\n          <m:interval closure="closed-open"><m:cn type="integer">0</m:cn><m:ci>log_k</m:ci></m:interval>\n        </slosl:foreach>\n      </slosl:buckets>\n    </slosl:statement>\n  </slosl:statements>\n' % (SLOSL_NAMESPACE_URI, MATHML_NAMESPACE_URI)
    doc = ElementTree(file=StringIO(slosl_xml))
    import sys
    statements = doc.getroot()
    statements._pretty_print()
    print
    print statements.validate() and 'Valid' or 'Invalid'