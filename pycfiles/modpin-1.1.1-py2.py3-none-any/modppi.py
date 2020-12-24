# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/scripts/modppi.py
# Compiled at: 2020-04-28 10:16:58
import sys, argparse, os, re
from Bio import SeqIO as SeqIE
from Bio import ExPASy
from Bio.Seq import Seq
from Bio import SeqRecord
from Bio.Alphabet import IUPAC
import ConfigParser, itertools, shutil, subprocess, time, random
src_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(src_path)
config = ConfigParser.ConfigParser()
config_file = os.path.join(src_path, 'config.ini')
config.read(config_file)
src_path = os.path.join(config.get('Paths', 'modppi_path'), config.get('Paths', 'sbi_library_path'))
sys.path.append(src_path)
src_path = os.path.join(config.get('Paths', 'modppi_path'), config.get('Paths', 'functions_path'))
sys.path.append(src_path)
from SeqIO import *
from functions import *
from SBI.external.blast import blast_parser
from SBI.structure.contacts import Complex
from SBI.sequence import Sequence
from SBI.structure import PDB

class ModelException(Exception):
    pass


def main():
    start_time = time.time()
    options = parse_user_arguments()
    verbose = options.show
    clean = options.clean
    dummy_dir = options.dummy_dir
    output_dir = options.outdir
    renumerate = options.renumerate
    queriesA, queriesB, all_edges, user_defined_edges = parse_inputs(options)
    queriesA_original = queriesA
    queriesB_original = queriesB
    start_time_init = time.time()
    for user_edge in user_defined_edges:
        current_query_A = {}
        current_query_B = {}
        if not queriesA.has_key(user_edge[0]) or not queriesB.has_key(user_edge[1]):
            continue
        current_query_A.setdefault(user_edge[0], queriesA[user_edge[0]])
        current_query_B.setdefault(user_edge[1], queriesB[user_edge[1]])
        hit_items_A, hit_items_B = do_blast(options, current_query_A, current_query_B)
        sections_modeled = {}
        remaining_sections_A = {}
        remaining_sections_B = {}
        for hit_A in hit_items_A:
            for hit_B in hit_items_B:
                if user_edge != (hit_A[0], hit_B[0]) and user_edge != (hit_B[0], hit_A[0]):
                    continue
                if (
                 hit_A[1], hit_B[1]) not in all_edges and (hit_B[1], hit_A[1]) not in all_edges:
                    continue
                start_time_model = time.time()
                try:
                    sections_modeled, remaining_sections_A, remaining_sections_B = modelling(queriesA_original, queriesB_original, queriesA, queriesB, hit_A, hit_B, sections_modeled, remaining_sections_A, remaining_sections_B, options)
                except ModelException:
                    continue

                if verbose:
                    sys.stdout.write('\t\t\tTotal time on model %s (template %s): %f seconds\n' % (user_edge[0] + '::' + user_edge[1], hit_A[1][:-2], time.time() - start_time_model))

        if not sections_modeled:
            has_modeled = False
        else:
            has_modeled = True
        sys.stdout.write('\t\tAccumulated time on main modelling of %s: %d seconds\n' % (user_edge[0] + '::' + user_edge[1], time.time() - start_time_init))
        start_time_remain = time.time()
        while remaining_sections_A or remaining_sections_B:
            queriesA_remaining = remaining_sections_A
            queriesB_remaining = remaining_sections_B
            hit_items_A, hit_items_B = do_blast(options, queriesA_remaining, queriesB_remaining)
            sections_modeled = {}
            remaining_sections_A = {}
            remaining_sections_B = {}
            for hit_A in hit_items_A:
                for hit_B in hit_items_B:
                    if user_edge != (hit_A[0], hit_B[0]) and user_edge != (hit_B[0], hit_A[0]):
                        continue
                    if (
                     hit_A[1], hit_B[1]) not in all_edges and (hit_B[1], hit_A[1]) not in all_edges:
                        continue
                    start_time_model = time.time()
                    try:
                        sections_modeled, remaining_sections_A, remaining_sections_B = modelling(queriesA_original, queriesB_original, queriesA_remaining, queriesB_remaining, hit_A, hit_B, sections_modeled, remaining_sections_A, remaining_sections_B, options)
                    except ModelException:
                        continue

                    if verbose:
                        sys.stdout.write('\t\t\tTotal time on model %s (template %s): %f seconds\n' % (user_edge[0] + '::' + user_edge[1], hit_A[1][:-2], time.time() - start_time_model))

        sys.stdout.write('\t\tAccumulated time on secondary regions modelling of %s: %d seconds\n' % (user_edge[0] + '::' + user_edge[1], time.time() - start_time_remain))
        with open(os.path.join(options.outdir, 'interactions_done.list'), 'a+') as (interactions_done_file):
            if not re.search('\\b%s\t%s\\b' % (user_edge[0], user_edge[1]), interactions_done_file.read()):
                if has_modeled:
                    interactions_done_file.write('%s\t%s\tDONE\t%s\n' % (user_edge[0], user_edge[1], os.path.abspath(os.path.join(options.outdir, user_edge[0] + '::' + user_edge[1], user_edge[0] + '::' + user_edge[1] + '.list'))))
                else:
                    interactions_done_file.write('%s\t%s\tFAILED\n' % (user_edge[0], user_edge[1]))
            elif has_modeled:
                interactions_done_file.write('%s\t%s\tFIXED\t%s\n' % (user_edge[0], user_edge[1], os.path.abspath(os.path.join(options.outdir, user_edge[0] + '::' + user_edge[1], user_edge[0] + '::' + user_edge[1] + '.list'))))

    if not verbose:
        shutil.rmtree(dummy_dir)
    if verbose and clean:
        sys.stdout.write('Cleaning folder %s\n' % dummy_dir)
        shutil.rmtree(dummy_dir)
    sys.stdout.write('Total elapsed time: %d seconds\n' % (time.time() - start_time))


