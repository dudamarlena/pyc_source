# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/gviz.py
# Compiled at: 2010-04-16 06:31:11
"""Graphviz library to generate dot-file and render them as SVG

Ticket Dependencies : 
  * Blocking and blocked by tickets.
  * Ticket url, summary
  * Ticket clustering by components, milestones, owners+promptusers
  * Ticket ranking by Creation-date, Due-date
  * Double border to indicate that tickets outside the current project.
  * Ticket Coloring based on configuration file.

Ticket Hierarchies : 
  * Parent-Child relationship
  * Ticket url, summary
  * Ticket clustering by components, milestones, owners+promptusers
  * Ticket ranking by Creation-date, Due-date
  * Double border to indicate that tickets outside the current project.
  * Ticket Coloring based on configuration file.
"""
from __future__ import with_statement
import time, re, os
from tempfile import mkstemp
import copy
from pylons import config
import zeta.lib.helpers as h
from zeta.lib.error import *
import zeta.lib.cache as cache
graphtmpl = '\ndigraph G {\nnode [ fontname="Terminus", fontsize=6, width=0.5, height=0.5 ];\n%s\n/* Node attributes */\n%s\n}\n'
tooltip = lambda st, summ: '%s - %s' % (st.upper(), summ)
nodeattrtmpl = '\n%s [ color="%s", shape="%s", style="filled,rounded", fillcolor="%s", URL="%s", tooltip="%s", target="%s" ];\n'

def nodeattr(name, color, fillcolor, url, tooltip=None, target='_top', shape='box'):
    tooltip = tooltip and tooltip.replace('"', "'") or name
    return nodeattrtmpl % (name, color, shape, fillcolor, url, tooltip, target)


edgetmpl = '\n%s [color="%s", style="%s" ];\n'

def edge(nodes, color, linewidth):
    style = 'setlinewidth(%s)' % linewidth
    return edgetmpl % ((' -> ').join([ str(n) for n in nodes ]), color, style)


@cache.cache('tosvgtext', useargs=True)
def tosvgtext(dottext):
    (srcfd, srcfile) = mkstemp()
    (dstfd, dstfile) = mkstemp()
    open(srcfile, 'wb').write(dottext)
    os.system('dot -Tsvg -o %s %s' % (dstfile, srcfile))
    svgtext = open(dstfile, 'rb').read()
    os.remove(srcfile)
    os.remove(dstfile)
    svgtext = re.search('<svg([\\n\\r]|.)*</svg>', svgtext).group()
    return svgtext


@cache.cache('topng', useargs=True)
def topng(dottext):
    (srcfd, srcfile) = mkstemp()
    (dstfd, dstfile) = mkstemp()
    open(srcfile, 'wb').write(dottext)
    os.system('dot -Tpng -o %s %s' % (dstfile, srcfile))
    pngcont = open(dstfile, 'rb').read()
    os.remove(srcfile)
    os.remove(dstfile)
    return pngcont


def _filltckdep(count):
    return [ [[], [], []] for i in range(count + 1)
           ]


@cache.cache('calctckdep', useargs=True)
def calctckdep(blockers, tckdetails):
    """Parse the list of `blockers` and build the dependency tree,
    `blockers` is a list of (blockedbyid, blockingid)
    `tckdetails` is a dictionary with ticket-id key mapped to list of tckdet
        [ projectname, summary, type, severity, status,
          component, milestone, version,
          owner, promptuser, duedate, created_on ]
    """
    tckdeps = _filltckdep(len(tckdetails))
    for (by, ing) in blockers:
        tckdeps[by][2].append(ing)
        tckdeps[ing][1].append(by)
        tckdeps[by][0] = tckdetails[by]
        tckdeps[ing][0] = tckdetails[ing]

    return tckdeps


