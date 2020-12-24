# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\cefdatabrowse\cefdatabrowse_support.py
# Compiled at: 2020-02-17 23:37:09
# Size of source mod 2**32: 32862 bytes
""" cefdatabrowse_support.py - Entry Point for CEFDatabrowse Application """
import sys, os, string
from lxml import etree
from time import time
import cgitb
cgitb.enable()
serverwrapper = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE doc [\n<!ENTITY agr    "&#x03B1;"> <!--  -->\n<!ENTITY Agr    "&#x0391;"> <!-- GREEK CAPITAL LETTER ALPHA -->\n<!ENTITY bgr    "&#x03B2;"> <!-- GREEK SMALL LETTER BETA -->\n<!ENTITY Bgr    "&#x0392;"> <!-- GREEK CAPITAL LETTER BETA -->\n<!ENTITY ggr    "&#x03B3;"> <!-- GREEK SMALL LETTER GAMMA -->\n<!ENTITY Ggr    "&#x0393;"> <!-- GREEK CAPITAL LETTER GAMMA -->\n<!ENTITY dgr    "&#x03B4;"> <!-- GREEK SMALL LETTER DELTA -->\n<!ENTITY Dgr    "&#x0394;"> <!-- GREEK CAPITAL LETTER DELTA -->\n<!ENTITY egr    "&#x03B5;"> <!--  -->\n<!ENTITY Egr    "&#x0395;"> <!-- GREEK CAPITAL LETTER EPSILON -->\n<!ENTITY zgr    "&#x03B6;"> <!-- GREEK SMALL LETTER ZETA -->\n<!ENTITY Zgr    "&#x0396;"> <!-- GREEK CAPITAL LETTER ZETA -->\n<!ENTITY eegr   "&#x03B7;"> <!-- GREEK SMALL LETTER ETA -->\n<!ENTITY EEgr   "&#x0397;"> <!-- GREEK CAPITAL LETTER ETA -->\n<!ENTITY thgr   "&#x03B8;"> <!--  -->\n<!ENTITY THgr   "&#x0398;"> <!-- GREEK CAPITAL LETTER THETA -->\n<!ENTITY igr    "&#x03B9;"> <!-- GREEK SMALL LETTER IOTA -->\n<!ENTITY Igr    "&#x0399;"> <!-- GREEK CAPITAL LETTER IOTA -->\n<!ENTITY kgr    "&#x03BA;"> <!-- GREEK SMALL LETTER KAPPA -->\n<!ENTITY Kgr    "&#x039A;"> <!-- GREEK CAPITAL LETTER KAPPA -->\n<!ENTITY lgr    "&#x03BB;"> <!-- GREEK SMALL LETTER LAMDA -->\n<!ENTITY Lgr    "&#x039B;"> <!-- GREEK CAPITAL LETTER LAMDA -->\n<!ENTITY mgr    "&#x03BC;"> <!-- GREEK SMALL LETTER MU -->\n<!ENTITY Mgr    "&#x039C;"> <!-- GREEK CAPITAL LETTER MU -->\n<!ENTITY ngr    "&#x03BD;"> <!-- GREEK SMALL LETTER NU -->\n<!ENTITY Ngr    "&#x039D;"> <!-- GREEK CAPITAL LETTER NU -->\n<!ENTITY xgr    "&#x03BE;"> <!-- GREEK SMALL LETTER XI -->\n<!ENTITY Xgr    "&#x039E;"> <!-- GREEK CAPITAL LETTER XI -->\n<!ENTITY ogr    "&#x03BF;"> <!-- GREEK SMALL LETTER OMICRON -->\n<!ENTITY Ogr    "&#x039F;"> <!-- GREEK CAPITAL LETTER OMICRON -->\n<!ENTITY pgr    "&#x03C0;"> <!-- GREEK SMALL LETTER PI -->\n<!ENTITY Pgr    "&#x03A0;"> <!-- GREEK CAPITAL LETTER PI -->\n<!ENTITY rgr    "&#x03C1;"> <!-- GREEK SMALL LETTER RHO -->\n<!ENTITY Rgr    "&#x03A1;"> <!-- GREEK CAPITAL LETTER RHO -->\n<!ENTITY sgr    "&#x03C3;"> <!-- GREEK SMALL LETTER SIGMA -->\n<!ENTITY Sgr    "&#x03A3;"> <!-- GREEK CAPITAL LETTER SIGMA -->\n<!ENTITY sfgr   "&#x03C2;"> <!--  -->\n<!ENTITY tgr    "&#x03C4;"> <!-- GREEK SMALL LETTER TAU -->\n<!ENTITY Tgr    "&#x03A4;"> <!-- GREEK CAPITAL LETTER TAU -->\n<!ENTITY ugr    "&#x03C5;"> <!-- GREEK SMALL LETTER UPSILON -->\n<!ENTITY Ugr    "&#x03A5;"> <!--  -->\n<!ENTITY phgr   "&#x03C6;"> <!-- GREEK SMALL LETTER PHI -->\n<!ENTITY PHgr   "&#x03A6;"> <!-- GREEK CAPITAL LETTER PHI -->\n<!ENTITY khgr   "&#x03C7;"> <!-- GREEK SMALL LETTER CHI -->\n<!ENTITY KHgr   "&#x03A7;"> <!-- GREEK CAPITAL LETTER CHI -->\n<!ENTITY psgr   "&#x03C8;"> <!-- GREEK SMALL LETTER PSI -->\n<!ENTITY PSgr   "&#x03A8;"> <!-- GREEK CAPITAL LETTER PSI -->\n<!ENTITY ohgr   "&#x03C9;"> <!-- GREEK SMALL LETTER OMEGA -->\n<!ENTITY OHgr   "&#x03A9;"> <!-- GREEK CAPITAL LETTER OMEGA -->\n]>\n<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:html="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="http://www.w3.org/2001/XInclude" version="1.0">\n    <xsl:output method="xml" omit-xml-declaration="no" indent="no" version="1.0" media-type="application/xhtml+xml" encoding="UTF-8" doctype-public="-//W3C//DTD XHTML 1.1//EN" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"/>\n    <xsl:variable name="resdir">%s</xsl:variable>\n    <xsl:variable name="dataroot">%s</xsl:variable>\n    <xsl:variable name="proctime">%s</xsl:variable>\n    <xsl:template match="/">\n        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse">\n            <body>\n                <xsl:attribute name="db:resdir"><xsl:value-of select="$resdir"/></xsl:attribute>\n                <xsl:attribute name="db:proctime"><xsl:value-of select="$proctime"/></xsl:attribute>\n                %s\n                <xsl:apply-templates mode="%s"/>\n            </body>\n        </html>\n    </xsl:template>\n    %s\n</xsl:stylesheet>'
localwrapper = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE doc [\n<!ENTITY agr    "&#x03B1;"> <!--  -->\n<!ENTITY Agr    "&#x0391;"> <!-- GREEK CAPITAL LETTER ALPHA -->\n<!ENTITY bgr    "&#x03B2;"> <!-- GREEK SMALL LETTER BETA -->\n<!ENTITY Bgr    "&#x0392;"> <!-- GREEK CAPITAL LETTER BETA -->\n<!ENTITY ggr    "&#x03B3;"> <!-- GREEK SMALL LETTER GAMMA -->\n<!ENTITY Ggr    "&#x0393;"> <!-- GREEK CAPITAL LETTER GAMMA -->\n<!ENTITY dgr    "&#x03B4;"> <!-- GREEK SMALL LETTER DELTA -->\n<!ENTITY Dgr    "&#x0394;"> <!-- GREEK CAPITAL LETTER DELTA -->\n<!ENTITY egr    "&#x03B5;"> <!--  -->\n<!ENTITY Egr    "&#x0395;"> <!-- GREEK CAPITAL LETTER EPSILON -->\n<!ENTITY zgr    "&#x03B6;"> <!-- GREEK SMALL LETTER ZETA -->\n<!ENTITY Zgr    "&#x0396;"> <!-- GREEK CAPITAL LETTER ZETA -->\n<!ENTITY eegr   "&#x03B7;"> <!-- GREEK SMALL LETTER ETA -->\n<!ENTITY EEgr   "&#x0397;"> <!-- GREEK CAPITAL LETTER ETA -->\n<!ENTITY thgr   "&#x03B8;"> <!--  -->\n<!ENTITY THgr   "&#x0398;"> <!-- GREEK CAPITAL LETTER THETA -->\n<!ENTITY igr    "&#x03B9;"> <!-- GREEK SMALL LETTER IOTA -->\n<!ENTITY Igr    "&#x0399;"> <!-- GREEK CAPITAL LETTER IOTA -->\n<!ENTITY kgr    "&#x03BA;"> <!-- GREEK SMALL LETTER KAPPA -->\n<!ENTITY Kgr    "&#x039A;"> <!-- GREEK CAPITAL LETTER KAPPA -->\n<!ENTITY lgr    "&#x03BB;"> <!-- GREEK SMALL LETTER LAMDA -->\n<!ENTITY Lgr    "&#x039B;"> <!-- GREEK CAPITAL LETTER LAMDA -->\n<!ENTITY mgr    "&#x03BC;"> <!-- GREEK SMALL LETTER MU -->\n<!ENTITY Mgr    "&#x039C;"> <!-- GREEK CAPITAL LETTER MU -->\n<!ENTITY ngr    "&#x03BD;"> <!-- GREEK SMALL LETTER NU -->\n<!ENTITY Ngr    "&#x039D;"> <!-- GREEK CAPITAL LETTER NU -->\n<!ENTITY xgr    "&#x03BE;"> <!-- GREEK SMALL LETTER XI -->\n<!ENTITY Xgr    "&#x039E;"> <!-- GREEK CAPITAL LETTER XI -->\n<!ENTITY ogr    "&#x03BF;"> <!-- GREEK SMALL LETTER OMICRON -->\n<!ENTITY Ogr    "&#x039F;"> <!-- GREEK CAPITAL LETTER OMICRON -->\n<!ENTITY pgr    "&#x03C0;"> <!-- GREEK SMALL LETTER PI -->\n<!ENTITY Pgr    "&#x03A0;"> <!-- GREEK CAPITAL LETTER PI -->\n<!ENTITY rgr    "&#x03C1;"> <!-- GREEK SMALL LETTER RHO -->\n<!ENTITY Rgr    "&#x03A1;"> <!-- GREEK CAPITAL LETTER RHO -->\n<!ENTITY sgr    "&#x03C3;"> <!-- GREEK SMALL LETTER SIGMA -->\n<!ENTITY Sgr    "&#x03A3;"> <!-- GREEK CAPITAL LETTER SIGMA -->\n<!ENTITY sfgr   "&#x03C2;"> <!--  -->\n<!ENTITY tgr    "&#x03C4;"> <!-- GREEK SMALL LETTER TAU -->\n<!ENTITY Tgr    "&#x03A4;"> <!-- GREEK CAPITAL LETTER TAU -->\n<!ENTITY ugr    "&#x03C5;"> <!-- GREEK SMALL LETTER UPSILON -->\n<!ENTITY Ugr    "&#x03A5;"> <!--  -->\n<!ENTITY phgr   "&#x03C6;"> <!-- GREEK SMALL LETTER PHI -->\n<!ENTITY PHgr   "&#x03A6;"> <!-- GREEK CAPITAL LETTER PHI -->\n<!ENTITY khgr   "&#x03C7;"> <!-- GREEK SMALL LETTER CHI -->\n<!ENTITY KHgr   "&#x03A7;"> <!-- GREEK CAPITAL LETTER CHI -->\n<!ENTITY psgr   "&#x03C8;"> <!-- GREEK SMALL LETTER PSI -->\n<!ENTITY PSgr   "&#x03A8;"> <!-- GREEK CAPITAL LETTER PSI -->\n<!ENTITY ohgr   "&#x03C9;"> <!-- GREEK SMALL LETTER OMEGA -->\n<!ENTITY OHgr   "&#x03A9;"> <!-- GREEK CAPITAL LETTER OMEGA -->\n]>\n<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:html="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="http://www.w3.org/2001/XInclude" version="1.0">\n    <xsl:output method="xml" omit-xml-declaration="no" indent="no" version="1.0" media-type="application/xhtml+xml" encoding="UTF-8" doctype-public="-//W3C//DTD XHTML 1.1//EN" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"/>\n    <xsl:variable name="resdir">%s</xsl:variable>\n    <xsl:variable name="dataroot">%s</xsl:variable>\n    <xsl:variable name="proctime">%s</xsl:variable>\n    <xsl:template match="/">\n        <xsl:processing-instruction name="xml-stylesheet">type="text/xsl" href="/dbres/db_web.xml"</xsl:processing-instruction>\n        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse">\n            <body>\n                <xsl:attribute name="db:resdir"><xsl:value-of select="$resdir"/></xsl:attribute>\n                <xsl:attribute name="db:proctime"><xsl:value-of select="$proctime"/></xsl:attribute>\n                %s\n                <xsl:apply-templates mode="%s"/>\n            </body>\n        </html>\n    </xsl:template>\n    %s\n</xsl:stylesheet>'
ajaxwrapper = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE doc [\n<!ENTITY agr    "&#x03B1;"> <!--  -->\n<!ENTITY Agr    "&#x0391;"> <!-- GREEK CAPITAL LETTER ALPHA -->\n<!ENTITY bgr    "&#x03B2;"> <!-- GREEK SMALL LETTER BETA -->\n<!ENTITY Bgr    "&#x0392;"> <!-- GREEK CAPITAL LETTER BETA -->\n<!ENTITY ggr    "&#x03B3;"> <!-- GREEK SMALL LETTER GAMMA -->\n<!ENTITY Ggr    "&#x0393;"> <!-- GREEK CAPITAL LETTER GAMMA -->\n<!ENTITY dgr    "&#x03B4;"> <!-- GREEK SMALL LETTER DELTA -->\n<!ENTITY Dgr    "&#x0394;"> <!-- GREEK CAPITAL LETTER DELTA -->\n<!ENTITY egr    "&#x03B5;"> <!--  -->\n<!ENTITY Egr    "&#x0395;"> <!-- GREEK CAPITAL LETTER EPSILON -->\n<!ENTITY zgr    "&#x03B6;"> <!-- GREEK SMALL LETTER ZETA -->\n<!ENTITY Zgr    "&#x0396;"> <!-- GREEK CAPITAL LETTER ZETA -->\n<!ENTITY eegr   "&#x03B7;"> <!-- GREEK SMALL LETTER ETA -->\n<!ENTITY EEgr   "&#x0397;"> <!-- GREEK CAPITAL LETTER ETA -->\n<!ENTITY thgr   "&#x03B8;"> <!--  -->\n<!ENTITY THgr   "&#x0398;"> <!-- GREEK CAPITAL LETTER THETA -->\n<!ENTITY igr    "&#x03B9;"> <!-- GREEK SMALL LETTER IOTA -->\n<!ENTITY Igr    "&#x0399;"> <!-- GREEK CAPITAL LETTER IOTA -->\n<!ENTITY kgr    "&#x03BA;"> <!-- GREEK SMALL LETTER KAPPA -->\n<!ENTITY Kgr    "&#x039A;"> <!-- GREEK CAPITAL LETTER KAPPA -->\n<!ENTITY lgr    "&#x03BB;"> <!-- GREEK SMALL LETTER LAMDA -->\n<!ENTITY Lgr    "&#x039B;"> <!-- GREEK CAPITAL LETTER LAMDA -->\n<!ENTITY mgr    "&#x03BC;"> <!-- GREEK SMALL LETTER MU -->\n<!ENTITY Mgr    "&#x039C;"> <!-- GREEK CAPITAL LETTER MU -->\n<!ENTITY ngr    "&#x03BD;"> <!-- GREEK SMALL LETTER NU -->\n<!ENTITY Ngr    "&#x039D;"> <!-- GREEK CAPITAL LETTER NU -->\n<!ENTITY xgr    "&#x03BE;"> <!-- GREEK SMALL LETTER XI -->\n<!ENTITY Xgr    "&#x039E;"> <!-- GREEK CAPITAL LETTER XI -->\n<!ENTITY ogr    "&#x03BF;"> <!-- GREEK SMALL LETTER OMICRON -->\n<!ENTITY Ogr    "&#x039F;"> <!-- GREEK CAPITAL LETTER OMICRON -->\n<!ENTITY pgr    "&#x03C0;"> <!-- GREEK SMALL LETTER PI -->\n<!ENTITY Pgr    "&#x03A0;"> <!-- GREEK CAPITAL LETTER PI -->\n<!ENTITY rgr    "&#x03C1;"> <!-- GREEK SMALL LETTER RHO -->\n<!ENTITY Rgr    "&#x03A1;"> <!-- GREEK CAPITAL LETTER RHO -->\n<!ENTITY sgr    "&#x03C3;"> <!-- GREEK SMALL LETTER SIGMA -->\n<!ENTITY Sgr    "&#x03A3;"> <!-- GREEK CAPITAL LETTER SIGMA -->\n<!ENTITY sfgr   "&#x03C2;"> <!--  -->\n<!ENTITY tgr    "&#x03C4;"> <!-- GREEK SMALL LETTER TAU -->\n<!ENTITY Tgr    "&#x03A4;"> <!-- GREEK CAPITAL LETTER TAU -->\n<!ENTITY ugr    "&#x03C5;"> <!-- GREEK SMALL LETTER UPSILON -->\n<!ENTITY Ugr    "&#x03A5;"> <!--  -->\n<!ENTITY phgr   "&#x03C6;"> <!-- GREEK SMALL LETTER PHI -->\n<!ENTITY PHgr   "&#x03A6;"> <!-- GREEK CAPITAL LETTER PHI -->\n<!ENTITY khgr   "&#x03C7;"> <!-- GREEK SMALL LETTER CHI -->\n<!ENTITY KHgr   "&#x03A7;"> <!-- GREEK CAPITAL LETTER CHI -->\n<!ENTITY psgr   "&#x03C8;"> <!-- GREEK SMALL LETTER PSI -->\n<!ENTITY PSgr   "&#x03A8;"> <!-- GREEK CAPITAL LETTER PSI -->\n<!ENTITY ohgr   "&#x03C9;"> <!-- GREEK SMALL LETTER OMEGA -->\n<!ENTITY OHgr   "&#x03A9;"> <!-- GREEK CAPITAL LETTER OMEGA -->\n]>\n<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:html="http://www.w3.org/1999/xhtml" xmlns:xi="http://www.w3.org/2001/XInclude" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0">\n    <xsl:output method="xml" omit-xml-declaration="no" indent="yes" version="1.0" media-type="application/xhtml+xml" encoding="UTF-8" doctype-public="-//W3C//DTD XHTML 1.1//EN" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"/>\n    <xsl:template match="/">\n        <xsl:apply-templates mode="%s"/>\n    </xsl:template>\n    %s\n</xsl:stylesheet>'

