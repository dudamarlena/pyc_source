# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/process_includes.py
# Compiled at: 2020-04-21 18:19:58
# Size of source mod 2**32: 31393 bytes
"""
    python %prog [options] <in_schema.xsd>  [<out_schema.xsd>]
Synopsis:
    Prepare schema document.  Replace include and import elements.
    Read from in_schema or stdin.  Write to out_schema or stdout.
Examples:
    python %prog myschema.xsd
    python %prog myschema.xsd newschema.xsd
    python %prog -f myschema.xsd newschema.xsd
    cat infile.xsd | python %prog > outfile.xsd
"""
from __future__ import print_function
import sys, os, copy
from optparse import OptionParser, Values
import itertools
from copy import deepcopy
from lxml import etree
import requests
try:
    from gds_inner_name_map import Inner_name_map
except ImportError:
    Inner_name_map = None

VERSION = '2.35.20'
CatalogDict = {}
CatalogBaseUrl = None
XSDNameSpace = 'http://www.w3.org/2001/XMLSchema'
BuiltinSimpleTypeNames = [
 'string',
 'boolean',
 'float',
 'double',
 'decimal',
 'duration',
 'dateTime',
 'time',
 'date',
 'gYearMonth',
 'gYear',
 'gMonthDay',
 'gDay',
 'gMonth',
 'hexBinary',
 'base64Binary',
 'anyURI',
 'QName',
 'NOTATION',
 'normalizedString',
 'token',
 'language',
 'IDREFS',
 'ENTITIES',
 'NMTOKEN',
 'NMTOKENS',
 'Name',
 'NCName',
 'ID',
 'IDREF',
 'ENTITY',
 'integer',
 'nonPositiveInteger',
 'negativeInteger',
 'long',
 'int',
 'short',
 'byte',
 'nonNegativeInteger',
 'unsignedLong',
 'unsignedInt',
 'unsignedShort',
 'unsignedByte',
 'positiveInteger',
 'yearMonthDuration',
 'dayTimeDuration',
 'dateTimeStamp']

class SchemaIOError(IOError):
    __doc__ = 'Exception definition'


class InnerNameMapError(Exception):
    __doc__ = 'Exception definition'


class RenameData(object):
    __doc__ = 'A structure used to carry parameters.'
    __slots__ = ('global_names', 'global_count', 'modified_elements', 'name_mappings')

    def __init__(self, global_names=None, global_count=0, modified_elements=None, name_mappings=None):
        if global_names is None:
            self.global_names = set()
        else:
            self.global_names = global_names
        self.global_count = global_count
        if modified_elements is None:
            self.modified_elements = set()
        else:
            self.modified_elements = modified_elements
        if name_mappings is None:
            self.name_mappings = {}
        else:
            self.name_mappings = name_mappings

    def __str__(self):
        s1 = '<RenameData at {}\n    global_names: {}\n    global_count: {}\n    modified_elements: {}\n    name_mappings: {}\n>'.format(id(self), self.global_names, self.global_count, self.modified_elements, self.name_mappings)
        return s1


def load_catalog(catalogpath):
    """Load the catalog base URL and save in global variable."""
    global CatalogBaseUrl
    if catalogpath:
        CatalogBaseUrl = os.path.split(catalogpath)[0]
        catalog = etree.parse(open(catalogpath, 'rb'))
        for elements in catalog.getroot().findall('{urn:oasis:names:tc:entity:xmlns:xml:catalog}public'):
            CatalogDict[elements.get('publicId')] = elements.get('uri')


def process_include_files(infile, outfile, inpath='', catalogpath=None, fixtypenames=None, no_collect_includes=False, no_redefine_groups=False):
    """The root/main function"""
    load_catalog(catalogpath)
    options = Values({'force':False, 
     'fixtypenames':fixtypenames, 
     'no_collect_includes':no_collect_includes, 
     'no_redefine_groups':no_redefine_groups})
    doc, ns_dict, schema_ns_dict, rename_data = prep_schema_doc(infile, outfile, inpath, options)
    return (doc, ns_dict, schema_ns_dict, rename_data)


def get_all_root_file_paths(infile, inpath='', catalogpath=None, shallow=False):
    """Get the file path for all imported and included schema files."""
    if inpath.startswith('/'):
        inpath = os.path.relpath(inpath)
    load_catalog(catalogpath)
    doc1 = etree.parse(infile)
    root1 = doc1.getroot()
    rootPaths = []
    params = Params()
    params.parent_url = infile
    params.base_url = os.path.split(inpath)[0]
    get_root_file_paths(root1, params, rootPaths, shallow)
    rootPaths.append(inpath)
    return rootPaths


