# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/genwikidoc.py
# Compiled at: 2010-07-15 05:14:31
"""Library function to generate wiki documents from source code."""
import sys, types, os
from os.path import join, dirname, abspath
stylehdr = '[< <style type="text/css"> >]\n    h1, h2, h3, h4, h5 { \n        margin : 0px;\n        padding: 5px 0px 2px 3px;\n        background-color : #EAEAFC;\n        border-bottom: 1px solid #CCCCCC;\n    }\n[< </style> >]\n'
schemadochdr = '\nAuto generated file. Based on SQLalchemy schema definitions\n-----------------------------------------------------------\n\n( Attrs  Column_name  Column_type  Length  Constraints )\n\n  ( attrs P - primary_key, U - Unique, N - Nullable )\n\n\n'

def schemadoc(docsdir, tables):
    fd = open(join(docsdir, 'schema'), 'w')
    fd.write(schemadochdr)
    tdata = {'table_name': '', 'mysql_engine': ''}
    cdata = {'column_name': '', 'data_type': '', 
       'limit': '', 
       'constraint': '', 
       'attributes': ''}
    for t in tables:
        table = {}
        table.update(tdata)
        table['table_name'] = t.name
        table['mysql_engine'] = t.kwargs.get('mysql_engine', 'NA')
        fd.write('[ %s ] %s : ' % (table['table_name'], table['mysql_engine']))
        fd.write('\n\n')
        for c in t.columns:
            col = {}
            col.update(cdata)
            attr = c.unique and 'U' or '_'
            attr += c.nullable and 'N' or '_'
            attr += c.primary_key and 'P' or '_'
            constraints = (', ').join([ f.target_fullname for f in c.foreign_keys ])
            col['column_name'] = c.name
            col['data_type'] = str(c.type).split('(')[0]
            col['limit'] = getattr(c.type, 'length', 'NA')
            col['constraint'] = constraints
            col['attributes'] = attr
            fd.write('  %-4s %-25s  %-15s  %-6s %-25s\n' % (
             col['attributes'], col['column_name'],
             col['data_type'], col['limit'], col['constraint']))

        fd.write('\n\n')


zwhtmltmpl = "\n{{ Toc( float='right' ) }}\n\n%s\n\n== List of Templated Tags\n\n%s\n"

def zwhtml(docsdir):
    import zwiki.ttags as tt
    fd = open(join(docsdir, 'ZWTemplateTags'), 'wb')
    mods = sorted([ attr for attr in dir(tt) if attr[:3] == 'tt_' ])
    docstr = ('\n').join([ getattr(getattr(tt, attr), 'func_doc') for attr in mods
                         ])
    wikitext = zwhtmltmpl % (tt.wikidoc, docstr)
    fd.write(stylehdr + wikitext)


zwmacrostmpl = "\n{{ Toc( float='right' ) }}\n\n%s\n\n== List of ZWiki macros\n\n%s\n"

def zwmacros(docsdir):
    import zwiki.macro as zwm
    fd = open(join(docsdir, 'ZWMacros'), 'wb')
    macronames = zwm.macronames[:]
    macronames.remove('ZWMacro')
    macronames.sort()
    docstr = ('\n').join([ getattr(sys.modules[getattr(zwm, macroname).__module__], 'wikidoc', '') for macroname in macronames
                         ])
    wikitext = zwmacrostmpl % (zwm.__doc__, docstr)
    fd.write(stylehdr + wikitext)


zweexttmpl = "\n{{ Toc( float='right' ) }}\n\n%s\n\n== List of ZWiki extensions\n\n%s\n"

def zwextensions(docsdir):
    import zwiki.zwext as zwe
    fd = open(join(docsdir, 'ZWExtensions'), 'wb')
    extnames = zwe.extnames[:]
    extnames.remove('ZWExtension')
    extnames.sort()
    docstr = ('\n').join([ sys.modules[getattr(zwe, extname).__module__].wikidoc for extname in extnames
                         ])
    wikitext = zweexttmpl % (zwe.__doc__, docstr)
    fd.write(stylehdr + wikitext)


