# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/utilities.py
# Compiled at: 2019-06-28 13:12:13
__doc__ = '\n    Utilities for PDB2PQR Suite\n\n    This module provides various utilities for the PDB2PQR suite to be\n    imported into other Python scripts.\n    \n    ----------------------------\n   \n    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of\n    Poisson-Boltzmann electrostatics calculations\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification, \n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice, \n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice, \n\t\t  this list of conditions and the following disclaimer in the documentation \n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n    ----------------------------\n'
__date__ = '6 November 2007'
__author__ = 'Todd Dolinsky, Yong Huang'
SMALL = 1e-07
DIHEDRAL = 57.2958
import math, os
from os.path import splitext
import sys
from aconf import INSTALLDIR, TMPDIR

def startLogFile(jobName, fileName, logInput):
    with open('%s%s%s/%s' % (INSTALLDIR, TMPDIR, jobName, fileName), 'w') as (f):
        f.write(logInput)


def appendToLogFile(jobName, fileName, logInput):
    with open('%s%s%s/%s' % (INSTALLDIR, TMPDIR, jobName, fileName), 'a') as (f):
        f.write(logInput)


def resetLogFile(jobName, fileName):
    """
    For clearing out old log files if needed.
    Used mainly for removing apbs_end_time if apbs is rerun.
    """
    filename = '%s%s%s/%s' % (INSTALLDIR, TMPDIR, jobName, fileName)
    try:
        os.remove(filename)
    except EnvironmentError:
        pass


def getTrackingScriptString(jobid=None):
    """
    For injecting tracking script into a web page.
    
    jobid -> current jobid. Adds "jobid" custom variable to events and page views on this page.
    """
    customVarString = ''
    if jobid is not None:
        customVarString = ("_gaq.push(['_setCustomVar',1,'jobid','{jobid}',3]);").format(jobid=str(jobid))
    string = ('<script type="text/javascript">\n\n  var _gaq = _gaq || [];\n  _gaq.push([\'_setAccount\', \'UA-11026338-3\']);\n  _gaq.push([\'_setDomainName\', \'none\']);\n  _gaq.push([\'_setAllowLinker\', true]);\n  {customVar}\n  _gaq.push([\'_trackPageview\']);\n\n  (function() {{\n    var ga = document.createElement(\'script\'); ga.type = \'text/javascript\'; ga.async = true;\n    ga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\n    var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\n  }})();\n\n</script>').format(customVar=customVarString)
    return string


def getEventTrackingString(category, action, label, value=None):
    valueString = (', {value}').format(value=value) if value is not None else ''
    eventString = '_gaq.push(["_trackEvent", "{category}", "{action}", "{label}"{valuestr}]);\n'
    return eventString.format(category=str(category), action=str(action), label=str(label), valuestr=valueString)


class ExtraOptions(object):
    pass


def createPropkaOptions(pH, verbose=False, reference='neutral'):
    """
    Create a propka options object for running propka.
    """
    propkaOpts = ExtraOptions()
    propkaOpts.pH = pH
    propkaOpts.reference = reference
    propkaOpts.chains = None
    propkaOpts.thermophiles = None
    propkaOpts.alignment = None
    propkaOpts.mutations = None
    propkaOpts.verbose = verbose
    propkaOpts.protonation = 'old-school'
    propkaOpts.window = (0.0, 14.0, 1.0)
    propkaOpts.grid = (0.0, 14.0, 0.1)
    propkaOpts.mutator = None
    propkaOpts.mutator_options = None
    propkaOpts.display_coupled_residues = None
    propkaOpts.print_iterations = None
    propkaOpts.version_label = 'Nov30'
    from propka30.Source import lib
    lib.interpretMutator(propkaOpts)
    lib.setDefaultAlignmentFiles(propkaOpts)
    return propkaOpts


def getPQRBaseFileName(filename):
    root, ext = splitext(filename)
    if ext.lower() == '.pqr':
        return root
    return filename


def sortDictByValue(inputdict):
    """
        Sort a dictionary by its values

        Parameters
            inputdict:  The dictionary to sort (inputdict)
        Returns
            items: The dictionary sorted by value (list)
    """
    items = [ (v, k) for k, v in inputdict.items() ]
    items.sort()
    items.reverse()
    items = [ k for v, k in items ]
    return items


