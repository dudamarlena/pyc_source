# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/topology.py
# Compiled at: 2018-06-29 21:47:06
"""
    Parser for TOPOLOGY.xml

    ----------------------------
   
    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of
    Poisson-Boltzmann electrostatics calculations

    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; 
    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific 
    Northwest National Laboratory, operated by Battelle Memorial Institute, 
    Pacific Northwest Division for the U.S. Department Energy.; 
    Paul Czodrowski & Gerhard Klebe, University of Marburg.

        All rights reserved.

        Redistribution and use in source and binary forms, with or without modification, 
        are permitted provided that the following conditions are met:

                * Redistributions of source code must retain the above copyright notice, 
                  this list of conditions and the following disclaimer.
                * Redistributions in binary form must reproduce the above copyright notice, 
                  this list of conditions and the following disclaimer in the documentation 
                  and/or other materials provided with the distribution.
        * Neither the names of University College Dublin, Battelle Memorial Institute,
          Pacific Northwest National Laboratory, US Department of Energy, or University
          of Marburg nor the names of its contributors may be used to endorse or promote
          products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
        IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
        INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
        BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
        DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
        LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
        OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
        OF THE POSSIBILITY OF SUCH DAMAGE.

    ----------------------------

"""
__date__ = '12 November 2008'
__author__ = 'Nathan Baker, Yong Huang'
TOPOLOGYPATH = 'TOPOLOGY.xml'
from sys import stderr
from xml import sax

