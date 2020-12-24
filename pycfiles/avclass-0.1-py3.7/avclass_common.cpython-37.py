# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/avclass/avclass_common.py
# Compiled at: 2019-11-13 15:43:45
# Size of source mod 2**32: 9992 bytes
"""
Main AVClass class
"""
import os, re, string
from collections import OrderedDict as OrdDict
from collections import namedtuple
from operator import itemgetter, attrgetter
package_dir = os.path.dirname(__file__)
default_alias_file = os.path.join(package_dir, 'data/default.aliases')
default_gen_file = os.path.join(package_dir, 'data/default.generics')
SampleInfo = namedtuple('SampleInfo', [
 'md5', 'sha1', 'sha256', 'labels'])

class AvLabels:
    __doc__ = '\n    Class to operate on AV labels, \n    such as extracting the most likely family name.\n    '

    def __init__(self, gen_file=None, alias_file=None, av_file=None):
        self.gen_set = self.read_generics(gen_file) if gen_file else self.read_generics(default_gen_file)
        self.aliases_map = self.read_aliases(alias_file) if alias_file else self.read_aliases(default_alias_file)
        self.avs = self.read_avs(av_file) if av_file else None

    @staticmethod
    def read_aliases(alfile):
        """Read aliases map from given file"""
        if alfile is None:
            return {}
        almap = {}
        with open(alfile, 'r') as (fd):
            for line in fd:
                alias, token = line.strip().split()[0:2]
                almap[alias] = token

        return almap

    @staticmethod
    def read_generics(generics_file):
        """Read generic token set from given file"""
        gen_set = set()
        with open(generics_file) as (gen_fd):
            for line in gen_fd:
                if not line.startswith('#'):
                    if line == '\n':
                        continue
                    gen_set.add(line.strip())

        return gen_set

    @staticmethod
    def read_avs(avs_file):
        """Read AV engine set from given file"""
        with open(avs_file) as (fd):
            avs = set(map(str.strip, fd.readlines()))
        return avs

    @staticmethod
    def get_sample_info(vt_rep, from_vt):
        """Parse and extract sample information from JSON line
           Returns a SampleInfo named tuple: md5, sha1, sha256, label_pairs 
        """
        label_pairs = []
        if from_vt:
            try:
                scans = vt_rep['scans']
            except KeyError:
                return
            else:
                for av, res in scans.items():
                    if res['detected']:
                        label = res['result']
                        clean_label = ''.join((c for c in label if c in string.printable))
                        label_pairs.append((av, clean_label))

        else:
            label_pairs = vt_rep['av_labels']
        return SampleInfo(vt_rep['md5'], vt_rep['sha1'], vt_rep['sha256'], label_pairs)

    @staticmethod
    def is_pup(av_label_pairs):
        """This function classifies the sample as PUP or not 
           using the AV labels as explained in the paper:
           "Certified PUP: Abuse in Authenticode Code Signing" 
           (ACM CCS 2015)
           It uses the AV labels of 11 specific AVs. 
           The function checks for 13 keywords used to indicate PUP.
           Return:
              True/False/None
        """
        if not av_label_pairs:
            return
        pup = False
        threshold = 0.5
        av_set = set(['Malwarebytes', 'K7AntiVirus', 'Avast',
         'AhnLab-V3', 'Kaspersky', 'K7GW', 'Ikarus',
         'Fortinet', 'Antiy-AVL', 'Agnitum', 'ESET-NOD32'])
        tags = set(['PUA', 'Adware', 'PUP', 'Unwanted', 'Riskware', 'grayware',
         'Unwnt', 'Adknowledge', 'toolbar', 'casino', 'casonline',
         'AdLoad', 'not-a-virus'])
        bool_set = set([(pair[0], t.lower() in pair[1].lower()) for t in tags if pair[0] in av_set for pair in av_label_pairs])
        av_detected = len([p[0] for p in av_label_pairs if p[0] in av_set])
        av_pup = map(lambda x: x[1], bool_set).count(True)
        if float(av_pup) >= float(av_detected) * threshold:
            if av_pup != 0:
                pup = True
        return pup

    @staticmethod
    def __remove_suffixes(av_name, label):
        """Remove AV specific suffixes from given label
           Returns updated label"""
        if av_name in set(['Norman', 'Avast', 'Avira', 'Kaspersky',
         'ESET-NOD32', 'Fortinet', 'Jiangmin', 'Comodo',
         'GData', 'Avast', 'Sophos',
         'TrendMicro-HouseCall', 'TrendMicro',
         'NANO-Antivirus', 'Microsoft']):
            label = label.rsplit('.', 1)[0]
        if av_name == 'AVG':
            tokens = label.rsplit('.', 1)
            if len(tokens) > 1:
                if re.match('^[A-Z0-9]+$', tokens[1]):
                    label = tokens[0]
        if av_name in set(['Agnitum', 'McAffee', 'McAffee-GW-Edition']):
            label = label.rsplit('!', 1)[0]
        if av_name in set(['K7AntiVirus', 'K7GW']):
            label = label.rsplit('(', 1)[0]
        if av_name in set(['Ad-Aware', 'BitDefender', 'Emsisoft', 'F-Secure',
         'Microworld-eScan']):
            label = label.rsplit('(', 1)[0]
        return label

    def __normalize(self, label, hashes):
        """Tokenize label, filter tokens, and replace aliases"""
        if not label:
            return []
        ret = []
        for token in re.split('[^0-9a-zA-Z]', label):
            token = token.lower()
            end_len = len(re.findall('\\d*$', token)[0])
            if end_len:
                token = token[:-end_len]
            if len(token) < 4:
                continue
            if token in self.gen_set:
                continue
            hash_token = False
            for hash_str in hashes:
                if hash_str[0:len(token)] == token:
                    hash_token = True
                    break

            if hash_token:
                continue
            token = self.aliases_map[token] if token in self.aliases_map else token
            ret.append(token)

        return ret

    def get_family_ranking(self, sample_info):
        """
        Returns sorted dictionary of most likely family names for sample
        """
        av_label_pairs = sample_info[3]
        hashes = [sample_info[0], sample_info[1], sample_info[2]]
        av_whitelist = self.avs
        labels_seen = set()
        token_map = {}
        for av_name, label in av_label_pairs:
            if not label:
                continue
            else:
                if av_whitelist:
                    if av_name not in av_whitelist:
                        continue
                if label.endswith(' (B)'):
                    label = label[:-4]
                if label in labels_seen:
                    continue
                else:
                    labels_seen.add(label)
            label = self._AvLabels__remove_suffixes(av_name, label)
            tokens = self._AvLabels__normalize(label, hashes)
            for t in tokens:
                c = token_map[t] if t in token_map else 0
                token_map[t] = c + 1

        sorted_tokens = sorted((token_map.items()), key=(itemgetter(1, 0)),
          reverse=True)
        sorted_dict = OrdDict()
        for t, c in sorted_tokens:
            if c > 1:
                sorted_dict[t] = c
            else:
                break

        return sorted_dict