class Params(object):
    __doc__ = 'A structure used to carry parameters.'
    members = ('base_url', 'already_processed', 'parent_url')

    def __init__(self):
        self.base_url = None
        self.already_processed = set()
        self.parent_url = None

    def __setattr__(self, name, value):
        if name not in self.members:
            raise AttributeError('Class %s has no set-able attribute "%s"' % (
             self.__class__.__name__, name))
        self.__dict__[name] = value


def clear_includes_and_imports(node):
    namespace = node.nsmap[node.prefix]
    child_iter1 = node.iterfind('{%s}include' % (namespace,))
    child_iter2 = node.iterfind('{%s}import' % (namespace,))
    for child in itertools.chain(child_iter1, child_iter2):
        repl = etree.Comment(etree.tostring(child))
        repl.tail = '\n'
        node.replace(child, repl)


def get_ref_info(node, params):
    namespace = node.get('namespace')
    url = None
    baseUrl = None
    if namespace in CatalogDict:
        url = CatalogDict[namespace]
        baseUrl = CatalogBaseUrl
    if not url:
        url = node.get('schemaLocation')
    if not url:
        msg = '*** Warning: missing "schemaLocation" attribute in %s\n' % (
         params.parent_url,)
        sys.stderr.write(msg)
        return (None, None)
    if not baseUrl:
        baseUrl = params.base_url
    elif baseUrl:
        locn = url.startswith('/') or url.startswith('http:') or url.startswith('ftp:') or '%s/%s' % (baseUrl, url)
        schema_name = locn
    else:
        locn = url
        schema_name = url
    return (
     locn, schema_name)


def resolve_ref(node, params, options):
    content = None
    locn, schema_name = get_ref_info(node, params)
    if locn is not None:
        if not locn.startswith('/'):
            if not locn.startswith('http:'):
                if not locn.startswith('ftp:'):
                    schema_name = os.path.abspath(locn)
    if locn is not None:
        if schema_name not in params.already_processed:
            params.already_processed.add(schema_name)
            if locn.startswith('http:') or locn.startswith('ftp:'):
                try:
                    headers = {'User-Agent': "Mozilla/5.0 (X11; 'Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "}
                    content = requests.get(locn, headers=headers).content
                    params.parent_url = locn
                    params.base_url = os.path.split(locn)[0]
                except requests.exceptions.HTTPError:
                    msg = "Can't find file %s referenced in %s." % (
                     locn, params.parent_url)
                    raise SchemaIOError(msg)

            else:
                if os.path.exists(locn):
                    if sys.version_info.major == 2:
                        infile = open(locn)
                        unencoded_content = infile.read()
                        content = unencoded_content
                    else:
                        infile = open(locn, 'rb')
                        content = infile.read()
                    infile.close()
                    params.parent_url = locn
                    params.base_url = os.path.split(locn)[0]
                if content is None:
                    msg = "Can't find file %s referenced in %s." % (
                     locn, params.parent_url)
                    raise SchemaIOError(msg)
    return content


def get_fixed_schema_nsmap(node, prefix='xs'):
    """Fix namespace map -- remove (key) None; add key 'xs' --> schema NS."""
    nsmap = node.nsmap
    namespace = XSDNameSpace
    if None in nsmap:
        nsmap.pop(None)
    if 'xsd' in nsmap:
        if prefix != 'xsd':
            namespace = nsmap.pop('xsd')
    if prefix not in nsmap:
        nsmap[prefix] = namespace
    return nsmap


def collect_inserts(node, params, inserts, ns_dict, schema_ns_dict, rename_data, options):
    """Collect all the schemas (imported and included).
    If there are duplicate unqualified names, rename all but one, and
    collect a dictionary of the renamed names."""
    nsmap = get_fixed_schema_nsmap(node)
    roots = []
    child_iter1 = node.iterfind('xs:include', namespaces=nsmap)
    child_iter2 = node.iterfind('xs:import', namespaces=nsmap)
    for child in itertools.chain(child_iter1, child_iter2):
        aux_roots = collect_inserts_aux(child, params, inserts, ns_dict, schema_ns_dict, rename_data, options)
        roots.extend(aux_roots)

    return roots