xmlrpctmpl = "\n{{ Toc( float='right' ) }}\n\n== XMLRPC API\nXMLRPC is a way of interfacing with ''ZETA server'' via HTTP.\n\n== List of XMLRPC API\n\n%s\n"

def xmlrpc(docsdir):
    import zeta.controllers.xmlrpc as x
    fd = open(join(docsdir, 'XmlRpcApi'), 'wb')
    docstr = ''
    attrs = sorted(dir(x.XmlrpcController))
    for attrname in attrs:
        attr = getattr(x.XmlrpcController, attrname)
        if isinstance(attr, types.MethodType) and attrname[0] != '_':
            docstr += '\n\n%s' % attr.func_doc

    wikitext = xmlrpctmpl % docstr
    fd.write(stylehdr + wikitext)


pasteradmintmpl = "\n{{ Toc( float='right' ) }}\n\n== Paster Admin commands\nPaster-admin is a command line tool to manage the site.\n\n== List of Commands\n\n%s\n"

def pasteradmin(docsdir):
    import zeta.controllers.pasteradmin as pa
    fd = open(join(docsdir, 'PasterAdmin'), 'wb')
    docstr = ''
    attrs = sorted(dir(pa.PasteradminController))
    for attrname in attrs:
        attr = getattr(pa.PasteradminController, attrname)
        if isinstance(attr, types.MethodType) and attrname[0] != '_':
            docstr += '\n\n%s' % attr.func_doc

    wikitext = pasteradmintmpl % docstr
    fd.write(stylehdr + wikitext)


pygmenttmpl = '\n== List of formats supported by \'/ pygments /\'\n\n{{{ Html\n<table style="width: %s; margin-left: 10px;">\n    <tr style="border-bottom: 1px solid gray">\n        <th style="padding: 2px;">Name</th>\n        <th style="padding: 2px;">Alias</th>\n        <th style="padding: 2px;">File-extensions</th>\n        <th style="padding: 2px;">Mime-types</th>\n    </tr>\n    %s\n</table>\n}}}\n'
pygrowtmpl = '\n<tr>\n    <td style="font-weight: bold; padding: 2px;">%s</td>\n    <td style="font-style: italic; padding: 2px;">%s</td>\n    <td style="padding: 2px;">%s</td>\n    <td style="padding: 2px;">%s</td>\n</tr>\n'

def pygments(docsdir):
    import pygments.lexers as pl
    fd = open(join(docsdir, 'pygments'), 'wb')
    formats = sorted(pl.get_all_lexers(), key=lambda x: x[0])
    docstr = ''
    for (name, alias, fnames, mimetypes) in formats:
        docstr += pygrowtmpl % (name, (', ').join(alias), (', ').join(fnames),
         (', ').join(mimetypes))

    wikitext = pygmenttmpl % ('100%', docstr)
    fd.write(stylehdr + wikitext)


def vimdoc(docsdir):
    import imp
    vimfile = abspath(join(dirname(__file__), '../extras/vim/plugin/zetavim.py'))
    zetavim = imp.load_source('zetavim', vimfile)
    fd = open(join(docsdir, 'VimIntegration'), 'wb')
    docstr = zetavim.__doc__
    docfns = [
     'addprofile', 'listprofiles', 'clearprofiles', 'connect',
     'listprojects', 'listgw', 'newgw', 'fetchgw', 'listwiki',
     'newwiki', 'fetchwiki', 'listticket', 'newtck', 'fetchticket',
     'addtags', 'deltags', 'vote', 'fav', 'nofav', 'comment']
    docstr = docstr + ('\n\n').join(getattr(zetavim, 'doclist'))
    wikitext = docstr
    fd.write(stylehdr + wikitext)