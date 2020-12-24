# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/scaffolding.py
# Compiled at: 2013-09-20 12:23:36
""" _dryxTBS_scaffolding.py
=============================
:Summary:
    Layout / scaffolding partial for the dryxTwitterBootstrap module

:Author:
    David Young

:Date Created:
    March 27, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk """

def htmlDocument(contentType=False, content=''):
    """The doctype and html tags

    **Key Arguments:**
        - ``content`` -- the head and body of the html page

    **Return:**
        - ``contentType`` -- the content type [ "text/html" ]
        - ``doctype`` -- the HTML5 doctype
    """
    if not contentType:
        contentType = ''
    htmlDocument = '%s\n\n        <!DOCTYPE html>\n        <html lang="en">\n            %s\n        </html>\n    ' % (
     contentType, content)
    return htmlDocument


def head(relativeUrlBase='', mainCssFileName='main.css', pageTitle='', extras=''):
    """Generate an html head element for your webpage

    **Key Arguments:**
        ``relativeUrlBase`` -- relative base url for js, css, image folders
        ``pageTitle`` -- well, the page title!
        ``mainCssFileName`` -- css file name
        ``extras`` -- any extra info to be included in the ``head`` element

    **Return:**
        - ``head`` -- the head """
    cssUrl = relativeUrlBase + '/assets/styles/css/' + mainCssFileName
    cssLink = '\n        <link rel="stylesheet" href="%s" type="text/css" />\n    ' % (cssUrl,)
    head = '\n    <!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->\n    <!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->\n    <!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->\n    <!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->\n    <head>\n        <meta charset="utf-8">\n        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n        <title>%s</title>\n        <meta name="description" content="">\n        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n        %s\n        %s\n    </head>\n    ' % (pageTitle, cssLink, extras)
    return head


def body(navBar=False, content='', htmlId='', extraAttr='', relativeUrlBase='', responsive=True, googleAnalyticsCode=False, jsFileName='main.js'):
    """Generate an HTML body

    **Key Arguments:**
        - ``navBar`` -- the top navigation bar
        - ``htmlId`` -- *id* attribute of the body
        - ``content`` -- body content built from smaller HTML code blocks
        - ``extraAttr`` -- an extra attributes to be added to the body definition
        - ``relativeUrlBase`` -- how to get back to the document root
        - ``responsive`` -- should the webpage be responsive to screen-size?
        - ``googleAnalyticsCode`` -- google analytics code for the website
        - ``jsFileName`` -- the name of the main javascript file

    **Return:**
        - ``body`` -- the body
    """
    if not navBar:
        navBar = ''
    if googleAnalyticsCode:
        googleAnalyticsCode = "\n        <!-- Google Analytics -->\n        <script>\n            var _gaq=[['_setAccount','%s'],['_trackPageview']];\n            (function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];\n            g.src=('https:'==location.protocol?'//ssl':'//www')+'.google-analytics.com/ga.js';\n            s.parentNode.insertBefore(g,s)}(document,'script'));\n        </script>\n        " % (googleAnalyticsCode,)
    else:
        googleAnalyticsCode = ''
    container = _container(responsive=responsive, content=content, htmlId=False, htmlClass=False, onPhone=True, onTablet=True, onDesktop=True)
    body = '\n      <body id="%s" %s>\n      <!--[if lt IE 7]>\n        <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>\n      <![endif]-->\n        %s\n        %s\n      <script src="%s/assets/js/%s"></script>\n      %s\n      </body><!-- /#%s-->\n      ' % (
     htmlId,
     extraAttr,
     navBar,
     container,
     relativeUrlBase,
     jsFileName,
     googleAnalyticsCode,
     htmlId)
    return body


def row(responsive=True, columns='', htmlId=False, htmlClass=False, onPhone=True, onTablet=True, onDesktop=True):
    """Create a row using the Twitter Bootstrap static layout grid.
    The static Bootstrap grid system utilizes 12 columns.

    **Key Arguments:**
        - ``responsive`` -- fluid layout if true, fixed if false
        - ``columns`` -- coulmns to be included in this row
        - ``htmlId`` -- the id of the row
        - ``htmlClass`` -- the class of the row
        - ``onPhone`` -- does this row get displayed on a phone sized screen
        - ``onTablet`` -- does this row get displayed on a tablet sized screen
        - ``onDesktop`` -- does this row get displayed on a desktop sized screen

    **Return:**
        - ``row`` -- the row """
    if responsive:
        responsive = '-fluid'
    else:
        responsive = ''
    if htmlId:
        htmlId = 'id="%s" ' % (htmlId,)
    else:
        htmlId = ''
    if not htmlClass:
        htmlClass = ''
    if onPhone:
        onPhone = ''
    else:
        onPhone = 'hidden-phone'
    if onTablet:
        onTablet = ''
    else:
        onTablet = 'hidden-tablet'
    if onDesktop:
        onDesktop = ''
    else:
        onDesktop = 'hidden-desktop'
    row = '\n        <div class="row%s %s %s %s %s" %s>\n            %s\n        </div>\n    ' % (
     responsive,
     htmlClass,
     onPhone,
     onTablet,
     onDesktop,
     htmlId,
     columns)
    return row