class TopologyHandler(sax.ContentHandler):
    """ Handler for XML-based topology files.  Assumes the following hierarchy of tags:
        topology
        -->residue
           |-->reference
           |-->titrationstate
               |-->tautomer
                   |-->conformer
        """

    def __init__(self):
        self.currentElement = None
        self.currentAtom = None
        self.currentDihedral = None
        self.currentReference = None
        self.currentResidue = None
        self.currentTitrationState = None
        self.currentTautomer = None
        self.currentConformer = None
        self.currentConformerAdd = None
        self.currentConformerRemove = None
        self.residues = []
        self.incomplete = 0
        return

    def startElement--- This code section failed: ---

 L.  78         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'incomplete'
                6  POP_JUMP_IF_TRUE    812  'to 812'

 L.  80         9  LOAD_FAST             1  'tagName'
               12  LOAD_CONST               'topology'
               15  COMPARE_OP            2  ==
             18_0  COME_FROM             6  '6'
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  81        21  JUMP_ABSOLUTE       812  'to 812'

 L.  82        24  LOAD_FAST             1  'tagName'
               27  LOAD_CONST               'residue'
               30  COMPARE_OP            2  ==
               33  POP_JUMP_IF_FALSE    77  'to 77'

 L.  83        36  LOAD_FAST             0  'self'
               39  LOAD_ATTR             1  'currentResidue'
               42  LOAD_CONST               None
               45  COMPARE_OP            3  !=
               48  POP_JUMP_IF_FALSE    59  'to 59'

 L.  84        51  LOAD_CONST               '** Overwriting current TopologyResidue object!'
               54  PRINT_ITEM       
               55  PRINT_NEWLINE_CONT
               56  JUMP_FORWARD          0  'to 59'
             59_0  COME_FROM            56  '56'

 L.  85        59  LOAD_GLOBAL           3  'TopologyResidue'
               62  LOAD_FAST             0  'self'
               65  CALL_FUNCTION_1       1  None
               68  LOAD_FAST             0  'self'
               71  STORE_ATTR            1  'currentResidue'
               74  JUMP_ABSOLUTE       812  'to 812'

 L.  86        77  LOAD_FAST             1  'tagName'
               80  LOAD_CONST               'reference'
               83  COMPARE_OP            2  ==
               86  POP_JUMP_IF_FALSE   133  'to 133'

 L.  87        89  LOAD_FAST             0  'self'
               92  LOAD_ATTR             4  'currentReference'
               95  LOAD_CONST               None
               98  COMPARE_OP            3  !=
              101  POP_JUMP_IF_FALSE   112  'to 112'

 L.  88       104  LOAD_CONST               '** Overwriting current TopologyReference object!'
              107  PRINT_ITEM       
              108  PRINT_NEWLINE_CONT
              109  JUMP_FORWARD          0  'to 112'
            112_0  COME_FROM           109  '109'

 L.  89       112  LOAD_GLOBAL           5  'TopologyReference'
              115  LOAD_FAST             0  'self'
              118  LOAD_ATTR             1  'currentResidue'
              121  CALL_FUNCTION_1       1  None
              124  LOAD_FAST             0  'self'
              127  STORE_ATTR            4  'currentReference'
              130  JUMP_ABSOLUTE       812  'to 812'

 L.  90       133  LOAD_FAST             1  'tagName'
              136  LOAD_CONST               'titrationstate'
              139  COMPARE_OP            2  ==
              142  POP_JUMP_IF_FALSE   189  'to 189'

 L.  91       145  LOAD_FAST             0  'self'
              148  LOAD_ATTR             6  'currentTitrationState'
              151  LOAD_CONST               None
              154  COMPARE_OP            3  !=
              157  POP_JUMP_IF_FALSE   168  'to 168'

 L.  92       160  LOAD_CONST               '** Overwriting current TopologyTitrationState object!'
              163  PRINT_ITEM       
              164  PRINT_NEWLINE_CONT
              165  JUMP_FORWARD          0  'to 168'
            168_0  COME_FROM           165  '165'

 L.  93       168  LOAD_GLOBAL           7  'TopologyTitrationState'
              171  LOAD_FAST             0  'self'
              174  LOAD_ATTR             1  'currentResidue'
              177  CALL_FUNCTION_1       1  None
              180  LOAD_FAST             0  'self'
              183  STORE_ATTR            6  'currentTitrationState'
              186  JUMP_ABSOLUTE       812  'to 812'

 L.  94       189  LOAD_FAST             1  'tagName'
              192  LOAD_CONST               'tautomer'
              195  COMPARE_OP            2  ==
              198  POP_JUMP_IF_FALSE   245  'to 245'

 L.  95       201  LOAD_FAST             0  'self'
              204  LOAD_ATTR             8  'currentTautomer'
              207  LOAD_CONST               None
              210  COMPARE_OP            3  !=
              213  POP_JUMP_IF_FALSE   224  'to 224'

 L.  96       216  LOAD_CONST               '** Overwriting current Tautomer object!'
              219  PRINT_ITEM       
              220  PRINT_NEWLINE_CONT
              221  JUMP_FORWARD          0  'to 224'
            224_0  COME_FROM           221  '221'

 L.  97       224  LOAD_GLOBAL           9  'TopologyTautomer'
              227  LOAD_FAST             0  'self'
              230  LOAD_ATTR             6  'currentTitrationState'
              233  CALL_FUNCTION_1       1  None
              236  LOAD_FAST             0  'self'
              239  STORE_ATTR            8  'currentTautomer'
              242  JUMP_ABSOLUTE       812  'to 812'

 L.  98       245  LOAD_FAST             1  'tagName'
              248  LOAD_CONST               'conformer'
              251  COMPARE_OP            2  ==
              254  POP_JUMP_IF_FALSE   301  'to 301'

 L.  99       257  LOAD_FAST             0  'self'
              260  LOAD_ATTR            10  'currentConformer'
              263  LOAD_CONST               None
              266  COMPARE_OP            3  !=
              269  POP_JUMP_IF_FALSE   280  'to 280'

 L. 100       272  LOAD_CONST               '** Overwriting current Conformer object!'
              275  PRINT_ITEM       
              276  PRINT_NEWLINE_CONT
              277  JUMP_FORWARD          0  'to 280'
            280_0  COME_FROM           277  '277'

 L. 101       280  LOAD_GLOBAL          11  'TopologyConformer'
              283  LOAD_FAST             0  'self'
              286  LOAD_ATTR             8  'currentTautomer'
              289  CALL_FUNCTION_1       1  None
              292  LOAD_FAST             0  'self'
              295  STORE_ATTR           10  'currentConformer'
              298  JUMP_ABSOLUTE       812  'to 812'

 L. 102       301  LOAD_FAST             1  'tagName'
              304  LOAD_CONST               'name'
              307  COMPARE_OP            2  ==
              310  POP_JUMP_IF_FALSE   325  'to 325'

 L. 103       313  LOAD_FAST             1  'tagName'
              316  LOAD_FAST             0  'self'
              319  STORE_ATTR           12  'currentElement'
              322  JUMP_ABSOLUTE       812  'to 812'

 L. 104       325  LOAD_FAST             1  'tagName'
              328  LOAD_CONST               'atom'
              331  COMPARE_OP            2  ==
              334  POP_JUMP_IF_FALSE   453  'to 453'

 L. 105       337  LOAD_FAST             0  'self'
              340  LOAD_ATTR            13  'currentConformerAdd'
              343  LOAD_CONST               None
              346  COMPARE_OP            3  !=
              349  POP_JUMP_IF_FALSE   373  'to 373'

 L. 107       352  LOAD_GLOBAL          14  'TopologyAtom'
              355  LOAD_FAST             0  'self'
              358  LOAD_ATTR            13  'currentConformerAdd'
              361  CALL_FUNCTION_1       1  None
              364  LOAD_FAST             0  'self'
              367  STORE_ATTR           15  'currentAtom'
              370  JUMP_ABSOLUTE       809  'to 809'

 L. 108       373  LOAD_FAST             0  'self'
              376  LOAD_ATTR            16  'currentConformerRemove'
              379  LOAD_CONST               None
              382  COMPARE_OP            3  !=
              385  POP_JUMP_IF_FALSE   409  'to 409'

 L. 110       388  LOAD_GLOBAL          14  'TopologyAtom'
              391  LOAD_FAST             0  'self'
              394  LOAD_ATTR            16  'currentConformerRemove'
              397  CALL_FUNCTION_1       1  None
              400  LOAD_FAST             0  'self'
              403  STORE_ATTR           15  'currentAtom'
              406  JUMP_ABSOLUTE       809  'to 809'

 L. 111       409  LOAD_FAST             0  'self'
              412  LOAD_ATTR             4  'currentReference'
              415  LOAD_CONST               None
              418  COMPARE_OP            3  !=
              421  POP_JUMP_IF_FALSE   445  'to 445'

 L. 113       424  LOAD_GLOBAL          14  'TopologyAtom'
              427  LOAD_FAST             0  'self'
              430  LOAD_ATTR             4  'currentReference'
              433  CALL_FUNCTION_1       1  None
              436  LOAD_FAST             0  'self'
              439  STORE_ATTR           15  'currentAtom'
              442  JUMP_ABSOLUTE       809  'to 809'

 L. 115       445  LOAD_CONST               "** Don't know what to do with this atom!"
              448  PRINT_ITEM       
              449  PRINT_NEWLINE_CONT
              450  JUMP_ABSOLUTE       812  'to 812'

 L. 116       453  LOAD_FAST             1  'tagName'
              456  LOAD_CONST               'x'
              459  COMPARE_OP            2  ==
              462  POP_JUMP_IF_FALSE   477  'to 477'

 L. 117       465  LOAD_FAST             1  'tagName'
              468  LOAD_FAST             0  'self'
              471  STORE_ATTR           12  'currentElement'
              474  JUMP_ABSOLUTE       812  'to 812'

 L. 118       477  LOAD_FAST             1  'tagName'
              480  LOAD_CONST               'y'
              483  COMPARE_OP            2  ==
              486  POP_JUMP_IF_FALSE   501  'to 501'

 L. 119       489  LOAD_FAST             1  'tagName'
              492  LOAD_FAST             0  'self'
              495  STORE_ATTR           12  'currentElement'
              498  JUMP_ABSOLUTE       812  'to 812'

 L. 120       501  LOAD_FAST             1  'tagName'
              504  LOAD_CONST               'z'
              507  COMPARE_OP            2  ==
              510  POP_JUMP_IF_FALSE   525  'to 525'

 L. 121       513  LOAD_FAST             1  'tagName'
              516  LOAD_FAST             0  'self'
              519  STORE_ATTR           12  'currentElement'
              522  JUMP_ABSOLUTE       812  'to 812'

 L. 122       525  LOAD_FAST             1  'tagName'
              528  LOAD_CONST               'bond'
              531  COMPARE_OP            2  ==
              534  POP_JUMP_IF_FALSE   549  'to 549'

 L. 123       537  LOAD_FAST             1  'tagName'
              540  LOAD_FAST             0  'self'
              543  STORE_ATTR           12  'currentElement'
              546  JUMP_ABSOLUTE       812  'to 812'

 L. 124       549  LOAD_FAST             1  'tagName'
              552  LOAD_CONST               'altname'
              555  COMPARE_OP            2  ==
              558  POP_JUMP_IF_FALSE   573  'to 573'

 L. 125       561  LOAD_FAST             1  'tagName'
              564  LOAD_FAST             0  'self'
              567  STORE_ATTR           12  'currentElement'
              570  JUMP_ABSOLUTE       812  'to 812'

 L. 126       573  LOAD_FAST             1  'tagName'
              576  LOAD_CONST               'dihedral'
              579  COMPARE_OP            2  ==
              582  POP_JUMP_IF_FALSE   710  'to 710'

 L. 127       585  LOAD_FAST             1  'tagName'
              588  LOAD_FAST             0  'self'
              591  STORE_ATTR           12  'currentElement'

 L. 128       594  LOAD_FAST             0  'self'
              597  LOAD_ATTR            13  'currentConformerAdd'
              600  LOAD_CONST               None
              603  COMPARE_OP            3  !=
              606  POP_JUMP_IF_FALSE   630  'to 630'

 L. 130       609  LOAD_GLOBAL          17  'TopologyDihedral'
              612  LOAD_FAST             0  'self'
              615  LOAD_ATTR            13  'currentConformerAdd'
              618  CALL_FUNCTION_1       1  None
              621  LOAD_FAST             0  'self'
              624  STORE_ATTR           18  'currentDihedral'
              627  JUMP_ABSOLUTE       809  'to 809'

 L. 131       630  LOAD_FAST             0  'self'
              633  LOAD_ATTR            16  'currentConformerRemove'
              636  LOAD_CONST               None
              639  COMPARE_OP            3  !=
              642  POP_JUMP_IF_FALSE   666  'to 666'

 L. 133       645  LOAD_GLOBAL          17  'TopologyDihedral'
              648  LOAD_FAST             0  'self'
              651  LOAD_ATTR            16  'currentConformerRemove'
              654  CALL_FUNCTION_1       1  None
              657  LOAD_FAST             0  'self'
              660  STORE_ATTR           18  'currentDihedral'
              663  JUMP_ABSOLUTE       809  'to 809'

 L. 134       666  LOAD_FAST             0  'self'
              669  LOAD_ATTR             4  'currentReference'
              672  LOAD_CONST               None
              675  COMPARE_OP            3  !=
              678  POP_JUMP_IF_FALSE   702  'to 702'

 L. 136       681  LOAD_GLOBAL          17  'TopologyDihedral'
              684  LOAD_FAST             0  'self'
              687  LOAD_ATTR             4  'currentReference'
              690  CALL_FUNCTION_1       1  None
              693  LOAD_FAST             0  'self'
              696  STORE_ATTR           18  'currentDihedral'
              699  JUMP_ABSOLUTE       809  'to 809'

 L. 138       702  LOAD_CONST               "** Don't know what to do with this dihedral!"
              705  PRINT_ITEM       
              706  PRINT_NEWLINE_CONT
              707  JUMP_ABSOLUTE       812  'to 812'

 L. 139       710  LOAD_FAST             1  'tagName'
              713  LOAD_CONST               'add'
              716  COMPARE_OP            2  ==
              719  POP_JUMP_IF_FALSE   743  'to 743'

 L. 140       722  LOAD_GLOBAL          19  'TopologyConformerAdd'
              725  LOAD_FAST             0  'self'
              728  LOAD_ATTR            10  'currentConformer'
              731  CALL_FUNCTION_1       1  None
              734  LOAD_FAST             0  'self'
              737  STORE_ATTR           13  'currentConformerAdd'
              740  JUMP_ABSOLUTE       812  'to 812'

 L. 141       743  LOAD_FAST             1  'tagName'
              746  LOAD_CONST               'remove'
              749  COMPARE_OP            2  ==
              752  POP_JUMP_IF_FALSE   776  'to 776'

 L. 143       755  LOAD_GLOBAL          20  'TopologyConformerRemove'
              758  LOAD_FAST             0  'self'
              761  LOAD_ATTR            10  'currentConformer'
              764  CALL_FUNCTION_1       1  None
              767  LOAD_FAST             0  'self'
              770  STORE_ATTR           16  'currentConformerRemove'
              773  JUMP_ABSOLUTE       812  'to 812'

 L. 144       776  LOAD_FAST             1  'tagName'
              779  LOAD_CONST               'incomplete'
              782  COMPARE_OP            2  ==
              785  POP_JUMP_IF_FALSE   800  'to 800'

 L. 146       788  LOAD_CONST               1
              791  LOAD_FAST             0  'self'
              794  STORE_ATTR            0  'incomplete'
              797  JUMP_ABSOLUTE       812  'to 812'

 L. 148       800  LOAD_CONST               '** NOT handling %s start tag'
              803  LOAD_FAST             1  'tagName'
              806  BINARY_MODULO    
              807  PRINT_ITEM       
              808  PRINT_NEWLINE_CONT
              809  JUMP_FORWARD          0  'to 812'
            812_0  COME_FROM           809  '809'
              812  LOAD_CONST               None
              815  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 21

    def endElement(self, tagName):
        if not self.incomplete:
            self.currentElement == None
            if tagName == 'x':
                pass
            elif tagName == 'y':
                pass
            elif tagName == 'z':
                pass
            elif tagName == 'name':
                pass
            elif tagName == 'bond':
                pass
            elif tagName == 'altname':
                pass
            elif tagName == 'atom':
                self.currentAtom = None
            elif tagName == 'dihedral':
                self.currentDihedral = None
            elif tagName == 'reference':
                self.currentReference = None
            elif tagName == 'add':
                self.currentConformerAdd = None
            elif tagName == 'remove':
                self.currentConformerRemove = None
            elif tagName == 'titrationstate':
                residue = self.currentTitrationState.topologyResidue
                self.currentTitrationState = None
            elif tagName == 'conformer':
                tautomer = self.currentConformer.topologyTautomer
                self.currentConformer = None
            elif tagName == 'tautomer':
                titrationState = self.currentTautomer.topologyTitrationState
                self.currentTautomer = None
            elif tagName == 'residue':
                self.currentResidue = None
            elif tagName == 'topology':
                pass
            else:
                print '** NOT handling %s end tag' % tagName
        elif tagName == 'incomplete':
            self.incomplete = 0
        return

    def characters(self, text):
        if text.isspace():
            return
        else:
            if not self.incomplete:
                if self.currentElement == 'name':
                    if self.currentAtom != None:
                        self.currentAtom.name = text
                    elif self.currentConformer != None:
                        self.currentConformer.name = text
                    elif self.currentTautomer != None:
                        self.currentTautomer.name = text
                    elif self.currentTitrationState != None:
                        self.currentTitrationState.name = text
                    elif self.currentResidue != None:
                        self.currentResidue.name = text
                    else:
                        print "    *** Don't know what to do with name %s!" % text
                elif self.currentElement == 'x':
                    self.currentAtom.x = float(text)
                elif self.currentElement == 'y':
                    self.currentAtom.y = float(text)
                elif self.currentElement == 'z':
                    self.currentAtom.z = float(text)
                elif self.currentElement == 'bond':
                    self.currentAtom.bonds.append(text)
                elif self.currentElement == 'altname':
                    self.currentAtom.altname = text
                elif self.currentElement == 'dihedral':
                    self.currentDihedral.atomList = text
                else:
                    print '** NOT handling character text:  %s' % text
            return