def shortestPath(graph, start, end, path=[]):
    """
        Uses recursion to find the shortest path from one node to
        another in an unweighted graph.  Adapted from
        http://www.python.org/doc/essays/graphs.html .

        Parameters:
            graph: A mapping of the graph to analyze, of the form
                   {0: [1,2], 1:[3,4], ...} . Each key has a list
                   of edges.
            start: The ID of the key to start the analysis from
            end:   The ID of the key to end the analysis
            path:  Optional argument used during the recursive step
                   to keep the current path up to that point

        Returns:
            (variable): Returns a list of the shortest path (list)
                        Returns None if start and end are not
                        connected
    """
    path = path + [start]
    if start == end:
        return path
    else:
        if not graph.has_key(start):
            return
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = shortestPath(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath

        return shortest


def analyzeConnectivity(map, key):
    """
        Analyze the connectivity of a given map using the key value.

        Parameters
            map:  The map to analyze (dict)
            key:  The key value (variable)
        Returns
            list: A list of connected values to the key (list)
    """
    list = []
    keys = [
     key]
    while len(keys) > 0:
        key = keys[0]
        if key not in list:
            list.append(key)
            if key in map:
                for value in map[key]:
                    if value not in list:
                        keys.append(value)

        keys.pop(keys.index(key))

    return list


def getAngle(coords1, coords2, coords3):
    """
            Get the angle between three coordinates

            Parameters
                coords1:  The first coordinate set (atom)
                coords2:  The second (vertex) coordinate set (atom)
                coords3:  The third coordinate set (atom)
            Returns
                angle:  The angle between the atoms (float)
        """
    angle = 0.0
    c1 = subtract(coords3, coords2)
    c2 = subtract(coords1, coords2)
    norm1 = normalize(c1)
    norm2 = normalize(c2)
    dotted = dot(norm1, norm2)
    if dotted > 1.0:
        dotted = 1.0
    rad = abs(math.acos(dotted))
    angle = rad * 180.0 / math.pi
    if angle > 180.0:
        angle = 360.0 - angle
    return angle


def getFFfile(name):
    """
        Grab the forcefield file.  May or may not residue in the dat/
        directory.
    """
    if name is None:
        return ''
    else:
        path = ''
        dirs = sys.path + ['dat']
        if name in ('gromos', 'amber', 'charmm', 'parse', 'tyl06', 'peoepb', 'swanson'):
            name = name.upper()
        names = [
         'dat/%s.DAT' % name]
        names.append('%s.DAT' % name)
        names.append('%s.dat' % name)
        names.append('dat/%s' % name)
        names.append(name)
        for guess in names:
            if os.path.isfile(guess):
                return guess
            for p in dirs:
                testpath = '%s/%s' % (p, guess)
                if os.path.isfile(testpath):
                    return testpath

        return ''


def getNamesFile(name):
    """
        Grab the *.names file that contains the XML mapping.

        Parameters
            name:  The name of the forcefield (string)
        Returns
            path:  The path to the file (string)
    """
    if name is None:
        return ''
    else:
        path = ''
        dirs = sys.path + ['dat']
        if name in ('gromos', 'amber', 'charmm', 'parse', 'tyl06', 'peoepb', 'swanson'):
            name = name.upper()
        names = [
         'dat/%s.names' % name]
        names.append('%s.names' % name)
        for guess in names:
            if os.path.isfile(guess):
                return guess
            for p in dirs:
                testpath = '%s/%s' % (p, guess)
                if os.path.isfile(testpath):
                    return testpath

        return ''


def getDatFile(name):
    """
        Grab a data file. If the file cannot be found in the
        given directory, try the current system path.

        Parameters
            name:  The name of the file to get (string)
        Returns
            path:  The path to the file (string)
    """
    path = ''
    if os.path.isfile(name):
        path = name
    for p in sys.path:
        testpath = '%s/%s' % (p, name)
        if os.path.isfile(testpath):
            path = testpath

    return path


def getPDBFile(path):
    """
        Obtain a PDB file.  First check the path given on the command
        line - if that file is not available, obtain the file from the
        PDB webserver at http://www.rcsb.org/pdb/ .

        Parameters
            path:  Name of PDB file to obtain (string)

        Returns
            file:  File object containing PDB file (file object)
    """
    import os, urllib
    file = None
    if not os.path.isfile(path):
        URLpath = 'https://files.rcsb.org/download/' + path + '.pdb'
        try:
            file = urllib.urlopen(URLpath)
            if file.getcode() != 200 or 'nosuchfile' in file.geturl():
                raise IOError
        except IOError:
            return

    else:
        file = open(path, 'rU')
    return file


def distance(coords1, coords2):
    """
        Calculate the distance between two coordinates, as denoted by

            dist = sqrt((x2- x1)^2 + (y2 - y1)^2 + (z2 - z1)^2))

        Parameters
            coords1: Coordinates of form [x,y,z]
            coords2: Coordinates of form [x,y,z]
        Returns
            dist:  Distance between the two coordinates (float)
    """
    dist = 0.0
    list = []
    p = coords2[0] - coords1[0]
    q = coords2[1] - coords1[1]
    r = coords2[2] - coords1[2]
    dist = math.sqrt(p * p + q * q + r * r)
    return dist


def add(coords1, coords2):
    """
        Add one 3-dimensional point to another
        
        Parameters
            coords1: coordinates of form [x,y,z]
            coords2: coordinates of form [x,y,z]
        Returns
            list:  List of coordinates equal to coords2 + coords1 (list)
    """
    x = coords1[0] + coords2[0]
    y = coords1[1] + coords2[1]
    z = coords1[2] + coords2[2]
    return [
     x, y, z]


def subtract(coords1, coords2):
    """
        Subtract one 3-dimensional point from another

        Parameters
            coords1: coordinates of form [x,y,z]
            coords2: coordinates of form [x,y,z]
        Returns
            list:  List of coordinates equal to coords1 - coords2 (list)
    """
    x = coords1[0] - coords2[0]
    y = coords1[1] - coords2[1]
    z = coords1[2] - coords2[2]
    return [
     x, y, z]


def cross(coords1, coords2):
    """
        Find the cross product of two 3-dimensional points

        Parameters
            coords1: coordinates of form [x,y,z]
            coords2: coordinates of form [x,y,z]
        Returns
            list:  Cross product coords2 and coords1 (list)
    """
    list = []
    x = coords1[1] * coords2[2] - coords1[2] * coords2[1]
    y = coords1[2] * coords2[0] - coords1[0] * coords2[2]
    z = coords1[0] * coords2[1] - coords1[1] * coords2[0]
    list = [x, y, z]
    return list


def dot(coords1, coords2):
    """
        Find the dot product of two 3-dimensional points

        Parameters
            coords1: coordinates of form [x,y,z]
            coords2: coordinates of form [x,y,z]
        Returns
            value:  Dot product coords2 and coords1 (float)
    """
    value = 0.0
    for i in range(3):
        value += coords1[i] * coords2[i]

    return value


def normalize(coords):
    """
        Normalize a set of coordinates
        
        Parameters
            coords: coordinates of form [x,y,z]
        Returns
            list: normalized coordinates (list)
    """
    list = []
    dist = math.sqrt(pow(coords[0], 2) + pow(coords[1], 2) + pow(coords[2], 2))
    if dist > SMALL:
        a = coords[0] / dist
        b = coords[1] / dist
        c = coords[2] / dist
        list = [a, b, c]
    else:
        list = coords
    return list


def factorial(n):
    """
        Returns the factorial of the given number n
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def getDihedral(coords1, coords2, coords3, coords4):
    """
        Calculate the angle using the four atoms

        Parameters
            coords1: First of four coordinates of form [x,y,z]
            coords2: Second of four
            coords3: Third of four
            coords4: Fourth of four
        Returns
            value: Size of the angle (float)
    """
    value = 0.0
    list43 = subtract(coords4, coords3)
    list32 = subtract(coords3, coords2)
    list12 = subtract(coords1, coords2)
    A = cross(list12, list32)
    Anorm = normalize(A)
    B = cross(list43, list32)
    Bnorm = normalize(B)
    scal = dot(Anorm, Bnorm)
    if abs(scal + 1.0) < SMALL:
        value = 180.0
    elif abs(scal - 1.0) < SMALL:
        value = 0.0
    else:
        value = DIHEDRAL * math.acos(scal)
    chiral = dot(cross(Anorm, Bnorm), list32)
    if chiral < 0:
        value = value * -1.0
    return value