def parse_user_arguments(*args, **kwds):
    parser = argparse.ArgumentParser(description='Automatic modelling of protein-protein interactions', epilog="@Oliva's lab 2016")
    parser.add_argument('-seq', '--query', dest='query_file', action='store', help='Input file with a list of FASTA sequences of the proteins to test')
    parser.add_argument('-ppi', '--interactions', dest='interactions_file', action='store', help='Input file with a list of the interactions to test')
    parser.add_argument('-o', '--output_directory', dest='outdir', action='store', default='ModPPI_models', help='Output directory (default is ModPPI_models)')
    parser.add_argument('-n', '--number_of_models', dest='nmodels', action='store', default=1, type=int, help='Number of models for each template (default is 1)')
    parser.add_argument('-d', '--dummy_dir', dest='dummy_dir', action='store', default='/tmp/modppi_dummy', help='Specifies the location of the dummy folder (default is /tmp/modppi_dummy)')
    parser.add_argument('-opt', '--optimize', dest='optimize', action='store_true', help='Flag to allow model optimization (default is False)')
    parser.add_argument('-3did', '--use_domain_interactions', dest='did', action='store_true', help='Flag to include domain-domain interactions from 3DiD (default is False)')
    parser.add_argument('-init_pdb', '--initialize_PDB_dataset', dest='init_pdb', action='store_true', help='Flag to force initialization of dataset from PDB (default is False)')
    parser.add_argument('-init_3did', '--initialize_3did_dataset', dest='init_3did', action='store_true', help='Flag to force initialization of dataset from 3DiD (default is False)')
    parser.add_argument('-init_blast', '--initialize_blast_dataset', dest='init_blast', action='store_true', help='Flag to force formatting the sequence dataset for BLAST (default is False)')
    parser.add_argument('-skip', '--skip_protein_check', dest='skip_check', action='store_true', help='Flag to skip the check of the sequence dataset and fasten up the modeling (default is False)')
    parser.add_argument('-hydro', '--hydrogens', dest='hbplus', action='store_true', help='Flag to include hydrogens (default is False)')
    parser.add_argument('-force', '--force', dest='force', action='store_true', help='Flag to force the modelling even if the model already exist (default is False)')
    parser.add_argument('-clean', '--force_clean_dummy', dest='clean', action='store_true', help='Flag to force removing the dummy files (default is False)')
    parser.add_argument('-r', '--renumerate', dest='renumerate', action='store_true', help='Flag to renumber the sequences as in the original FastA (default is False)')
    parser.add_argument('-v', '--verbose', dest='show', action='store_true', help='Flag for verbose mode (default is False)')
    options = parser.parse_args()
    return options


