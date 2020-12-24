# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/Protein.py
# Compiled at: 2009-10-12 08:02:02
__doc__ = '\nDefines a protein.\n'

class Protein(object):
    """
    This class must be used to represents a protein.
    """

    def __init__(self, str_id=None, Header=None, Date=None, Compound=None, Source=None, Author=None, Exp_Method=None, Resolution=None, R_Factor=None, Free_R=None, N_Models=None, Ref_Prog=None, HSSP_N_Align=None, T_Frac_Helix=None, T_Frac_Beta=None, T_Nres_Prot=None, T_non_Std=None, T_Nres_Nucl=None, T_Water_Mols=None, HET_Groups=None, Het_Id=None, Natom=None, Name=None, obsolete=False):
        self.str_id = str_id
        self.Header = Header
        self.Date = Date
        self.Compound = Compound
        self.Source = Source
        self.Author = Author
        self.Exp_Method = Exp_Method
        self.Resolution = Resolution
        self.R_Factor = R_Factor
        self.Free_R = Free_R
        self.N_Models = N_Models
        self.Ref_Prog = Ref_Prog
        self.HSSP_N_Align = HSSP_N_Align
        self.T_Frac_Helix = T_Frac_Helix
        self.T_Frac_Beta = T_Frac_Beta
        self.T_Nres_Prot = T_Nres_Prot
        self.T_non_Std = T_non_Std
        self.T_Nres_Nucl = T_Nres_Nucl
        self.T_Water_Mols = T_Water_Mols
        self.HET_Groups = HET_Groups
        self.Het_Id = Het_Id
        self.Natom = Natom
        self.Name = Name
        self.obsolete = obsolete

    def getSequence(self, chain_id):
        """
        Returns the sequence of the protein.
        
        parameters:
            chain_id: a chain identifier
        """
        return [ chain.sequence for chain in self.chains if chain.chain_id == chain_id ][0]

    def getStructure(self, chain_id):
        """
        Returns the secondary structure of the protein.
        
        parameters:
            chain_id: a chain identifier
        """
        return [ chain.s_structure for chain in self.chains if chain.chain_id == chain_id ][0]

    def getChains(self):
        """
        Gets the chains identifiers of the protein.
        
        return:
            a list of chain identifiers
        """
        return [ chain.chain_id for chain in self.chains ]

    def getMembership(self):
        """
        Looks for dataset memberships of the protein
        
        return:
            SC: a list containing the dataset names
            
        """
        membership = set()
        for chain in self.chains:
            membership.update([ dataset.name for dataset in chain.datasets ])

        return list(membership)

    def isCATHClassified(self):
        """
        Checks if the protein is CATH classified.
        
        return:
            a boolean value
        """
        return len(self.cathClassification) > 0

    def isSCOPClassified(self):
        """
        Checks if the protein is SCOP classified.
        
        return:
            a boolean value
        """
        return len(self.scopClassification) > 0

    def hasTMSegments(self, chain_id):
        """
        Checks if the protein has TM segments
        
        return:
            a boolean value
        """
        return len([ chain.mpData for chain in self.chains if chain.chain_id == chain_id ]) > 0

    def isCATHCompliant(self, **classification):
        """
        Checks if a protein is compliant with a given CATH classification.

        arguments:
            str_id: a protein structure identifier

            **classification: a CATH classification (keys:  'Class', 'architecture', 'topology', 'homologous').

        return:
            a boolean value. Returns True if the protein is compliant with the given CATH classification.
        """
        found = True
        cathProteinData = self.cathClassification[0]
        for level in classification.keys():
            exec "found=found and cathProteinData.%s=='%s'" % (level, classification[level])

        return found

    def isSCOPCompliant(self, **classification):
        """
        Checks if a protein is compliant with a given CATH classification.

        arguments:
            str_id: a protein structure identifier

            **classification: a CATH classification (keys:  'Class', 'architecture', 'topology', 'homologous').

        return:
            a boolean value. Returns True if the protein is compliant with the given CATH classification.
        """
        found = True
        scopProteinData = self.scopClassification[0]
        for level in classification.keys():
            exec "found=found and scopProteinData.%s=='%s'" % (level, classification[level])

        return found