class TopologyResidue:
    """ A class for residue topology information """

    def __init__(self, topology):
        """ Initialize with a Topology object """
        self.name = None
        self.reference = None
        self.titrationStates = []
        self.topology = topology
        self.topology.residues.append(self)
        return

    def __str__(self):
        return self.name


class TopologyDihedral:
    """ A class for dihedral topology information.  """

    def __init__(self, parent):
        """ Needs a parent that has a dihedral list. """
        self.parent = parent
        self.parent.dihedrals.append(self)
        self.atomList = None
        return

    def __str__(self):
        return self.atomList


class TopologyAtom:
    """ A class for atom topology information """

    def __init__(self, parent):
        """ Needs to be intialized with an upper-level class that contains an atoms array (e.g., TopologyReference
                or TopologyConformerAddition)"""
        self.parent = parent
        self.parent.atoms.append(self)
        self.name = None
        self.x = None
        self.y = None
        self.z = None
        self.bonds = []
        self.altname = None
        return

    def __str__(self):
        return self.name


class TopologyTitrationState:
    """ A class for the titration state of a residue """

    def __init__(self, topologyResidue):
        """ Initialize with a TopologyResidue object """
        self.topologyResidue = topologyResidue
        self.topologyResidue.titrationStates.append(self)
        self.tautomers = []
        self.name = None
        return

    def __str__(self):
        return self.name


