# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/scour/scour.py
# Compiled at: 2019-07-07 17:34:49
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import math, optparse, os, re, sys, time, xml.dom.minidom
from xml.dom import Node, NotFoundErr
from collections import namedtuple, defaultdict
from decimal import Context, Decimal, InvalidOperation, getcontext
import six
from six.moves import range, urllib
from beampy.scour.svg_regex import svg_parser
from beampy.scour.svg_transform import svg_transform_parser
from beampy.scour.yocto_css import parseCssString
from beampy.scour import __version__
APP = 'scour'
VER = __version__
COPYRIGHT = 'Copyright Jeff Schiller, Louis Simard, 2010'
NS = {'SVG': 'http://www.w3.org/2000/svg', 'XLINK': 'http://www.w3.org/1999/xlink', 
   'SODIPODI': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd', 
   'INKSCAPE': 'http://www.inkscape.org/namespaces/inkscape', 
   'ADOBE_ILLUSTRATOR': 'http://ns.adobe.com/AdobeIllustrator/10.0/', 
   'ADOBE_GRAPHS': 'http://ns.adobe.com/Graphs/1.0/', 
   'ADOBE_SVG_VIEWER': 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/', 
   'ADOBE_VARIABLES': 'http://ns.adobe.com/Variables/1.0/', 
   'ADOBE_SFW': 'http://ns.adobe.com/SaveForWeb/1.0/', 
   'ADOBE_EXTENSIBILITY': 'http://ns.adobe.com/Extensibility/1.0/', 
   'ADOBE_FLOWS': 'http://ns.adobe.com/Flows/1.0/', 
   'ADOBE_IMAGE_REPLACEMENT': 'http://ns.adobe.com/ImageReplacement/1.0/', 
   'ADOBE_CUSTOM': 'http://ns.adobe.com/GenericCustomNamespace/1.0/', 
   'ADOBE_XPATH': 'http://ns.adobe.com/XPath/1.0/', 
   'SKETCH': 'http://www.bohemiancoding.com/sketch/ns'}
unwanted_ns = [
 NS['SODIPODI'], NS['INKSCAPE'], NS['ADOBE_ILLUSTRATOR'],
 NS['ADOBE_GRAPHS'], NS['ADOBE_SVG_VIEWER'], NS['ADOBE_VARIABLES'],
 NS['ADOBE_SFW'], NS['ADOBE_EXTENSIBILITY'], NS['ADOBE_FLOWS'],
 NS['ADOBE_IMAGE_REPLACEMENT'], NS['ADOBE_CUSTOM'],
 NS['ADOBE_XPATH'], NS['SKETCH']]
svgAttributes = [
 'alignment-baseline',
 'baseline-shift',
 'clip',
 'clip-path',
 'clip-rule',
 'color',
 'color-interpolation',
 'color-interpolation-filters',
 'color-profile',
 'color-rendering',
 'cursor',
 'direction',
 'display',
 'dominant-baseline',
 'enable-background',
 'fill',
 'fill-opacity',
 'fill-rule',
 'filter',
 'flood-color',
 'flood-opacity',
 'font',
 'font-family',
 'font-size',
 'font-size-adjust',
 'font-stretch',
 'font-style',
 'font-variant',
 'font-weight',
 'glyph-orientation-horizontal',
 'glyph-orientation-vertical',
 'image-rendering',
 'kerning',
 'letter-spacing',
 'lighting-color',
 'marker',
 'marker-end',
 'marker-mid',
 'marker-start',
 'mask',
 'opacity',
 'overflow',
 'pointer-events',
 'shape-rendering',
 'stop-color',
 'stop-opacity',
 'stroke',
 'stroke-dasharray',
 'stroke-dashoffset',
 'stroke-linecap',
 'stroke-linejoin',
 'stroke-miterlimit',
 'stroke-opacity',
 'stroke-width',
 'text-anchor',
 'text-decoration',
 'text-rendering',
 'unicode-bidi',
 'visibility',
 'word-spacing',
 'writing-mode',
 'audio-level',
 'buffered-rendering',
 'display-align',
 'line-increment',
 'solid-color',
 'solid-opacity',
 'text-align',
 'vector-effect',
 'viewport-fill',
 'viewport-fill-opacity']
colors = {'aliceblue': 'rgb(240, 248, 255)', 
   'antiquewhite': 'rgb(250, 235, 215)', 
   'aqua': 'rgb( 0, 255, 255)', 
   'aquamarine': 'rgb(127, 255, 212)', 
   'azure': 'rgb(240, 255, 255)', 
   'beige': 'rgb(245, 245, 220)', 
   'bisque': 'rgb(255, 228, 196)', 
   'black': 'rgb( 0, 0, 0)', 
   'blanchedalmond': 'rgb(255, 235, 205)', 
   'blue': 'rgb( 0, 0, 255)', 
   'blueviolet': 'rgb(138, 43, 226)', 
   'brown': 'rgb(165, 42, 42)', 
   'burlywood': 'rgb(222, 184, 135)', 
   'cadetblue': 'rgb( 95, 158, 160)', 
   'chartreuse': 'rgb(127, 255, 0)', 
   'chocolate': 'rgb(210, 105, 30)', 
   'coral': 'rgb(255, 127, 80)', 
   'cornflowerblue': 'rgb(100, 149, 237)', 
   'cornsilk': 'rgb(255, 248, 220)', 
   'crimson': 'rgb(220, 20, 60)', 
   'cyan': 'rgb( 0, 255, 255)', 
   'darkblue': 'rgb( 0, 0, 139)', 
   'darkcyan': 'rgb( 0, 139, 139)', 
   'darkgoldenrod': 'rgb(184, 134, 11)', 
   'darkgray': 'rgb(169, 169, 169)', 
   'darkgreen': 'rgb( 0, 100, 0)', 
   'darkgrey': 'rgb(169, 169, 169)', 
   'darkkhaki': 'rgb(189, 183, 107)', 
   'darkmagenta': 'rgb(139, 0, 139)', 
   'darkolivegreen': 'rgb( 85, 107, 47)', 
   'darkorange': 'rgb(255, 140, 0)', 
   'darkorchid': 'rgb(153, 50, 204)', 
   'darkred': 'rgb(139, 0, 0)', 
   'darksalmon': 'rgb(233, 150, 122)', 
   'darkseagreen': 'rgb(143, 188, 143)', 
   'darkslateblue': 'rgb( 72, 61, 139)', 
   'darkslategray': 'rgb( 47, 79, 79)', 
   'darkslategrey': 'rgb( 47, 79, 79)', 
   'darkturquoise': 'rgb( 0, 206, 209)', 
   'darkviolet': 'rgb(148, 0, 211)', 
   'deeppink': 'rgb(255, 20, 147)', 
   'deepskyblue': 'rgb( 0, 191, 255)', 
   'dimgray': 'rgb(105, 105, 105)', 
   'dimgrey': 'rgb(105, 105, 105)', 
   'dodgerblue': 'rgb( 30, 144, 255)', 
   'firebrick': 'rgb(178, 34, 34)', 
   'floralwhite': 'rgb(255, 250, 240)', 
   'forestgreen': 'rgb( 34, 139, 34)', 
   'fuchsia': 'rgb(255, 0, 255)', 
   'gainsboro': 'rgb(220, 220, 220)', 
   'ghostwhite': 'rgb(248, 248, 255)', 
   'gold': 'rgb(255, 215, 0)', 
   'goldenrod': 'rgb(218, 165, 32)', 
   'gray': 'rgb(128, 128, 128)', 
   'grey': 'rgb(128, 128, 128)', 
   'green': 'rgb( 0, 128, 0)', 
   'greenyellow': 'rgb(173, 255, 47)', 
   'honeydew': 'rgb(240, 255, 240)', 
   'hotpink': 'rgb(255, 105, 180)', 
   'indianred': 'rgb(205, 92, 92)', 
   'indigo': 'rgb( 75, 0, 130)', 
   'ivory': 'rgb(255, 255, 240)', 
   'khaki': 'rgb(240, 230, 140)', 
   'lavender': 'rgb(230, 230, 250)', 
   'lavenderblush': 'rgb(255, 240, 245)', 
   'lawngreen': 'rgb(124, 252, 0)', 
   'lemonchiffon': 'rgb(255, 250, 205)', 
   'lightblue': 'rgb(173, 216, 230)', 
   'lightcoral': 'rgb(240, 128, 128)', 
   'lightcyan': 'rgb(224, 255, 255)', 
   'lightgoldenrodyellow': 'rgb(250, 250, 210)', 
   'lightgray': 'rgb(211, 211, 211)', 
   'lightgreen': 'rgb(144, 238, 144)', 
   'lightgrey': 'rgb(211, 211, 211)', 
   'lightpink': 'rgb(255, 182, 193)', 
   'lightsalmon': 'rgb(255, 160, 122)', 
   'lightseagreen': 'rgb( 32, 178, 170)', 
   'lightskyblue': 'rgb(135, 206, 250)', 
   'lightslategray': 'rgb(119, 136, 153)', 
   'lightslategrey': 'rgb(119, 136, 153)', 
   'lightsteelblue': 'rgb(176, 196, 222)', 
   'lightyellow': 'rgb(255, 255, 224)', 
   'lime': 'rgb( 0, 255, 0)', 
   'limegreen': 'rgb( 50, 205, 50)', 
   'linen': 'rgb(250, 240, 230)', 
   'magenta': 'rgb(255, 0, 255)', 
   'maroon': 'rgb(128, 0, 0)', 
   'mediumaquamarine': 'rgb(102, 205, 170)', 
   'mediumblue': 'rgb( 0, 0, 205)', 
   'mediumorchid': 'rgb(186, 85, 211)', 
   'mediumpurple': 'rgb(147, 112, 219)', 
   'mediumseagreen': 'rgb( 60, 179, 113)', 
   'mediumslateblue': 'rgb(123, 104, 238)', 
   'mediumspringgreen': 'rgb( 0, 250, 154)', 
   'mediumturquoise': 'rgb( 72, 209, 204)', 
   'mediumvioletred': 'rgb(199, 21, 133)', 
   'midnightblue': 'rgb( 25, 25, 112)', 
   'mintcream': 'rgb(245, 255, 250)', 
   'mistyrose': 'rgb(255, 228, 225)', 
   'moccasin': 'rgb(255, 228, 181)', 
   'navajowhite': 'rgb(255, 222, 173)', 
   'navy': 'rgb( 0, 0, 128)', 
   'oldlace': 'rgb(253, 245, 230)', 
   'olive': 'rgb(128, 128, 0)', 
   'olivedrab': 'rgb(107, 142, 35)', 
   'orange': 'rgb(255, 165, 0)', 
   'orangered': 'rgb(255, 69, 0)', 
   'orchid': 'rgb(218, 112, 214)', 
   'palegoldenrod': 'rgb(238, 232, 170)', 
   'palegreen': 'rgb(152, 251, 152)', 
   'paleturquoise': 'rgb(175, 238, 238)', 
   'palevioletred': 'rgb(219, 112, 147)', 
   'papayawhip': 'rgb(255, 239, 213)', 
   'peachpuff': 'rgb(255, 218, 185)', 
   'peru': 'rgb(205, 133, 63)', 
   'pink': 'rgb(255, 192, 203)', 
   'plum': 'rgb(221, 160, 221)', 
   'powderblue': 'rgb(176, 224, 230)', 
   'purple': 'rgb(128, 0, 128)', 
   'red': 'rgb(255, 0, 0)', 
   'rosybrown': 'rgb(188, 143, 143)', 
   'royalblue': 'rgb( 65, 105, 225)', 
   'saddlebrown': 'rgb(139, 69, 19)', 
   'salmon': 'rgb(250, 128, 114)', 
   'sandybrown': 'rgb(244, 164, 96)', 
   'seagreen': 'rgb( 46, 139, 87)', 
   'seashell': 'rgb(255, 245, 238)', 
   'sienna': 'rgb(160, 82, 45)', 
   'silver': 'rgb(192, 192, 192)', 
   'skyblue': 'rgb(135, 206, 235)', 
   'slateblue': 'rgb(106, 90, 205)', 
   'slategray': 'rgb(112, 128, 144)', 
   'slategrey': 'rgb(112, 128, 144)', 
   'snow': 'rgb(255, 250, 250)', 
   'springgreen': 'rgb( 0, 255, 127)', 
   'steelblue': 'rgb( 70, 130, 180)', 
   'tan': 'rgb(210, 180, 140)', 
   'teal': 'rgb( 0, 128, 128)', 
   'thistle': 'rgb(216, 191, 216)', 
   'tomato': 'rgb(255, 99, 71)', 
   'turquoise': 'rgb( 64, 224, 208)', 
   'violet': 'rgb(238, 130, 238)', 
   'wheat': 'rgb(245, 222, 179)', 
   'white': 'rgb(255, 255, 255)', 
   'whitesmoke': 'rgb(245, 245, 245)', 
   'yellow': 'rgb(255, 255, 0)', 
   'yellowgreen': 'rgb(154, 205, 50)'}
default_properties = {'baseline-shift': 'baseline', 
   'clip-path': 'none', 
   'clip-rule': 'nonzero', 
   'color': '#000', 
   'color-interpolation-filters': 'linearRGB', 
   'color-interpolation': 'sRGB', 
   'direction': 'ltr', 
   'display': 'inline', 
   'enable-background': 'accumulate', 
   'fill': '#000', 
   'fill-opacity': '1', 
   'fill-rule': 'nonzero', 
   'filter': 'none', 
   'flood-color': '#000', 
   'flood-opacity': '1', 
   'font-size-adjust': 'none', 
   'font-size': 'medium', 
   'font-stretch': 'normal', 
   'font-style': 'normal', 
   'font-variant': 'normal', 
   'font-weight': 'normal', 
   'glyph-orientation-horizontal': '0deg', 
   'letter-spacing': 'normal', 
   'lighting-color': '#fff', 
   'marker': 'none', 
   'marker-start': 'none', 
   'marker-mid': 'none', 
   'marker-end': 'none', 
   'mask': 'none', 
   'opacity': '1', 
   'pointer-events': 'visiblePainted', 
   'stop-color': '#000', 
   'stop-opacity': '1', 
   'stroke': 'none', 
   'stroke-dasharray': 'none', 
   'stroke-dashoffset': '0', 
   'stroke-linecap': 'butt', 
   'stroke-linejoin': 'miter', 
   'stroke-miterlimit': '4', 
   'stroke-opacity': '1', 
   'stroke-width': '1', 
   'text-anchor': 'start', 
   'text-decoration': 'none', 
   'unicode-bidi': 'normal', 
   'visibility': 'visible', 
   'word-spacing': 'normal', 
   'writing-mode': 'lr-tb', 
   'audio-level': '1', 
   'solid-color': '#000', 
   'solid-opacity': '1', 
   'text-align': 'start', 
   'vector-effect': 'none', 
   'viewport-fill': 'none', 
   'viewport-fill-opacity': '1'}

