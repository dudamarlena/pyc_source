# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/structure/header/Molecule.py
# Compiled at: 2018-02-02 06:38:51
from . import process_COMPND_line
from . import process_SOURCE_line
from SBI.beans.JSONer import JSONer
import re

class Molecule(JSONer):
    """
    Includes the data from COMPND and SOURCE.
    Each one includes several tokens; those of COMPND:

    TOKEN           VALUE DEFINITION
    -------------------------------------------------------------------------
    MOL_ID          Numbers each component; also used in  SOURCE to associate
                    the information.
    MOLECULE        Name of the macromolecule.
    CHAIN           Comma-separated list of chain  identifier(s).
    FRAGMENT        Specifies a domain or region of the  molecule.
    SYNONYM         Comma-separated list of synonyms for  the MOLECULE.
    EC              The Enzyme Commission number associated  with the molecule.
                    If there is more than one EC number,  they are presented
                    as a comma-separated list.
    ENGINEERED      Indicates that the molecule was  produced using
                    recombinant technology or by purely  chemical synthesis.
    MUTATION        Indicates if there is a mutation.
    OTHER_DETAILS   Additional comments.

    And those of SOURCE:

    TOKEN                     VALUE  DEFINITION
    --------------------------------------------------------------------------
    MOL_ID                    Numbers each molecule. Same as appears in COMPND
    SYNTHETIC                 Indicates a  chemically-synthesized source.
    FRAGMENT                  A domain or  fragment of the molecule may be
                              specified.
    ORGANISM_SCIENTIFIC       Scientific name of the  organism.
    ORGANISM_COMMON           Common name of the  organism.
    ORGANISM_TAXID            NCBI Taxonomy ID number  of the organism.
    STRAIN                    Identifies the  strain.
    VARIANT                   Identifies the  variant.
    CELL_LINE                 The specific line of cells used in
                              the experiment
    ATCC                      American Type  Culture Collection tissue
                              culture  number.
    ORGAN                     Organized group of  tissues that carries on
                              a specialized function.
    TISSUE                    Organized group  of cells with a common
                              function and  structure.
    CELL                      Identifies the  particular cell type.
    ORGANELLE                 Organized structure  within a cell.
    SECRETION                 Identifies the secretion, such as  saliva, urine,
                              or venom,  from which the molecule was isolated.
    CELLULAR_LOCATION         Identifies the location  inside/outside the cell.
    PLASMID                   Identifies the plasmid  containing the gene.
    GENE                      Identifies the  gene.
    EXPRESSION_SYSTEM         Scientific name of the organism in  which the
                              molecule was expressed.
    EXPRESSION_SYSTEM_COMMON  Common name of the organism in which the
                              molecule was  expressed.
    EXPRESSION_SYSTEM_TAXID   NCBI Taxonomy ID of the organism  used as the
                              expression  system.
    EXPRESSION_SYSTEM_STRAIN  Strain of the organism in which  the molecule
                              was  expressed.
    EXPRESSION_SYSTEM_VARIANT Variant of the organism used as the
                              expression  system.
    EXPRESSION_SYSTEM_CELL_LINE  The specific line of cells used as  the
                                 expression  system.
    EXPRESSION_SYSTEM_ATCC_NUMBER  Identifies the ATCC number of the
                                   expression system.
    EXPRESSION_SYSTEM_ORGAN      Specific organ which expressed  the molecule.
    EXPRESSION_SYSTEM_TISSUE     Specific tissue which expressed  the molecule.
    EXPRESSION_SYSTEM_CELL       Specific cell type which  expressed the
                                 molecule.
    EXPRESSION_SYSTEM_ORGANELLE  Specific organelle which expressed
                                 the molecule.
    EXPRESSION_SYSTEM_CELLULAR_LOCATION  Identifies the location inside or
                                         outside the cell  which expressed
                                         the molecule.
    EXPRESSION_SYSTEM_VECTOR_TYPE   Identifies the type of vector used,  i.e.,
                                    plasmid,  virus, or cosmid.
    EXPRESSION_SYSTEM_VECTOR      Identifies the vector used.
    EXPRESSION_SYSTEM_PLASMID     Plasmid used in the recombinant experiment.
    EXPRESSION_SYSTEM_GENE        Name of the gene used in  recombinant
                                  experiment.
    OTHER_DETAILS                 Used to present  information on the
                                  source which
                                  is not  given elsewhere.
    """

    def __init__(self, pdb):
        self._pdb = pdb
        self._COMPND = ''
        self._SOURCE = ''
        self._chains = []
        self._name = ''
        self._ec = set()
        self._taxid = set()
        self._processd = False

    @property
    def pdb(self):
        return self._pdb

    @property
    def chains(self):
        return self._chains

    @property
    def name(self):
        return self._name

    @property
    def ec(self):
        return self._ec

    @property
    def taxid(self):
        return self._taxid

    @property
    def is_processed(self):
        return self._processd

    def add_line(self, switch, line):
        if switch == 'COMPND':
            self._COMPND += process_COMPND_line(line)
        elif switch == 'SOURCE':
            self._SOURCE += process_SOURCE_line(line)

    def _parse--- This code section failed: ---

 L. 143         0  SETUP_LOOP          211  'to 214'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             0  '_SOURCE'
                9  LOAD_ATTR             1  'split'
               12  LOAD_CONST               ';'
               15  CALL_FUNCTION_1       1  None
               18  GET_ITER         
               19  FOR_ITER            191  'to 213'
               22  STORE_FAST            1  'field'

 L. 144        25  LOAD_FAST             1  'field'
               28  LOAD_ATTR             2  'startswith'
               31  LOAD_CONST               'ORGANISM_TAXID'
               34  CALL_FUNCTION_1       1  None
               37  POP_JUMP_IF_FALSE   146  'to 146'

 L. 145        40  SETUP_LOOP           97  'to 140'
               43  LOAD_GLOBAL           3  're'
               46  LOAD_ATTR             1  'split'
               49  LOAD_CONST               ','
               52  LOAD_FAST             1  'field'
               55  LOAD_ATTR             1  'split'
               58  LOAD_CONST               ':'
               61  CALL_FUNCTION_1       1  None
               64  LOAD_CONST               1
               67  BINARY_SUBSCR    
               68  LOAD_ATTR             4  'strip'
               71  CALL_FUNCTION_0       0  None
               74  CALL_FUNCTION_2       2  None
               77  GET_ITER         
               78  FOR_ITER             58  'to 139'
               81  STORE_FAST            2  'tax'

 L. 146        84  SETUP_EXCEPT         42  'to 129'

 L. 147        87  LOAD_GLOBAL           5  'int'
               90  LOAD_FAST             2  'tax'
               93  LOAD_ATTR             4  'strip'
               96  CALL_FUNCTION_0       0  None
               99  CALL_FUNCTION_1       1  None
              102  POP_TOP          

 L. 148       103  LOAD_FAST             0  'self'
              106  LOAD_ATTR             6  'taxid'
              109  LOAD_ATTR             7  'add'
              112  LOAD_FAST             2  'tax'
              115  LOAD_ATTR             4  'strip'
              118  CALL_FUNCTION_0       0  None
              121  CALL_FUNCTION_1       1  None
              124  POP_TOP          
              125  POP_BLOCK        
              126  JUMP_BACK            78  'to 78'
            129_0  COME_FROM            84  '84'

 L. 149       129  POP_TOP          
              130  POP_TOP          
              131  POP_TOP          

 L. 150       132  JUMP_BACK            78  'to 78'
              135  END_FINALLY      
            136_0  COME_FROM           135  '135'
              136  JUMP_BACK            78  'to 78'
              139  POP_BLOCK        
            140_0  COME_FROM            40  '40'

 L. 151       140  CONTINUE             19  'to 19'
              143  JUMP_FORWARD          0  'to 146'
            146_0  COME_FROM           143  '143'

 L. 152       146  LOAD_FAST             1  'field'
              149  LOAD_ATTR             4  'strip'
              152  CALL_FUNCTION_0       0  None
              155  LOAD_CONST               'SYNTHETIC: YES'
              158  COMPARE_OP            2  ==
              161  POP_JUMP_IF_FALSE    19  'to 19'

 L. 153       164  LOAD_GLOBAL           8  'len'
              167  LOAD_FAST             0  'self'
              170  LOAD_ATTR             6  'taxid'
              173  CALL_FUNCTION_1       1  None
              176  LOAD_CONST               0
              179  COMPARE_OP            2  ==
            182_0  COME_FROM           161  '161'
              182  POP_JUMP_IF_FALSE    19  'to 19'

 L. 154       185  LOAD_FAST             0  'self'
              188  LOAD_ATTR             6  'taxid'
              191  LOAD_ATTR             7  'add'
              194  LOAD_CONST               '32630'
              197  CALL_FUNCTION_1       1  None
              200  POP_TOP          
              201  JUMP_BACK            19  'to 19'

 L. 155       204  CONTINUE             19  'to 19'
              207  JUMP_BACK            19  'to 19'
              210  JUMP_BACK            19  'to 19'
              213  POP_BLOCK        
            214_0  COME_FROM             0  '0'

 L. 156       214  LOAD_GLOBAL           9  'True'
              217  LOAD_FAST             0  'self'
              220  STORE_ATTR           10  '_processd'

Parse error at or near `JUMP_BACK' instruction at offset 210

    def _parse_cmpnd(self):
        self._COMPND = re.sub('\\\\;', ',', self._COMPND)
        for field in self._COMPND.split(';'):
            fdata = field.split(':')
            if field.startswith('CHAIN:'):
                self._chains = [ f.strip() for f in fdata[1].strip().split(',') ]
                if '' in self._chains:
                    self._chains.remove('')
                continue
            if field.startswith('MOLECULE:'):
                self._name = (':').join(fdata[1:]).strip()
                continue
            if field.startswith('EC:'):
                self._ec = set([ x.strip() for x in fdata[1].split(',') ])
                continue

    def as_dict(self):
        nobj = {}
        nobj['name'] = self.name
        nobj['chains'] = self.chains
        nobj['ec'] = list(self.ec)
        nobj['taxid'] = list(self.taxid)
        return nobj

    def __repr__(self):
        return self.json()