def parse_inputs(options):
    verbose = options.show
    output_dir = options.outdir
    dummy_dir = options.dummy_dir
    init_pdb = options.init_pdb
    init_3did = options.init_3did
    init_blast = options.init_blast
    skip_check = options.skip_check
    make_database = init_pdb or init_3did or init_blast
    src_path = config.get('Paths', 'modppi_path')
    blast_path = config.get('Paths', 'blast_path')
    blast_dir = os.path.join(src_path, config.get('Paths', 'blast_dir'))
    queriesA = {}
    queriesB = {}
    if not os.path.exists(output_dir) and fileExist(options.interactions_file) and fileExist(options.query_file):
        os.makedirs(output_dir)
    if not os.path.exists(blast_dir):
        os.makedirs(blast_dir)
    if not os.path.exists(dummy_dir):
        os.makedirs(dummy_dir)
    if init_pdb or init_3did or init_blast:
        skip_check = False
    if not skip_check:
        proteins = {}
        protein_names = set()
        fasta_list_file = os.path.join(src_path, config.get('Files', 'fasta_list_file'))
        if fileExist(fasta_list_file):
            if verbose:
                sys.stdout.write('\t\t-- Reading protein sequences...\n')
            for protein in FASTA_iterator(fasta_list_file):
                name = protein.get_identifier()
                seq = protein.get_sequence()
                if len(seq) > 0:
                    try:
                        proteins.setdefault(name, ProteinSequence(name, seq))
                        protein_names.add(name)
                    except IncorrectSequenceLetter as e:
                        sys.stderr.write('WARNING: %s\n' % e)
                        sys.stdout.write('\t\t-- Skip input sequence: %s Sequence: %s\n' % (name, seq))

        else:
            sys.stderr.write('EXIT: Missing NR sequence list file %s\n' % fasta_list_file)
            exit(0)
        nr90_names = set()
        nr90_list_file = os.path.join(src_path, config.get('Files', 'nr90_list_file'))
        if fileExist(nr90_list_file):
            if verbose:
                sys.stdout.write('\t\t-- Reading non-redundant sequences...\n')
            for protein in FASTA_iterator(nr90_list_file):
                name = protein.get_identifier()
                seq = protein.get_sequence()
                if len(seq) > 0:
                    try:
                        proteins.setdefault(name, ProteinSequence(name, seq))
                        nr90_names.add(name)
                    except IncorrectSequenceLetter as e:
                        if verbose:
                            sys.stderr.write('WARNING: %s\n' % e)
                        if verbose:
                            sys.stdout.write('\t\t-- Skip input sequence: %s Sequence: %s\n' % (name, seq))

        else:
            sys.stderr.write('EXIT: Missing NR sequence list file %s\n' % nr90_list_file)
            exit(0)
    ppi_files = os.path.join(src_path, config.get('Files', 'ppi_files'))
    ppi_files_edges = ppi_files + '.ppi'
    ppi_files_dat = ppi_files + '.dat'
    if not fileExist(ppi_files_edges) or init_pdb:
        if verbose:
            sys.stdout.write('\t\t-- Writing PPI file...\n')
        pdb_list_file = config.get('Files', 'pdb_list_file')
        functions_path = config.get('Paths', 'functions_path')
        python_path = config.get('Paths', 'python_path')
        data_path = os.path.join(src_path, config.get('Paths', 'data_path'))
        PPI_distance_threshold = config.get('Parameters', 'PPI_distance_threshold')
        PPI_threshold_type = config.get('Parameters', 'PPI_threshold_type')
        pdb2pin = os.path.join(functions_path, 'PDB2PIN.py')
        if verbose:
            process = subprocess.Popen([os.path.join(python_path, 'python'), pdb2pin, '-i', pdb_list_file, '-o', ppi_files, '-v', '--PPI_distance', PPI_distance_threshold, '--PPI_type', PPI_threshold_type], stderr=subprocess.STDOUT)
            process.wait()
        else:
            process = subprocess.Popen([os.path.join(python_path, 'python'), pdb2pin, '-i', pdb_list_file, '-o', ppi_files, '--PPI_distance', PPI_distance_threshold, '--PPI_type', PPI_threshold_type], stderr=subprocess.STDOUT)
            process.wait()
    if not skip_check:
        pdb_edges = set((x, y) for x, y, alt_a, alt_b in PPI_iterator(ppi_files_edges) if x in protein_names and y in protein_names)
        all_edges = pdb_edges
        nodes = get_nodes(pdb_edges)
    else:
        sys.stderr.write('WARNING: the background set of PPIs is untested \n')
        pdb_edges = set((x, y) for x, y, alt_a, alt_b in PPI_iterator(ppi_files_edges))
        all_edges = pdb_edges
        nodes = get_nodes(pdb_edges)
    if options.did:
        ddi_files = os.path.join(src_path, config.get('Files', 'ddi_files'))
        ddi_files_edges = ddi_files + '.ppi'
        ddi_files_dat = ddi_files + '.dat'
        if not fileExist(ddi_files_edges) or init_3did:
            if verbose:
                sys.stdout.write('\t\t-- Writing DDI file...\n')
            did_list_file = os.path.join(src_path, config.get('Files', '3did_list_file'))
            python_path = config.get('Paths', 'python_path')
            functions_path = os.path.join(src_path, config.get('Paths', 'functions_path'))
            data_path = os.path.join(src_path, config.get('Paths', 'data_path'))
            PPI_distance_threshold = config.get('Parameters', 'PPI_distance_threshold')
            PPI_threshold_type = config.get('Parameters', 'PPI_threshold_type')
            pdb2pin = os.path.join(functions_path, 'PDB2PIN.py')
            if verbose:
                process = subprocess.Popen([os.path.join(python_path, 'python'), pdb2pin, '-i', did_list_file, '-o', ddi_files, '-v', '--PPI_distance', PPI_distance_threshold, '--PPI_type', PPI_threshold_type], stderr=subprocess.STDOUT)
                process.wait()
            else:
                process = subprocess.Popen([os.path.join(python_path, 'python'), pdb2pin, '-i', did_list_file, '-o', ddi_files, '--PPI_distance', PPI_distance_threshold, '--PPI_type', PPI_threshold_type], stderr=subprocess.STDOUT)
                process.wait()
        if not skip_check:
            ddi_edges = set((x, y) for x, y, alt_a, alt_b in PPI_iterator(ddi_files_edges) if x in protein_names and y in protein_names)
            all_edges.update(ddi_edges)
            nodes.update(get_nodes(ddi_edges))
        else:
            sys.stderr.write('WARNING: the background set of DDIs is untested \n')
            ddi_edges = set((x, y) for x, y, alt_a, alt_b in PPI_iterator(ddi_files_edges))
            all_edges.update(ddi_edges)
            nodes.update(get_nodes(ddi_edges))
    edges = {}
    for x, y in all_edges:
        edges.setdefault(x, set()).add(y)
        edges.setdefault(y, set()).add(x)

    blast_dir = os.path.join(src_path, config.get('Paths', 'blast_dir'))
    database = config.get('Files', 'database_file')
    database_file = os.path.join(blast_dir, database)
    included = {}
    if not fileExist(database_file) or make_database:
        if fileExist(nr90_list_file + '.clstr'):
            if verbose:
                sys.stdout.write('\t\t-- Reading clusters of redundancy...\n')
            cluster_id = parse_clusters(nr90_list_file + '.clstr')
        else:
            cluster_id = {}
        if verbose:
            sys.stdout.write('\t\t-- Building database of sequences...\n')
        if nodes is not None:
            out = open(database_file, 'w')
            for name in nodes:
                if name in nr90_names:
                    printfasta(out, name, proteins[name].get_sequence())
                    included.setdefault(name, True)

            add = set()
            for name in included.keys():
                cset = set(cluster_id[x] for x in edges[name] if included.has_key(x) and cluster_id.has_key(x))
                iset = set()
                for x in edges[name]:
                    if included.has_key(x):
                        continue
                    if cluster_id.has_key(x):
                        if cluster_id[x] not in cset:
                            iset.add(x)
                            cset.add(cluster_id[x])
                    else:
                        iset.add(x)

                add.update(iset)

            while len(add) > 0:
                if verbose:
                    sys.stdout.write('\t\t\t Missing %d nodes. Add and check for new\n' % len(add))
                for name in add:
                    printfasta(out, name, proteins[name].get_sequence())
                    included.setdefault(name, True)

                add_new = set()
                for name in add:
                    cset = set(cluster_id[x] for x in edges[name] if included.has_key(x) and cluster_id.has_key(x))
                    iset = set()
                    for x in edges[name]:
                        if included.has_key(x):
                            continue
                        if cluster_id.has_key(x):
                            if cluster_id[x] not in cset:
                                iset.add(x)
                                cset.add(cluster_id[x])
                        else:
                            iset.add(x)

                    add_new.update(iset)

                add = add_new

            out.close()
            if verbose:
                sys.stdout.write('\t\t-- Formatting and indexing the database...\n\t\t   %s\n' % (blast_path + 'formatdb' + ' -i ' + database_file))
            process = subprocess.Popen([blast_path + 'formatdb', '-i', database_file], stderr=subprocess.STDOUT)
            process.wait()
            remove_files(['formatdb.log'])
    else:
        sys.stderr.write('WARNING: the database of sequences already exists. Be aware you are using the last created file for BLAST\n')
    if verbose:
        sys.stdout.write('\t\t-- Reading input PPI file...\n')
    user_interactions = set()
    if fileExist(options.interactions_file):
        protein_pairs = open(options.interactions_file, 'r')
        group_A = []
        group_B = []
        for pair in protein_pairs:
            group_A.append(pair.split('\t')[0])
            group_B.append(pair.split('\t')[1].strip())
            given_interaction = (pair.split('\t')[0], pair.split('\t')[1].strip())
            user_interactions.add(given_interaction)

        protein_pairs.close()
    else:
        sys.stderr.write('EXIT: Missing input PPI file %s\n' % options.interactions_file)
        exit(0)
    if verbose:
        sys.stdout.write('\t\t-- Reading query sequences file...\n')
    if fileExist(options.query_file):
        for protein in FASTA_iterator(options.query_file):
            name = protein.get_identifier()
            if re.search('[a-z][|A-Z0-9][|A-Z0-9]', name):
                if len(name.split('|')) > 1:
                    name = name.split('|')[1]
            seq = protein.get_sequence()
            if len(seq) > 0:
                try:
                    if name in group_A:
                        queriesA.setdefault(name, ProteinSequence(name, seq))
                    if name in group_B:
                        queriesB.setdefault(name, ProteinSequence(name, seq))
                except IncorrectSequenceLetter as e:
                    sys.stderr.write('WARNING: %s\n' % e)
                    if verbose:
                        sys.stdout.write('\t\t -- Skip input sequence: %s Sequence: %s\n' % (name, seq))

    else:
        sys.stderr.write('EXIT: Missing query sequences file %s\n' % options.query_file)
        exit(0)
    return (
     queriesA, queriesB, all_edges, user_interactions)


