# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlpython/output_templates.py
# Compiled at: 2012-05-26 21:28:24
import genshi.template
output_templates = {'\\x': genshi.template.NewTextTemplate('\n<xml>\n  <${tblname}_resultset>{% for row in rows %}\n    <$tblname>{% for (colname, itm) in zip(colnames, row) %}\n      <${colname.lower()}>$itm</${colname.lower()}>{% end %}\n    </$tblname>{% end %}\n  </${tblname}_resultset>\n</xml>'), 
   '\\j': genshi.template.NewTextTemplate('\n{"${tblname}": [\n${\',\\n\'.join(\'        {%s}\' % \', \'.join(\'"%s": %s\' % (colname,\n        ((isinstance(itm,int) or isinstance(itm,float)) and \'%s\' or \'"%s"\') % str(itm)\n    ) for (colname, itm) in zip(colnames, row)) for row in rows)}\n    ]\n}'), 
   '\\h': genshi.template.MarkupTemplate('\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns:py="http://genshi.edgewall.org/" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n  <head>\n    <title py:content="tblname">Table Name</title>\n    <meta http-equiv="content-type" content="text/html;charset=utf-8" />\n  </head>\n  <body>\n    <table py:attrs="{\'id\':tblname, \n     \'summary\':\'Result set from query on table \' + tblname}">\n      <tr>\n        <th py:for="colname in colnames"\n         py:attrs="{\'id\':\'header_\' + colname.lower()}">\n          <span py:replace="colname.lower()">Column Name</span>\n        </th>\n      </tr>\n      <tr py:for="row in rows">\n        <td py:for="(colname, itm) in zip(colnames, row)" py:attrs="{\'headers\':\'header_\' + colname.lower()}">\n          <span py:replace="(hasattr(itm, \'html\') and Markup(itm.html())) or str(itm)">Value</span>\n        </td>\n      </tr>\n    </table>\n  </body>\n</html>'), 
   '\\g': genshi.template.NewTextTemplate('\n{% for (rowNum, row) in enumerate(rows) %}\n**** Row: ${rowNum + 1}\n{% for (colname, itm) in zip(colnames, row) %}$colname: $itm\n{% end %}{% end %}'), 
   '\\G': genshi.template.NewTextTemplate('\n{% for (rowNum, row) in enumerate(rows) %}\n**** Row: ${rowNum + 1}\n{% for (colname, itm) in zip(colnames, row) %}${colname.ljust(colnamelen)}: $itm\n{% end %}{% end %}'), 
   '\\i': genshi.template.NewTextTemplate("{% for (rowNum, row) in enumerate(rows) %}\nINSERT INTO $tblname (${', '.join(colnames)}) VALUES (${', '.join(formattedForSql(r) for r in row)});{% end %}"), 
   '\\c': genshi.template.NewTextTemplate('\n${\',\'.join(colnames)}{% for row in rows %}\n${\',\'.join(\'"%s"\' % val for val in row)}{% end %}'), 
   '\\C': genshi.template.NewTextTemplate('\n{% for row in rows %}\n${\',\'.join(\'"%s"\' % val for val in row)}{% end %}')}
output_templates['\\s'] = output_templates['\\c']
output_templates['\\S'] = output_templates['\\C']