@cache.cache('tckdeptodot', useargs=True)
def tckdeptodot(tid, tckdeps, tckccodes):
    """Construct the dot file (using dot-language), optionally the graph can
    be ranked by `createdon` or `due_date`
    or clustered by `projectname`, `component`, `milestone`, `user`"""
    tckdeps = copy.deepcopy(tckdeps)

    def nodelines(nodes):
        lines = []
        nodes.append(tid)
        for nid in set(nodes):
            tck = tckdeps[nid][0]
            if nid == tid:
                (col, shape) = ('', 'ellipse')
                lines.append(nodeattr(nid, 'black', 'white', '', shape=shape))
            else:
                dic = dict(zip([
                 'tck_typename', 'tck_severityname', 'tck_statusname'], tck[2:5]))
                col = h.tckcolorcode(dic, h.json.loads(tckccodes))
                shape = 'box'
                toolt = tooltip(tck[4], tck[1])
                lines.append(nodeattr(nid, col, col, h.url_forticket(tck[0], nid), tooltip=toolt, shape=shape))

        return lines

    def graphblockedby(tid, elines=[], nodes=[]):
        bys = tckdeps[tid][1]
        nodes.extend(bys)
        tckdeps[tid][1] = []
        elines.extend([ edge([by, tid], '#1FDBFD', '0.3') for by in bys ])
        [ graphblockedby(by, elines, nodes) for by in bys ]

    def graphblocking(tid, elines=[], nodes=[]):
        ings = tckdeps[tid][2]
        nodes.extend(ings)
        tckdeps[tid][2] = []
        elines.extend([ edge([tid, ing], '#1FDBFD', '0.3') for ing in ings ])
        [ graphblocking(ing, elines, nodes) for ing in ings ]

    elines = []
    nodes = []
    graphblocking(tid, elines, nodes)
    graphblockedby(tid, elines, nodes)
    dottext = graphtmpl % (('\n').join(elines), ('\n').join(nodelines(nodes)))
    return dottext


def _filltckhier(count):
    return [ [[], None, []] for i in range(count + 1)
           ]


@cache.cache('calctckhier', useargs=True)
def calctckhier(hierarchies, tckdetails):
    """Parse the list of `hierarchies` and build the dependency tree,
    `hierarchies` is a list of (partckid, childtckid)
    `tckdetails` is a dictionary with ticket-id key mapped to list of tckdet
        [ projectname, summary, type, severity, status,
          component, milestone, version,
          owner, promptuser, duedate, created_on, url ]
    """
    tckhier = _filltckhier(len(tckdetails))
    for (par, child) in hierarchies:
        tckhier[par][0] = tckdetails[par]
        tckhier[child][0] = tckdetails[child]
        tckhier[child][1] = par
        tckhier[par][2].append(child)

    return tckhier


@cache.cache('tckhiertodot', useargs=True)
def tckhiertodot(tid, tckhier, tckccodes):
    """Construct the dot file (using dot-language), graphing ticket
    hierarchies"""
    tckhier = copy.deepcopy(tckhier)

    def nodelines(nodes):
        lines = []
        nodes.append(tid)
        for nid in set(nodes):
            tck = tckhier[nid][0]
            if nid == tid:
                (col, shape) = ('', 'ellipse')
                lines.append(nodeattr(nid, 'black', 'white', '', shape=shape))
            else:
                dic = dict(zip([
                 'tck_typename', 'tck_severityname', 'tck_statusname'], tck[2:5]))
                col = h.tckcolorcode(dic, h.json.loads(tckccodes))
                shape = 'box'
                toolt = tooltip(tck[4], tck[1])
                lines.append(nodeattr(nid, col, col, h.url_forticket(tck[0], nid), tooltip=toolt, shape=shape))

        return lines

    def graphparent(tid, elines=[], nodes=[]):
        parent = tckhier[tid][1]
        if parent:
            nodes.append(parent)
            elines.append(edge([parent, tid], '#1FDBFD', '0.3'))
            graphparent(parent, elines, nodes)

    def graphchildren(tid, elines=[], nodes=[]):
        children = tckhier[tid][2]
        nodes.extend(children)
        tckhier[tid][2] = []
        elines.extend([ edge([tid, child], '#1FDBFD', '0.3') for child in children ])
        [ graphchildren(child, elines, nodes) for child in children ]

    elines = []
    nodes = []
    graphparent(tid, elines, nodes)
    graphchildren(tid, elines, nodes)
    dottext = graphtmpl % (('\n').join(elines), ('\n').join(nodelines(nodes)))
    return dottext