def is_same_sign(a, b):
    return a <= 0 and b <= 0 or a >= 0 and b >= 0


def is_same_direction(x1, y1, x2, y2):
    if is_same_sign(x1, x2) and is_same_sign(y1, y2):
        diff = y1 / x1 - y2 / x2
        return scouringContext.plus(1 + diff) == 1
    else:
        return False


scinumber = re.compile('[-+]?(\\d*\\.?)?\\d+[eE][-+]?\\d+')
number = re.compile('[-+]?(\\d*\\.?)?\\d+')
sciExponent = re.compile('[eE]([-+]?\\d+)')
unit = re.compile('(em|ex|px|pt|pc|cm|mm|in|%){1,1}$')

class Unit(object):
    INVALID = -1
    NONE = 0
    PCT = 1
    PX = 2
    PT = 3
    PC = 4
    EM = 5
    EX = 6
    CM = 7
    MM = 8
    IN = 9
    s2u = {'': NONE, 
       '%': PCT, 
       'px': PX, 
       'pt': PT, 
       'pc': PC, 
       'em': EM, 
       'ex': EX, 
       'cm': CM, 
       'mm': MM, 
       'in': IN}
    u2s = {NONE: '', 
       PCT: '%', 
       PX: 'px', 
       PT: 'pt', 
       PC: 'pc', 
       EM: 'em', 
       EX: 'ex', 
       CM: 'cm', 
       MM: 'mm', 
       IN: 'in'}

    def get(unitstr):
        if unitstr is None:
            return Unit.NONE
        else:
            try:
                return Unit.s2u[unitstr]
            except KeyError:
                return Unit.INVALID

            return

    def str(unitint):
        try:
            return Unit.u2s[unitint]
        except KeyError:
            return 'INVALID'

    get = staticmethod(get)
    str = staticmethod(str)


class SVGLength(object):

    def __init__(self, str):
        try:
            self.value = float(str)
            if int(self.value) == self.value:
                self.value = int(self.value)
            self.units = Unit.NONE
        except ValueError:
            self.value = 0
            unitBegin = 0
            scinum = scinumber.match(str)
            if scinum is not None:
                numMatch = number.match(str)
                expMatch = sciExponent.search(str, numMatch.start(0))
                self.value = float(numMatch.group(0)) * 10 ** float(expMatch.group(1))
                unitBegin = expMatch.end(1)
            else:
                numMatch = number.match(str)
                if numMatch is not None:
                    self.value = float(numMatch.group(0))
                    unitBegin = numMatch.end(0)
            if int(self.value) == self.value:
                self.value = int(self.value)
            if unitBegin != 0:
                unitMatch = unit.search(str, unitBegin)
                if unitMatch is not None:
                    self.units = Unit.get(unitMatch.group(0))
            else:
                self.value = 0
                self.units = Unit.INVALID

        return


def findElementsWithId(node, elems=None):
    """
    Returns all elements with id attributes
    """
    if elems is None:
        elems = {}
    id = node.getAttribute('id')
    if id != '':
        elems[id] = node
    if node.hasChildNodes():
        for child in node.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                findElementsWithId(child, elems)

    return elems


referencingProps = [
 'fill', 'stroke', 'filter', 'clip-path', 'mask', 'marker-start', 'marker-end', 'marker-mid']

def findReferencedElements(node, ids=None):
    """
    Returns IDs of all referenced elements
    - node is the node at which to start the search.
    - returns a map which has the id as key and
      each value is is a list of nodes

    Currently looks at 'xlink:href' and all attributes in 'referencingProps'
    """
    global referencingProps
    if ids is None:
        ids = {}
    if node.nodeName == 'style' and node.namespaceURI == NS['SVG']:
        stylesheet = ('').join([ child.nodeValue for child in node.childNodes ])
        if stylesheet != '':
            cssRules = parseCssString(stylesheet)
            for rule in cssRules:
                for propname in rule['properties']:
                    propval = rule['properties'][propname]
                    findReferencingProperty(node, propname, propval, ids)

        return ids
    href = node.getAttributeNS(NS['XLINK'], 'href')
    if href != '' and len(href) > 1 and href[0] == '#':
        id = href[1:]
        if id in ids:
            ids[id].append(node)
        else:
            ids[id] = [
             node]
    styles = node.getAttribute('style').split(';')
    for style in styles:
        propval = style.split(':')
        if len(propval) == 2:
            prop = propval[0].strip()
            val = propval[1].strip()
            findReferencingProperty(node, prop, val, ids)

    for attr in referencingProps:
        val = node.getAttribute(attr).strip()
        if not val:
            continue
        findReferencingProperty(node, attr, val, ids)

    if node.hasChildNodes():
        for child in node.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                findReferencedElements(child, ids)

    return ids


def findReferencingProperty(node, prop, val, ids):
    if prop in referencingProps and val != '':
        if len(val) >= 7 and val[0:5] == 'url(#':
            id = val[5:val.find(')')]
            if id in ids:
                ids[id].append(node)
            else:
                ids[id] = [
                 node]
        elif len(val) >= 8:
            id = None
            if val[0:6] == 'url("#':
                id = val[6:val.find('")')]
            elif val[0:6] == "url('#":
                id = val[6:val.find("')")]
            if id is not None:
                if id in ids:
                    ids[id].append(node)
                else:
                    ids[id] = [
                     node]
    return


def removeUnusedDefs(doc, defElem, elemsToRemove=None, referencedIDs=None):
    if elemsToRemove is None:
        elemsToRemove = []
    if referencedIDs is None:
        referencedIDs = findReferencedElements(doc.documentElement)
    keepTags = ['font', 'style', 'metadata', 'script', 'title', 'desc']
    for elem in defElem.childNodes:
        if elem.nodeType == Node.ELEMENT_NODE and (elem.getAttribute('id') == '' or elem.getAttribute('id') not in referencedIDs):
            if elem.nodeName == 'g' and elem.namespaceURI == NS['SVG']:
                elemsToRemove = removeUnusedDefs(doc, elem, elemsToRemove, referencedIDs=referencedIDs)
            elif elem.nodeName not in keepTags:
                elemsToRemove.append(elem)

    return elemsToRemove


def removeUnreferencedElements(doc, keepDefs):
    """
    Removes all unreferenced elements except for <svg>, <font>, <metadata>, <title>, and <desc>.
    Also vacuums the defs of any non-referenced renderable elements.

    Returns the number of unreferenced elements removed from the document.
    """
    global _num_elements_removed
    num = 0
    removeTags = [
     'linearGradient', 'radialGradient', 'pattern']
    identifiedElements = findElementsWithId(doc.documentElement)
    referencedIDs = findReferencedElements(doc.documentElement)
    for id in identifiedElements:
        if id not in referencedIDs:
            goner = identifiedElements[id]
            if goner is not None and goner.nodeName in removeTags and goner.parentNode is not None and goner.parentNode.tagName != 'defs':
                goner.parentNode.removeChild(goner)
                num += 1
                _num_elements_removed += 1

    if not keepDefs:
        defs = doc.documentElement.getElementsByTagName('defs')
        for aDef in defs:
            elemsToRemove = removeUnusedDefs(doc, aDef)
            for elem in elemsToRemove:
                elem.parentNode.removeChild(elem)
                _num_elements_removed += 1
                num += 1

    return num


def shortenIDs(doc, prefix, unprotectedElements=None):
    """
    Shortens ID names used in the document. ID names referenced the most often are assigned the
    shortest ID names.
    If the list unprotectedElements is provided, only IDs from this list will be shortened.

    Returns the number of bytes saved by shortening ID names in the document.
    """
    num = 0
    identifiedElements = findElementsWithId(doc.documentElement)
    if unprotectedElements is None:
        unprotectedElements = identifiedElements
    referencedIDs = findReferencedElements(doc.documentElement)
    idList = [ (len(referencedIDs[rid]), rid) for rid in referencedIDs if rid in unprotectedElements
             ]
    idList.sort(reverse=True)
    idList = [ rid for count, rid in idList ]
    idList.extend([ rid for rid in unprotectedElements if rid not in idList ])
    curIdNum = 1
    for rid in idList:
        curId = intToID(curIdNum, prefix)
        if curId != rid:
            while curId in identifiedElements:
                curIdNum += 1
                curId = intToID(curIdNum, prefix)

            num += renameID(doc, rid, curId, identifiedElements, referencedIDs)
        curIdNum += 1

    return num


def intToID(idnum, prefix):
    """
    Returns the ID name for the given ID number, spreadsheet-style, i.e. from a to z,
    then from aa to az, ba to bz, etc., until zz.
    """
    rid = ''
    while idnum > 0:
        idnum -= 1
        rid = chr(idnum % 26 + ord('a')) + rid
        idnum = int(idnum / 26)

    return prefix + rid


def renameID(doc, idFrom, idTo, identifiedElements, referencedIDs):
    """
    Changes the ID name from idFrom to idTo, on the declaring element
    as well as all references in the document doc.

    Updates identifiedElements and referencedIDs.
    Does not handle the case where idTo is already the ID name
    of another element in doc.

    Returns the number of bytes saved by this replacement.
    """
    num = 0
    definingNode = identifiedElements[idFrom]
    definingNode.setAttribute('id', idTo)
    del identifiedElements[idFrom]
    identifiedElements[idTo] = definingNode
    num += len(idFrom) - len(idTo)
    referringNodes = referencedIDs.get(idFrom)
    if referringNodes is not None:
        for node in referringNodes:
            if node.nodeName == 'style' and node.namespaceURI == NS['SVG']:
                if node.firstChild is not None:
                    oldValue = ('').join([ child.nodeValue for child in node.childNodes ])
                    newValue = oldValue.replace('url(#' + idFrom + ')', 'url(#' + idTo + ')')
                    newValue = newValue.replace("url(#'" + idFrom + "')", 'url(#' + idTo + ')')
                    newValue = newValue.replace('url(#"' + idFrom + '")', 'url(#' + idTo + ')')
                    node.childNodes[:] = [
                     node.ownerDocument.createTextNode(newValue)]
                    num += len(oldValue) - len(newValue)
            href = node.getAttributeNS(NS['XLINK'], 'href')
            if href == '#' + idFrom:
                node.setAttributeNS(NS['XLINK'], 'href', '#' + idTo)
                num += len(idFrom) - len(idTo)
            styles = node.getAttribute('style')
            if styles != '':
                newValue = styles.replace('url(#' + idFrom + ')', 'url(#' + idTo + ')')
                newValue = newValue.replace("url('#" + idFrom + "')", 'url(#' + idTo + ')')
                newValue = newValue.replace('url("#' + idFrom + '")', 'url(#' + idTo + ')')
                node.setAttribute('style', newValue)
                num += len(styles) - len(newValue)
            for attr in referencingProps:
                oldValue = node.getAttribute(attr)
                if oldValue != '':
                    newValue = oldValue.replace('url(#' + idFrom + ')', 'url(#' + idTo + ')')
                    newValue = newValue.replace("url('#" + idFrom + "')", 'url(#' + idTo + ')')
                    newValue = newValue.replace('url("#' + idFrom + '")', 'url(#' + idTo + ')')
                    node.setAttribute(attr, newValue)
                    num += len(oldValue) - len(newValue)

        del referencedIDs[idFrom]
        referencedIDs[idTo] = referringNodes
    return num


def unprotected_ids(doc, options):
    """Returns a list of unprotected IDs within the document doc."""
    identifiedElements = findElementsWithId(doc.documentElement)
    if not (options.protect_ids_noninkscape or options.protect_ids_list or options.protect_ids_prefix):
        return identifiedElements
    if options.protect_ids_list:
        protect_ids_list = options.protect_ids_list.split(',')
    if options.protect_ids_prefix:
        protect_ids_prefixes = options.protect_ids_prefix.split(',')
    for id in list(identifiedElements):
        protected = False
        if options.protect_ids_noninkscape and not id[(-1)].isdigit():
            protected = True
        if options.protect_ids_list and id in protect_ids_list:
            protected = True
        if options.protect_ids_prefix:
            for prefix in protect_ids_prefixes:
                if id.startswith(prefix):
                    protected = True

        if protected:
            del identifiedElements[id]

    return identifiedElements


def removeUnreferencedIDs(referencedIDs, identifiedElements):
    """
    Removes the unreferenced ID attributes.

    Returns the number of ID attributes removed
    """
    global _num_ids_removed
    keepTags = [
     'font']
    num = 0
    for id in identifiedElements:
        node = identifiedElements[id]
        if id not in referencedIDs and node.nodeName not in keepTags:
            node.removeAttribute('id')
            _num_ids_removed += 1
            num += 1

    return num


def removeNamespacedAttributes(node, namespaces):
    global _num_attributes_removed
    num = 0
    if node.nodeType == Node.ELEMENT_NODE:
        attrList = node.attributes
        attrsToRemove = []
        for attrNum in range(attrList.length):
            attr = attrList.item(attrNum)
            if attr is not None and attr.namespaceURI in namespaces:
                attrsToRemove.append(attr.nodeName)

        for attrName in attrsToRemove:
            num += 1
            _num_attributes_removed += 1
            node.removeAttribute(attrName)

        for child in node.childNodes:
            num += removeNamespacedAttributes(child, namespaces)

    return num


def removeNamespacedElements(node, namespaces):
    global _num_elements_removed
    num = 0
    if node.nodeType == Node.ELEMENT_NODE:
        childList = node.childNodes
        childrenToRemove = []
        for child in childList:
            if child is not None and child.namespaceURI in namespaces:
                childrenToRemove.append(child)

        for child in childrenToRemove:
            num += 1
            _num_elements_removed += 1
            node.removeChild(child)

        for child in node.childNodes:
            num += removeNamespacedElements(child, namespaces)

    return num


def removeDescriptiveElements(doc, options):
    global _num_elements_removed
    elementTypes = []
    if options.remove_descriptive_elements:
        elementTypes.extend(('title', 'desc', 'metadata'))
    else:
        if options.remove_titles:
            elementTypes.append('title')
        if options.remove_descriptions:
            elementTypes.append('desc')
        if options.remove_metadata:
            elementTypes.append('metadata')
        if not elementTypes:
            return
        num = 0
        elementsToRemove = []
        for elementType in elementTypes:
            elementsToRemove.extend(doc.documentElement.getElementsByTagName(elementType))

        for element in elementsToRemove:
            element.parentNode.removeChild(element)
            num += 1
            _num_elements_removed += 1

    return num


