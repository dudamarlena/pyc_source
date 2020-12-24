# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/BioClients/uniprot/Utils.py
# Compiled at: 2020-03-06 16:37:18
# Size of source mod 2**32: 1673 bytes
import sys, os, re, logging
from ..util import rest_utils

def GetData(base_uri, uids, ofmt, fout):
    """Need to handle xml, rdf better (merge)."""
    n_prot = 0
    n_err = 0
    for uid in uids:
        rval = rest_utils.GetURL(base_uri + '/%s.%s' % (uid, ofmt))
        if not rval:
            n_err += 1
        else:
            if ofmt == 'tab':
                lines = []
                for line in rval.splitlines():
                    vals = re.split('\\t', line)
                    lines.append('\t'.join(vals))
                else:
                    for i, line in enumerate(lines):
                        if n_prot > 0 and i == 0:
                            pass
                        else:
                            fout.write(line + '\n')

            else:
                fout.write(rval + '\n')
            n_prot += 1
    else:
        logging.info('n_in: %d; n_prot: %d; n_err: %d' % (len(uids), n_prot, n_err))


def UIDs2JSON(base_uri, uids, fout):
    """ Uses uniprot library from Bosco Ho (https://github.com/boscoh/uniprot)."""
    import uniprot
    uniprot_data = uniprot.batch_uniprot_metadata(uids, None)
    for uid in uniprot_data.keys():
        for key in uniprot_data[uid].keys():
            if key in ('accs', 'sequence', 'go', 'description'):
                del uniprot_data[uid][key]
        else:
            json_txt = json.dumps(uniprot_data, sort_keys=True, indent=2)
            fout.write(json_txt + '\n')