def collect_inserts_aux(child, params, inserts, ns_dict, schema_ns_dict, rename_data, options):
    """A helper function."""
    roots = []
    save_base_url = params.base_url
    string_content = resolve_ref(child, params, options)
    if string_content is not None:
        root = etree.fromstring(string_content, base_url=(params.base_url))
        make_names_unique(root, rename_data, options)
        roots.append(root)
        schema_ns_dict.update(root.nsmap)
        update_ns_dict(root, ns_dict, options)
        for child1 in root:
            namespace = isinstance(child1, etree._Comment) or child1.nsmap[child1.prefix]
            if child1.tag != '{%s}include' % (namespace,) and child1.tag != '{%s}import' % (namespace,):
                comment = etree.Comment(etree.tostring(child))
                comment.tail = '\n'
                inserts.append(comment)
                inserts.append(child1)

        insert_roots = collect_inserts(root, params, inserts, ns_dict, schema_ns_dict, rename_data, options)
        roots.extend(insert_roots)
    params.base_url = save_base_url
    return roots


def make_map_name(root, name):
    target_namespace = root.get('targetNamespace')
    if target_namespace is not None:
        qname = '{%s}%s' % (target_namespace, name)
    else:
        qname = name
    return qname


def make_names_unique(root, rename_data, options):
    """If there are duplicate names, rename each to something unique."""
    nsmap = get_fixed_schema_nsmap(root)
    ct_defs = root.xpath('./xs:complexType', namespaces=nsmap)
    st_defs = root.xpath('./xs:simpleType', namespaces=nsmap)
    for type_def in itertools.chain(ct_defs, st_defs):
        name = type_def.get('name')
        map_name = make_map_name(root, name)
        if name in rename_data.global_names:
            new_name = unique_name(name, rename_data)
            if new_name != name:
                type_def.attrib['name'] = new_name
                rename_data.modified_elements.add(type_def)
        else:
            new_name = name
        if new_name != name:
            rename_data.name_mappings[map_name] = new_name
        rename_data.global_names.add(name)


def update_ns_dict(root, ns_dict, options):
    """Update the namespace dictionary with the target namespace prefix,
    if there is one, for each global xs:element and xs:complexType.
    """
    if 'targetNamespace' in root.attrib:
        namespace = root.get('targetNamespace')
        defs = [nsdef for nsdef in root.nsmap.items() if nsdef[1] == namespace]
        if defs:
            prefix = defs[0][0]
            nsmap = {'xs': XSDNameSpace}
            items1 = root.xpath('./xs:complexType', namespaces=nsmap)
            items2 = root.xpath('./xs:element', namespaces=nsmap)
            names = [item.get('name') for item in items1] + [item.get('name') for item in items2]
            for name in names:
                ns_dict[name] = (
                 prefix, namespace)


def get_root_file_paths(node, params, rootPaths, shallow):
    """Get the file path for all imported and included schema files."""
    namespace = node.nsmap[node.prefix]
    child_iter1 = node.iterfind('{%s}include' % (namespace,))
    child_iter2 = node.iterfind('{%s}import' % (namespace,))
    for child in itertools.chain(child_iter1, child_iter2):
        get_root_file_paths_aux(child, params, rootPaths, shallow)


def get_root_file_paths_aux(child, params, rootPaths, shallow):
    """Helper function"""
    save_base_url = params.base_url
    path, _ = get_ref_info(child, params)
    string_content = resolve_ref(child, params, None)
    if string_content is not None:
        if not shallow:
            root = etree.fromstring(string_content, base_url=(params.base_url))
            get_root_file_paths(root, params, rootPaths, shallow)
    if path is not None:
        if path not in rootPaths:
            rootPaths.append(path)
    params.base_url = save_base_url


def make_file(outFileName, options):
    outFile = None
    if not options.force:
        if os.path.exists(outFileName):
            if sys.version_info.major == 3:
                raw_input = input
            reply = raw_input('File %s exists.  Overwrite? (y/n): ' % outFileName)
            if reply == 'y':
                outFile = open(outFileName, 'w')
    else:
        outFile = open(outFileName, 'w')
    return outFile