def removeNestedGroups(node):
    """
    This walks further and further down the tree, removing groups
    which do not have any attributes or a title/desc child and
    promoting their children up one level
    """
    global _num_elements_removed
    num = 0
    groupsToRemove = []
    if not (node.nodeType == Node.ELEMENT_NODE and node.nodeName == 'switch'):
        for child in node.childNodes:
            if child.nodeName == 'g' and child.namespaceURI == NS['SVG'] and len(child.attributes) == 0:
                for grandchild in child.childNodes:
                    if grandchild.nodeType == Node.ELEMENT_NODE and grandchild.namespaceURI == NS['SVG'] and grandchild.nodeName in ('title',
                                                                                                                                     'desc'):
                        break
                else:
                    groupsToRemove.append(child)

    for g in groupsToRemove:
        while g.childNodes.length > 0:
            g.parentNode.insertBefore(g.firstChild, g)

        g.parentNode.removeChild(g)
        _num_elements_removed += 1
        num += 1

    for child in node.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            num += removeNestedGroups(child)

    return num


def moveCommonAttributesToParentGroup(elem, referencedElements):
    """
    This recursively calls this function on all children of the passed in element
    and then iterates over all child elements and removes common inheritable attributes
    from the children and places them in the parent group.  But only if the parent contains
    nothing but element children and whitespace.  The attributes are only removed from the
    children if the children are not referenced by other elements in the document.
    """
    num = 0
    childElements = []
    for child in elem.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.getAttribute('id') not in referencedElements:
                childElements.append(child)
                num += moveCommonAttributesToParentGroup(child, referencedElements)
        elif child.nodeType == Node.TEXT_NODE and child.nodeValue.strip():
            return num

    if len(childElements) <= 1:
        return num
    commonAttrs = {}
    attrList = childElements[0].attributes
    for index in range(attrList.length):
        attr = attrList.item(index)
        if attr.nodeName in ('clip-rule', 'display-align', 'fill', 'fill-opacity',
                             'fill-rule', 'font', 'font-family', 'font-size', 'font-size-adjust',
                             'font-stretch', 'font-style', 'font-variant', 'font-weight',
                             'letter-spacing', 'pointer-events', 'shape-rendering',
                             'stroke', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-linecap',
                             'stroke-linejoin', 'stroke-miterlimit', 'stroke-opacity',
                             'stroke-width', 'text-anchor', 'text-decoration', 'text-rendering',
                             'visibility', 'word-spacing', 'writing-mode'):
            commonAttrs[attr.nodeName] = attr.nodeValue

    for childNum in range(len(childElements)):
        if childNum == 0:
            continue
        child = childElements[childNum]
        if child.localName in ('set', 'animate', 'animateColor', 'animateTransform',
                               'animateMotion'):
            continue
        distinctAttrs = []
        for name in commonAttrs:
            if child.getAttribute(name) != commonAttrs[name]:
                distinctAttrs.append(name)

        for name in distinctAttrs:
            del commonAttrs[name]

    for name in commonAttrs:
        for child in childElements:
            child.removeAttribute(name)

        elem.setAttribute(name, commonAttrs[name])

    num += (len(childElements) - 1) * len(commonAttrs)
    return num


def createGroupsForCommonAttributes(elem):
    """
    Creates <g> elements to contain runs of 3 or more
    consecutive child elements having at least one common attribute.

    Common attributes are not promoted to the <g> by this function.
    This is handled by moveCommonAttributesToParentGroup.

    If all children have a common attribute, an extra <g> is not created.

    This function acts recursively on the given element.
    """
    global _num_elements_removed
    num = 0
    for curAttr in ['clip-rule',
     'display-align',
     'fill', 'fill-opacity', 'fill-rule',
     'font', 'font-family', 'font-size', 'font-size-adjust', 'font-stretch',
     'font-style', 'font-variant', 'font-weight',
     'letter-spacing',
     'pointer-events', 'shape-rendering',
     'stroke', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-linecap', 'stroke-linejoin',
     'stroke-miterlimit', 'stroke-opacity', 'stroke-width',
     'text-anchor', 'text-decoration', 'text-rendering', 'visibility',
     'word-spacing', 'writing-mode']:
        curChild = elem.childNodes.length - 1
        while curChild >= 0:
            childNode = elem.childNodes.item(curChild)
            if childNode.nodeType == Node.ELEMENT_NODE and childNode.getAttribute(curAttr) != '' and childNode.nodeName in ('animate',
                                                                                                                            'animateColor',
                                                                                                                            'animateMotion',
                                                                                                                            'animateTransform',
                                                                                                                            'set',
                                                                                                                            'desc',
                                                                                                                            'metadata',
                                                                                                                            'title',
                                                                                                                            'circle',
                                                                                                                            'ellipse',
                                                                                                                            'line',
                                                                                                                            'path',
                                                                                                                            'polygon',
                                                                                                                            'polyline',
                                                                                                                            'rect',
                                                                                                                            'defs',
                                                                                                                            'g',
                                                                                                                            'svg',
                                                                                                                            'symbol',
                                                                                                                            'use',
                                                                                                                            'linearGradient',
                                                                                                                            'radialGradient',
                                                                                                                            'a',
                                                                                                                            'altGlyphDef',
                                                                                                                            'clipPath',
                                                                                                                            'color-profile',
                                                                                                                            'cursor',
                                                                                                                            'filter',
                                                                                                                            'font',
                                                                                                                            'font-face',
                                                                                                                            'foreignObject',
                                                                                                                            'image',
                                                                                                                            'marker',
                                                                                                                            'mask',
                                                                                                                            'pattern',
                                                                                                                            'script',
                                                                                                                            'style',
                                                                                                                            'switch',
                                                                                                                            'text',
                                                                                                                            'view',
                                                                                                                            'animation',
                                                                                                                            'audio',
                                                                                                                            'discard',
                                                                                                                            'handler',
                                                                                                                            'listener',
                                                                                                                            'prefetch',
                                                                                                                            'solidColor',
                                                                                                                            'textArea',
                                                                                                                            'video'):
                value = childNode.getAttribute(curAttr)
                runStart, runEnd = curChild, curChild
                runElements = 1
                while runStart > 0:
                    nextNode = elem.childNodes.item(runStart - 1)
                    if nextNode.nodeType == Node.ELEMENT_NODE:
                        if nextNode.getAttribute(curAttr) != value:
                            break
                        else:
                            runElements += 1
                            runStart -= 1
                    else:
                        runStart -= 1

                if runElements >= 3:
                    while runEnd < elem.childNodes.length - 1:
                        if elem.childNodes.item(runEnd + 1).nodeType == Node.ELEMENT_NODE:
                            break
                        else:
                            runEnd += 1

                    runLength = runEnd - runStart + 1
                    if runLength == elem.childNodes.length:
                        if elem.nodeName == 'g' and elem.namespaceURI == NS['SVG']:
                            curChild = -1
                            continue
                    document = elem.ownerDocument
                    group = document.createElementNS(NS['SVG'], 'g')
                    group.childNodes[:] = elem.childNodes[runStart:runEnd + 1]
                    for child in group.childNodes:
                        child.parentNode = group

                    elem.childNodes[runStart:(runEnd + 1)] = []
                    elem.childNodes.insert(runStart, group)
                    group.parentNode = elem
                    num += 1
                    curChild = runStart - 1
                    _num_elements_removed -= 1
                else:
                    curChild -= 1
            else:
                curChild -= 1

    for childNode in elem.childNodes:
        if childNode.nodeType == Node.ELEMENT_NODE:
            num += createGroupsForCommonAttributes(childNode)

    return num


def removeUnusedAttributesOnParent(elem):
    """
    This recursively calls this function on all children of the element passed in,
    then removes any unused attributes on this elem if none of the children inherit it
    """
    num = 0
    childElements = []
    for child in elem.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            childElements.append(child)
            num += removeUnusedAttributesOnParent(child)

    if len(childElements) <= 1:
        return num
    else:
        attrList = elem.attributes
        unusedAttrs = {}
        for index in range(attrList.length):
            attr = attrList.item(index)
            if attr.nodeName in ('clip-rule', 'display-align', 'fill', 'fill-opacity',
                                 'fill-rule', 'font', 'font-family', 'font-size',
                                 'font-size-adjust', 'font-stretch', 'font-style',
                                 'font-variant', 'font-weight', 'letter-spacing',
                                 'pointer-events', 'shape-rendering', 'stroke', 'stroke-dasharray',
                                 'stroke-dashoffset', 'stroke-linecap', 'stroke-linejoin',
                                 'stroke-miterlimit', 'stroke-opacity', 'stroke-width',
                                 'text-anchor', 'text-decoration', 'text-rendering',
                                 'visibility', 'word-spacing', 'writing-mode'):
                unusedAttrs[attr.nodeName] = attr.nodeValue

        for childNum in range(len(childElements)):
            child = childElements[childNum]
            inheritedAttrs = []
            for name in unusedAttrs:
                val = child.getAttribute(name)
                if val == '' or val is None or val == 'inherit':
                    inheritedAttrs.append(name)

            for a in inheritedAttrs:
                del unusedAttrs[a]

        for name in unusedAttrs:
            elem.removeAttribute(name)
            num += 1

        return num


def removeDuplicateGradientStops(doc):
    global _num_elements_removed
    num = 0
    for gradType in ['linearGradient', 'radialGradient']:
        for grad in doc.getElementsByTagName(gradType):
            stops = {}
            stopsToRemove = []
            for stop in grad.getElementsByTagName('stop'):
                offsetU = SVGLength(stop.getAttribute('offset'))
                if offsetU.units == Unit.PCT:
                    offset = offsetU.value / 100.0
                elif offsetU.units == Unit.NONE:
                    offset = offsetU.value
                else:
                    offset = 0
                if int(offset) == offset:
                    stop.setAttribute('offset', str(int(offset)))
                else:
                    stop.setAttribute('offset', str(offset))
                color = stop.getAttribute('stop-color')
                opacity = stop.getAttribute('stop-opacity')
                style = stop.getAttribute('style')
                if offset in stops:
                    oldStop = stops[offset]
                    if oldStop[0] == color and oldStop[1] == opacity and oldStop[2] == style:
                        stopsToRemove.append(stop)
                stops[offset] = [
                 color, opacity, style]

            for stop in stopsToRemove:
                stop.parentNode.removeChild(stop)
                num += 1
                _num_elements_removed += 1

    return num


def collapseSinglyReferencedGradients(doc):
    global _num_elements_removed
    num = 0
    identifiedElements = findElementsWithId(doc.documentElement)
    for rid, nodes in six.iteritems(findReferencedElements(doc.documentElement)):
        if len(nodes) == 1 and rid in identifiedElements:
            elem = identifiedElements[rid]
            if elem is not None and elem.nodeType == Node.ELEMENT_NODE and elem.nodeName in ('linearGradient',
                                                                                             'radialGradient') and elem.namespaceURI == NS['SVG']:
                refElem = nodes[0]
                if refElem.nodeType == Node.ELEMENT_NODE and refElem.nodeName in ('linearGradient',
                                                                                  'radialGradient') and refElem.namespaceURI == NS['SVG']:
                    if len(refElem.getElementsByTagName('stop')) == 0:
                        stopsToAdd = elem.getElementsByTagName('stop')
                        for stop in stopsToAdd:
                            refElem.appendChild(stop)

                    for attr in ['gradientUnits', 'spreadMethod', 'gradientTransform']:
                        if refElem.getAttribute(attr) == '' and not elem.getAttribute(attr) == '':
                            refElem.setAttributeNS(None, attr, elem.getAttribute(attr))

                    if elem.nodeName == 'radialGradient' and refElem.nodeName == 'radialGradient':
                        for attr in ['fx', 'fy', 'cx', 'cy', 'r']:
                            if refElem.getAttribute(attr) == '' and not elem.getAttribute(attr) == '':
                                refElem.setAttributeNS(None, attr, elem.getAttribute(attr))

                    if elem.nodeName == 'linearGradient' and refElem.nodeName == 'linearGradient':
                        for attr in ['x1', 'y1', 'x2', 'y2']:
                            if refElem.getAttribute(attr) == '' and not elem.getAttribute(attr) == '':
                                refElem.setAttributeNS(None, attr, elem.getAttribute(attr))

                    refElem.removeAttributeNS(NS['XLINK'], 'href')
                    elem.parentNode.removeChild(elem)
                    _num_elements_removed += 1
                    num += 1

    return num


def computeGradientBucketKey(grad):
    gradBucketAttr = [
     'gradientUnits', 'spreadMethod', 'gradientTransform',
     'x1', 'y1', 'x2', 'y2', 'cx', 'cy', 'fx', 'fy', 'r']
    gradStopBucketsAttr = ['offset', 'stop-color', 'stop-opacity', 'style']
    subKeys = [ grad.getAttribute(a) for a in gradBucketAttr ]
    subKeys.append(grad.getAttributeNS(NS['XLINK'], 'href'))
    stops = grad.getElementsByTagName('stop')
    if stops.length:
        for i in range(stops.length):
            stop = stops.item(i)
            for attr in gradStopBucketsAttr:
                stopKey = stop.getAttribute(attr)
                subKeys.append(stopKey)

    return ('\x1e').join(subKeys)


def removeDuplicateGradients(doc):
    global _num_elements_removed
    num = 0
    gradientsToRemove = {}
    for gradType in ['linearGradient', 'radialGradient']:
        grads = doc.getElementsByTagName(gradType)
        gradBuckets = defaultdict(list)
        for grad in grads:
            key = computeGradientBucketKey(grad)
            gradBuckets[key].append(grad)

        for bucket in six.itervalues(gradBuckets):
            if len(bucket) < 2:
                continue
            master = bucket[0]
            duplicates = bucket[1:]
            gradientsToRemove[master] = duplicates

    referencedIDs = findReferencedElements(doc.documentElement)
    for masterGrad in gradientsToRemove:
        master_id = masterGrad.getAttribute('id')
        for dupGrad in gradientsToRemove[masterGrad]:
            if not dupGrad.parentNode:
                continue
            dup_id = dupGrad.getAttribute('id')
            funcIRI = re.compile('url\\([\'"]?#' + dup_id + '[\'"]?\\)')
            if dup_id in referencedIDs:
                for elem in referencedIDs[dup_id]:
                    for attr in ['fill', 'stroke']:
                        v = elem.getAttribute(attr)
                        v_new, n = funcIRI.subn('url(#' + master_id + ')', v)
                        if n > 0:
                            elem.setAttribute(attr, v_new)

                    if elem.getAttributeNS(NS['XLINK'], 'href') == '#' + dup_id:
                        elem.setAttributeNS(NS['XLINK'], 'href', '#' + master_id)
                    styles = _getStyle(elem)
                    for style in styles:
                        v = styles[style]
                        v_new, n = funcIRI.subn('url(#' + master_id + ')', v)
                        if n > 0:
                            styles[style] = v_new

                    _setStyle(elem, styles)

            dupGrad.parentNode.removeChild(dupGrad)
            _num_elements_removed += 1
            num += 1

    return num


def _getStyle(node):
    """Returns the style attribute of a node as a dictionary."""
    if node.nodeType == Node.ELEMENT_NODE and len(node.getAttribute('style')) > 0:
        styleMap = {}
        rawStyles = node.getAttribute('style').split(';')
        for style in rawStyles:
            propval = style.split(':')
            if len(propval) == 2:
                styleMap[propval[0].strip()] = propval[1].strip()

        return styleMap
    return {}