class FileResolver(etree.Resolver):
    _path = None

    def __init__(self, path):
        self._path = path

    def resolve(self, url, pubid, context):
        if url.startswith('http://'):
            return self.resolve_filename(url, context)
        return self.resolve_filename(os.path.abspath(self._path + '/' + url), context)


def application(filename, params):
    """ Entry Point for CEFDatabrowse Application """
    starttime = time()
    import databrowse.support.dummy_web_support as db_web_support_module
    db_web_support = db_web_support_module.web_support(filename, params)
    try:
        if 'path' not in db_web_support.req.form:
            fullpath = db_web_support.dataroot
            relpath = '/'
        else:
            fullpath = os.path.abspath(db_web_support.req.form['path'].value)
            if not fullpath.startswith(db_web_support.dataroot):
                return db_web_support.req.return_error(403)
            else:
                if os.access(fullpath, os.R_OK):
                    if os.path.exists(fullpath):
                        if fullpath == db_web_support.dataroot:
                            relpath = '/'
                        else:
                            relpath = fullpath.replace(db_web_support.dataroot, '')
                    else:
                        if not os.path.exists(fullpath):
                            return db_web_support.req.return_error(404)
                        return db_web_support.req.return_error(401)
                else:
                    relpath = '/'.join(relpath.split('\\'))
                    import databrowse.support.handler_support as handler_support_module
                    handler_support = handler_support_module.handler_support(db_web_support.icondbpath, db_web_support.hiddenfiledbpath, db_web_support.directorypluginpath)
                    handlers = handler_support.GetHandler(fullpath)
                    handler = handlers[(-1)]
                    if 'handler' in db_web_support.req.form:
                        handler = db_web_support.req.form['handler'].value
                    caller = 'databrowse'
                    exec('import databrowse.plugins.%s.%s as %s_module' % (handler, handler, handler))
                    renderer = eval('%s_module.%s(relpath, fullpath, db_web_support, handler_support, caller, handlers%s%s%s)' % (handler, handler,
                     ', content_mode="' + db_web_support.req.form['content_mode'].value + '"' if 'content_mode' in db_web_support.req.form else '',
                     ', style_mode="' + db_web_support.req.form['style_mode'].value + '"' if 'style_mode' in db_web_support.req.form else '',
                     ', recursion_depth=' + db_web_support.req.form['recursion_depth'].value + '' if 'recursion_depth' in db_web_support.req.form else ''))
                    topbarstring = renderer.isRaw() or '<div class="pathbar"><div style="float:left">'
                    linkstring = db_web_support.siteurl
                    itemslist = relpath.split('/')[1:]
                    count = 1
                    if itemslist[0] != '':
                        topbarstring += '<a style="padding:0 5px;position:relative;top:3px;" href="%s"><img src="%s/icons/go-home.png"/></a><a class="button" href="%s">/</a>&gt;' % (db_web_support.siteurl, db_web_support.resurl, db_web_support.siteurl)
                    for item in itemslist:
                        if item != '' and count != len(itemslist):
                            linkstring += '/' + item
                            topbarstring += '<a class="button" href="%s">%s</a>&gt;' % (linkstring, item)
                        else:
                            if item != '' and count == len(itemslist):
                                linkstring += '/' + item
                                topbarstring += '<a class="button active" href="%s">%s</a>' % (linkstring, item)
                            else:
                                topbarstring += '<a style="padding:0 5px;position:relative;top:3px;" href="%s"><img src="%s/icons/go-home.png"/></a><a class="button active" href="%s">/</a>' % (linkstring, db_web_support.resurl, linkstring)
                        count += 1

                    topbarstring += "</div><div id='toggleexpand'><a onclick='togglefullwidth()' style='position:relative; right: 3px; top: 2px; float:right; cursor:pointer'><img src='%s/icons/gtk-fullscreen.png'/></a></div></div>" % db_web_support.resurl
                    if 'contentonly' in db_web_support.req.form:
                        xml = etree.ElementTree(renderer.getContent())
                        db_web_support.req.response_headers['Content-Type'] = 'text/xml'
                        db_web_support.req.output = etree.tostring(xml)
                        return [db_web_support.req.return_page()]
                        if 'styleonly' in db_web_support.req.form:
                            endtime = time()
                            runtime = '%.6f' % (endtime - starttime)
                            style = serverwrapper % (db_web_support.resurl, db_web_support.dataroot.replace('\\', '/'), runtime, topbarstring, renderer.getContentMode(), db_web_support.style.GetStyle())
                            parser = etree.XMLParser()
                            parser.resolvers.add(FileResolver(os.path.dirname(fullpath)))
                            styletree = etree.ElementTree(etree.XML(style, parser))
                            styletree.xinclude()
                            db_web_support.req.response_headers['Content-Type'] = 'text/xml'
                            db_web_support.req.output = etree.tostring(styletree)
                            return [db_web_support.req.return_page()]
                        parser = etree.XMLParser()
                        parser.resolvers.add(FileResolver(os.path.dirname(fullpath)))
                        if 'ajax' in db_web_support.req.form:
                            return [
                             renderer.getContent(), db_web_support.req.response_headers, db_web_support.req.status]
                        if renderer.getContentMode() == 'ajax':
                            xml = etree.ElementTree(renderer.getContent())
                            style = ajaxwrapper % (renderer.getContentMode(), db_web_support.style.GetStyle())
                            styletree = etree.ElementTree(etree.XML(style, parser))
                            styletree.xinclude()
                            content = xml.xslt(styletree.getroot())
                            db_web_support.req.output = etree.tostring(content)
                            db_web_support.req.response_headers['Content-Type'] = 'application/xhtml+xml'
                            return [db_web_support.req.return_page(), db_web_support.req.response_headers, db_web_support.req.status]
                        if 'nopagestyle' in db_web_support.req.form:
                            xml = etree.ElementTree(renderer.getContent())
                            endtime = time()
                            runtime = '%.6f' % (endtime - starttime)
                            style = serverwrapper % (db_web_support.resurl, db_web_support.dataroot.replace('\\', '/'), runtime, topbarstring, renderer.getContentMode(), db_web_support.style.GetStyle())
                            styletree = etree.ElementTree(etree.XML(style, parser))
                            styletree.xinclude()
                            content = xml.xslt(styletree.getroot())
                            db_web_support.req.output = etree.tostring(content)
                            db_web_support.req.response_headers['Content-Type'] = 'application/xhtml+xml'
                            return [db_web_support.req.return_page(), db_web_support.req.response_headers, db_web_support.req.status]
                        if 'localpagestyle' in db_web_support.req.form:
                            xml = etree.ElementTree(renderer.getContent())
                            endtime = time()
                            runtime = '%.6f' % (endtime - starttime)
                            style = localwrapper % (db_web_support.resurl, db_web_support.dataroot.replace('\\', '/'), runtime, topbarstring, renderer.getContentMode(), db_web_support.style.GetStyle())
                            styletree = etree.ElementTree(etree.XML(style, parser))
                            styletree.xinclude()
                            content = xml.xslt(styletree.getroot())
                            contentroot = content.getroot()
                            renderer.loadMenu()
                            contentroot.append(db_web_support.menu.GetMenu())
                            db_web_support.req.output = etree.tostring(content)
                            db_web_support.req.response_headers['Content-Type'] = 'application/xhtml+xml'
                            return [db_web_support.req.return_page(), db_web_support.req.response_headers, db_web_support.req.status]
                        xml = etree.ElementTree(renderer.getContent())
                        endtime = time()
                        runtime = '%.6f' % (endtime - starttime)
                        style = serverwrapper % (db_web_support.resurl, db_web_support.dataroot.replace('\\', '/'), runtime, topbarstring, renderer.getContentMode(), db_web_support.style.GetStyle())
                        styletree = etree.ElementTree(etree.XML(style.encode(), parser))
                        styletree.xinclude()
                        content = xml.xslt(styletree.getroot())
                        contentroot = content.getroot()
                        renderer.loadMenu()
                        contentroot.append(db_web_support.menu.GetMenu())
                        f = open(os.path.join(db_web_support.webdir, 'resources/db_cef.xml'))
                        template = etree.parse(f)
                        f.close()
                        db_web_support.req.output = str(content.xslt(template))
                        db_web_support.req.response_headers['Content-Type'] = 'application/xhtml+xml'
                        return [
                         db_web_support.req.return_page(), db_web_support.req.response_headers, db_web_support.req.status]
                    else:
                        pass
                return [
                 renderer.getContent(), db_web_support.req.response_headers, db_web_support.req.status]
    except Exception as err:
        try:
            errormessage = '        <?xml-stylesheet type="text/xsl" href="{}/db_cef.xml"?>\n        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:html="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse">\n        <body db:resdir="{}/">\n            <h1>500 Internal Server Error</h1>\n            <p>An unhandled exception has occurred.  Notify the administrators for assistance.  Please make note of what you were doing, the steps to reproduce the error, and the approximate time.  More details are shown below:</p>\n            <p>\n                <strong>Error:</strong>  {}                                                     <br/>\n                <strong>Time:</strong> {}                                                       <br/>\n                <strong>Hostname:</strong> {}                                                   <br/>\n                <strong>Platform:</strong> {} <strong>Python:</strong> {}                       <br/>\n                <strong>PID:</strong> {}                                                        <br/>\n                <strong>Traceback:</strong>                                                     <br/>\n                <pre style="overflow:auto">{}</pre>\n                <strong>Environment:</strong>                                                   <br/>\n                <pre style="overflow:auto">{}</pre>\n                <strong>Request Variables:</strong>                                             <br/>\n                <pre style="overflow:auto">{}</pre>\n                <strong>Dir()</strong>                                                          <br/>\n                <pre style="overflow:auto">{}</pre>\n            </p>\n        </body>\n        <db:navigation xmlns="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse">\n            <db:navbar>\n                <db:navelem><a href="javascript:window.history.back()">Go Back</a></db:navelem>\n            </db:navbar>\n        </db:navigation>\n        </html>'
            import traceback, cgi, socket
            from time import gmtime, strftime
            try:
                from StringIO import StringIO
            except ImportError:
                from io import StringIO

            trace = StringIO()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=trace)
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            tracestring = trace.getvalue()
            trace.close()
            tracestring = tracestring.replace('&', '&#160;').replace('<', '&lt;').replace('>', '&gt;')
            if 'ajax' in db_web_support.req.form:
                return ['500 Internal Server Error', db_web_support.req.response_headers]
            inputstring = ''
            for key in db_web_support.req.form.keys():
                try:
                    inputstring = inputstring + '%s:  %s \n' % (key, repr(db_web_support.req.form[key].value))
                except AttributeError:
                    pass

            inputstring = inputstring.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&#160;')
            keystring = ''
            dirstring = ''
            for name in dir():
                dirstring = dirstring + '%s %s: %s \n' % (name, str(type(name)), repr(eval(name)))

            dirstring = dirstring.replace('&', '&#160;').replace('<', '&lt;').replace('>', '&gt;')
            err = str(err).replace('&', '&#160;').replace('<', '&lt;').replace('>', '&gt;')
            errormessage = errormessage.format(db_web_support.resurl, db_web_support.resurl, err, strftime('%Y-%m-%d %H:%M:%S', gmtime()), socket.getfqdn(), sys.platform, sys.version, os.getpid(), tracestring, keystring, inputstring, dirstring)
            db_web_support.req.start_response(200, {'Content-Type':'text/xml',  'Content-Length':str(len(errormessage))}.items())
            return [errormessage, db_web_support.req.response_headers, db_web_support.req.status]
        finally:
            err = None
            del err


class Debugger:
    __doc__ = ' Code Used To Enable PDB in Single Instance Apache Mode '

    def __init__(self, object):
        self._Debugger__object = object

    def __call__(self, *args, **kwargs):
        import pdb, sys
        debugger = pdb.Pdb()
        debugger.use_rawinput = 0
        debugger.reset()
        sys.settrace(debugger.trace_dispatch)
        try:
            return (self._Debugger__object)(*args, **kwargs)
        finally:
            debugger.quitting = 1
            sys.settrace(None)


class Profiler:
    __doc__ = ' Code Used to Enable Profiling in Single Instance Apache Mode '

    def __init__(self, object):
        self._Profiler__object = object

    def __call__(self, *args, **kwargs):
        from pycallgraph import PyCallGraph
        from pycallgraph.output import GraphvizOutput
        with PyCallGraph(output=GraphvizOutput(output_file='/tmp/pycallgraph.svg', output_type='svg')):
            return (self._Profiler__object)(*args, **kwargs)