def prep_schema_doc(infile, outfile, inpath, options):
    if inpath.startswith('/'):
        inpath = os.path.relpath(inpath)
    else:
        doc1 = etree.parse(infile)
        root1 = doc1.getroot()
        params = Params()
        params.parent_url = infile
        params.base_url = os.path.split(inpath)[0]
        inserts = []
        ns_dict = {}
        schema_ns_dict = {}
        rename_data = RenameData()
        schema_ns_dict.update(root1.nsmap)
        if not options.no_collect_includes:
            collect_inserts(root1, params, inserts, ns_dict, schema_ns_dict, rename_data, options)
            make_names_unique(root1, rename_data, options)
            fixup_refs(root1, inserts, rename_data)
            fixup_refs(root1, root1.getchildren(), rename_data)
            root2 = copy.copy(root1)
            clear_includes_and_imports(root2)
            for insert_node in inserts:
                root2.append(insert_node)

        else:
            root2 = root1
        if not options.no_redefine_groups:
            process_groups(root2)
        raise_anon_complextypes(root2, rename_data)
        fix_type_names(root2, options)
        doc2 = etree.ElementTree(root2)
        if sys.version_info.major == 2:
            doc2.write(outfile)
        else:
            outfile.write(etree.tostring(root2).decode('utf-8'))
    return (
     doc2, ns_dict, schema_ns_dict, rename_data)


def prep_schema(inpath, outpath, options):
    if inpath:
        infile = open(inpath, 'rb')
    else:
        infile = sys.stdin
    if outpath:
        outfile = make_file(outpath, options)
    else:
        outfile = sys.stdout
    if outfile is None:
        return
    prep_schema_doc(infile, outfile, inpath, options)
    if inpath:
        infile.close()
    if outpath:
        outfile.close()


def process_groups(root):
    """Get all the xs:group definitions at top level."""
    if root.prefix:
        namespaces = {root.prefix: root.nsmap[root.prefix]}
        pattern = './%s:group' % (root.prefix,)
        defs = root.xpath(pattern, namespaces=namespaces)
    else:
        pattern = './group'
        defs = root.xpath(pattern)
    defs = [node for node in defs if node.get('name') is not None]
    if root.prefix:
        namespaces = {root.prefix: root.nsmap[root.prefix]}
        pattern = './*//%s:group' % (root.prefix,)
        refs = root.xpath(pattern, namespaces=namespaces)
    else:
        pattern = './*//group'
        refs = root.xpath(pattern)
    refs = [node for node in refs if node.get('ref') is not None]
    def_dict = {}
    for node in defs:
        def_dict[trim_prefix(node.get('name'))] = node

    replace_group_defs(def_dict, refs)


def fix_type_names(root, options):
    """Fix up (complexType) type names."""
    fixnamespec = options.fixtypenames
    if fixnamespec:
        namespecs = fixnamespec.split(';')
    else:
        namespecs = []
    for namespec in namespecs:
        names = namespec.split(':')
        if len(names) == 2:
            oldname = names[0]
            newname = names[1]
        else:
            if len(names) == 1:
                oldname = names[0]
                newname = '%sxx' % (oldname,)
            else:
                continue
            pat = './/%s:complexType[@name="%s"]' % (
             root.prefix, oldname)
            elements = xpath_find(root, pat)
            if len(elements) < 1:
                sys.stderr.write("\nWarning: fix-type-names can't find complexType '%s'.  Exiting.\n\n" % (
                 oldname,))
                sys.exit(1)
            if len(elements) < 1:
                sys.stderr.write("Warning: fix-type-names found more than one complexType '%s'.  Changing first." % (
                 oldname,))
            element = elements[0]
            element.set('name', newname)
            pat = './/%s:element' % (root.prefix,)
            elements = xpath_find(root, pat)
            for element in elements:
                typename = element.get('type')
                if not typename:
                    continue
                names = typename.split(':')
                if len(names) == 2:
                    typename = names[1]
                else:
                    if len(names) == 1:
                        typename = names[0]
                    else:
                        continue
                    if typename != oldname:
                        continue
                if not element.getchildren():
                    element.set('type', newname)

            pat = './/%s:extension' % (root.prefix,)
            elements = xpath_find(root, pat)
            for element in elements:
                typename = element.get('base')
                if not typename:
                    continue
                names = typename.split(':')
                if len(names) == 2:
                    typename = names[1]
                else:
                    if len(names) == 1:
                        typename = names[0]
                    else:
                        continue
                    if typename != oldname:
                        continue
                    element.set('base', newname)