def _setStyle(node, styleMap):
    """Sets the style attribute of a node to the dictionary ``styleMap``."""
    fixedStyle = (';').join([ prop + ':' + styleMap[prop] for prop in styleMap ])
    if fixedStyle != '':
        node.setAttribute('style', fixedStyle)
    elif node.getAttribute('style'):
        node.removeAttribute('style')
    return node


def repairStyle(node, options):
    num = 0
    styleMap = _getStyle(node)
    if styleMap:
        for prop in ['fill', 'stroke']:
            if prop in styleMap:
                chunk = styleMap[prop].split(') ')
                if len(chunk) == 2 and (chunk[0][:5] == 'url(#' or chunk[0][:6] == 'url("#' or chunk[0][:6] == "url('#") and chunk[1] == 'rgb(0, 0, 0)':
                    styleMap[prop] = chunk[0] + ')'
                    num += 1

        if 'opacity' in styleMap:
            opacity = float(styleMap['opacity'])
            if opacity == 0.0:
                for uselessStyle in ['fill', 'fill-opacity', 'fill-rule', 'stroke', 'stroke-linejoin', 'stroke-opacity', 'stroke-miterlimit', 'stroke-linecap', 'stroke-dasharray',
                 'stroke-dashoffset', 'stroke-opacity']:
                    if uselessStyle in styleMap and not styleInheritedByChild(node, uselessStyle):
                        del styleMap[uselessStyle]
                        num += 1

        if 'stroke' in styleMap and styleMap['stroke'] == 'none':
            for strokestyle in ['stroke-width', 'stroke-linejoin', 'stroke-miterlimit', 'stroke-linecap', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity']:
                if strokestyle in styleMap and not styleInheritedByChild(node, strokestyle):
                    del styleMap[strokestyle]
                    num += 1

            if not styleInheritedByChild(node, 'stroke'):
                if styleInheritedFromParent(node, 'stroke') in (None, 'none'):
                    del styleMap['stroke']
                    num += 1
        if 'fill' in styleMap and styleMap['fill'] == 'none':
            for fillstyle in ['fill-rule', 'fill-opacity']:
                if fillstyle in styleMap and not styleInheritedByChild(node, fillstyle):
                    del styleMap[fillstyle]
                    num += 1

        if 'fill-opacity' in styleMap:
            fillOpacity = float(styleMap['fill-opacity'])
            if fillOpacity == 0.0:
                for uselessFillStyle in ['fill', 'fill-rule']:
                    if uselessFillStyle in styleMap and not styleInheritedByChild(node, uselessFillStyle):
                        del styleMap[uselessFillStyle]
                        num += 1

        if 'stroke-opacity' in styleMap:
            strokeOpacity = float(styleMap['stroke-opacity'])
            if strokeOpacity == 0.0:
                for uselessStrokeStyle in ['stroke', 'stroke-width', 'stroke-linejoin', 'stroke-linecap', 'stroke-dasharray', 'stroke-dashoffset']:
                    if uselessStrokeStyle in styleMap and not styleInheritedByChild(node, uselessStrokeStyle):
                        del styleMap[uselessStrokeStyle]
                        num += 1

        if 'stroke-width' in styleMap:
            strokeWidth = SVGLength(styleMap['stroke-width'])
            if strokeWidth.value == 0.0:
                for uselessStrokeStyle in ['stroke', 'stroke-linejoin', 'stroke-linecap', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity']:
                    if uselessStrokeStyle in styleMap and not styleInheritedByChild(node, uselessStrokeStyle):
                        del styleMap[uselessStrokeStyle]
                        num += 1

        if not mayContainTextNodes(node):
            for fontstyle in ['font-family', 'font-size', 'font-stretch', 'font-size-adjust', 'font-style', 'font-variant', 'font-weight',
             'letter-spacing', 'line-height', 'kerning',
             'text-align', 'text-anchor', 'text-decoration',
             'text-rendering', 'unicode-bidi',
             'word-spacing', 'writing-mode']:
                if fontstyle in styleMap:
                    del styleMap[fontstyle]
                    num += 1

        for inkscapeStyle in ['-inkscape-font-specification']:
            if inkscapeStyle in styleMap:
                del styleMap[inkscapeStyle]
                num += 1

        if 'overflow' in styleMap:
            if node.nodeName not in ('svg', 'symbol', 'image', 'foreignObject', 'marker',
                                     'pattern'):
                del styleMap['overflow']
                num += 1
            elif node != node.ownerDocument.documentElement:
                if styleMap['overflow'] == 'hidden':
                    del styleMap['overflow']
                    num += 1
            elif styleMap['overflow'] == 'visible':
                del styleMap['overflow']
                num += 1
        if options.style_to_xml:
            for propName in list(styleMap):
                if propName in svgAttributes:
                    node.setAttribute(propName, styleMap[propName])
                    del styleMap[propName]

        _setStyle(node, styleMap)
    for child in node.childNodes:
        num += repairStyle(child, options)

    return num


def styleInheritedFromParent(node, style):
    """
    Returns the value of 'style' that is inherited from the parents of the passed-in node

    Warning: This method only considers presentation attributes and inline styles,
             any style sheets are ignored!
    """
    parentNode = node.parentNode
    if parentNode.nodeType == Node.DOCUMENT_NODE:
        return None
    else:
        styles = _getStyle(parentNode)
        if style in styles:
            value = styles[style]
            if not value == 'inherit':
                return value
        value = parentNode.getAttribute(style)
        if value not in ('', 'inherit'):
            return parentNode.getAttribute(style)
        return styleInheritedFromParent(parentNode, style)


def styleInheritedByChild(node, style, nodeIsChild=False):
    """
    Returns whether 'style' is inherited by any children of the passed-in node

    If False is returned, it is guaranteed that 'style' can safely be removed
    from the passed-in node without influencing visual output of it's children

    If True is returned, the passed-in node should not have its text-based
    attributes removed.

    Warning: This method only considers presentation attributes and inline styles,
             any style sheets are ignored!
    """
    if node.nodeType != Node.ELEMENT_NODE:
        return False
    if nodeIsChild:
        if node.getAttribute(style) not in ('', 'inherit'):
            return False
        styles = _getStyle(node)
        if style in styles and not styles[style] == 'inherit':
            return False
    elif not node.childNodes:
        return False
    if node.childNodes:
        for child in node.childNodes:
            if styleInheritedByChild(child, style, True):
                return True

    if node.nodeName in ('a', 'defs', 'glyph', 'g', 'marker', 'mask', 'missing-glyph',
                         'pattern', 'svg', 'switch', 'symbol'):
        return False
    return True


def mayContainTextNodes(node):
    """
    Returns True if the passed-in node is probably a text element, or at least
    one of its descendants is probably a text element.

    If False is returned, it is guaranteed that the passed-in node has no
    business having text-based attributes.

    If True is returned, the passed-in node should not have its text-based
    attributes removed.
    """
    try:
        return node.mayContainTextNodes
    except AttributeError:
        pass

    result = True
    if node.nodeType != Node.ELEMENT_NODE:
        result = False
    elif node.namespaceURI != NS['SVG']:
        result = True
    elif node.nodeName in ('rect', 'circle', 'ellipse', 'line', 'polygon', 'polyline',
                           'path', 'image', 'stop'):
        result = False
    elif node.nodeName in ('g', 'clipPath', 'marker', 'mask', 'pattern', 'linearGradient',
                           'radialGradient', 'symbol'):
        result = False
        for child in node.childNodes:
            if mayContainTextNodes(child):
                result = True

    node.mayContainTextNodes = result
    return result


DefaultAttribute = namedtuple('DefaultAttribute', ['name', 'value', 'units', 'elements', 'conditions'])
DefaultAttribute.__new__.__defaults__ = (None,) * len(DefaultAttribute._fields)
default_attributes = [
 DefaultAttribute('clipPathUnits', 'userSpaceOnUse', elements=['clipPath']),
 DefaultAttribute('filterUnits', 'objectBoundingBox', elements=['filter']),
 DefaultAttribute('gradientUnits', 'objectBoundingBox', elements=['linearGradient', 'radialGradient']),
 DefaultAttribute('maskUnits', 'objectBoundingBox', elements=['mask']),
 DefaultAttribute('maskContentUnits', 'userSpaceOnUse', elements=['mask']),
 DefaultAttribute('patternUnits', 'objectBoundingBox', elements=['pattern']),
 DefaultAttribute('patternContentUnits', 'userSpaceOnUse', elements=['pattern']),
 DefaultAttribute('primitiveUnits', 'userSpaceOnUse', elements=['filter']),
 DefaultAttribute('externalResourcesRequired', 'false', elements=[
  'a', 'altGlyph', 'animate', 'animateColor',
  'animateMotion', 'animateTransform', 'circle', 'clipPath', 'cursor', 'defs', 'ellipse',
  'feImage', 'filter', 'font', 'foreignObject', 'g', 'image', 'line', 'linearGradient',
  'marker', 'mask', 'mpath', 'path', 'pattern', 'polygon', 'polyline', 'radialGradient',
  'rect', 'script', 'set', 'svg', 'switch', 'symbol', 'text', 'textPath', 'tref', 'tspan',
  'use', 'view']),
 DefaultAttribute('width', 100, Unit.PCT, elements=['svg']),
 DefaultAttribute('height', 100, Unit.PCT, elements=['svg']),
 DefaultAttribute('baseProfile', 'none', elements=['svg']),
 DefaultAttribute('preserveAspectRatio', 'xMidYMid meet', elements=[
  'feImage', 'image', 'marker', 'pattern', 'svg', 'symbol', 'view']),
 DefaultAttribute('x', 0, elements=['cursor', 'fePointLight', 'feSpotLight', 'foreignObject',
  'image', 'pattern', 'rect', 'svg', 'text', 'use']),
 DefaultAttribute('y', 0, elements=['cursor', 'fePointLight', 'feSpotLight', 'foreignObject',
  'image', 'pattern', 'rect', 'svg', 'text', 'use']),
 DefaultAttribute('z', 0, elements=['fePointLight', 'feSpotLight']),
 DefaultAttribute('x1', 0, elements=['line']),
 DefaultAttribute('y1', 0, elements=['line']),
 DefaultAttribute('x2', 0, elements=['line']),
 DefaultAttribute('y2', 0, elements=['line']),
 DefaultAttribute('cx', 0, elements=['circle', 'ellipse']),
 DefaultAttribute('cy', 0, elements=['circle', 'ellipse']),
 DefaultAttribute('markerUnits', 'strokeWidth', elements=['marker']),
 DefaultAttribute('refX', 0, elements=['marker']),
 DefaultAttribute('refY', 0, elements=['marker']),
 DefaultAttribute('markerHeight', 3, elements=['marker']),
 DefaultAttribute('markerWidth', 3, elements=['marker']),
 DefaultAttribute('orient', 0, elements=['marker']),
 DefaultAttribute('lengthAdjust', 'spacing', elements=['text', 'textPath', 'tref', 'tspan']),
 DefaultAttribute('startOffset', 0, elements=['textPath']),
 DefaultAttribute('method', 'align', elements=['textPath']),
 DefaultAttribute('spacing', 'exact', elements=['textPath']),
 DefaultAttribute('x', -10, Unit.PCT, ['filter', 'mask']),
 DefaultAttribute('x', -0.1, Unit.NONE, ['filter', 'mask'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('y', -10, Unit.PCT, ['filter', 'mask']),
 DefaultAttribute('y', -0.1, Unit.NONE, ['filter', 'mask'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('width', 120, Unit.PCT, ['filter', 'mask']),
 DefaultAttribute('width', 1.2, Unit.NONE, ['filter', 'mask'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('height', 120, Unit.PCT, ['filter', 'mask']),
 DefaultAttribute('height', 1.2, Unit.NONE, ['filter', 'mask'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('x1', 0, elements=['linearGradient']),
 DefaultAttribute('y1', 0, elements=['linearGradient']),
 DefaultAttribute('y2', 0, elements=['linearGradient']),
 DefaultAttribute('x2', 100, Unit.PCT, elements=['linearGradient']),
 DefaultAttribute('x2', 1, Unit.NONE, elements=['linearGradient'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('fx', elements=['radialGradient'], conditions=lambda node: node.getAttribute('fx') == node.getAttribute('cx')),
 DefaultAttribute('fy', elements=['radialGradient'], conditions=lambda node: node.getAttribute('fy') == node.getAttribute('cy')),
 DefaultAttribute('r', 50, Unit.PCT, elements=['radialGradient']),
 DefaultAttribute('r', 0.5, Unit.NONE, elements=['radialGradient'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('cx', 50, Unit.PCT, elements=['radialGradient']),
 DefaultAttribute('cx', 0.5, Unit.NONE, elements=['radialGradient'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('cy', 50, Unit.PCT, elements=['radialGradient']),
 DefaultAttribute('cy', 0.5, Unit.NONE, elements=['radialGradient'], conditions=lambda node: node.getAttribute('gradientUnits') != 'userSpaceOnUse'),
 DefaultAttribute('spreadMethod', 'pad', elements=['linearGradient', 'radialGradient']),
 DefaultAttribute('amplitude', 1, elements=['feFuncA', 'feFuncB', 'feFuncG', 'feFuncR']),
 DefaultAttribute('azimuth', 0, elements=['feDistantLight']),
 DefaultAttribute('baseFrequency', '0', elements=['feFuncA', 'feFuncB', 'feFuncG', 'feFuncR']),
 DefaultAttribute('bias', 1, elements=['feConvolveMatrix']),
 DefaultAttribute('diffuseConstant', 1, elements=['feDiffuseLighting']),
 DefaultAttribute('edgeMode', 'duplicate', elements=['feConvolveMatrix']),
 DefaultAttribute('elevation', 0, elements=['feDistantLight']),
 DefaultAttribute('exponent', 1, elements=['feFuncA', 'feFuncB', 'feFuncG', 'feFuncR']),
 DefaultAttribute('intercept', 0, elements=['feFuncA', 'feFuncB', 'feFuncG', 'feFuncR']),
 DefaultAttribute('k1', 0, elements=['feComposite']),
 DefaultAttribute('k2', 0, elements=['feComposite']),
 DefaultAttribute('k3', 0, elements=['feComposite']),
 DefaultAttribute('k4', 0, elements=['feComposite']),
 DefaultAttribute('mode', 'normal', elements=['feBlend']),
 DefaultAttribute('numOctaves', 1, elements=['feTurbulence']),
 DefaultAttribute('offset', 0, elements=['feFuncA', 'feFuncB', 'feFuncG', 'feFuncR']),
 DefaultAttribute('operator', 'over', elements=['feComposite']),
 DefaultAttribute('operator', 'erode', elements=['feMorphology']),
 DefaultAttribute('order', '3', elements=['feConvolveMatrix']),
 DefaultAttribute('pointsAtX', 0, elements=['feSpotLight']),
 DefaultAttribute('pointsAtY', 0, elements=['feSpotLight']),
 DefaultAttribute('pointsAtZ', 0, elements=['feSpotLight']),
 DefaultAttribute('preserveAlpha', 'false', elements=['feConvolveMatrix']),
 DefaultAttribute('radius', '0', elements=['feMorphology']),
 DefaultAttribute('scale', 0, elements=['feDisplacementMap']),
 DefaultAttribute('seed', 0, elements=['feTurbulence']),
 DefaultAttribute('specularConstant', 1, elements=['feSpecularLighting']),
 DefaultAttribute('specularExponent', 1, elements=['feSpecularLighting', 'feSpotLight']),
 DefaultAttribute('stdDeviation', '0', elements=['feGaussianBlur']),
 DefaultAttribute('stitchTiles', 'noStitch', elements=['feTurbulence']),
 DefaultAttribute('surfaceScale', 1, elements=['feDiffuseLighting', 'feSpecularLighting']),
 DefaultAttribute('type', 'matrix', elements=['feColorMatrix']),
 DefaultAttribute('type', 'turbulence', elements=['feTurbulence']),
 DefaultAttribute('xChannelSelector', 'A', elements=['feDisplacementMap']),
 DefaultAttribute('yChannelSelector', 'A', elements=['feDisplacementMap'])]
default_attributes_universal = []
default_attributes_per_element = defaultdict(list)
for default_attribute in default_attributes:
    if default_attribute.elements is None:
        default_attributes_universal.append(default_attribute)
    else:
        for element in default_attribute.elements:
            default_attributes_per_element[element].append(default_attribute)

def taint(taintedSet, taintedAttribute):
    """Adds an attribute to a set of attributes.

    Related attributes are also included."""
    taintedSet.add(taintedAttribute)
    if taintedAttribute == 'marker':
        taintedSet |= set(['marker-start', 'marker-mid', 'marker-end'])
    if taintedAttribute in ('marker-start', 'marker-mid', 'marker-end'):
        taintedSet.add('marker')
    return taintedSet


def removeDefaultAttributeValue(node, attribute):
    """
    Removes the DefaultAttribute 'attribute' from 'node' if specified conditions are fulfilled

    Warning: Does NOT check if the attribute is actually valid for the passed element type for increased preformance!
    """
    if not node.hasAttribute(attribute.name):
        return 0
    else:
        if isinstance(attribute.value, str):
            if node.getAttribute(attribute.name) == attribute.value:
                if attribute.conditions is None or attribute.conditions(node):
                    node.removeAttribute(attribute.name)
                    return 1
        else:
            nodeValue = SVGLength(node.getAttribute(attribute.name))
            if attribute.value is None or nodeValue.value == attribute.value and not nodeValue.units == Unit.INVALID:
                if attribute.units is None or nodeValue.units == attribute.units or isinstance(attribute.units, list) and nodeValue.units in attribute.units:
                    if attribute.conditions is None or attribute.conditions(node):
                        node.removeAttribute(attribute.name)
                        return 1
        return 0


def removeDefaultAttributeValues(node, options, tainted=set()):
    """'tainted' keeps a set of attributes defined in parent nodes.

    For such attributes, we don't delete attributes with default values."""
    num = 0
    if node.nodeType != Node.ELEMENT_NODE:
        return 0
    for attribute in default_attributes_universal:
        num += removeDefaultAttributeValue(node, attribute)

    if node.nodeName in default_attributes_per_element:
        for attribute in default_attributes_per_element[node.nodeName]:
            num += removeDefaultAttributeValue(node, attribute)

    attributes = [ node.attributes.item(i).nodeName for i in range(node.attributes.length) ]
    for attribute in attributes:
        if attribute not in tainted:
            if attribute in default_properties:
                if node.getAttribute(attribute) == default_properties[attribute]:
                    node.removeAttribute(attribute)
                    num += 1
                else:
                    tainted = taint(tainted, attribute)

    styles = _getStyle(node)
    for attribute in list(styles):
        if attribute not in tainted:
            if attribute in default_properties:
                if styles[attribute] == default_properties[attribute]:
                    del styles[attribute]
                    num += 1
                else:
                    tainted = taint(tainted, attribute)

    _setStyle(node, styles)
    for child in node.childNodes:
        num += removeDefaultAttributeValues(child, options, tainted.copy())

    return num


rgb = re.compile('\\s*rgb\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\)\\s*')
rgbp = re.compile('\\s*rgb\\(\\s*(\\d*\\.?\\d+)%\\s*,\\s*(\\d*\\.?\\d+)%\\s*,\\s*(\\d*\\.?\\d+)%\\s*\\)\\s*')

def convertColor(value):
    """
       Converts the input color string and returns a #RRGGBB (or #RGB if possible) string
    """
    s = value
    if s in colors:
        s = colors[s]
    rgbpMatch = rgbp.match(s)
    if rgbpMatch is not None:
        r = int(float(rgbpMatch.group(1)) * 255.0 / 100.0)
        g = int(float(rgbpMatch.group(2)) * 255.0 / 100.0)
        b = int(float(rgbpMatch.group(3)) * 255.0 / 100.0)
        s = '#%02x%02x%02x' % (r, g, b)
    else:
        rgbMatch = rgb.match(s)
        if rgbMatch is not None:
            r = int(rgbMatch.group(1))
            g = int(rgbMatch.group(2))
            b = int(rgbMatch.group(3))
            s = '#%02x%02x%02x' % (r, g, b)
    if s[0] == '#':
        s = s.lower()
        if len(s) == 7 and s[1] == s[2] and s[3] == s[4] and s[5] == s[6]:
            s = '#' + s[1] + s[3] + s[5]
    return s


def convertColors(element):
    """
       Recursively converts all color properties into #RRGGBB format if shorter
    """
    numBytes = 0
    if element.nodeType != Node.ELEMENT_NODE:
        return 0
    attrsToConvert = []
    if element.nodeName in ('rect', 'circle', 'ellipse', 'polygon', 'line', 'polyline',
                            'path', 'g', 'a'):
        attrsToConvert = [
         'fill', 'stroke']
    else:
        if element.nodeName in ('stop', ):
            attrsToConvert = [
             'stop-color']
        else:
            if element.nodeName in ('solidColor', ):
                attrsToConvert = [
                 'solid-color']
            styles = _getStyle(element)
            for attr in attrsToConvert:
                oldColorValue = element.getAttribute(attr)
                if oldColorValue != '':
                    newColorValue = convertColor(oldColorValue)
                    oldBytes = len(oldColorValue)
                    newBytes = len(newColorValue)
                    if oldBytes > newBytes:
                        element.setAttribute(attr, newColorValue)
                        numBytes += oldBytes - len(element.getAttribute(attr))
                if attr in styles:
                    oldColorValue = styles[attr]
                    newColorValue = convertColor(oldColorValue)
                    oldBytes = len(oldColorValue)
                    newBytes = len(newColorValue)
                    if oldBytes > newBytes:
                        styles[attr] = newColorValue
                        numBytes += oldBytes - len(element.getAttribute(attr))

        _setStyle(element, styles)
        for child in element.childNodes:
            numBytes += convertColors(child)

    return numBytes


def cleanPath(element, options):
    """
       Cleans the path string (d attribute) of the element
    """
    global _num_bytes_saved_in_path_data
    global _num_path_segments_removed
    oldPathStr = element.getAttribute('d')
    path = svg_parser.parse(oldPathStr)
    style = _getStyle(element)
    has_round_or_square_linecaps = element.getAttribute('stroke-linecap') in ('round',
                                                                              'square') or 'stroke-linecap' in style and style['stroke-linecap'] in ('round',
                                                                                                                                                     'square')
    has_intermediate_markers = element.hasAttribute('marker') or element.hasAttribute('marker-mid') or 'marker' in style or 'marker-mid' in style
    x = y = 0
    for pathIndex in range(len(path)):
        cmd, data = path[pathIndex]
        i = 0
        if cmd == 'A':
            for i in range(i, len(data), 7):
                data[(i + 5)] -= x
                data[(i + 6)] -= y
                x += data[(i + 5)]
                y += data[(i + 6)]

            path[pathIndex] = (
             'a', data)
        elif cmd == 'a':
            x += sum(data[5::7])
            y += sum(data[6::7])
        elif cmd == 'H':
            for i in range(i, len(data)):
                data[i] -= x
                x += data[i]

            path[pathIndex] = (
             'h', data)
        elif cmd == 'h':
            x += sum(data)
        elif cmd == 'V':
            for i in range(i, len(data)):
                data[i] -= y
                y += data[i]

            path[pathIndex] = (
             'v', data)
        elif cmd == 'v':
            y += sum(data)
        elif cmd == 'M':
            startx, starty = data[0], data[1]
            if pathIndex != 0:
                data[0] -= x
                data[1] -= y
            x, y = startx, starty
            i = 2
            for i in range(i, len(data), 2):
                data[i] -= x
                data[(i + 1)] -= y
                x += data[i]
                y += data[(i + 1)]

            path[pathIndex] = (
             'm', data)
        elif cmd in ('L', 'T'):
            for i in range(i, len(data), 2):
                data[i] -= x
                data[(i + 1)] -= y
                x += data[i]
                y += data[(i + 1)]

            path[pathIndex] = (
             cmd.lower(), data)
        elif cmd in ('m', ):
            if pathIndex == 0:
                startx, starty = data[0], data[1]
                x, y = startx, starty
                i = 2
            else:
                startx = x + data[0]
                starty = y + data[1]
            for i in range(i, len(data), 2):
                x += data[i]
                y += data[(i + 1)]

        elif cmd in ('l', 't'):
            x += sum(data[0::2])
            y += sum(data[1::2])
        elif cmd in ('S', 'Q'):
            for i in range(i, len(data), 4):
                data[i] -= x
                data[(i + 1)] -= y
                data[(i + 2)] -= x
                data[(i + 3)] -= y
                x += data[(i + 2)]
                y += data[(i + 3)]

            path[pathIndex] = (
             cmd.lower(), data)
        elif cmd in ('s', 'q'):
            x += sum(data[2::4])
            y += sum(data[3::4])
        elif cmd == 'C':
            for i in range(i, len(data), 6):
                data[i] -= x
                data[(i + 1)] -= y
                data[(i + 2)] -= x
                data[(i + 3)] -= y
                data[(i + 4)] -= x
                data[(i + 5)] -= y
                x += data[(i + 4)]
                y += data[(i + 5)]

            path[pathIndex] = (
             'c', data)
        elif cmd == 'c':
            x += sum(data[4::6])
            y += sum(data[5::6])
        elif cmd in ('z', 'Z'):
            x, y = startx, starty
            path[pathIndex] = ('z', data)

    if not has_round_or_square_linecaps:
        for pathIndex in range(len(path)):
            cmd, data = path[pathIndex]
            i = 0
            if cmd in ('m', 'l', 't'):
                if cmd == 'm':
                    i = 2
                while i < len(data):
                    if data[i] == data[(i + 1)] == 0:
                        del data[i:i + 2]
                        _num_path_segments_removed += 1
                    else:
                        i += 2

            elif cmd == 'c':
                while i < len(data):
                    if data[i] == data[(i + 1)] == data[(i + 2)] == data[(i + 3)] == data[(i + 4)] == data[(i + 5)] == 0:
                        del data[i:i + 6]
                        _num_path_segments_removed += 1
                    else:
                        i += 6

            elif cmd == 'a':
                while i < len(data):
                    if data[(i + 5)] == data[(i + 6)] == 0:
                        del data[i:i + 7]
                        _num_path_segments_removed += 1
                    else:
                        i += 7

            elif cmd == 'q':
                while i < len(data):
                    if data[i] == data[(i + 1)] == data[(i + 2)] == data[(i + 3)] == 0:
                        del data[i:i + 4]
                        _num_path_segments_removed += 1
                    else:
                        i += 4

            elif cmd in ('h', 'v'):
                oldLen = len(data)
                path[pathIndex] = (cmd, [ coord for coord in data if coord != 0 ])
                _num_path_segments_removed += len(path[pathIndex][1]) - oldLen

        pathIndex = len(path)
        subpath_needs_anchor = False
        while pathIndex > 1:
            pathIndex -= 1
            cmd, data = path[pathIndex]
            if cmd == 'z':
                next_cmd, next_data = path[(pathIndex - 1)]
                if next_cmd == 'm' and len(next_data) == 2:
                    del path[pathIndex]
                    _num_path_segments_removed += 1
                else:
                    subpath_needs_anchor = True
            elif cmd == 'm':
                if len(path) - 1 == pathIndex and len(data) == 2:
                    del path[pathIndex]
                    _num_path_segments_removed += 1
                    continue
                if subpath_needs_anchor:
                    subpath_needs_anchor = False
                elif data[0] == data[1] == 0:
                    path[pathIndex] = (
                     'l', data[2:])
                    _num_path_segments_removed += 1

    path = [ elem for elem in path if len(elem[1]) > 0 or elem[0] == 'z' ]
    newPath = [path[0]]
    for cmd, data in path[1:]:
        i = 0
        newData = data
        if cmd == 'c':
            newData = []
            while i < len(data):
                p1x, p1y = data[i], data[(i + 1)]
                p2x, p2y = data[(i + 2)], data[(i + 3)]
                dx = data[(i + 4)]
                dy = data[(i + 5)]
                foundStraightCurve = False
                if dx == 0:
                    if p1x == 0 and p2x == 0:
                        foundStraightCurve = True
                else:
                    m = dy / dx
                    if p1y == m * p1x and p2y == m * p2x:
                        foundStraightCurve = True
                if foundStraightCurve:
                    if newData:
                        newPath.append((cmd, newData))
                        newData = []
                    newPath.append(('l', [dx, dy]))
                else:
                    newData.extend(data[i:i + 6])
                i += 6

        if newData or cmd == 'z' or cmd == 'Z':
            newPath.append((cmd, newData))

    path = newPath
    prevCmd = ''
    prevData = []
    newPath = []
    for cmd, data in path:
        if prevCmd == '':
            prevCmd = cmd
            prevData = data
        elif cmd != 'm' and (cmd == prevCmd or cmd == 'l' and prevCmd == 'm'):
            prevData.extend(data)
        else:
            newPath.append((prevCmd, prevData))
            prevCmd = cmd
            prevData = data

    newPath.append((prevCmd, prevData))
    path = newPath
    newPath = []
    for cmd, data in path:
        if cmd == 'l':
            i = 0
            lineTuples = []
            while i < len(data):
                if data[i] == 0:
                    if lineTuples:
                        newPath.append(('l', lineTuples))
                        lineTuples = []
                    newPath.append(('v', [data[(i + 1)]]))
                    _num_path_segments_removed += 1
                elif data[(i + 1)] == 0:
                    if lineTuples:
                        newPath.append(('l', lineTuples))
                        lineTuples = []
                    newPath.append(('h', [data[i]]))
                    _num_path_segments_removed += 1
                else:
                    lineTuples.extend(data[i:i + 2])
                i += 2

            if lineTuples:
                newPath.append(('l', lineTuples))
        elif cmd == 'm':
            i = 2
            lineTuples = [data[0], data[1]]
            while i < len(data):
                if data[i] == 0:
                    if lineTuples:
                        newPath.append((cmd, lineTuples))
                        lineTuples = []
                        cmd = 'l'
                    newPath.append(('v', [data[(i + 1)]]))
                    _num_path_segments_removed += 1
                elif data[(i + 1)] == 0:
                    if lineTuples:
                        newPath.append((cmd, lineTuples))
                        lineTuples = []
                        cmd = 'l'
                    newPath.append(('h', [data[i]]))
                    _num_path_segments_removed += 1
                else:
                    lineTuples.extend(data[i:i + 2])
                i += 2

            if lineTuples:
                newPath.append((cmd, lineTuples))
        elif cmd == 'c':
            bez_ctl_pt = (0, 0)
            if len(newPath):
                prevCmd, prevData = newPath[(-1)]
                if prevCmd == 's':
                    bez_ctl_pt = (
                     prevData[(-2)] - prevData[(-4)], prevData[(-1)] - prevData[(-3)])
            i = 0
            curveTuples = []
            while i < len(data):
                if bez_ctl_pt[0] == data[i] and bez_ctl_pt[1] == data[(i + 1)]:
                    if curveTuples:
                        newPath.append(('c', curveTuples))
                        curveTuples = []
                    newPath.append(('s', [data[(i + 2)], data[(i + 3)], data[(i + 4)], data[(i + 5)]]))
                    _num_path_segments_removed += 1
                else:
                    j = 0
                    while j <= 5:
                        curveTuples.append(data[(i + j)])
                        j += 1

                bez_ctl_pt = (data[(i + 4)] - data[(i + 2)], data[(i + 5)] - data[(i + 3)])
                i += 6

            if curveTuples:
                newPath.append(('c', curveTuples))
        elif cmd == 'q':
            quad_ctl_pt = (0, 0)
            i = 0
            curveTuples = []
            while i < len(data):
                if quad_ctl_pt[0] == data[i] and quad_ctl_pt[1] == data[(i + 1)]:
                    if curveTuples:
                        newPath.append(('q', curveTuples))
                        curveTuples = []
                    newPath.append(('t', [data[(i + 2)], data[(i + 3)]]))
                    _num_path_segments_removed += 1
                else:
                    j = 0
                    while j <= 3:
                        curveTuples.append(data[(i + j)])
                        j += 1

                quad_ctl_pt = (
                 data[(i + 2)] - data[i], data[(i + 3)] - data[(i + 1)])
                i += 4

            if curveTuples:
                newPath.append(('q', curveTuples))
        else:
            newPath.append((cmd, data))

    path = newPath
    if not has_intermediate_markers:
        for pathIndex in range(len(path)):
            cmd, data = path[pathIndex]
            if cmd in ('h', 'v') and len(data) >= 2:
                coordIndex = 0
                while coordIndex + 1 < len(data):
                    if is_same_sign(data[coordIndex], data[(coordIndex + 1)]):
                        data[coordIndex] += data[(coordIndex + 1)]
                        del data[coordIndex + 1]
                        _num_path_segments_removed += 1
                    else:
                        coordIndex += 1

            elif cmd == 'l' and len(data) >= 4:
                coordIndex = 0
                while coordIndex + 2 < len(data):
                    if is_same_direction(*data[coordIndex:coordIndex + 4]):
                        data[coordIndex] += data[(coordIndex + 2)]
                        data[(coordIndex + 1)] += data[(coordIndex + 3)]
                        del data[coordIndex + 2]
                        del data[coordIndex + 2]
                        _num_path_segments_removed += 1
                    else:
                        coordIndex += 2

            elif cmd == 'm' and len(data) >= 6:
                coordIndex = 2
                while coordIndex + 2 < len(data):
                    if is_same_direction(*data[coordIndex:coordIndex + 4]):
                        data[coordIndex] += data[(coordIndex + 2)]
                        data[(coordIndex + 1)] += data[(coordIndex + 3)]
                        del data[coordIndex + 2]
                        del data[coordIndex + 2]
                        _num_path_segments_removed += 1
                    else:
                        coordIndex += 2

    prevCmd = ''
    prevData = []
    newPath = [path[0]]
    for cmd, data in path[1:]:
        if prevCmd != '':
            if cmd != prevCmd or cmd == 'm':
                newPath.append((prevCmd, prevData))
                prevCmd = ''
                prevData = []
        if cmd == prevCmd and cmd != 'm':
            prevData.extend(data)
        else:
            prevCmd = cmd
            prevData = data

    if prevCmd != '':
        newPath.append((prevCmd, prevData))
    path = newPath
    newPathStr = serializePath(path, options)
    if len(newPathStr) <= len(oldPathStr):
        _num_bytes_saved_in_path_data += len(oldPathStr) - len(newPathStr)
        element.setAttribute('d', newPathStr)


def parseListOfPoints(s):
    """
       Parse string into a list of points.

       Returns a list containing an even number of coordinate strings
    """
    i = 0
    ws_nums = re.split('\\s*[\\s,]\\s*', s.strip())
    nums = []
    for i in range(len(ws_nums)):
        negcoords = ws_nums[i].split('-')
        if len(negcoords) == 1:
            nums.append(negcoords[0])
        else:
            for j in range(len(negcoords)):
                if j == 0:
                    if negcoords[0] != '':
                        nums.append(negcoords[0])
                else:
                    prev = ''
                    if len(nums):
                        prev = nums[(len(nums) - 1)]
                    if prev and prev[(len(prev) - 1)] in ('e', 'E'):
                        nums[len(nums) - 1] = prev + '-' + negcoords[j]
                    else:
                        nums.append('-' + negcoords[j])

    if len(nums) % 2 != 0:
        return []
    i = 0
    while i < len(nums):
        try:
            nums[i] = getcontext().create_decimal(nums[i])
            nums[i + 1] = getcontext().create_decimal(nums[(i + 1)])
        except InvalidOperation:
            return []

        i += 2

    return nums


def cleanPolygon(elem, options):
    """
       Remove unnecessary closing point of polygon points attribute
    """
    global _num_points_removed_from_polygon
    pts = parseListOfPoints(elem.getAttribute('points'))
    N = len(pts) / 2
    if N >= 2:
        startx, starty = pts[:2]
        endx, endy = pts[-2:]
        if startx == endx and starty == endy:
            del pts[-2:]
            _num_points_removed_from_polygon += 1
    elem.setAttribute('points', scourCoordinates(pts, options, True))


def cleanPolyline(elem, options):
    """
       Scour the polyline points attribute
    """
    pts = parseListOfPoints(elem.getAttribute('points'))
    elem.setAttribute('points', scourCoordinates(pts, options, True))


def controlPoints(cmd, data):
    """
       Checks if there are control points in the path data

       Returns the indices of all values in the path data which are control points
    """
    cmd = cmd.lower()
    if cmd in ('c', 's', 'q'):
        indices = range(len(data))
        if cmd == 'c':
            return [ index for index in indices if index % 6 < 4 ]
        if cmd in ('s', 'q'):
            return [ index for index in indices if index % 4 < 2 ]
    return []


def flags(cmd, data):
    """
       Checks if there are flags in the path data

       Returns the indices of all values in the path data which are flags
    """
    if cmd.lower() == 'a':
        indices = range(len(data))
        return [ index for index in indices if index % 7 in (3, 4) ]
    return []


def serializePath(pathObj, options):
    """
       Reserializes the path data with some cleanups.
    """
    return ('').join([ cmd + scourCoordinates(data, options, control_points=controlPoints(cmd, data), flags=flags(cmd, data)) for cmd, data in pathObj
                     ])


def serializeTransform(transformObj):
    """
       Reserializes the transform data with some cleanups.
    """
    return (' ').join([ command + '(' + (' ').join([ scourUnitlessLength(number) for number in numbers ]) + ')' for command, numbers in transformObj
                      ])


def scourCoordinates(data, options, force_whitespace=False, control_points=[], flags=[]):
    """
       Serializes coordinate data with some cleanups:
          - removes all trailing zeros after the decimal
          - integerize coordinates if possible
          - removes extraneous whitespace
          - adds spaces between values in a subcommand if required (or if force_whitespace is True)
    """
    if data is not None:
        newData = []
        c = 0
        previousCoord = ''
        for coord in data:
            is_control_point = c in control_points
            scouredCoord = scourUnitlessLength(coord, renderer_workaround=options.renderer_workaround, is_control_point=is_control_point)
            if c > 0 and (force_whitespace or scouredCoord[0].isdigit() or scouredCoord[0] == '.' and not ('.' in previousCoord or 'e' in previousCoord)) and (c - 1 not in flags or options.renderer_workaround):
                newData.append(' ')
            newData.append(scouredCoord)
            previousCoord = scouredCoord
            c += 1

        if options.renderer_workaround:
            if len(newData) > 0:
                for i in range(1, len(newData)):
                    if newData[i][0] == '-' and 'e' in newData[(i - 1)]:
                        newData[(i - 1)] += ' '

                return ('').join(newData)
        else:
            return ('').join(newData)
    return ''


def scourLength(length):
    """
    Scours a length. Accepts units.
    """
    length = SVGLength(length)
    return scourUnitlessLength(length.value) + Unit.str(length.units)


def scourUnitlessLength(length, renderer_workaround=False, is_control_point=False):
    """
    Scours the numeric part of a length only. Does not accept units.

    This is faster than scourLength on elements guaranteed not to
    contain units.
    """
    if not isinstance(length, Decimal):
        length = getcontext().create_decimal(str(length))
    initial_length = length
    if is_control_point:
        length = scouringContextC.plus(length)
    else:
        length = scouringContext.plus(length)
    intLength = length.to_integral_value()
    if length == intLength:
        length = Decimal(intLength)
    else:
        length = length.normalize()
    nonsci = ('{0:f}').format(length)
    nonsci = ('{0:f}').format(initial_length.quantize(Decimal(nonsci)))
    if not renderer_workaround:
        if len(nonsci) > 2 and nonsci[:2] == '0.':
            nonsci = nonsci[1:]
        elif len(nonsci) > 3 and nonsci[:3] == '-0.':
            nonsci = '-' + nonsci[2:]
    return_value = nonsci
    if len(nonsci) > 3:
        exponent = length.adjusted()
        length = length.scaleb(-exponent).normalize()
        sci = six.text_type(length) + 'e' + six.text_type(exponent)
        if len(sci) < len(nonsci):
            return_value = sci
    return return_value


def reducePrecision(element):
    """
    Because opacities, letter spacings, stroke widths and all that don't need
    to be preserved in SVG files with 9 digits of precision.

    Takes all of these attributes, in the given element node and its children,
    and reduces their precision to the current Decimal context's precision.
    Also checks for the attributes actually being lengths, not 'inherit', 'none'
    or anything that isn't an SVGLength.

    Returns the number of bytes saved after performing these reductions.
    """
    num = 0
    styles = _getStyle(element)
    for lengthAttr in ['opacity', 'flood-opacity', 'fill-opacity',
     'stroke-opacity', 'stop-opacity', 'stroke-miterlimit',
     'stroke-dashoffset', 'letter-spacing', 'word-spacing',
     'kerning', 'font-size-adjust', 'font-size',
     'stroke-width']:
        val = element.getAttribute(lengthAttr)
        if val != '':
            valLen = SVGLength(val)
            if valLen.units != Unit.INVALID:
                newVal = scourLength(val)
                if len(newVal) < len(val):
                    num += len(val) - len(newVal)
                    element.setAttribute(lengthAttr, newVal)
        if lengthAttr in styles:
            val = styles[lengthAttr]
            valLen = SVGLength(val)
            if valLen.units != Unit.INVALID:
                newVal = scourLength(val)
                if len(newVal) < len(val):
                    num += len(val) - len(newVal)
                    styles[lengthAttr] = newVal

    _setStyle(element, styles)
    for child in element.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            num += reducePrecision(child)

    return num


def optimizeAngle(angle):
    """
    Because any rotation can be expressed within 360 degrees
    of any given number, and since negative angles sometimes
    are one character longer than corresponding positive angle,
    we shorten the number to one in the range to [-90, 270[.
    """
    if angle < 0:
        angle %= -360
    else:
        angle %= 360
    if angle >= 270:
        angle -= 360
    elif angle < -90:
        angle += 360
    return angle


def optimizeTransform(transform):
    """
    Optimises a series of transformations parsed from a single
    transform="" attribute.

    The transformation list is modified in-place.
    """
    if len(transform) == 1 and transform[0][0] == 'matrix':
        matrix = A1, B1, A2, B2, A3, B3 = transform[0][1]
        if matrix == [1, 0, 0, 1, 0, 0]:
            del transform[0]
        elif A1 == 1 and A2 == 0 and B1 == 0 and B2 == 1:
            transform[0] = (
             'translate', [A3, B3])
        elif A2 == 0 and A3 == 0 and B1 == 0 and B3 == 0:
            transform[0] = (
             'scale', [A1, B2])
        elif A1 == B2 and -1 <= A1 <= 1 and A3 == 0 and -B1 == A2 and -1 <= B1 <= 1 and B3 == 0 and abs(B1 ** 2 + A1 ** 2 - 1) < Decimal('1e-15'):
            sin_A, cos_A = B1, A1
            A = Decimal(str(math.degrees(math.asin(float(sin_A)))))
            if cos_A < 0:
                if sin_A < 0:
                    A = -180 - A
                else:
                    A = 180 - A
            transform[0] = (
             'rotate', [A])
    for type, args in transform:
        if type == 'translate':
            if len(args) == 2 and args[1] == 0:
                del args[1]
        elif type == 'rotate':
            args[0] = optimizeAngle(args[0])
            if len(args) == 3 and args[1] == args[2] == 0:
                del args[1:]
        elif type == 'scale':
            if len(args) == 2 and args[0] == args[1]:
                del args[1]

    i = 1
    while i < len(transform):
        currType, currArgs = transform[i]
        prevType, prevArgs = transform[(i - 1)]
        if currType == prevType == 'translate':
            prevArgs[0] += currArgs[0]
            if len(currArgs) == 2:
                if len(prevArgs) == 2:
                    prevArgs[1] += currArgs[1]
                elif len(prevArgs) == 1:
                    prevArgs.append(currArgs[1])
            del transform[i]
            if prevArgs[0] == prevArgs[1] == 0:
                i -= 1
                del transform[i]
        elif currType == prevType == 'rotate' and len(prevArgs) == len(currArgs) == 1:
            prevArgs[0] = optimizeAngle(prevArgs[0] + currArgs[0])
            del transform[i]
        elif currType == prevType == 'scale':
            prevArgs[0] *= currArgs[0]
            if len(prevArgs) == 2 and len(currArgs) == 2:
                prevArgs[1] *= currArgs[1]
            elif len(prevArgs) == 1 and len(currArgs) == 2:
                prevArgs.append(prevArgs[0] * currArgs[1])
            elif len(prevArgs) == 2 and len(currArgs) == 1:
                prevArgs[1] *= currArgs[0]
            del transform[i]
            if prevArgs[0] == 1 and (len(prevArgs) == 1 or prevArgs[1] == 1):
                i -= 1
                del transform[i]
        else:
            i += 1

    i = 0
    while i < len(transform):
        currType, currArgs = transform[i]
        if (currType == 'skewX' or currType == 'skewY') and len(currArgs) == 1 and currArgs[0] == 0:
            del transform[i]
        elif currType == 'rotate' and len(currArgs) == 1 and currArgs[0] == 0:
            del transform[i]
        else:
            i += 1


def optimizeTransforms(element, options):
    """
    Attempts to optimise transform specifications on the given node and its children.

    Returns the number of bytes saved after performing these reductions.
    """
    num = 0
    for transformAttr in ['transform', 'patternTransform', 'gradientTransform']:
        val = element.getAttribute(transformAttr)
        if val != '':
            transform = svg_transform_parser.parse(val)
            optimizeTransform(transform)
            newVal = serializeTransform(transform)
            if len(newVal) < len(val):
                if len(newVal):
                    element.setAttribute(transformAttr, newVal)
                else:
                    element.removeAttribute(transformAttr)
                num += len(val) - len(newVal)

    for child in element.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            num += optimizeTransforms(child, options)

    return num


def removeComments(element):
    """
       Removes comments from the element and its children.
    """
    global _num_bytes_saved_in_comments
    num = 0
    if isinstance(element, xml.dom.minidom.Comment):
        _num_bytes_saved_in_comments += len(element.data)
        element.parentNode.removeChild(element)
        num += 1
    else:
        for subelement in element.childNodes[:]:
            num += removeComments(subelement)

    return num


def embedRasters(element, options):
    global _num_rasters_embedded
    import base64
    href = element.getAttributeNS(NS['XLINK'], 'href')
    if href != '' and len(href) > 1:
        ext = os.path.splitext(os.path.basename(href))[1].lower()[1:]
        if ext in ('png', 'jpg', 'gif'):
            href_fixed = href.replace('\\', '/')
            href_fixed = re.sub('file:/+', 'file:///', href_fixed)
            parsed_href = urllib.parse.urlparse(href_fixed)
            if parsed_href.scheme == '':
                parsed_href = parsed_href._replace(scheme='file')
                if href_fixed[0] == '/':
                    href_fixed = 'file://' + href_fixed
                else:
                    href_fixed = 'file:' + href_fixed
            working_dir_old = None
            if parsed_href.scheme == 'file' and parsed_href.path[0] != '/':
                if options.infilename:
                    working_dir_old = os.getcwd()
                    working_dir_new = os.path.abspath(os.path.dirname(options.infilename))
                    os.chdir(working_dir_new)
            try:
                try:
                    file = urllib.request.urlopen(href_fixed)
                    rasterdata = file.read()
                    file.close()
                except Exception as e:
                    print("WARNING: Could not open file '" + href + "' for embedding. The raster image will be kept as a reference but might be invalid. (Exception details: " + str(e) + ')', file=options.ensure_value('stdout', sys.stdout))
                    rasterdata = ''

            finally:
                if working_dir_old is not None:
                    os.chdir(working_dir_old)

            if rasterdata != '':
                b64eRaster = base64.b64encode(rasterdata)
                if b64eRaster != '':
                    if ext == 'jpg':
                        ext = 'jpeg'
                    element.setAttributeNS(NS['XLINK'], 'href', 'data:image/' + ext + ';base64,' + b64eRaster.decode())
                    _num_rasters_embedded += 1
                    del b64eRaster
    return


def properlySizeDoc(docElement, options):
    w = SVGLength(docElement.getAttribute('width'))
    h = SVGLength(docElement.getAttribute('height'))
    if options.renderer_workaround:
        if w.units != Unit.NONE and w.units != Unit.PX or h.units != Unit.NONE and h.units != Unit.PX:
            return
    vbSep = re.split('[, ]+', docElement.getAttribute('viewBox'))
    vbWidth, vbHeight = (0, 0)
    if len(vbSep) == 4:
        try:
            vbX = float(vbSep[0])
            vbY = float(vbSep[1])
            if vbX != 0 or vbY != 0:
                return
            vbWidth = float(vbSep[2])
            vbHeight = float(vbSep[3])
            if vbWidth != w.value or vbHeight != h.value:
                return
        except ValueError:
            pass

    docElement.setAttribute('viewBox', '0 0 %s %s' % (w.value, h.value))
    docElement.removeAttribute('width')
    docElement.removeAttribute('height')


def remapNamespacePrefix(node, oldprefix, newprefix):
    if node is None or node.nodeType != Node.ELEMENT_NODE:
        return
    if node.prefix == oldprefix:
        localName = node.localName
        namespace = node.namespaceURI
        doc = node.ownerDocument
        parent = node.parentNode
        newNode = None
        if newprefix != '':
            newNode = doc.createElementNS(namespace, newprefix + ':' + localName)
        else:
            newNode = doc.createElement(localName)
        attrList = node.attributes
        for i in range(attrList.length):
            attr = attrList.item(i)
            newNode.setAttributeNS(attr.namespaceURI, attr.localName, attr.nodeValue)

        for child in node.childNodes:
            newNode.appendChild(child.cloneNode(True))

        parent.replaceChild(newNode, node)
        node = newNode
    for child in node.childNodes:
        remapNamespacePrefix(child, oldprefix, newprefix)

    return


def makeWellFormed(str, quote=''):
    xml_ents = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    if quote:
        xml_ents[quote] = '&apos;' if quote == "'" else '&quot;'
    return ('').join([ xml_ents[c] if c in xml_ents else c for c in str ])


def chooseQuoteCharacter(str):
    quotCount = str.count('"')
    aposCount = str.count("'")
    if quotCount > aposCount:
        quote = "'"
        hasEmbeddedQuote = aposCount
    else:
        quote = '"'
        hasEmbeddedQuote = quotCount
    return (
     quote, hasEmbeddedQuote)


def serializeXML(element, options, indent_depth=0, preserveWhitespace=False):
    outParts = []
    indent_type = ''
    newline = ''
    if options.newlines:
        if options.indent_type == 'tab':
            indent_type = '\t'
        elif options.indent_type == 'space':
            indent_type = ' '
        indent_type *= options.indent_depth
        newline = '\n'
    outParts.extend([indent_type * indent_depth, '<', element.nodeName])
    known_attr = [
     'id', 'xml:id', 'class', 'transform', 'x', 'y', 'z', 'width', 'height', 'x1', 'x2', 'y1', 'y2', 'dx', 'dy', 'rotate', 'startOffset', 'method', 'spacing', 'cx', 'cy', 'r', 'rx', 'ry', 'fx', 'fy', 'd', 'points'] + sorted(svgAttributes) + [
     'style']
    attrList = element.attributes
    attrName2Index = dict([ (attrList.item(i).nodeName, i) for i in range(attrList.length) ])
    attrIndices = []
    for name in known_attr:
        if name in attrName2Index:
            attrIndices.append(attrName2Index[name])
            del attrName2Index[name]

    attrIndices += [ attrName2Index[name] for name in sorted(attrName2Index) ]
    for index in attrIndices:
        attr = attrList.item(index)
        attrValue = attr.nodeValue
        quote, hasEmbeddedQuote = chooseQuoteCharacter(attrValue)
        attrValue = makeWellFormed(attrValue, quote if hasEmbeddedQuote else '')
        if attr.nodeName == 'style':
            attrValue = (';').join([ p for p in sorted(attrValue.split(';')) ])
        outParts.append(' ')
        if attr.prefix is not None:
            outParts.extend([attr.prefix, ':'])
        elif attr.namespaceURI is not None:
            if attr.namespaceURI == 'http://www.w3.org/2000/xmlns/' and attr.nodeName.find('xmlns') == -1:
                outParts.append('xmlns:')
            elif attr.namespaceURI == 'http://www.w3.org/1999/xlink':
                outParts.append('xlink:')
        outParts.extend([attr.localName, '=', quote, attrValue, quote])
        if attr.nodeName == 'xml:space':
            if attrValue == 'preserve':
                preserveWhitespace = True
            elif attrValue == 'default':
                preserveWhitespace = False

    children = element.childNodes
    if children.length == 0:
        outParts.append('/>')
    else:
        outParts.append('>')
        onNewLine = False
        for child in element.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                if preserveWhitespace or element.nodeName in ('text', 'tspan', 'tref',
                                                              'textPath', 'altGlyph'):
                    outParts.append(serializeXML(child, options, 0, preserveWhitespace))
                else:
                    outParts.extend([newline, serializeXML(child, options, indent_depth + 1, preserveWhitespace)])
                    onNewLine = True
            elif child.nodeType == Node.TEXT_NODE:
                text_content = child.nodeValue
                if not preserveWhitespace:
                    if element.nodeName in ('text', 'tspan', 'tref', 'textPath', 'altGlyph'):
                        text_content = text_content.replace('\n', '')
                        text_content = text_content.replace('\t', ' ')
                        if child == element.firstChild:
                            text_content = text_content.lstrip()
                        else:
                            if child == element.lastChild:
                                text_content = text_content.rstrip()
                            while '  ' in text_content:
                                text_content = text_content.replace('  ', ' ')

                    else:
                        text_content = text_content.strip()
                outParts.append(makeWellFormed(text_content))
            elif child.nodeType == Node.CDATA_SECTION_NODE:
                outParts.extend(['<![CDATA[', child.nodeValue, ']]>'])
            elif child.nodeType == Node.COMMENT_NODE:
                outParts.extend([newline, indent_type * (indent_depth + 1), '<!--', child.nodeValue, '-->'])

        if onNewLine:
            outParts.append(newline)
            outParts.append(indent_type * indent_depth)
        outParts.extend(['</', element.nodeName, '>'])
    return ('').join(outParts)


def scourString(in_string, options=None):
    global _num_attributes_removed
    global _num_bytes_saved_in_colors
    global _num_bytes_saved_in_comments
    global _num_bytes_saved_in_ids
    global _num_bytes_saved_in_lengths
    global _num_bytes_saved_in_path_data
    global _num_bytes_saved_in_transforms
    global _num_comments_removed
    global _num_elements_removed
    global _num_ids_removed
    global _num_path_segments_removed
    global _num_points_removed_from_polygon
    global _num_rasters_embedded
    global _num_style_properties_fixed
    global scouringContext
    global scouringContextC
    options = sanitizeOptions(options)
    if options.cdigits < 0:
        options.cdigits = options.digits
    scouringContext = Context(prec=options.digits)
    scouringContextC = Context(prec=options.cdigits)
    _num_elements_removed = 0
    _num_attributes_removed = 0
    _num_ids_removed = 0
    _num_comments_removed = 0
    _num_style_properties_fixed = 0
    _num_rasters_embedded = 0
    _num_path_segments_removed = 0
    _num_points_removed_from_polygon = 0
    _num_bytes_saved_in_path_data = 0
    _num_bytes_saved_in_colors = 0
    _num_bytes_saved_in_comments = 0
    _num_bytes_saved_in_ids = 0
    _num_bytes_saved_in_lengths = 0
    _num_bytes_saved_in_transforms = 0
    doc = xml.dom.minidom.parseString(in_string)
    cnt_flowText_el = len(doc.getElementsByTagName('flowRoot'))
    if cnt_flowText_el:
        errmsg = ("SVG input document uses {} flow text elements, which won't render on browsers!").format(cnt_flowText_el)
        if options.error_on_flowtext:
            raise Exception(errmsg)
        else:
            print(('WARNING: {}').format(errmsg), file=sys.stderr)
    removeDescriptiveElements(doc, options)
    if options.keep_editor_data is False:
        while removeNamespacedElements(doc.documentElement, unwanted_ns) > 0:
            pass

        while removeNamespacedAttributes(doc.documentElement, unwanted_ns) > 0:
            pass

        xmlnsDeclsToRemove = []
        attrList = doc.documentElement.attributes
        for index in range(attrList.length):
            if attrList.item(index).nodeValue in unwanted_ns:
                xmlnsDeclsToRemove.append(attrList.item(index).nodeName)

        for attr in xmlnsDeclsToRemove:
            doc.documentElement.removeAttribute(attr)
            _num_attributes_removed += 1

    if doc.documentElement.getAttribute('xmlns') != 'http://www.w3.org/2000/svg':
        doc.documentElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg')

    def xmlnsUnused(prefix, namespace):
        if doc.getElementsByTagNameNS(namespace, '*'):
            return False
        for element in doc.getElementsByTagName('*'):
            for attribute in element.attributes.values():
                if attribute.name.startswith(prefix):
                    return False

        return True

    attrList = doc.documentElement.attributes
    xmlnsDeclsToRemove = []
    redundantPrefixes = []
    for i in range(attrList.length):
        attr = attrList.item(i)
        name = attr.nodeName
        val = attr.nodeValue
        if name[0:6] == 'xmlns:':
            if val == 'http://www.w3.org/2000/svg':
                redundantPrefixes.append(name[6:])
                xmlnsDeclsToRemove.append(name)
            elif xmlnsUnused(name[6:], val):
                xmlnsDeclsToRemove.append(name)

    for attrName in xmlnsDeclsToRemove:
        doc.documentElement.removeAttribute(attrName)
        _num_attributes_removed += 1

    for prefix in redundantPrefixes:
        remapNamespacePrefix(doc.documentElement, prefix, '')

    if options.strip_comments:
        _num_comments_removed = removeComments(doc)
    if options.strip_xml_space_attribute and doc.documentElement.hasAttribute('xml:space'):
        doc.documentElement.removeAttribute('xml:space')
        _num_attributes_removed += 1
    _num_style_properties_fixed = repairStyle(doc.documentElement, options)
    if options.simple_colors:
        _num_bytes_saved_in_colors = convertColors(doc.documentElement)
    while removeUnreferencedElements(doc, options.keep_defs) > 0:
        pass

    for tag in ['defs', 'title', 'desc', 'metadata', 'g']:
        for elem in doc.documentElement.getElementsByTagName(tag):
            removeElem = not elem.hasChildNodes()
            if removeElem is False:
                for child in elem.childNodes:
                    if child.nodeType in [Node.ELEMENT_NODE, Node.CDATA_SECTION_NODE, Node.COMMENT_NODE]:
                        break
                    elif child.nodeType == Node.TEXT_NODE and not child.nodeValue.isspace():
                        break
                else:
                    removeElem = True

            if removeElem:
                elem.parentNode.removeChild(elem)
                _num_elements_removed += 1

    if options.strip_ids:
        referencedIDs = findReferencedElements(doc.documentElement)
        identifiedElements = unprotected_ids(doc, options)
        removeUnreferencedIDs(referencedIDs, identifiedElements)
    while removeDuplicateGradientStops(doc) > 0:
        pass

    while collapseSinglyReferencedGradients(doc) > 0:
        pass

    while removeDuplicateGradients(doc) > 0:
        pass

    if options.group_create:
        createGroupsForCommonAttributes(doc.documentElement)
    referencedIds = findReferencedElements(doc.documentElement)
    for child in doc.documentElement.childNodes:
        _num_attributes_removed += moveCommonAttributesToParentGroup(child, referencedIds)

    _num_attributes_removed += removeUnusedAttributesOnParent(doc.documentElement)
    if options.group_collapse:
        while removeNestedGroups(doc.documentElement) > 0:
            pass

    for polygon in doc.documentElement.getElementsByTagName('polygon'):
        cleanPolygon(polygon, options)

    for polyline in doc.documentElement.getElementsByTagName('polyline'):
        cleanPolyline(polyline, options)

    for elem in doc.documentElement.getElementsByTagName('path'):
        if elem.getAttribute('d') == '':
            elem.parentNode.removeChild(elem)
        else:
            cleanPath(elem, options)

    if options.shorten_ids:
        _num_bytes_saved_in_ids += shortenIDs(doc, options.shorten_ids_prefix, unprotected_ids(doc, options))
    for type in ['svg', 'image', 'rect', 'circle', 'ellipse', 'line',
     'linearGradient', 'radialGradient', 'stop', 'filter']:
        for elem in doc.getElementsByTagName(type):
            for attr in ['x', 'y', 'width', 'height', 'cx', 'cy', 'r', 'rx', 'ry',
             'x1', 'y1', 'x2', 'y2', 'fx', 'fy', 'offset']:
                if elem.getAttribute(attr) != '':
                    elem.setAttribute(attr, scourLength(elem.getAttribute(attr)))

    viewBox = doc.documentElement.getAttribute('viewBox')
    if viewBox:
        lengths = re.split('[, ]+', viewBox)
        lengths = [ scourUnitlessLength(length) for length in lengths ]
        doc.documentElement.setAttribute('viewBox', (' ').join(lengths))
    _num_bytes_saved_in_lengths = reducePrecision(doc.documentElement)
    _num_attributes_removed += removeDefaultAttributeValues(doc.documentElement, options)
    _num_bytes_saved_in_transforms = optimizeTransforms(doc.documentElement, options)
    if options.embed_rasters:
        for elem in doc.documentElement.getElementsByTagName('image'):
            embedRasters(elem, options)

    if options.enable_viewboxing:
        properlySizeDoc(doc.documentElement, options)
    out_string = serializeXML(doc.documentElement, options) + '\n'
    if options.strip_xml_prolog is False:
        total_output = '<?xml version="1.0" encoding="UTF-8"'
        if doc.standalone:
            total_output += ' standalone="yes"'
        total_output += '?>\n'
    else:
        total_output = ''
    for child in doc.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            total_output += out_string
        else:
            total_output += child.toxml() + '\n'

    return total_output


def scourXmlFile(filename, options=None):
    options = sanitizeOptions(options)
    options.ensure_value('infilename', filename)
    with open(filename, 'rb') as (f):
        in_string = f.read()
    out_string = scourString(in_string, options)
    doc = xml.dom.minidom.parseString(out_string.encode('utf-8'))
    all_nodes = doc.getElementsByTagName('*')
    for node in all_nodes:
        try:
            node.setIdAttribute('id')
        except NotFoundErr:
            pass

    return doc


class HeaderedFormatter(optparse.IndentedHelpFormatter):
    """
       Show application name, version number, and copyright statement
       above usage information.
    """

    def format_usage(self, usage):
        return '%s %s\n%s\n%s' % (APP, VER, COPYRIGHT,
         optparse.IndentedHelpFormatter.format_usage(self, usage))


_options_parser = optparse.OptionParser(usage='%prog [INPUT.SVG [OUTPUT.SVG]] [OPTIONS]', description='If the input/output files are not specified, stdin/stdout are used. If the input/output files are specified with a svgz extension, then compressed SVG is assumed.', formatter=HeaderedFormatter(max_help_position=33), version=VER)
_options_parser.add_option('-p', action='store', type=int, dest='digits', help=optparse.SUPPRESS_HELP)
_options_parser.add_option('-q', '--quiet', action='store_true', dest='quiet', default=False, help='suppress non-error output')
_options_parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='verbose output (statistics, etc.)')
_options_parser.add_option('-i', action='store', dest='infilename', metavar='INPUT.SVG', help='alternative way to specify input filename')
_options_parser.add_option('-o', action='store', dest='outfilename', metavar='OUTPUT.SVG', help='alternative way to specify output filename')
_option_group_optimization = optparse.OptionGroup(_options_parser, 'Optimization')
_option_group_optimization.add_option('--set-precision', action='store', type=int, dest='digits', default=5, metavar='NUM', help='set number of significant digits (default: %default)')
_option_group_optimization.add_option('--set-c-precision', action='store', type=int, dest='cdigits', default=-1, metavar='NUM', help="set number of significant digits for control points (default: same as '--set-precision')")
_option_group_optimization.add_option('--disable-simplify-colors', action='store_false', dest='simple_colors', default=True, help="won't convert colors to #RRGGBB format")
_option_group_optimization.add_option('--disable-style-to-xml', action='store_false', dest='style_to_xml', default=True, help="won't convert styles into XML attributes")
_option_group_optimization.add_option('--disable-group-collapsing', action='store_false', dest='group_collapse', default=True, help="won't collapse <g> elements")
_option_group_optimization.add_option('--create-groups', action='store_true', dest='group_create', default=False, help='create <g> elements for runs of elements with identical attributes')
_option_group_optimization.add_option('--keep-editor-data', action='store_true', dest='keep_editor_data', default=False, help="won't remove Inkscape, Sodipodi, Adobe Illustrator or Sketch elements and attributes")
_option_group_optimization.add_option('--keep-unreferenced-defs', action='store_true', dest='keep_defs', default=False, help="won't remove elements within the defs container that are unreferenced")
_option_group_optimization.add_option('--renderer-workaround', action='store_true', dest='renderer_workaround', default=True, help='work around various renderer bugs (currently only librsvg) (default)')
_option_group_optimization.add_option('--no-renderer-workaround', action='store_false', dest='renderer_workaround', default=True, help='do not work around various renderer bugs (currently only librsvg)')
_options_parser.add_option_group(_option_group_optimization)
_option_group_document = optparse.OptionGroup(_options_parser, 'SVG document')
_option_group_document.add_option('--strip-xml-prolog', action='store_true', dest='strip_xml_prolog', default=False, help="won't output the XML prolog (<?xml ?>)")
_option_group_document.add_option('--remove-titles', action='store_true', dest='remove_titles', default=False, help='remove <title> elements')
_option_group_document.add_option('--remove-descriptions', action='store_true', dest='remove_descriptions', default=False, help='remove <desc> elements')
_option_group_document.add_option('--remove-metadata', action='store_true', dest='remove_metadata', default=False, help='remove <metadata> elements (which may contain license/author information etc.)')
_option_group_document.add_option('--remove-descriptive-elements', action='store_true', dest='remove_descriptive_elements', default=False, help='remove <title>, <desc> and <metadata> elements')
_option_group_document.add_option('--enable-comment-stripping', action='store_true', dest='strip_comments', default=False, help='remove all comments (<!-- -->)')
_option_group_document.add_option('--disable-embed-rasters', action='store_false', dest='embed_rasters', default=True, help="won't embed rasters as base64-encoded data")
_option_group_document.add_option('--enable-viewboxing', action='store_true', dest='enable_viewboxing', default=False, help='changes document width/height to 100%/100% and creates viewbox coordinates')
_options_parser.add_option_group(_option_group_document)
_option_group_formatting = optparse.OptionGroup(_options_parser, 'Output formatting')
_option_group_formatting.add_option('--indent', action='store', type='string', dest='indent_type', default='space', metavar='TYPE', help='indentation of the output: none, space, tab (default: %default)')
_option_group_formatting.add_option('--nindent', action='store', type=int, dest='indent_depth', default=1, metavar='NUM', help='depth of the indentation, i.e. number of spaces/tabs: (default: %default)')
_option_group_formatting.add_option('--no-line-breaks', action='store_false', dest='newlines', default=True, help='do not create line breaks in output(also disables indentation; might be overridden by xml:space="preserve")')
_option_group_formatting.add_option('--strip-xml-space', action='store_true', dest='strip_xml_space_attribute', default=False, help='strip the xml:space="preserve" attribute from the root SVG element')
_options_parser.add_option_group(_option_group_formatting)
_option_group_ids = optparse.OptionGroup(_options_parser, 'ID attributes')
_option_group_ids.add_option('--enable-id-stripping', action='store_true', dest='strip_ids', default=False, help='remove all unreferenced IDs')
_option_group_ids.add_option('--shorten-ids', action='store_true', dest='shorten_ids', default=False, help='shorten all IDs to the least number of letters possible')
_option_group_ids.add_option('--shorten-ids-prefix', action='store', type='string', dest='shorten_ids_prefix', default='', metavar='PREFIX', help='add custom prefix to shortened IDs')
_option_group_ids.add_option('--protect-ids-noninkscape', action='store_true', dest='protect_ids_noninkscape', default=False, help="don't remove IDs not ending with a digit")
_option_group_ids.add_option('--protect-ids-list', action='store', type='string', dest='protect_ids_list', metavar='LIST', help="don't remove IDs given in this comma-separated list")
_option_group_ids.add_option('--protect-ids-prefix', action='store', type='string', dest='protect_ids_prefix', metavar='PREFIX', help="don't remove IDs starting with the given prefix")
_options_parser.add_option_group(_option_group_ids)
_option_group_compatibility = optparse.OptionGroup(_options_parser, 'SVG compatibility checks')
_option_group_compatibility.add_option('--error-on-flowtext', action='store_true', dest='error_on_flowtext', default=False, help='exit with error if the input SVG uses non-standard flowing text (only warn by default)')
_options_parser.add_option_group(_option_group_compatibility)

def parse_args(args=None, ignore_additional_args=False):
    options, rargs = _options_parser.parse_args(args)
    if rargs:
        if not options.infilename:
            options.infilename = rargs.pop(0)
        if not options.outfilename and rargs:
            options.outfilename = rargs.pop(0)
        if not ignore_additional_args and rargs:
            _options_parser.error('Additional arguments not handled: %r, see --help' % rargs)
    if options.digits < 1:
        _options_parser.error('Number of significant digits has to be larger than zero, see --help')
    if options.cdigits > options.digits:
        options.cdigits = -1
        print("WARNING: The value for '--set-c-precision' should be lower than the value for '--set-precision'. Number of significant digits for control points reset to default value, see --help", file=sys.stderr)
    if options.indent_type not in ('tab', 'space', 'none'):
        _options_parser.error('Invalid value for --indent, see --help')
    if options.indent_depth < 0:
        _options_parser.error('Value for --nindent should be positive (or zero), see --help')
    if options.infilename and options.outfilename and options.infilename == options.outfilename:
        _options_parser.error('Input filename is the same as output filename')
    return options


def generateDefaultOptions():
    return sanitizeOptions()


def sanitizeOptions(options=None):
    optionsDict = dict((key, getattr(options, key)) for key in dir(options) if not key.startswith('__'))
    sanitizedOptions = _options_parser.get_default_values()
    sanitizedOptions._update_careful(optionsDict)
    return sanitizedOptions


def maybe_gziped_file(filename, mode='r'):
    if os.path.splitext(filename)[1].lower() in ('.svgz', '.gz'):
        import gzip
        return gzip.GzipFile(filename, mode)
    return open(filename, mode)


def getInOut(options):
    if options.infilename:
        infile = maybe_gziped_file(options.infilename, 'rb')
    else:
        try:
            infile = sys.stdin.buffer
        except AttributeError:
            infile = sys.stdin

        if sys.stdin.isatty():
            _options_parser.error('No input file specified, see --help for detailed usage information')
        if options.outfilename:
            outfile = maybe_gziped_file(options.outfilename, 'wb')
        else:
            try:
                outfile = sys.stdout.buffer
            except AttributeError:
                outfile = sys.stdout

        options.stdout = sys.stderr
    return [infile, outfile]


def getReport():
    return '  Number of elements removed: ' + str(_num_elements_removed) + os.linesep + '  Number of attributes removed: ' + str(_num_attributes_removed) + os.linesep + '  Number of unreferenced IDs removed: ' + str(_num_ids_removed) + os.linesep + '  Number of comments removed: ' + str(_num_comments_removed) + os.linesep + '  Number of style properties fixed: ' + str(_num_style_properties_fixed) + os.linesep + '  Number of raster images embedded: ' + str(_num_rasters_embedded) + os.linesep + '  Number of path segments reduced/removed: ' + str(_num_path_segments_removed) + os.linesep + '  Number of points removed from polygons: ' + str(_num_points_removed_from_polygon) + os.linesep + '  Number of bytes saved in path data: ' + str(_num_bytes_saved_in_path_data) + os.linesep + '  Number of bytes saved in colors: ' + str(_num_bytes_saved_in_colors) + os.linesep + '  Number of bytes saved in comments: ' + str(_num_bytes_saved_in_comments) + os.linesep + '  Number of bytes saved in IDs: ' + str(_num_bytes_saved_in_ids) + os.linesep + '  Number of bytes saved in lengths: ' + str(_num_bytes_saved_in_lengths) + os.linesep + '  Number of bytes saved in transformations: ' + str(_num_bytes_saved_in_transforms)


def start(options, input, output):
    options = sanitizeOptions(options)
    start = time.time()
    in_string = input.read()
    out_string = scourString(in_string, options).encode('UTF-8')
    output.write(out_string)
    if not (input is sys.stdin or hasattr(sys.stdin, 'buffer') and input is sys.stdin.buffer):
        input.close()
    if not (output is sys.stdout or hasattr(sys.stdout, 'buffer') and output is sys.stdout.buffer):
        output.close()
    end = time.time()
    duration = int(round((end - start) * 1000.0))
    oldsize = len(in_string)
    newsize = len(out_string)
    sizediff = newsize / oldsize * 100.0
    if not options.quiet:
        print(('Scour processed file "{}" in {} ms: {}/{} bytes new/orig -> {:.1f}%').format(input.name, duration, newsize, oldsize, sizediff), file=options.ensure_value('stdout', sys.stdout))
        if options.verbose:
            print(getReport(), file=options.ensure_value('stdout', sys.stdout))


def run():
    options = parse_args()
    input, output = getInOut(options)
    start(options, input, output)


if __name__ == '__main__':
    run()