def get_javascript_block(jsPath):
    """ Create a javascript *<script>* html code block

  ****Key Arguments:****
    - ``jsPath`` -- path the js file

  **Return:**
    - ``block`` -- HTML code block """
    block = '<script src="%s" type="text/javascript" charset="utf-8"></script>' % (jsPath,)
    return block
    d = attributeDict
    block = '<%s ' % (d['tag'],)
    if d.has_key('htmlClass'):
        block += 'class="%s" ' % (d['htmlClass'],)
    if d.has_key('htmlId'):
        block += 'id="%s" ' % (d['htmlId'],)
    if d.has_key('jsEvents'):
        block += '%s ' % (d['jsEvents'],)
    if d.has_key('extraAttr'):
        block += '%s ' % (d['extraAttr'],)
    if d.has_key('href'):
        block += 'href="%s" ' % (d['href'],)
        if d['href'][0] not in ('.', '/') and 'index.py' not in d['href']:
            block += 'target="_blank" '
    if d.has_key('src'):
        block += 'src="%s" ' % (d['src'],)
    if d.has_key('alt'):
        block += 'alt="%s" ' % (d['alt'],)
    if d.has_key('action'):
        block += 'action="%s" ' % (d['action'],)
    if d.has_key('method'):
        block += 'method="%s" ' % (d['method'],)
    if d.has_key('type'):
        block += 'type="%s" ' % (d['type'],)
    block += '>'
    if d.has_key('blockContent'):
        block += str(d['blockContent'])
    if d.has_key('htmlId'):
        block += '</%s><!--- /#%s --->' % (d['tag'], d['htmlId'])
    else:
        block += '</%s>' % (d['tag'],)
    return block


def grid_column(log, span=1, offset=0, content='', htmlId=False, htmlClass=False, onPhone=True, onTablet=True, onDesktop=True):
    """ Get a column block for the Twiiter Bootstrap static layout grid.

    **Key Arguments:**
        - ``log`` -- logger
        - ``span`` -- the relative width of the column
        - ``offset`` -- increase the left margin of the column by this amount
        - ``htmlId`` -- the id of the column
        - ``htmlClass`` -- the class of the column
        - ``onPhone`` -- does this column get displayed on a phone sized screen
        - ``onTablet`` -- does this column get displayed on a tablet sized screen
        - ``onDesktop`` -- does this column get displayed on a desktop sized screen

    **Return:**
        - ``column`` -- the column """
    if htmlId:
        htmlId = 'id="%s" ' % (htmlId,)
    else:
        htmlId = ''
    if not htmlClass:
        htmlClass = ''
    if onPhone:
        onPhone = ''
    else:
        onPhone = 'hidden-phone'
    if onTablet:
        onTablet = ''
    else:
        onTablet = 'hidden-tablet'
    if onDesktop:
        onDesktop = ''
    else:
        onDesktop = 'hidden-desktop'
    column = '\n        <div class="span%s offset%s %s %s %s %s" %s>\n            %s\n        </div>\n    ' % (
     span,
     offset,
     htmlClass,
     onPhone,
     onTablet,
     onDesktop,
     htmlId,
     content)
    return column


def _container(responsive=True, content='', htmlId=False, htmlClass=False, onPhone=True, onTablet=True, onDesktop=True):
    """ The over-all content container for the twitter bootstrap webpage

    **Key Arguments:**
        - ``responsive`` -- fluid layout if true, fixed if false
        - ``content`` -- html content of the container div
        - ``htmlId`` -- the id of the container
        - ``htmlClass`` -- the class of the container
        - ``onPhone`` -- does this container get displayed on a phone sized screen
        - ``onTablet`` -- does this container get displayed on a tablet sized screen
        - ``onDesktop`` -- does this container get displayed on a desktop sized screen

    **Return:**
        - None """
    if responsive:
        responsive = '-fluid'
    else:
        responsive = ''
    if htmlId:
        htmlId = 'id="%s" ' % (htmlId,)
    else:
        htmlId = ''
    if not htmlClass:
        htmlClass = ''
    if onPhone:
        onPhone = ''
    else:
        onPhone = 'hidden-phone'
    if onTablet:
        onTablet = ''
    else:
        onTablet = 'hidden-tablet'
    if onDesktop:
        onDesktop = ''
    else:
        onDesktop = 'hidden-desktop'
    container = '\n        <div class="container%s %s %s %s %s" %s>\n            %s\n        </div>\n    ' % (
     responsive,
     htmlClass,
     onPhone,
     onTablet,
     onDesktop,
     htmlId,
     content)
    return container