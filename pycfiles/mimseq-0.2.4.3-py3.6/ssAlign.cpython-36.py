# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimseq/ssAlign.py
# Compiled at: 2020-03-18 10:50:45
# Size of source mod 2**32: 11172 bytes
import subprocess, os, re
from Bio import AlignIO
from Bio.Alphabet import generic_rna
from collections import defaultdict, Counter
from itertools import groupby
from operator import itemgetter
stkname = ''

def aligntRNA(tRNAseqs, out):
    global stkname
    stkname = tRNAseqs.split('.fa')[0] + '_align.stk'
    cmfile = os.path.dirname(os.path.realpath(__file__)) + '/data/tRNAmatureseq.cm'
    cmcommand = ['cmalign', '-o', stkname, '--nonbanded', '-g', cmfile, tRNAseqs]
    subprocess.check_call(cmcommand, stdout=(open(out + 'cm.log', 'w')))


def extraCCA():
    extra_cca = list()
    stk = AlignIO.read(stkname, 'stockholm', alphabet=generic_rna)
    for record in stk:
        if record.seq[-3:] == 'cca':
            extra_cca.append(record.name)

    os.remove(stkname)
    return extra_cca


def tRNAclassifier(out):
    struct_dict = structureParser()
    stk = AlignIO.read(stkname, 'stockholm', alphabet=generic_rna)
    ss_cons = ''.join([line.split()[(-1)] for line in open(stkname) if line.startswith('#=GC SS_cons')])
    cons_pos = 0
    cons_pos_list = list()
    cons_pos_dict = defaultdict()
    openstem_count = 0
    closestem_count = 0
    for pos, char in enumerate(ss_cons):
        if not ss_cons[pos] == '.':
            if cons_pos < 46:
                if not cons_pos == 17:
                    if not cons_pos == 20:
                        cons_pos_list.append(str(cons_pos))
                        cons_pos_dict[pos + 1] = str(cons_pos)
                        cons_pos += 1
                    elif cons_pos == 17 and '17' not in cons_pos_list:
                        cons_pos_dict[pos + 1] = '17'
                        cons_pos_list.append('17')
                    else:
                        if cons_pos == 17 and '17' in cons_pos_list:
                            cons_pos_dict[pos + 1] = '17a'
                            cons_pos_list.append('17a')
                            cons_pos += 1
                        elif cons_pos == 20:
                            if '20' not in cons_pos_list:
                                cons_pos_dict[pos + 1] = '20'
                                cons_pos_list.append('20')
                            else:
                                if '20a' not in cons_pos_list:
                                    cons_pos_dict[pos + 1] = '20a'
                                    cons_pos_list.append('20a')
                                elif '20b' not in cons_pos_list:
                                    pass
                                cons_pos_dict[pos + 1] = '20b'
                                cons_pos_list.append('20b')
                                cons_pos += 1
                else:
                    if cons_pos == 46:
                        if not closestem_count == openstem_count or closestem_count == 0 or openstem_count == 0:
                            if ss_cons[pos] == '<':
                                openstem_count += 1
                                cons_pos_dict[pos + 1] = 'e'
                                cons_pos_list.append('e')
                            else:
                                if ss_cons[pos] == '>':
                                    closestem_count += 1
                                    cons_pos_dict[pos + 1] = 'e'
                                    cons_pos_list.append('e')
                                else:
                                    if ss_cons[pos] == '_':
                                        cons_pos_dict[pos + 1] = 'e'
                                        cons_pos_list.append('e')
                        else:
                            if closestem_count == openstem_count and (not closestem_count == 0 or not openstem_count == 0):
                                cons_pos_dict[pos + 1] = str(cons_pos)
                                cons_pos_list.append(str(cons_pos))
                                cons_pos += 1
                    elif cons_pos > 46:
                        cons_pos_dict[pos + 1] = str(cons_pos)
                        cons_pos_list.append(str(cons_pos))
                        cons_pos += 1
            elif ss_cons[pos] == '.':
                cons_pos_dict[pos + 1] = '-'
                cons_pos_list.append('-')

    cons_pos_list = '_'.join(cons_pos_list)
    tRNA_struct = defaultdict(dict)
    tRNA_ungap2canon = defaultdict(dict)
    for record in stk:
        tRNA = record.id
        seq = record.seq
        ungapped_pos = 0
        bases = ['A', 'C', 'G', 'U']
        for i, letter in enumerate(seq, 1):
            if letter.upper() in bases:
                tRNA_ungap2canon[tRNA][ungapped_pos] = cons_pos_dict[i]
                ungapped_pos += 1
                tRNA_struct[tRNA][i] = struct_dict[i]
            else:
                tRNA_struct[tRNA][i] = 'gap'

    return (
     tRNA_struct, tRNA_ungap2canon, cons_pos_list, cons_pos_dict)


def tRNAclassifier_nogaps():
    struct_dict = structureParser()
    tRNA_struct = defaultdict(dict)
    stk = AlignIO.read(stkname, 'stockholm', alphabet=generic_rna)
    for record in stk:
        tRNA = record.id
        seq = record.seq
        pos = 0
        bases = ['A', 'C', 'G', 'U']
        for i, letter in enumerate(seq):
            if letter.upper() in bases:
                tRNA_struct[tRNA][pos] = struct_dict[(i + 1)]
                pos += 1

    return tRNA_struct


