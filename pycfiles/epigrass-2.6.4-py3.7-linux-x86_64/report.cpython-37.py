# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Epigrass/report.py
# Compiled at: 2020-04-13 15:18:46
# Size of source mod 2**32: 14387 bytes
"""
This module generates a report of the network simulation model
using LaTeX.
"""
import os, sys, string, time, matplotlib, codecs, pweave, datetime
from pylab import *
header = '\n'

class Report:
    __doc__ = '\n    Generates reports in pdf format.\n    Takes as input arg. a simulation object.\n    '

    def __init__(self, simulation):
        self.workdir = os.getcwd()
        self.sim = simulation
        self.encoding = self.sim.encoding
        if self.encoding == 'latin-1':
            enc = 'latin1'
        else:
            if self.encoding == 'utf-8':
                enc = 'utf8'
        self.header = '\n        '

    def genNetTitle(self):
        """
        Generates title section of the preamble from 
        data extracted from the simulation.
        """
        modname = self.sim.modelName
        title = f"\n% Model {modname} Network Report\n% John Doe\n% {datetime.date.today()}\n    \n\n        **Abstract**\n        Edit the report.pmd file and add your model's description here.\n        \n"
        return title

    def genEpiTitle(self):
        """
        Generates title section of the preamble from 
        data extracted from the simulation.
        """
        modname = self.sim.modelName
        title = f"\n        % Model {modname} Epidemiological Report\n        % John Doe\n        % {datetime.date.today()}\n\n\n                **Abstract**\n                Edit the report.pmd file and add your model's description here.\n\n        "
        return title

    def genFullTitle(self):
        """
        Generates title section of the preamble from 
        data extracted from the simulation.
        """
        modname = self.sim.modelName
        title = f"\n        % Model {modname} Full Report\n        % John Doe\n        % {datetime.date.today()}\n\n\n                **Abstract**\n                Edit the report.pmd file and add your model's description here.\n\n        "
        return title

    def graphDesc(self):
        """
        Generates the Graph description section.
        """
        stats = tuple(self.sim.g.doStats())
        nodd = sum([1 for i in self.sim.g.site_list if len(i.neighbors) % 2 != 0])
        if nodd:
            Eul = 'No'
            if nodd == 2:
                Trav = 'Yes'
            else:
                Trav = 'No'
        else:
            Eul = 'Yes'
        nnodes = len(self.sim.g.site_list)
        nedges = len(self.sim.g.edge_list)
        deglist = [len(i.neighbors) for i in self.sim.g.site_list]
        if nnodes >= 3:
            if min(deglist) >= nnodes / 2.0:
                Ham = 'Yes'
            else:
                Ham = 'Possibly'
        else:
            Ham = 'Yes'
        matrix = f"\n## General Network Analyses\nThe figure below contains a simple drawing of your graph. If your network \nis not very complex,it can help you to verify if the topology specified corresponds to\nyour expectations.\n```python\nself.sim.g.drawGraph()\n```\n## Network Descriptive Statistics\nIn this section you will find quantitative descriptors and plots \nthat will help you analyze you network.\n\n### Basic statistics\n\n - **Order (Number of Nodes):** {nnodes}\n - **Size (Number of Edges):** {nedges}\n - **Eulerian:** {Eul}\n - **Traversable:** {Trav}\n - **Hamiltonian:** {Ham}\n\n\n\n## Distance matrix\nThe distance Matrix represents the number of edges separating any\npair of nodes via the shortest path between them. \n\n```python\nhist(stats[0].flat, normed=1)\ntitle('Shortest paths distribution')\n```\n\n\n## Adjacencyy Matrix\nThe most basic measure of accessibility involves network connectivity\nwhere a network is represented as a connectivity matrix(below), which \nexpresses the connectivity of each node with its adjacent nodes. \n\nThe number of columns and rows in this matrix is equal to the number \nof nodes in the network and a value of 1 is given for each cell where \nthis is a connected pair and a value of 0 for each cell where there \nis an unconnected pair. The summation of this matrix provides a very \nbasic measure of accessibility, also known as the degree of a node.\n\n```python\npcolor(stats[12])\ntitle('Adjacency Matrix')\ncolorbar()\n```\n            \n"
        indices = f"\n## Number of Cycles\nThe maximum number of independent cycles in a graph.\nThis number ($u$) is estimated by knowing the number of nodes ($v$), \nlinks ($e$) and of sub-graphs ($p$); $u = e-v+p$.\n\nTrees and simple networks will have a value of 0 since they have \nno cycles. \nThe more complex a network is, the higher the value of u, \nso it can be used as an indicator of the level of development \nof a transport system.\n\nCycles(u) $={stats[1]}$\n\n## Wiener Distance\nThe Wiener distance is the sum of all the shortest distances in the network.\n\nWiener's D $={stats[2]}$\n\n## Mean Distance\nThe mean distance of a network is the mean of of the set of shortest paths, \nexcluding the 0-length paths." + '\n$\\bar{D}={}$ \n'.format(stats[3]) + f"\n## Network Diameter\nThe diameter of a network is the longest element of the shortest paths set.\n\n$D(N)={stats[4]}$\n## Length of the Network\nThe length of a network is the sum in metric units (e.g., km) of all the edges in the network.\n\n$L(N)={stats[5]}$\n## Weight of the Network\nThe weight of a network is the weight of all nodes in the graph ($W(N)$), which is the summation \nof each node's order ($o$) multiplied by 2 for all orders above 1.\n\n$W(N)={stats[6]}$\n## Iota ($\\iota$) Index\nThe Iota index measures the ratio between the network and its weighed vertices. \nIt considers the structure, the length and the function \nof a network and it is mainly used when data about traffic \nis not available. \n\nIt divides the length of a network (L(N)) by its weight (W(N)). \nThe lower its value, the more efficient the network is. \nThis measure is based on the fact that an intersection \n(represented as a node) of a high order is able to handle \nlarge amounts of traffic. \n\nThe weight of all nodes in the network (W(N)) is the summation \nof each node's order (o) multiplied by 2 for all orders above 1.\n" + '\n$\\iota=\\frac{L(N)}{W(N)}={}$\n\\subsection{Pi ($\\Pi$) Index}\nThe Pi index represents the relationship between the \ntotal length of the network L(N)\nand the distance along the diameter D(d). \n\nIt is labeled as Pi because of its similarity with the \ntrigonometric $\\Pi$ (3.14), which is expressing the ratio between \nthe circumference and the diameter of a circle. \n\nA high index shows a developed network. It is a measure \nof distance per units of diameter and an indicator of \nthe  shape of a network.\n'.format(stats[7]) + f"\n$\\Pi=L(N)/D(d)={stats[8]}$\n## Beta ($\x08eta$) Index\nThe Beta index\nmeasures the level of connectivity in a network and is \nexpressed by the relationship between the number of \nedges (e) over the number of nodes (v). \n\nTrees and simple networks have Beta value of less than one. \nA connected network with one cycle has a value of 1. \nMore complex networks have a value greater than 1. \nIn a network with a fixed number of nodes, the higher the \nnumber of links, the higher the number of paths possible in \nthe network. Complex networks have a high value of Beta.\n\n$\x08eta = {stats[10]}$"
        section = matrix + indices
        return section

    def siteReport(self, geoc):
        """
        Puts together a report for a given site.
        """
        site = None
        for i in self.sim.g.site_list:
            if int(i.geocode) == int(geoc):
                site = i

        if not site:
            sys.exit('Wrong Geocode specified in the siteRep list')
        stats = site.doStats()
        name = [site.sitename]
        site.plotItself()
        section = f"\n# {name}\n## Centrality\n$$C={stats[0]}$$\n## Degree\n$$D={stats[1]}$$\n## Theta Index\n$$\\theta={stats[2]}$$\n## Betweeness \n$$B={stats[3]}$$\n```python\nsite.plotItself()\n```\n        "
        return section

    def genSiteEpi(self, geoc):
        """
        Generate epidemiological reports at the site level.
        """
        site = None
        for i in self.sim.g.site_list:
            if int(i.geocode) == int(geoc):
                site = i

        if not site:
            sys.exit('Wrong Geocode specified in the siteRep list')
        name = site.sitename
        incidence = site.incidence
        totcases = site.totalcases
        cuminc = [sum(incidence[:i]) for i in range(len(incidence))]
        infc = site.thetahist
        section = f"\n# {name}\n## Incidence\n```python\nbar(list(range(len(cuminc))), cuminc)\nxlabel('Time')\nylabel('Incidence')\ntitle('Incidence per unit of time')\n```\n```python\nbar(list(range(len(infc))), infc)\ntitle('Number of infectious individuals arriving per unit of time')\nxlabel('Time')\nylabel('Infectious individuous')\n```  \n        "
        return section

    def genEpi(self):
        """
        Generate epidemiological report.
        """
        epistats = self.sim.g.getEpistats()
        cumcities = [sum(epistats[1][:i]) for i in range(len(epistats[1]))]
        section = f"\n# Epidemiological Statistics\n\n## Network-wide Epidemiological Statistics\nIn the table  below, we present some useful epidemiological statistics about this simulation.\nThey include the following descriptors:\n\n - **Epidemic size (people)** This is the total number \nof cases that happened during the full course of the simulation.\n - **Epidemic size (sites)** This is the total number of sites infected durint the epidemic.\n - **Epidemic speed** This is the average number of new cities infected \nper unit of time, during the epidemic.\n - **Epidemic duration** The total number of units of time, the epidemic lasted.\n- **Median survival time** The time it took for fifty percent of the cities to become infected.\n\n\n |---------------|---------------|\n | Size (people) | {epistats[0]} |\n |---------------|---------------|\n | Speed         | {mean(epistats[1])} |\n |---------------|---------------|\n | Size (sites)  | {epistats[2]} |\n |---------------|---------------|\n | Duration      | {epistats[3]} |\n |---------------|---------------|\n | Survival      | {epistats[4]} |\n |---------------|---------------|\n | Total vaccines| {epistats[5]} |\n |---------------|---------------|\n |Total Quarantined | {epistats[6]}|\n\n```python\nbar(list(range(len(cumcities))), cumcities)\nylabel('Number of infected cities')\nxlabel('Time')\n```\n            "
        return section

    def Assemble(self, type):
        """
        Assemble the type of report desired
        types:
        1: network only
        2: epidemiological only
        3: both
        """
        dirname = self.sim.modelName + '-report-'
        Path = dirname + time.ctime()
        Path = Path.replace(' ', '-')
        os.system('mkdir ' + Path)
        os.chdir(Path)
        print('Starting report generation...')
        sitehead = '\n# Site Specific Analyses\n\n - **Centrality:** Also known as closeness. A measure of global centrality, is the \ninverse of the sum of the shortest paths to all other nodes\nin the graph.\n - **Degree:** The order (degree) of a node is the number of its attached links \nand is a simple, but effective measure of nodal importance. \n\nThe higher its value, the more a node is important in a graph \nas many links converge to it. Hub nodes have a high order, \nwhile terminal points have an order that can be as low as 1. \n\nA perfect hub would have its order equal to the summation of \nall the orders of the other nodes in the graph and a perfect \nspoke would have an order of 1.\n\n - **Theta Index:** Measures the function of a node, that is the average\namount of traffic per intersection. The higher theta is,\nthe greater the load of the network.\n - **Betweeness:** Is the number of times any node figures in the the shortest path\nbetween any other pair of nodes.\n'
        tail = ''
        if type == 1:
            start = time.clock()
            latexsrc = header + self.genNetTitle() + self.graphDesc()
            if self.sim.siteRep:
                latexsrc += sitehead
                for site in self.sim.siteRep:
                    latexsrc += self.siteReport(site)

            latexsrc += tail
            timer = time.clock() - start
            print('Time to generate Network report: %s seconds.' % timer)
            self.savenBuild('Netreport', latexsrc)
        else:
            if type == 2:
                start = time.clock()
                latexsrc = header + self.genEpiTitle() + self.genEpi()
                if self.sim.siteRep:
                    for site in self.sim.siteRep:
                        latexsrc += self.genSiteEpi(site)

                latexsrc += tail
                timer = time.clock() - start
                print('Time to generate Epidemiological report: %s seconds.' % timer)
                if self.sim.gui:
                    self.sim.gui.textEdit1.insertParagraph('Time to generate epidemiological report: %s seconds.' % timer, -1)
                self.savenBuild('epireport', latexsrc)
            else:
                if type == 3:
                    start = time.clock()
                    latexsrc = header + self.genFullTitle() + self.graphDesc()
                    if self.sim.siteRep:
                        latexsrc += sitehead
                        for site in self.sim.siteRep:
                            latexsrc += self.siteReport(site)

                    latexsrc += self.genEpi()
                    if self.sim.siteRep:
                        for site in self.sim.siteRep:
                            latexsrc += self.genSiteEpi(site)

                    latexsrc += tail
                    timer = time.clock() - start
                    print('Time to generate full report: %s seconds.' % timer)
                    self.savenBuild('fullreport', latexsrc)

    def Say(self, string):
        """
        Exits outputs messages to the console or the gui accordingly
        """
        print(string)

    def savenBuild(self, name, src):
        """
        Saves the LaTeX in a newly created directory and builds it.
        """
        fs = codecs.open(f"{name}.pmd", 'w', self.encoding)
        fs.write(src)
        fs.close()
        pweave.weave(f"{name}.pmd", doctype='markdown')