def parse_clusters(clstr):
    cl = open(clstr, 'r')
    cluster_id = {}
    for line in cl:
        if line.startswith('>Cluster'):
            cluster_name = line.strip().split()[1]
        m = re.search('(\\w+), >(\\w+)...', line)
        if m:
            cluster_id.setdefault(m.group(2), cluster_name)

    cl.close()
    return cluster_id


def do_blast(options, queriesA, queriesB):
    verbose = options.show
    dummy_dir = options.dummy_dir
    blast_results_dir = os.path.join(dummy_dir, 'blast')
    make_subdirs(dummy_dir, subdirs=['blast'])
    src_path = config.get('Paths', 'modppi_path')
    blast_path = os.path.join(src_path, config.get('Paths', 'blast_path'))
    blast_dir = os.path.join(src_path, config.get('Paths', 'blast_dir'))
    database_file = os.path.join(blast_dir, './database.fasta')
    if verbose:
        sys.stdout.write('\t\t-- BLAST of Query A and Query B files...\n')
    hit_items_A = []
    for name in queriesA:
        fasta_file = os.path.join(blast_results_dir, name + '.fa')
        seq_queryA = queriesA[name].get_sequence()
        if not os.path.exists(fasta_file):
            fd = open(fasta_file, 'w')
            printfasta(fd, name, seq_queryA)
            fd.close()
        blast_file = os.path.join(blast_results_dir, name + '.blast.out')
        skip = False
        if not os.path.exists(blast_file):
            try:
                if verbose:
                    sys.stdout.write('\t\t\t-- Blast of %s...\n' % fasta_file)
                if seq_queryA:
                    process = subprocess.Popen([os.path.join(blast_path, 'blastpgp'), '-d', database_file, '-i', fasta_file, '-m 7', '-o', blast_file], stderr=subprocess.STDOUT)
                    process.wait()
            except:
                sys.stderr.write('WARNING: "blastpgp on %s" execution failed!\n' % name)
                skip = True

            if not os.path.exists(blast_file):
                sys.stderr.write('WARNING: No blast output on %s could be found!\n' % name)
                skip = True
        if not skip:
            done = set()
            if verbose:
                sys.stdout.write('\t\t\t-- Parsing BLAST %s...\n' % blast_file)
            try:
                blast_obj = blast_parser.parse_blast(query_sequence=None, blast_output_file=blast_file, selfHit=False, hitIDformat='all')
            except Exception as e:
                sys.stderr.write('ERROR: BLAST output  %s collapsed; remove "dummy" folder and run again when all queues are done\n' % blast_file)

            n_parameter_twilight_zone = config.get('Parameters', 'n_parameter_twilight_zone')
            n = -1
            for hit in blast_obj.get_hits(tz_parameter=n_parameter_twilight_zone, tz_type='ID'):
                n += 1
                if hit.sequenceID in done:
                    continue
                done.add(hit.sequenceID)
                if blast_obj.query.split(':')[0] == hit.sequenceID.split('_')[0]:
                    continue
                hit_items_A.append((blast_obj.query, hit.sequenceID, hit.query_seq, hit.hit_seq, hit.query_pos, hit.hit_pos))

    hit_items_B = []
    for name in queriesB:
        fasta_file = os.path.join(blast_results_dir, name + '.fa')
        seq_queryB = queriesB[name].get_sequence()
        if not os.path.exists(fasta_file):
            fd = open(fasta_file, 'w')
            printfasta(fd, name, seq_queryB)
            fd.close()
        blast_file = os.path.join(blast_results_dir, name + '.blast.out')
        skip = False
        if not os.path.exists(blast_file):
            try:
                if verbose:
                    sys.stdout.write('\t\t\t-- Blast of %s...\n' % fasta_file)
                if seq_queryB:
                    process = subprocess.Popen([os.path.join(blast_path, 'blastpgp'), '-d', database_file, '-i', fasta_file, '-m 7', '-o', blast_file], stderr=subprocess.STDOUT)
                    process.wait()
            except:
                sys.stderr.write('WARNING: "blastpgp on %s" execution failed!\n' % name)
                skip = True

            if not os.path.exists(blast_file):
                sys.stderr.write('WARNING: No blast output on %s could be found!\n' % name)
                skip = True
        if not skip:
            done = set()
            if verbose:
                sys.stdout.write('\t\t\t-- Parsing BLAST %s...\n' % blast_file)
            try:
                blast_obj = blast_parser.parse_blast(query_sequence=None, blast_output_file=blast_file, selfHit=False, hitIDformat='all')
            except Exception as e:
                sys.stderr.write('ERROR: BLAST output  %s collapsed; remove "dummy" folder and run again when all queues are done\n' % blast_file)

            n_parameter_twilight_zone = config.get('Parameters', 'n_parameter_twilight_zone')
            n = -1
            for hit in blast_obj.get_hits(tz_parameter=n_parameter_twilight_zone, tz_type='ID'):
                n += 1
                if hit.sequenceID in done:
                    continue
                done.add(hit.sequenceID)
                if blast_obj.query.split(':')[0] == hit.sequenceID.split('_')[0]:
                    continue
                hit_items_B.append((blast_obj.query, hit.sequenceID, hit.query_seq, hit.hit_seq, hit.query_pos, hit.hit_pos))

    return (
     hit_items_A, hit_items_B)