def fixup_refs(root, inserts, rename_data):
    """Fixup/change references for duplicate unqualified names."""
    nsmap = get_fixed_schema_nsmap(root)
    ct_tag = '{{{}}}complexType'.format(nsmap['xs'])
    st_tag = '{{{}}}simpleType'.format(nsmap['xs'])
    for node in inserts:
        if node.tag == ct_tag:
            fixup_refs_complextype(node, rename_data)


def fixup_refs_complextype(complextype, rename_data):
    """Fixup/change references for duplicate unqualified names."""
    nsmap = get_fixed_schema_nsmap(complextype)
    elements = complextype.xpath('.//xs:element', namespaces=nsmap)
    attributes = complextype.xpath('.//xs:attribute', namespaces=nsmap)
    for node in itertools.chain(elements, attributes):
        fixup_refs_complextype_helper(node, 'type', nsmap, rename_data)
        fixup_refs_complextype_helper(node, 'ref', nsmap, rename_data)


def fixup_refs_complextype_helper(node, spec, nsmap, rename_data):
    """Change references for specified attribute, e.g. 'type' or 'ref'."""
    type_name = node.get(spec)
    if type_name:
        prefix, type_name1 = split_prefix(type_name)
        if prefix:
            namespace = nsmap.get(prefix)
            if namespace:
                qname = '{{{}}}{}'.format(namespace, type_name1)
                unique_name = rename_data.name_mappings.get(qname)
                if unique_name:
                    if unique_name != type_name:
                        node.attrib[spec] = unique_name
                        rename_data.modified_elements.add(node)


def fixup_refs_simpletype(simpletype, rename_data):
    """Fixup/change references for duplicate unqualified names."""
    nsmap = get_fixed_schema_nsmap(simpletype)
    restriction = simpletype.xpath('./xs:restriction', namespaces=nsmap)
    if restriction:
        restriction = restriction[0]
        base = restriction.get('base')
        if base:
            prefix, name = split_prefix(base)
            if prefix:
                namespace = nsmap.get(prefix)
                if namespace:
                    qname = '{{{}}}{}'.format(namespace, name)
                    unique_name = rename_data.name_mappings.get(qname)
                    if unique_name:
                        restriction.attrib['base'] = unique_name
                        rename_data.modified_elements.add(restriction)


def xpath_find(node, pat):
    """A helper function for using xpath"""
    namespaces = {node.prefix: node.nsmap[node.prefix]}
    elements = node.xpath(pat, namespaces=namespaces)
    return elements


def replace_group_defs(def_dict, refs):
    """Copy group definitions and replace the reference."""
    for ref_node in refs:
        name = trim_prefix(ref_node.get('ref'))
        if name is None:
            continue
        def_node = def_dict.get(name)
        namespaces = {def_node.prefix: def_node.nsmap[def_node.prefix]}
        if def_node is not None:
            pattern = './%s:sequence|./%s:choice|./%s:all' % (
             def_node.prefix, def_node.prefix, def_node.prefix)
            content = def_node.xpath(pattern,
              namespaces=namespaces)
            if content:
                content = content[0]
                parent = ref_node.getparent()
                for node in content:
                    if not isinstance(node, etree._Comment):
                        new_node = deepcopy(node)
                        value = ref_node.get('minOccurs')
                        if value is not None:
                            new_node.set('minOccurs', value)
                        value = ref_node.get('maxOccurs')
                        if value is not None:
                            new_node.set('maxOccurs', value)
                        ref_node.addprevious(new_node)

                parent.remove(ref_node)


def raise_anon_complextypes(root, rename_data):
    """ Raise each anonymous complexType to top level and give it a name.
    Rename if necessary to prevent duplicates.
    """
    def_names = collect_type_names(root)
    el = etree.Comment(text='Raised anonymous complexType definitions')
    el.tail = '\n\n'
    root.append(el)
    prefix = root.prefix
    if prefix:
        pattern = './*/*//%s:complexType|./*/*//%s:simpleType' % (
         prefix, prefix)
        element_tag = '{%s}element' % (root.nsmap[prefix],)
        namespaces = {prefix: root.nsmap[prefix]}
        defs = root.xpath(pattern, namespaces=namespaces)
        annotation_pattern = './%s:annotation' % (prefix,)
    else:
        pattern = './*/*//complexType|./*/*//simpleType'
        element_tag = 'element'
        defs = root.xpath(pattern)
        annotation_pattern = './annotation'
    for node in defs:
        parent = node.getparent()
        if parent.tag != element_tag:
            continue
        else:
            name = parent.get('name')
            if not name:
                continue
            type_name = '%sType' % (name,)
            if Inner_name_map is None:
                type_name = unique_name(type_name, rename_data)
                rename_data.global_names.add(type_name)
            else:
                type_name = map_inner_name(node, Inner_name_map)
        annotations = parent.xpath(annotation_pattern, namespaces=namespaces)
        for annotation in reversed(annotations):
            type_annotation = deepcopy(annotation)
            node.insert(0, type_annotation)

        def_names.add(type_name)
        parent.set('type', type_name)
        node.set('name', type_name)
        root.append(node)


