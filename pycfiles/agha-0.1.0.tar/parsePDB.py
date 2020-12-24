# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/olek/Wszystkie_aggrescamy_swiata/aggrescan3d/a3d_gui/parsePDB.py
# Compiled at: 2018-08-29 04:49:14
import gzip
from re import compile, sub
import json

def arraytostring(ar):
    i = [ '%d-%d' % e for e in ar ]
    return (', ').join(i)


class PdbParser:

    def __init__(self, filehandler, chain=''):
        self.codification = {'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L', 'MET': 'M', 'MSE': 'M', 'ASN': 'N', 'PYL': 'O', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R', 'SER': 'S', 'THR': 'T', 'SEC': 'U', 'VAL': 'V', 'TRP': 'W', '5HP': 'E', 'ABA': 'A', 'AIB': 'A', 'BMT': 'T', 'CEA': 'C', 'CGU': 'E', 'CME': 'C', 'CRO': 'X', 'CSD': 'C', 'CSO': 'C', 'CSS': 'C', 'CSW': 'C', 'CSX': 'C', 'CXM': 'M', 'DAL': 'A', 'DAR': 'R', 'DCY': 'C', 'DGL': 'E', 'DGN': 'Q', 'DHI': 'H', 'DIL': 'I', 'DIV': 'V', 'DLE': 'L', 'DLY': 'K', 'DPN': 'F', 'DPR': 'P', 'DSG': 'N', 'DSN': 'S', 'DSP': 'D', 'DTH': 'T', 'DTR': 'X', 'DTY': 'Y', 'DVA': 'V', 'FME': 'M', 'HYP': 'P', 'KCX': 'K', 'LLP': 'K', 'MLE': 'L', 'MVA': 'V', 'NLE': 'L', 'OCS': 'C', 'ORN': 'A', 'PCA': 'E', 'PTR': 'Y', 'SAR': 'G', 'SEP': 'S', 'STY': 'Y', 'TPO': 'T', 'TPQ': 'F', 'TYS': 'Y', 'TYR': 'Y'}
        keys = self.codification.keys()
        self.sequences = {}
        self.onlycalfa = ''
        self.chain = chain
        self.canumber = 0
        self.allnumber = 0
        seq = compile('^ATOM.{9}CA..(?P<seqid>.{3}).(?P<chain>.{1})(?P<resid>.{4})')
        if chain != '':
            ch = ('|').join(list(chain))
            seq_c = compile('^ATOM.{9}CA.( |A)(?P<seqid>.{3}).(' + ch + ')')
            atm = compile('^ATOM.{9}(.{3})( |A)(?P<seqid>.{3}).(' + ch + ')(?P<resid>.{4})(?P<x>.{12})(?P<y>.{8})(?P<z>.{8})')
        else:
            atm = compile('^ATOM.{9}(.{3})( |A)(?P<seqid>.{3})..(?P<resid>.{4})(?P<x>.{12})(?P<y>.{8})(?P<z>.{8})')
            seq_c = compile('^ATOM.{9}CA.( |A)(?P<seqid>.{3})')
        ter = compile('^TER')
        mod = compile('^ENDMDL')
        self.trajectory = []
        self.sequence = ''
        self.resindexes = []
        self.mutatedata = {}
        f = filehandler
        lines = f.readlines()
        end = len(lines) - 1
        counter = 0
        tmp = []
        chains_order = []
        old_chain_id = ''
        chain_break = False
        for line in lines:
            line = self._replaceExotic(line)
            data = atm.match(line)
            data_seq = seq.match(line)
            data_seqc = seq_c.match(line)
            if data_seqc and data_seqc.group('seqid') in keys:
                self.canumber += 1
            if data_seq:
                seqid = data_seq.group('seqid').strip()
                if seqid not in self.codification.keys():
                    continue
                chainid = data_seq.group('chain').strip()
                if chainid != old_chain_id:
                    if old_chain_id != '':
                        chain_break = True
                    old_chain_id = chainid
                if chainid not in chains_order:
                    chains_order.append(chainid)
                resid = data_seq.group('resid').strip()
                if seqid in keys:
                    self.sequence += self.codification[seqid]
                    s = self.codification[seqid]
                else:
                    s = 'X'
                    self.sequence += 'X'
                if chainid in self.sequences.keys():
                    self.sequences[chainid] += s
                else:
                    self.sequences[chainid] = s
                if chainid in self.mutatedata.keys():
                    self.mutatedata[chainid].append({'chain': chainid, 'resname': s, 
                       'residx': resid})
                else:
                    self.mutatedata[chainid] = [{'chain': chainid, 'resname': s, 
                        'residx': resid}]
                if chainid in self.sequences.keys():
                    self.sequences[chainid] += s
                else:
                    self.sequences[chainid] = s
            if data:
                seqid = data.group('seqid').strip()
                if seqid not in self.codification.keys():
                    continue
                self.allnumber += 1
                self.onlycalfa += line
                dg = data.groups()
                if dg[0].strip() == 'CA':
                    try:
                        tmp.append(int(data.group('resid')))
                    except ValueError:
                        raise ValueError('Wrong residue index number. We do not support negative residue indexes which is the most likely cause for this error. Offending line : %s' % line)

            if ter.match(line) or counter == end or chain_break:
                self.resindexes.append(tmp)
                tmp = []
                chain_break = False
            if mod.match(line) and len(self.onlycalfa) > 1 or counter == end:
                break
            counter += 1

        filehandler.seek(0)
        o = {}
        for i in range(len(chains_order)):
            o[chains_order[i]] = self.resindexes[i]

        self.numb = o

    def _replaceExotic(self, line):
        if line.startswith('HETATM') and len(line) > 21:
            res = line[17:20]
            if res in self.nonstandard:
                sf = '^HETATM(.{10}(A| ))' + res
                st = 'ATOM  \\1' + self.modres[res]
                line = sub(sf, st, line)
        return line

    def isSingleChain(self):
        if self.chain != '' or len(self.sequences.keys()) == 1:
            return True
        return False

    def containsOnlyCA(self):
        if self.allnumber == self.canumber:
            return True
        else:
            return False

    def getMissing(self):
        return self.isBroken() + len(self.sequences.keys())

    def isBroken(self):
        brk = []
        for j in self.numb.keys():
            indexes = self.numb[j]
            if len(indexes) == 0:
                continue
            first = indexes[0]
            for i in range(1, len(indexes)):
                if indexes[i] - 1 != first:
                    brk.append(str(first) + '-' + str(indexes[i]))
                first = indexes[i]

        return len(brk)

    def getResIndexes(self):
        return (',').join([ str(i) for i in self.numb[self.chain] ])

    def getChains(self):
        return self.sequences.keys()

    def getBody(self):
        t = []
        for line in self.onlycalfa.split('\n'):
            t.append(line[:16] + ' ' + line[17:])

        return ('\n').join(t)

    def savePdbFile(self, outfilename):
        with gzip.open(outfilename, 'wb') as (fw):
            fw.write(self.getBody())

    def containsChain(self, chain):
        if chain in self.sequences.keys():
            return True

    def get_num_chains(self):
        return len(self.sequences.keys())

    def getSequence(self):
        if self.chain != '':
            o = ''
            for e in list(self.chain):
                if e in self.sequences.keys():
                    o += self.sequences[e]

            return o
        out = ''
        for k in self.sequences.keys():
            out += ('').join(self.sequences[k])

        return out

    def getChainIdxResname(self):
        if self.chain == '':
            return json.dumps(self.mutatedata)
        else:
            return json.dumps({self.chain: self.mutatedata[self.chain]})

    def getChainLengths(self):
        out = []
        if self.chain != '':
            for e in list(self.chain):
                if self.containsChain(e):
                    out.append(len(self.sequences[e]))

        else:
            for k in self.sequences.keys():
                out.append(len(self.sequences[k]))

        return out

    modres = {'0CS': 'ALA', 
       '1AB': 'PRO', 
       '1LU': 'LEU', 
       '1PA': 'PHE', 
       '1TQ': 'TRP', 
       '1TY': 'TYR', 
       '23F': 'PHE', 
       '23S': 'TRP', 
       '2BU': 'ALA', 
       '2ML': 'LEU', 
       '2MR': 'ARG', 
       '2MT': 'PRO', 
       '2OP': 'ALA', 
       '2TY': 'TYR', 
       '32S': 'TRP', 
       '32T': 'TRP', 
       '3AH': 'HIS', 
       '3MD': 'ASP', 
       '3TY': 'TYR', 
       '4DP': 'TRP', 
       '4F3': 'ALA', 
       '4FB': 'PRO', 
       '4FW': 'TRP', 
       '4HT': 'TRP', 
       '4IN': 'TRP', 
       '4PH': 'PHE', 
       '5CS': 'CYS', 
       '6CL': 'LYS', 
       '6CW': 'TRP', 
       'A0A': 'ASP', 
       'AA4': 'ALA', 
       'AAR': 'ARG', 
       'AB7': 'GLU', 
       'ABA': 'ALA', 
       'ACB': 'ASP', 
       'ACL': 'ARG', 
       'ACY': 'GLY', 
       'AEI': 'THR', 
       'AFA': 'ASN', 
       'AGM': 'ARG', 
       'AGT': 'CYS', 
       'AHB': 'ASN', 
       'AHO': 'ALA', 
       'AHP': 'ALA', 
       'AIB': 'ALA', 
       'AKL': 'ASP', 
       'ALA': 'ALA', 
       'ALC': 'ALA', 
       'ALG': 'ARG', 
       'ALM': 'ALA', 
       'ALN': 'ALA', 
       'ALO': 'THR', 
       'ALS': 'ALA', 
       'ALT': 'ALA', 
       'ALY': 'LYS', 
       'AME': 'MET', 
       'AP7': 'ALA', 
       'APH': 'ALA', 
       'API': 'LYS', 
       'APK': 'LYS', 
       'AR2': 'ARG', 
       'AR4': 'GLU', 
       'ARG': 'ARG', 
       'ARM': 'ARG', 
       'ARO': 'ARG', 
       'ASA': 'ASP', 
       'ASB': 'ASP', 
       'ASI': 'ASP', 
       'ASK': 'ASP', 
       'ASL': 'ASP', 
       'ASN': 'ASN', 
       'ASP': 'ASP', 
       'AYA': 'ALA', 
       'AYG': 'ALA', 
       'AZK': 'LYS', 
       'B2A': 'ALA', 
       'B2F': 'PHE', 
       'B2I': 'ILE', 
       'B2V': 'VAL', 
       'B3A': 'ALA', 
       'B3D': 'ASP', 
       'B3E': 'GLU', 
       'B3K': 'LYS', 
       'B3S': 'SER', 
       'B3X': 'ASN', 
       'B3Y': 'TYR', 
       'BAL': 'ALA', 
       'BBC': 'CYS', 
       'BCS': 'CYS', 
       'BCX': 'CYS', 
       'BFD': 'ASP', 
       'BG1': 'SER', 
       'BHD': 'ASP', 
       'BIF': 'PHE', 
       'BLE': 'LEU', 
       'BLY': 'LYS', 
       'BMT': 'THR', 
       'BNN': 'ALA', 
       'BOR': 'ARG', 
       'BPE': 'CYS', 
       'BTR': 'TRP', 
       'BUC': 'CYS', 
       'BUG': 'LEU', 
       'C12': 'ALA', 
       'C1X': 'LYS', 
       'C3Y': 'CYS', 
       'C5C': 'CYS', 
       'C6C': 'CYS', 
       'C99': 'ALA', 
       'CAB': 'ALA', 
       'CAF': 'CYS', 
       'CAS': 'CYS', 
       'CCS': 'CYS', 
       'CGU': 'GLU', 
       'CH6': 'ALA', 
       'CH7': 'ALA', 
       'CHG': 'GLY', 
       'CHP': 'GLY', 
       'CHS': 'PHE', 
       'CIR': 'ARG', 
       'CLB': 'ALA', 
       'CLD': 'ALA', 
       'CLE': 'LEU', 
       'CLG': 'LYS', 
       'CLH': 'LYS', 
       'CLV': 'ALA', 
       'CME': 'CYS', 
       'CML': 'CYS', 
       'CMT': 'CYS', 
       'CQR': 'ALA', 
       'CR2': 'ALA', 
       'CR5': 'ALA', 
       'CR7': 'ALA', 
       'CR8': 'ALA', 
       'CRK': 'ALA', 
       'CRO': 'THR', 
       'CRQ': 'TYR', 
       'CRW': 'ALA', 
       'CRX': 'ALA', 
       'CS1': 'CYS', 
       'CS3': 'CYS', 
       'CS4': 'CYS', 
       'CSA': 'CYS', 
       'CSB': 'CYS', 
       'CSD': 'CYS', 
       'CSE': 'CYS', 
       'CSI': 'ALA', 
       'CSO': 'CYS', 
       'CSR': 'CYS', 
       'CSS': 'CYS', 
       'CSU': 'CYS', 
       'CSW': 'CYS', 
       'CSX': 'CYS', 
       'CSY': 'ALA', 
       'CSZ': 'CYS', 
       'CTH': 'THR', 
       'CWR': 'ALA', 
       'CXM': 'MET', 
       'CY0': 'CYS', 
       'CY1': 'CYS', 
       'CY3': 'CYS', 
       'CY4': 'CYS', 
       'CY7': 'CYS', 
       'CYD': 'CYS', 
       'CYF': 'CYS', 
       'CYG': 'CYS', 
       'CYJ': 'LYS', 
       'CYQ': 'CYS', 
       'CYR': 'CYS', 
       'CYS': 'CYS', 
       'CZ2': 'CYS', 
       'CZZ': 'CYS', 
       'DA2': 'ARG', 
       'DAB': 'ALA', 
       'DAH': 'PHE', 
       'DAL': 'ALA', 
       'DAM': 'ALA', 
       'DAR': 'ARG', 
       'DAS': 'ASP', 
       'DBU': 'ALA', 
       'DBY': 'TYR', 
       'DBZ': 'ALA', 
       'DCL': 'LEU', 
       'DCY': 'CYS', 
       'DDE': 'HIS', 
       'DGL': 'GLU', 
       'DGN': 'GLN', 
       'DHA': 'ALA', 
       'DHI': 'HIS', 
       'DHL': 'SER', 
       'DIL': 'ILE', 
       'DIV': 'VAL', 
       'DLE': 'LEU', 
       'DLS': 'LYS', 
       'DLY': 'LYS', 
       'DMH': 'ASN', 
       'DMK': 'ASP', 
       'DNE': 'LEU', 
       'DNG': 'LEU', 
       'DNL': 'LYS', 
       'DNM': 'LEU', 
       'DPH': 'PHE', 
       'DPL': 'PRO', 
       'DPN': 'PHE', 
       'DPP': 'ALA', 
       'DPQ': 'TYR', 
       'DPR': 'PRO', 
       'DSE': 'SER', 
       'DSG': 'ASN', 
       'DSN': 'SER', 
       'DTH': 'THR', 
       'DTR': 'TRP', 
       'DTY': 'TYR', 
       'DVA': 'VAL', 
       'DYG': 'ALA', 
       'DYS': 'CYS', 
       'EFC': 'CYS', 
       'ESB': 'TYR', 
       'ESC': 'MET', 
       'FCL': 'PHE', 
       'FGL': 'ALA', 
       'FGP': 'SER', 
       'FHL': 'LYS', 
       'FLE': 'LEU', 
       'FLT': 'TYR', 
       'FME': 'MET', 
       'FOE': 'CYS', 
       'FOG': 'PHE', 
       'FOR': 'MET', 
       'FRF': 'PHE', 
       'FTR': 'TRP', 
       'FTY': 'TYR', 
       'GHG': 'GLN', 
       'GHP': 'GLY', 
       'GL3': 'GLY', 
       'GLH': 'GLN', 
       'GLN': 'GLN', 
       'GLU': 'GLU', 
       'GLY': 'GLY', 
       'GLZ': 'GLY', 
       'GMA': 'GLU', 
       'GMU': 'ALA', 
       'GPL': 'LYS', 
       'GT9': 'CYS', 
       'GVL': 'SER', 
       'GYC': 'CYS', 
       'GYS': 'GLY', 
       'H5M': 'PRO', 
       'HHK': 'ALA', 
       'HIA': 'HIS', 
       'HIC': 'HIS', 
       'HIP': 'HIS', 
       'HIQ': 'HIS', 
       'HIS': 'HIS', 
       'HLU': 'LEU', 
       'HMF': 'ALA', 
       'HMR': 'ARG', 
       'HPE': 'PHE', 
       'HPH': 'PHE', 
       'HPQ': 'PHE', 
       'HRG': 'ARG', 
       'HSE': 'SER', 
       'HSL': 'SER', 
       'HSO': 'HIS', 
       'HTI': 'CYS', 
       'HTR': 'TRP', 
       'HY3': 'PRO', 
       'HYP': 'PRO', 
       'IAM': 'ALA', 
       'IAS': 'ASP', 
       'IGL': 'ALA', 
       'IIL': 'ILE', 
       'ILE': 'ILE', 
       'ILG': 'GLU', 
       'ILX': 'ILE', 
       'IML': 'ILE', 
       'IPG': 'GLY', 
       'IT1': 'LYS', 
       'IYR': 'TYR', 
       'KCX': 'LYS', 
       'KGC': 'LYS', 
       'KOR': 'CYS', 
       'KST': 'LYS', 
       'KYN': 'ALA', 
       'LA2': 'LYS', 
       'LAL': 'ALA', 
       'LCK': 'LYS', 
       'LCX': 'LYS', 
       'LDH': 'LYS', 
       'LED': 'LEU', 
       'LEF': 'LEU', 
       'LET': 'LYS', 
       'LEU': 'LEU', 
       'LLP': 'LYS', 
       'LLY': 'LYS', 
       'LME': 'GLU', 
       'LNT': 'LEU', 
       'LPD': 'PRO', 
       'LSO': 'LYS', 
       'LYM': 'LYS', 
       'LYN': 'LYS', 
       'LYP': 'LYS', 
       'LYR': 'LYS', 
       'LYS': 'LYS', 
       'LYX': 'LYS', 
       'LYZ': 'LYS', 
       'M0H': 'CYS', 
       'M2L': 'LYS', 
       'M3L': 'LYS', 
       'MAA': 'ALA', 
       'MAI': 'ARG', 
       'MBQ': 'TYR', 
       'MC1': 'SER', 
       'MCL': 'LYS', 
       'MCS': 'CYS', 
       'MDO': 'ALA', 
       'MEA': 'PHE', 
       'MEG': 'GLU', 
       'MEN': 'ASN', 
       'MET': 'MET', 
       'MEU': 'GLY', 
       'MFC': 'ALA', 
       'MGG': 'ARG', 
       'MGN': 'GLN', 
       'MHL': 'LEU', 
       'MHO': 'MET', 
       'MHS': 'HIS', 
       'MIS': 'SER', 
       'MLE': 'LEU', 
       'MLL': 'LEU', 
       'MLY': 'LYS', 
       'MLZ': 'LYS', 
       'MME': 'MET', 
       'MNL': 'LEU', 
       'MNV': 'VAL', 
       'MPQ': 'GLY', 
       'MSA': 'GLY', 
       'MSE': 'MET', 
       'MSO': 'MET', 
       'MTY': 'PHE', 
       'MVA': 'VAL', 
       'N10': 'SER', 
       'NAL': 'ALA', 
       'NAM': 'ALA', 
       'NBQ': 'TYR', 
       'NC1': 'SER', 
       'NCB': 'ALA', 
       'NEP': 'HIS', 
       'NFA': 'PHE', 
       'NIY': 'TYR', 
       'NLE': 'LEU', 
       'NLN': 'LEU', 
       'NLO': 'LEU', 
       'NMC': 'GLY', 
       'NMM': 'ARG', 
       'NPH': 'CYS', 
       'NRQ': 'ALA', 
       'NVA': 'VAL', 
       'NYC': 'ALA', 
       'NYS': 'CYS', 
       'NZH': 'HIS', 
       'OAS': 'SER', 
       'OBS': 'LYS', 
       'OCS': 'CYS', 
       'OCY': 'CYS', 
       'OHI': 'HIS', 
       'OHS': 'ASP', 
       'OLT': 'THR', 
       'OMT': 'MET', 
       'OPR': 'ARG', 
       'ORN': 'ALA', 
       'ORQ': 'ARG', 
       'OSE': 'SER', 
       'OTY': 'TYR', 
       'OXX': 'ASP', 
       'P1L': 'CYS', 
       'P2Y': 'PRO', 
       'PAQ': 'TYR', 
       'PAT': 'TRP', 
       'PBB': 'CYS', 
       'PBF': 'PHE', 
       'PCA': 'PRO', 
       'PCS': 'PHE', 
       'PEC': 'CYS', 
       'PF5': 'PHE', 
       'PFF': 'PHE', 
       'PG1': 'SER', 
       'PG9': 'GLY', 
       'PHA': 'PHE', 
       'PHD': 'ASP', 
       'PHE': 'PHE', 
       'PHI': 'PHE', 
       'PHL': 'PHE', 
       'PHM': 'PHE', 
       'PIA': 'ALA', 
       'PLE': 'LEU', 
       'PM3': 'PHE', 
       'POM': 'PRO', 
       'PPH': 'LEU', 
       'PPN': 'PHE', 
       'PR3': 'CYS', 
       'PRO': 'PRO', 
       'PRQ': 'PHE', 
       'PRR': 'ALA', 
       'PRS': 'PRO', 
       'PSA': 'PHE', 
       'PSH': 'HIS', 
       'PTH': 'TYR', 
       'PTM': 'TYR', 
       'PTR': 'TYR', 
       'PYA': 'ALA', 
       'PYC': 'ALA', 
       'PYR': 'SER', 
       'PYT': 'ALA', 
       'PYX': 'CYS', 
       'R1A': 'CYS', 
       'R1B': 'CYS', 
       'R1F': 'CYS', 
       'R7A': 'CYS', 
       'RC7': 'ALA', 
       'RCY': 'CYS', 
       'S1H': 'SER', 
       'SAC': 'SER', 
       'SAH': 'CYS', 
       'SAR': 'GLY', 
       'SBD': 'SER', 
       'SBG': 'SER', 
       'SBL': 'SER', 
       'SC2': 'CYS', 
       'SCH': 'CYS', 
       'SCS': 'CYS', 
       'SCY': 'CYS', 
       'SDP': 'SER', 
       'SEB': 'SER', 
       'SEC': 'ALA', 
       'SEL': 'SER', 
       'SEP': 'SER', 
       'SER': 'SER', 
       'SET': 'SER', 
       'SGB': 'SER', 
       'SGR': 'SER', 
       'SHC': 'CYS', 
       'SHP': 'GLY', 
       'SIC': 'ALA', 
       'SLZ': 'LYS', 
       'SMC': 'CYS', 
       'SME': 'MET', 
       'SMF': 'PHE', 
       'SNC': 'CYS', 
       'SNN': 'ASP', 
       'SOC': 'CYS', 
       'SOY': 'SER', 
       'SUI': 'ALA', 
       'SUN': 'SER', 
       'SVA': 'SER', 
       'SVV': 'SER', 
       'SVX': 'SER', 
       'SVY': 'SER', 
       'SVZ': 'SER', 
       'SXE': 'SER', 
       'TBG': 'GLY', 
       'TBM': 'THR', 
       'TCQ': 'TYR', 
       'TEE': 'CYS', 
       'TH5': 'THR', 
       'THC': 'THR', 
       'THR': 'THR', 
       'TIH': 'ALA', 
       'TMD': 'THR', 
       'TNB': 'CYS', 
       'TOX': 'TRP', 
       'TPL': 'TRP', 
       'TPO': 'THR', 
       'TPQ': 'ALA', 
       'TQQ': 'TRP', 
       'TRF': 'TRP', 
       'TRN': 'TRP', 
       'TRO': 'TRP', 
       'TRP': 'TRP', 
       'TRQ': 'TRP', 
       'TRW': 'TRP', 
       'TRX': 'TRP', 
       'TTQ': 'TRP', 
       'TTS': 'TYR', 
       'TY2': 'TYR', 
       'TY3': 'TYR', 
       'TYB': 'TYR', 
       'TYC': 'TYR', 
       'TYI': 'TYR', 
       'TYN': 'TYR', 
       'TYO': 'TYR', 
       'TYQ': 'TYR', 
       'TYR': 'TYR', 
       'TYS': 'TYR', 
       'TYT': 'TYR', 
       'TYX': 'CYS', 
       'TYY': 'TYR', 
       'TYZ': 'ARG', 
       'UMA': 'ALA', 
       'VAD': 'VAL', 
       'VAF': 'VAL', 
       'VAL': 'VAL', 
       'VDL': 'VAL', 
       'VLL': 'VAL', 
       'HSD': 'HIS', 
       'VME': 'VAL', 
       'X9Q': 'ALA', 
       'XX1': 'LYS', 
       'XXY': 'ALA', 
       'XYG': 'ALA', 
       'YCM': 'CYS', 
       'YOF': 'TYR'}
    nonstandard = modres.keys()