def modelling(queriesA_original, queriesB_original, queriesA, queriesB, hit_items_A, hit_items_B, sections_modeled, remaining_sections_A, remaining_sections_B, options):
    verbose = options.show
    output_dir = options.outdir
    dummy_dir = options.dummy_dir
    hydrogens = options.hbplus
    force_model = options.force
    python_path = config.get('Paths', 'python_path')
    src_path = config.get('Paths', 'modppi_path')
    modeller_path = os.path.join(config.get('Paths', 'modeller_path'))
    modpy_path = os.path.join(src_path, config.get('Paths', 'functions_path'), 'modpy')
    numMod = options.nmodels
    renumerate = options.renumerate
    modelling_dummy_name = 'modelling_' + str(os.getpid()) + str(random.randint(0, os.getpid()))
    make_subdirs(dummy_dir, subdirs=[modelling_dummy_name])
    modelling_dir = os.path.join(dummy_dir, modelling_dummy_name)
    query_A_orig = queriesA_original.get(hit_items_A[0])
    query_B_orig = queriesB_original.get(hit_items_B[0])
    query_A = queriesA.get(hit_items_A[0]).get_sequence()
    query_B = queriesB.get(hit_items_B[0]).get_sequence()
    query_name_A = hit_items_A[0]
    query_name_B = hit_items_B[0]
    query_id_A = query_name_A.split(':')[0]
    query_start = hit_items_A[4][0]
    query_end = int(hit_items_A[4][(-1)]) + int(hit_items_B[4][(-1)])
    template_name_A_chain = hit_items_A[1]
    template_name_B_chain = hit_items_B[1]
    template_chain_A_chain = template_name_A_chain.split('_')[(-1)]
    template_chain_B_chain = template_name_B_chain.split('_')[(-1)]
    template_A_chain_start = hit_items_A[5][0]
    template_B_chain_start = hit_items_B[5][0]
    template_id_A = ('_').join(template_name_A_chain.split('_')[:-1])
    template_id_B = ('_').join(template_name_B_chain.split('_')[:-1])
    sequences_complex = {}
    sequences_complex.setdefault('A', query_A_orig)
    sequences_complex.setdefault('B', query_B_orig)
    extension_threshold = int(config.get('Parameters', 'extension_threshold'))
    current_A_section = [hit_items_A[4][0], hit_items_A[4][(-1)]]
    current_B_section = [hit_items_B[4][0], hit_items_B[4][(-1)]]
    current_sections = [current_A_section, current_B_section]
    current_interaction = '%s::%s' % (query_name_A, query_name_B)
    if not sections_modeled.get(current_interaction):
        section_group = sections_modeled.setdefault(current_interaction, [])
        section_group.append(current_sections)
    for section_pair in sections_modeled.get(current_interaction):
        if section_pair[0][0] - extension_threshold <= current_sections[0][0] <= section_pair[0][0] + extension_threshold and section_pair[0][1] - extension_threshold <= current_sections[0][1] <= section_pair[0][1] + extension_threshold and section_pair[1][0] - extension_threshold <= current_sections[1][0] <= section_pair[1][0] + extension_threshold and section_pair[1][1] - extension_threshold <= current_sections[1][1] <= section_pair[1][1] + extension_threshold:
            current_sections = section_pair
            break
    else:
        section_group = sections_modeled.setdefault(current_interaction, [])
        section_group.append(current_sections)

    query_A_fragment_used = hit_items_A[2].replace('-', '')
    query_B_fragment_used = hit_items_B[2].replace('-', '')
    remaining_terminus_A = query_A.split(query_A_fragment_used)
    remaining_terminus_B = query_B.split(query_B_fragment_used)
    Nterminus_name_A = '%s_1-%s' % (query_name_A, hit_items_A[4][0] - 1)
    Cterminus_name_A = '%s_%s-%s' % (query_name_A, hit_items_A[4][(-1)] + 1, len(query_A))
    Nterminus_name_B = '%s_1-%s' % (query_name_B, hit_items_B[4][0] - 1)
    Cterminus_name_B = '%s_%s-%s' % (query_name_B, hit_items_B[4][(-1)] + 1, len(query_B))
    if hit_items_A[4][0] > 1:
        remaining_sections_A[Nterminus_name_A] = ProteinSequence(Nterminus_name_A, remaining_terminus_A[0])
    if hit_items_A[4][(-1)] < len(query_A):
        remaining_sections_A[Cterminus_name_A] = ProteinSequence(Cterminus_name_A, remaining_terminus_A[(-1)])
    if hit_items_B[4][0] > 1:
        remaining_sections_B[Nterminus_name_B] = ProteinSequence(Nterminus_name_B, remaining_terminus_B[0])
    if hit_items_B[4][(-1)] < len(query_B):
        remaining_sections_B[Cterminus_name_B] = ProteinSequence(Cterminus_name_B, remaining_terminus_B[(-1)])
    if verbose:
        dummy_log_file = '%s/%s.log' % (modelling_dir, template_id_A)
        dummy_log = open(dummy_log_file, 'a')
    if verbose:
        sys.stdout.write('\t\t-- Using templates %s and %s...\n' % (template_name_A_chain, template_name_B_chain))
    pdb_name = template_id_A
    dummy_pdb_file = '%s/%s.pdb' % (modelling_dir, pdb_name.replace(':', '-'))
    pdb_obj = PDB()
    src_path = config.get('Paths', 'modppi_path')
    pdb_path = os.path.join(src_path, config.get('Paths', 'pdb_path'), template_id_A[1:3].lower())
    pdb_file = os.path.join(pdb_path, 'pdb' + template_id_A.lower() + '.ent')
    if not os.path.exists(pdb_file):
        sys.stderr.write('WARNING: PDB file %s was not found, try compressed\n' % pdb_file)
        pdb_file = os.path.join(pdb_path, 'pdb' + template_id_A.lower() + '.ent.gz')
    if not os.path.exists(pdb_file):
        sys.stderr.write('WARNING: PDB file %s was not found, try 3DiD ".brk" suffix\n' % pdb_file)
        pdb_path = os.path.join(src_path, config.get('Paths', '3did_path'))
        pdb_file = os.path.join(pdb_path, template_id_A.lower() + '.brk')
        if not os.path.exists(pdb_file):
            sys.stderr.write('WARNING: PDB file %s was not found, try 3DiD ".brk" suffix compressed\n' % pdb_file)
            pdb_file = os.path.join(pdb_path, template_id_A.lower() + '.brk.gz')
    if not os.path.exists(pdb_file):
        sys.stderr.write('WARNING: PDB file %s was not found\n' % pdb_file)
        raise ModelException
    pdb_chain_obj = PDB(pdb_file)
    pdb_chain_obj.clean()
    pdb_obj.add_chain(pdb_chain_obj.get_chain_by_id(template_chain_A_chain))
    pdb_obj.add_chain(pdb_chain_obj.get_chain_by_id(template_chain_B_chain))
    pdb_seqA = pdb_obj.chains[0].gapped_protein_sequence.replace('x', '-').replace('X', '.')
    pdb_seqB = pdb_obj.chains[1].gapped_protein_sequence.replace('x', '-').replace('X', '.')
    pdb_obj.clean()
    pdb_obj.write(output_file=dummy_pdb_file, force=True)
    PPI_threshold_type = config.get('Parameters', 'PPI_threshold_type')
    PPI_distance_threshold = float(config.get('Parameters', 'PPI_distance_threshold'))
    protein_complex = Complex(pdb_obj, PPI_type=PPI_threshold_type, PPI_distance=PPI_distance_threshold)
    if len(protein_complex.PPInterfaces[0].contacts) == 0:
        sys.stderr.write('WARNING: No interaction between %s and %s ( for %s %s)\n' % (template_name_A_chain, template_name_B_chain, query_name_A, query_name_B))
        remove_files([dummy_pdb_file])
        raise ModelException
    else:
        if verbose:
            sys.stdout.write('\t\t\t-- Accepted interaction between %s and %s ( for %s %s)...\n' % (template_name_A_chain, template_name_B_chain, query_name_A, query_name_B))
        template_seqA = hit_items_A[3]
        template_seqA_ungapped = re.sub('-', '', template_seqA)
        pdbA_section = pdb_seqA[hit_items_A[5][0] - 1:hit_items_A[5][(-1)]]
        for pair in itertools.izip(template_seqA_ungapped, pdbA_section):
            if pair[0] == 'X' or pair[0] == 'x':
                template_seqA = re.sub('[xX]', pair[1], template_seqA, 1)

        template_seqB = hit_items_B[3]
        template_seqB_ungapped = re.sub('-', '', template_seqB)
        pdbB_section = pdb_seqB[hit_items_B[5][0] - 1:hit_items_B[5][(-1)]]
        for pair in itertools.izip(template_seqB_ungapped, pdbB_section):
            if pair[0] == 'X' or pair[0] == 'x':
                template_seqB = re.sub('[xX]', pair[1], template_seqB, 1)

        if verbose:
            dummy_log.write('Hits_items_A: %s\n' % [ str(x) for x in hit_items_A ])
        if verbose:
            dummy_log.write('Hits_items_B: %s\n' % [ str(x) for x in hit_items_B ])
        if verbose:
            dummy_log.write('pdbA_section %s\n' % pdbA_section)
        if verbose:
            dummy_log.write('pdbB_section %s\n' % pdbB_section)
        if verbose:
            dummy_log.write('length PDB A: %d\n' % len(pdb_seqA))
        if verbose:
            dummy_log.write('length PDB B: %d\n' % len(pdb_seqB))
        template_seqA = re.sub('[xX]', '-', template_seqA)
        if template_A_chain_start > 1:
            template_A_first_residues = ('').join(pdb_seqA[:hit_items_A[5][0] - 1])
            template_seqA = template_A_first_residues + template_seqA
        if hit_items_A[5][(-1)] < len(pdb_seqA):
            template_seqA += ('').join(pdb_seqA[hit_items_A[5][(-1)]:])
        template_seqB = re.sub('[xX]', '-', template_seqB)
        if template_B_chain_start > 1:
            template_B_first_residues = ('').join(pdb_seqB[:hit_items_B[5][0] - 1])
            template_seqB = template_B_first_residues + template_seqB
        if hit_items_B[5][(-1)] < len(pdb_seqB):
            template_seqB += ('').join(pdb_seqB[hit_items_B[5][(-1)]:])
        if verbose:
            dummy_log.write('FINAL template_seqA %s\n' % template_seqA)
        if verbose:
            dummy_log.write('FINAL template_seqB %s\n' % template_seqB)
        gaps_number_A_chain_beginning = 0
        gaps_number_B_chain_beginning = 0
        if template_A_chain_start > 1:
            gaps_number_A_chain_beginning = int(template_A_chain_start) - 1
        if template_B_chain_start > 1:
            gaps_number_B_chain_beginning = int(template_B_chain_start) - 1
        A_chain_query_seq = ('').join([ '-' for i in range(gaps_number_A_chain_beginning) ]) + re.sub('[xX]', '-', hit_items_A[2])
        B_chain_query_seq = ('').join([ '-' for i in range(gaps_number_B_chain_beginning) ]) + re.sub('[xX]', '-', hit_items_B[2])
        for pair in itertools.izip_longest(A_chain_query_seq, template_seqA):
            if pair[0] == None:
                A_chain_query_seq += '-'

        for pair in itertools.izip_longest(B_chain_query_seq, template_seqB):
            if pair[0] == None:
                B_chain_query_seq += '-'

        query_whole_seq = A_chain_query_seq + '/' + B_chain_query_seq + '*'
        template_whole_seq = template_seqA + '/' + template_seqB + '*'
        header1 = '>P1;%s\nsequence:%s:%s:.:%s:.:.:.:.:.' % (query_id_A, query_id_A, query_start, query_end)
        header2 = '>P1;%s\nstructureX:%s:1:%s:.:%s:.:.:.:.' % (template_id_A.replace(':', '-'), template_id_A.replace(':', '-'), template_chain_A_chain, template_chain_B_chain)
        lines = []
        lines.append(header1)
        lines.extend([ query_whole_seq[i:i + 60] for i in range(0, len(query_whole_seq), 60) ])
        lines.append(header2)
        lines.extend([ template_whole_seq[i:i + 60] for i in range(0, len(template_whole_seq), 60) ])
        pir_alignment = ('\n').join(lines)
        pir_file = open('%s/alignment.pir' % modelling_dir, 'w+')
        for line in lines:
            pir_file.write('%s\n' % line)

        pir_file.close()
        if '-' in query_name_A:
            query_name_A = query_name_A.rsplit('_', 1)[0]
        if '-' in query_name_B:
            query_name_B = query_name_B.rsplit('_', 1)[0]
        interaction_dir = os.path.join(output_dir, '%s::%s' % (query_name_A, query_name_B))
        if not os.path.exists(interaction_dir):
            make_subdirs(output_dir, subdirs=['./%s::%s' % (query_name_A, query_name_B)])
        do_model = False
        model_path = os.path.abspath(interaction_dir)
        for imodel in xrange(1, numMod + 1):
            model_name = '%s_%s_%d-%d::%s_%s_%d-%d#%d.pdb' % (template_id_A, template_chain_A_chain, current_sections[0][0], current_sections[0][1], template_id_B, template_chain_B_chain, current_sections[1][0], current_sections[1][1], imodel)
            model_path_model = os.path.join(model_path, model_name)
            with open(interaction_dir + '/%s.list' % current_interaction, 'a+') as (paths_to_models_file):
                if model_path_model not in paths_to_models_file.read():
                    paths_to_models_file.write(model_path_model + '\n')
            if not do_model and not fileExist(model_path_model):
                do_model = True

        if do_model or force_model:
            cwd = os.getcwd()
            os.chdir(modelling_dir)
            try:
                if options.optimize:
                    process = subprocess.check_output([os.path.join(modeller_path, 'modpy.sh'), os.path.join(python_path, 'python'), os.path.join(modpy_path, 'simpleModel.py'), '--pir=' + './alignment.pir', '--out=%s-%s' % (template_name_A_chain, template_name_B_chain), '--models=%d' % numMod, '--optimize'], stderr=subprocess.STDOUT)
                else:
                    process = subprocess.check_output([os.path.join(modeller_path, 'modpy.sh'), os.path.join(python_path, 'python'), os.path.join(modpy_path, 'simpleModel.py'), '--pir=' + './alignment.pir', '--out=%s-%s' % (template_name_A_chain, template_name_B_chain), '--models=%d' % numMod], stderr=subprocess.STDOUT)
            except Exception as e:
                sys.stderr.write('ERROR: %s\n' % e)
                sys.stderr.write('LOCATION; %s\n' % modelling_dir)
                if verbose:
                    os.system('grep get_ran %s' % (template_name_A_chain + '-' + template_name_B_chain + '.log'))
                if verbose:
                    sys.stderr.write('\t\tSkip models with template %s\n' % model_name)
                os.chdir(cwd)
                raise ModelException

            for imodel in xrange(1, numMod + 1):
                label_model = 99990000 + imodel
                input_model = '%s.B%s.pdb' % (query_id_A, str(label_model))
                model_name = '%s_%s_%d-%d::%s_%s_%d-%d#%d.pdb' % (template_id_A, template_chain_A_chain, current_sections[0][0], current_sections[0][1], template_id_B, template_chain_B_chain, current_sections[1][0], current_sections[1][1], imodel)
                model_path_model = os.path.join(model_path, model_name)
                if fileExist(os.path.abspath('%s' % input_model)):
                    check_pdb_obj = PDB(os.path.abspath('%s' % input_model))
                    PPI_threshold_type = config.get('Parameters', 'PPI_threshold_type')
                    PPI_distance_threshold = float(config.get('Parameters', 'PPI_distance_threshold'))
                    check_protein_complex = Complex(check_pdb_obj, PPI_type=PPI_threshold_type, PPI_distance=PPI_distance_threshold)
                    if len(check_protein_complex.PPInterfaces[0].contacts) == 0:
                        if verbose:
                            sys.stdout.write('\t\t\t-- Skip model without contacts %s\n' % model_name)
                        continue
                    elif verbose:
                        sys.stdout.write('\t\t\t-- Accepted model %s\n' % model_name)
                    if hydrogens:
                        if verbose:
                            sys.stdout.write('\t\t\t-- Adding hydrogens and relaxing the model %s\n' % model_name)
                        output_model = model_name
                        try:
                            add_hydrogens(config, os.path.abspath('./'), input_model, output_model, dummy_dir)
                        except ValueError as e:
                            sys.stderr.write('WARNING %s\n' % e)
                            os.rename(input_model, output_model)

                    else:
                        output_model = model_name
                        os.rename(input_model, output_model)
                    if renumerate:
                        if verbose:
                            sys.stdout.write('\t\t\t-- Renumerate residues as original sequence\n')
                        output_model_renumber = model_name + '.re'
                        try:
                            pdb_renumber = PDB()
                            pdb_renumber = renumber_pdb(config, os.path.abspath('./'), output_model, sequences_complex, os.path.abspath('./'))
                            pdb_renumber.write(output_model_renumber)
                            os.rename(output_model_renumber, output_model)
                        except Exception as e:
                            sys.stderr.write('WARNING %s\n' % e)

                    shutil.copy(output_model, model_path_model)

            os.chdir(cwd)
        try:
            shutil.rmtree(modelling_dir)
        except Exception as e:
            sys.stderr.write('WARNING first attempt to remove folder %s\n' % e)
            try:
                os.system('\\rm -r %s' % modelling_dir)
            except Exception as ee:
                sys.stderr.write('WARNING last attempt %s\n' % ee)

    return (sections_modeled, remaining_sections_A, remaining_sections_B)


if __name__ == '__main__':
    main()