def getAnticodon():
    anticodon = list()
    rf_cons = ''.join([line.split()[(-1)] for line in open(stkname) if line.startswith('#=GC RF')])
    for pos, char in enumerate(rf_cons):
        if char == '*':
            anticodon.append(pos)

    return anticodon


def getAnticodon_1base():
    anticodon = list()
    rf_cons = ''.join([line.split()[(-1)] for line in open(stkname) if line.startswith('#=GC RF')])
    for pos, char in enumerate(rf_cons, 1):
        if char == '*':
            anticodon.append(pos)

    return anticodon


def clusterAnticodon(cons_anticodon, cluster):
    bases = [
     'A', 'C', 'G', 'U']
    stk = AlignIO.read(stkname, 'stockholm', alphabet=generic_rna)
    cluster_anticodon = list()
    for record in stk:
        if record.id == cluster:
            for pos in cons_anticodon:
                gapcount = 0
                for char in record.seq[:pos]:
                    if char.upper() not in bases:
                        gapcount += 1

                cluster_anticodon.append(pos - gapcount)

    return cluster_anticodon


def modContext(out):
    tRNA_struct, tRNA_ungap2canon, cons_pos_list, cons_pos_dict = tRNAclassifier(out)
    anticodon = getAnticodon_1base()
    sites_dict = defaultdict()
    mod_sites = ['9', '20', '26', '32', '34', '37', '58']
    for mod in mod_sites:
        sites_dict[mod] = list(cons_pos_dict.keys())[list(cons_pos_dict.values()).index(mod)]

    upstream_dict = defaultdict(lambda : defaultdict(list))
    stk = AlignIO.read(stkname, 'stockholm', alphabet=generic_rna)
    for record in stk:
        gene = record.id
        seq = record.seq
        for site in sites_dict.keys():
            pos = sites_dict[site]
            identity = seq[(pos - 1)]
            if identity in ('A', 'C', 'G', 'U', 'T'):
                up = pos - 2
                down = pos
                while seq[up].upper() not in ('A', 'C', 'G', 'U', 'T'):
                    up -= 1

                while seq[down].upper() not in ('A', 'C', 'G', 'U', 'T'):
                    down += 1

                upstream_dict[gene][pos].append(identity)
                upstream_dict[gene][pos].append(seq[up])
                upstream_dict[gene][pos].append(seq[down])

    try:
        os.mkdir(out + 'mods')
    except FileExistsError:
        pass

    with open(out + 'mods/modContext.txt', 'w') as (outfile):
        outfile.write('cluster\tpos\tidentity\tupstream\tdownstream\n')
        for cluster, data in upstream_dict.items():
            for pos, base in data.items():
                outfile.write(cluster + '\t' + str(pos) + '\t' + base[0] + '\t' + base[1] + '\t' + base[2] + '\n')

    mod_sites = str('_'.join(str(e) for e in mod_sites))
    return (
     mod_sites, cons_pos_list, cons_pos_dict)


def structureParser():
    struct_dict = dict()
    ss_cons = ''.join([line.split()[(-1)] for line in open(stkname) if line.startswith('#=GC SS_cons')])
    acc = defaultdict()
    term = defaultdict()
    term_type = "5'"
    bulges = defaultdict()
    bulge_list = []
    bulge_items = []
    bulge_count = 0
    stemloops = defaultdict()
    stemloops_count = 0
    stemloops_type = ['D stem-loop', 'Anticodon stem-loop', 'Variable loop', 'T stem-loop']
    open_count = 0
    close_count = 0
    for pos, char in enumerate(ss_cons):
        if char == ':':
            if pos < 10:
                term[pos + 1] = term_type
            else:
                term_type = "3'"
                term[pos + 1] = term_type
            if char == '(':
                acc[pos + 1] = "Acceptor stem 5'"
            if char == ')':
                acc[pos + 1] = "Acceptor stem 3'"
            if char == '<':
                open_count += 1
                stemloops[pos + 1] = stemloops_type[stemloops_count]
            if char == '>':
                close_count += 1
                stemloops[pos + 1] = stemloops_type[stemloops_count]
                if close_count == open_count:
                    stemloops_count += 1
                    open_count = 0
                    close_count = 0

    for i in ("Acceptor stem 5'", "Acceptor stem 3'"):
        pos_list = [k for k, v in acc.items() if v == i]
        start = min(pos_list)
        stop = max(pos_list)
        acc.update([(n, i) for n in range(start, stop + 1)])

    for i in stemloops_type:
        pos_list = [k for k, v in stemloops.items() if v == i]
        start = min(pos_list)
        stop = max(pos_list)
        stemloops.update([(n, i) for n in range(start, stop + 1)])

    struct_dict = {**term, **acc}
    struct_dict.update(stemloops)
    for pos, char in enumerate(ss_cons):
        if pos + 1 not in [x for x in struct_dict.keys()]:
            bulge_list.append(pos + 1)

    for k, g in groupby(enumerate(bulge_list), lambda x: x[0] - x[1]):
        group = map(itemgetter(1), g)
        group = list(map(int, group))
        bulge_items.append(group)

    for bulge in bulge_items:
        bulge_count += 1
        if bulge_count == 3 or bulge_count == 4:
            for pos in bulge:
                struct_dict[pos] = 'Variable loop'

        else:
            if bulge_count == 5:
                for pos in bulge:
                    struct_dict[pos] = 'bulge3'

            else:
                for pos in bulge:
                    struct_dict[pos] = 'bulge' + str(bulge_count)

    return struct_dict