def map_inner_name(node, inner_name_map):
    """Use a user-supplied mapping table to look up a name for this class/type.
    """
    node1 = node
    name2 = node1.get('name')
    while name2 is None:
        node1 = node1.getparent()
        if node1 is None:
            raise InnerNameMapError('cannot find parent with "name" attribute')
        name2 = node1.get('name')

    node1 = node1.getparent()
    name1 = node1.get('name')
    while name1 is None:
        node1 = node1.getparent()
        if node1 is None:
            raise InnerNameMapError('cannot find parent with "name" attribute')
        name1 = node1.get('name')

    new_name = inner_name_map.get((name1, name2))
    if new_name is None:
        msg1 = '("{}", "{}")'.format(name1, name2)
        sys.stderr.write('\n*** error.  Must add entry to inner_name_map:\n')
        sys.stderr.write('\n    {}: "xxxx",\n\n'.format(msg1))
        raise InnerNameMapError('mapping missing for {}'.format(msg1))
    return new_name


def collect_type_names(node):
    """Collect the names of all currently defined types (complexType,
    simpleType, element).
    """
    prefix = node.prefix
    if prefix is not None and prefix.strip():
        pattern = './/%s:complexType|.//%s:simpleType|.//%s:element' % (
         prefix, prefix, prefix)
        namespaces = {prefix: node.nsmap[prefix]}
        elements = node.xpath(pattern, namespaces=namespaces)
    else:
        pattern = './/complexType|.//simpleType|.//element'
        elements = node.xpath(pattern)
    names = {el.attrib['name'] for el in elements if 'name' in el.attrib if el.getchildren() if el.getchildren()}
    return names


def unique_name(new_name, rename_data):
    """If necessary, create a new name that is not in def_names."""
    orig_name = new_name
    while True:
        if new_name not in rename_data.global_names:
            break
        rename_data.global_count += 1
        new_name = '{}{}'.format(orig_name, rename_data.global_count)

    return new_name


def trim_prefix(name):
    """Trim off the name space prefix."""
    names = name.split(':')
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return names[1]


def split_prefix(name):
    """Split a name into (prefix, name).  Return them."""
    name = name.split(':')
    if len(name) == 1:
        prefix = ''
        name = name[0]
    else:
        if len(name) == 2:
            prefix = name[0]
            name = name[1]
        else:
            prefix = ''
            name = ''
    return (
     prefix, name)


USAGE_TEXT = __doc__

def usage(parser):
    """Display usage info and exit."""
    parser.print_help()
    sys.exit(1)


def main():
    """A main function for running from the command line"""
    parser = OptionParser(USAGE_TEXT)
    parser.add_option('-f',
      '--force', action='store_true', dest='force',
      default=False,
      help='force overwrite without asking')
    parser.add_option('--fix-type-names',
      action='store', dest='fixtypenames',
      default=None,
      help='Fix up (replace) complex type names.')
    parser.add_option('--no-collect-includes',
      action='store_true', dest='no_collect_includes',
      default=False,
      help='do not process and insert schemas referenced by xs:include and xs:import elements')
    parser.add_option('--no-redefine-groups',
      action='store_true', dest='no_redefine_groups',
      default=False,
      help='do not pre-process and redefine xs:group elements')
    options, args = parser.parse_args()
    if len(args) == 2:
        inpath = args[0]
        outpath = args[1]
    else:
        if len(args) == 1:
            inpath = args[0]
            outpath = None
        else:
            if len(args) == 0:
                inpath = None
                outpath = None
            else:
                usage(parser)
    prep_schema(inpath, outpath, options)


if __name__ == '__main__':
    main()