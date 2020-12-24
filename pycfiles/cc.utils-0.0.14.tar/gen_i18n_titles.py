# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cc/licenserdf/tools/gen_i18n_titles.py
# Compiled at: 2011-07-11 14:56:02
import pkg_resources, os, urlparse, rdflib
from cc.licenserdf.tools import support
I18N_DIR = pkg_resources.resource_filename('cc.i18n', 'i18n/')
LICENSES_DIR = pkg_resources.resource_filename('cc.licenserdf', 'licenses/')

def setup_i18n_title(license_graph, filename):
    license_subj = list(license_graph.triples((
     None, support.NS_RDF['type'], support.NS_CC['License'])))[0][0]
    i18n_triples = [ (s, p, l) for (s, p, l) in license_graph.triples((license_subj, support.NS_DC['title'], None)) if l.language == 'i18n'
                   ]
    if i18n_triples:
        for i18n_triple in i18n_triples:
            license_graph.remove(i18n_triple)

    if '/publicdomain/zero/' in str(license_subj):
        license_code = 'cc0'
    else:
        (s, p, identifier_literal) = list(license_graph.triples((
         license_subj, support.NS_DC['identifier'], None)))[0]
        license_code = unicode(identifier_literal)
    try:
        license_version = unicode(list(license_graph.triples((
         None, support.NS_DCQ['hasVersion'], None)))[0][2])
    except IndexError:
        try:
            license_version = unicode(list(license_graph.triples((
             None, support.NS_DC['hasVersion'], None)))[0][2])
        except IndexError:
            license_version = None

    try:
        license_jurisdiction_url = unicode(list(license_graph.triples((
         license_subj, support.NS_CC['jurisdiction'], None)))[0][2])
        license_jurisdiction = urlparse.urlsplit(license_jurisdiction_url).path.strip('/').split('/')[1]
    except IndexError:
        license_jurisdiction = None

    i18n_str = support.gen_license_i18n_title(license_code, license_version, license_jurisdiction)
    i18n_literal = rdflib.Literal(i18n_str)
    i18n_literal.language = 'i18n'
    license_graph.add((
     license_subj, support.NS_DC['title'], i18n_literal))
    support.save_graph(license_graph, filename)
    return


def cli():
    for filename in os.listdir(LICENSES_DIR):
        if not filename.endswith('.rdf'):
            continue
        full_filename = os.path.join(LICENSES_DIR, filename)
        license_graph = support.load_graph(full_filename)
        setup_i18n_title(license_graph, full_filename)


if __name__ == '__main__':
    cli()