class TopologyTautomer:
    """ A class for topology tautomer information """

    def __init__(self, topologyTitrationState):
        """ Initialize with a TopologyTitrationState object """
        self.topologyTitrationState = topologyTitrationState
        self.topologyTitrationState.tautomers.append(self)
        self.conformers = []
        self.name = None
        return

    def __str__(self):
        return self.name


class TopologyConformer:
    """ A class for topology conformer information """

    def __init__(self, topologyTautomer):
        """ Initialize with a TopologyTautomer object """
        self.topologyTautomer = topologyTautomer
        self.topologyTautomer.conformers.append(self)
        self.name = None
        self.conformerAdds = []
        self.conformerRemoves = []
        return

    def __str__(self):
        return self.name


class TopologyReference:
    """ A class for the reference structure of a residue """

    def __init__(self, topologyResidue):
        """ Initialize with a TopologyResidue object """
        self.topologyResidue = topologyResidue
        self.topologyResidue.reference = self
        self.atoms = []
        self.dihedrals = []


class TopologyConformerAdd:
    """ A class for adding atoms to a conformer """

    def __init__(self, topologyConformer):
        """ Initialize with a TopologyConformer object """
        self.topologyConformer = topologyConformer
        self.topologyConformer.conformerAdds.append(self)
        self.atoms = []
        self.name = None
        self.dihedrals = []
        return


class TopologyConformerRemove:
    """ A class for removing atoms to a conformer """

    def __init__(self, topologyConformer):
        """ Initialize with a TopologyConformer object """
        self.topologyConformer = topologyConformer
        self.topologyConformer.conformerRemoves.append(self)
        self.atoms = []
        self.name = None
        return


class Topology:
    """ Contains the structured definitions of residue reference coordinates as well as alternate titration, 
        conformer, and tautomer states.
        """

    def __init__(self, topologyFile):
        """ Initialize with the topology file reference ready for reading """
        handler = TopologyHandler()
        sax.make_parser()
        sax.parseString(topologyFile.read(), handler)
        self.residues = handler.residues


if __name__ == '__main__':
    topologyFile = open(TOPOLOGYPATH, 'r')
    topology = Topology(topologyFile)