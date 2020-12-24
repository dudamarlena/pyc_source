# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/shrubbery/template.py
# Compiled at: 2007-08-21 17:53:26
"""
Shrubbery is a Smart Html Renderer (Using Blocks to Bind Expressions
RepeatedlY).

This is a simple templating engine designed to convert JSON_ data
into HTML or XML. The idea behind it is that templates are very
simple, containing only HTML tags, with nodes being repeated as
required by the number of elements in the data.

_JSON: http://json.org/

"""
import re, cgi, sgmllib
sgmllib.entityref = re.compile('[^\\W\\w]')
from BeautifulSoup import BeautifulSoup, NavigableString
TOKEN = '([\\w_:-]+)(\\[\\d+\\])*'
EXPR = re.compile('\\{(%s(\\.%s)*)\\}' % (TOKEN, TOKEN))

class Template(BeautifulSoup):
    """A Shrubbery template.

    Shrubbery is a smart template that holds *no logic* whatsoever,
    with behavior being dictated by the data.

    """

    def process(self, data, remove_empty_nodes=True, escape=True):
        """Process the template given some data.

        Here, ``data`` should be a dict-like object with the variables
        to be replaced. If ``escape`` is true, any HTML in the data
        will be escaped before the replacement.

        The option ``remove_empty_nodes`` will remove nodes with
        replacements not present in ``data``.
        """
        nstree = _get_namespaces(self)
        tree = search(self.copy(), data, '', nstree, remove_empty_nodes, escape)
        tree = apply(tree, '%SHRUBBERY_OPEN_TAG%', '{')
        tree = apply(tree, '%SHRUBBERY_CLOSE_TAG%', '}')
        return tree

    render = process

    def copy(self):
        """A lazy and *costy* copy of the template."""
        return Template(unicode(self))


def search(tree, data, ns, nstree, remove_empty_nodes, escape):
    """
    Search for all expressions inside a given namespace.

    This function finds all expressions inside a given namespace
    (say, ``entry`` or ``collection.id``). After that it locates
    the uppermost node common to all nodes, and replicates it
    according to the number of elements in the applied data. Each
    node is then processed to replace the expressions with the
    proper values.

    """
    regexp = re.compile('\\{%s.*\\}' % re.escape(ns.rstrip('.')))
    nodes = tree.findAll(replaceable(regexp)) + tree.findAll(text=regexp)
    if not nodes:
        return tree
    node = find_common_node(nodes)
    parent = node.parent
    index = parent.contents.index(node)
    if not isinstance(data, list):
        data = [data]
    data = [ v for v in data if v not in [None, {}, []] ]
    for (i, values) in enumerate(data):
        repl = apply(clone(node), '\\{%s\\}' % re.escape(ns.rstrip('.')), values, escape)
        parent.insert(index + i, repl)
        keys = nstree.keys()
        keys.sort()
        keys.reverse()
        for k in keys:
            new_ns = '%s%s.' % (ns, k)
            new_nstree = nstree.get(k)
            indexes = re.match(TOKEN, k)
            (k, slice_) = indexes.groups()
            try:
                subdata = values.get(k)
            except:
                subdata = getattr(values, k, None)

            if slice_ and subdata:
                subdata = subdata[int(slice_[1:-1])]
            repl = search(repl, subdata, new_ns, new_nstree, remove_empty_nodes, escape)

    if data or remove_empty_nodes:
        node.extract()
    return tree


def apply(tree, match, data, escape=False):
    """
    Apply replacement in expressions.

    This function replaces the expressions with the values in ``data``.

    """
    regexp = re.compile(match)
    nodes = tree.findAll(replaceable(regexp)) + tree.findAll(text=regexp)
    if isinstance(data, (int, long, float)):
        data = unicode(data)
    elif isinstance(data, str):
        data = data.decode('utf-8')
    elif not isinstance(data, unicode):
        data = ''
    data = EXPR.sub(lambda m: '%%SHRUBBERY_OPEN_TAG%%%s%%SHRUBBERY_CLOSE_TAG%%' % m.group(1), data)
    if escape:
        text = cgi.escape(data)
    else:
        text = data
    for node in nodes:
        if isinstance(node, NavigableString):
            repl = regexp.sub(text, node.string)
            if node.parent:
                node.replaceWith(repl)
        else:
            if node.string:
                node.string = regexp.sub(text, node.string)
            for (k, v) in node.attrs:
                node[k] = regexp.sub(data, v).strip()
                if not node[k]:
                    del node[k]

    return tree


def find_common_node(nodes):
    """
    Return the lowest node in common given a list of nodes.

    Given the nodes in ``nodes``, this function returns the
    lowest parent in common to all nodes.

    """
    if len(nodes) == 1:
        return nodes[0]
    parents = [ [node] + node.findParents() for node in nodes ]
    parents.sort(key=len)
    for candidate in parents.pop(0):
        for other_parents in parents:
            if candidate not in other_parents:
                break
        else:
            return candidate


def _get_namespaces(soup):
    """
    Get all namespaces from the template.

    This function searches ``soup`` for all namespaces, and returns
    them as a nested dict. A template like this::

        <html>
            <div id="{entry.id}"></div>
        </html>

    Would return ``{u'entry': {u'id': {}}}``, eg.

    """
    namespaces = {}
    nodes = soup.findAll(replaceable(EXPR)) + soup.findAll(text=EXPR)
    for node in nodes:
        for ns in EXPR.findall(node.string or ''):
            ns = ns[0].split('.')
            root = namespaces
            for item in ns:
                root = root.setdefault(item, {})

        if hasattr(node, 'attrs'):
            for (k, v) in node.attrs:
                for ns in EXPR.findall(v):
                    ns = ns[0].split('.')
                    root = namespaces
                    for item in ns:
                        root = root.setdefault(item, {})

    return namespaces


def clone(node):
    """
    Clone a node.

    We simply parse the HTML from ``node`` to be copied. Yes, I'm lazy.

    """
    return Template(unicode(node))


def replaceable(regexp=EXPR):
    """
    Return function to find nodes that are replaceable in a given namespace.

    Given a namespace defined by ``regexp``, this function returns
    a callable that can be used in ``findAll`` to search for
    corresponding nodes.

    """

    def func(tag):
        """Check both text and attributes for ``regexp``."""
        if tag.string and regexp.search(tag.string):
            return True
        for (k, v) in tag.attrs:
            if regexp.search(v):
                return True

        return False

    return func