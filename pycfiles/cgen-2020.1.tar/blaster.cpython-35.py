# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/blaster/blaster.py
# Compiled at: 2020-04-01 11:09:31
# Size of source mod 2**32: 28018 bytes
from __future__ import division
import sys, os, time, random, re, subprocess
from Bio.Blast import NCBIXML
from Bio import SeqIO
import collections

class Blaster:

    def __init__(self, inputfile, databases, db_path, out_path='', min_cov=0.6, threshold=0.9, blast='blastn', cut_off=True, max_target_seqs=50000, reuse_results=False, allowed_overlap=0):
        min_cov = 100 * float(min_cov)
        threshold = 100 * float(threshold)
        self.gene_align_query = dict()
        self.gene_align_homo = dict()
        self.gene_align_sbjct = dict()
        self.results = dict()
        self.results['excluded'] = dict()
        for db in databases:
            db_file = '%s/%s.fsa' % (db_path, db)
            tmp_out_path = '%s/tmp' % out_path
            out_file = '%s/out_%s.xml' % (tmp_out_path, db)
            os.makedirs(tmp_out_path, exist_ok=True)
            os.chmod(tmp_out_path, 509)
            if os.path.isfile(out_file) and os.access(out_file, os.R_OK) and reuse_results:
                print('Found ' + out_file + ' skipping DB.')
                out, err = ('', '')
            else:
                cmd = "%s -subject %s -query %s -out %s -outfmt '5' -perc_identity  %s -max_target_seqs %s -dust 'no'" % (
                 blast, db_file, inputfile,
                 out_file, threshold, max_target_seqs)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
            try:
                result_handle = open(out_file, 'r')
            except IOError:
                sys.exit('Error: BLAST did not run as expected. The expected output file, {}, did not exist.\nBLAST finished with the following response:\n{}\n{}'.format(os.path.abspath(out_file), out.decode('utf-8'), err.decode('utf-8')))

            if os.stat(out_file).st_size == 0:
                sys.exit('Error: BLAST did not run as expected. The output file {} was empty.\nBLAST finished with the following response:\n{}\n{}'.format(os.path.abspath(out_file), out.decode('utf-8'), err.decode('utf-8')))
            blast_records = NCBIXML.parse(result_handle)
            gene_results = dict()
            best_hsp = dict()
            gene_split = collections.defaultdict(dict)
            self.gene_align_query[db] = dict()
            self.gene_align_homo[db] = dict()
            self.gene_align_sbjct[db] = dict()
            for blast_record in blast_records:
                blast_record.alignments.sort(key=lambda align: max(int(hsp.identities) for hsp in align.hsps), reverse=True)
                query = blast_record.query
                for alignment in blast_record.alignments:
                    best_e_value = 1
                    best_bit = 0
                    start_hsp = 0
                    end_hsp = 0
                    for hsp in alignment.hsps:
                        if hsp.expect < best_e_value or hsp.bits > best_bit:
                            tmp = alignment.title.split(' ')
                            sbjct_header = tmp[1]
                            print('Found: {}'.format(sbjct_header))
                            bit = hsp.bits
                            sbjct_length = alignment.length
                            sbjct_start = hsp.sbjct_start
                            sbjct_end = hsp.sbjct_end
                            gaps = hsp.gaps
                            query_string = str(hsp.query)
                            homo_string = str(hsp.match)
                            sbjct_string = str(hsp.sbjct)
                            contig_name = query.replace('>', '')
                            query_start = hsp.query_start
                            query_end = hsp.query_end
                            HSP_length = len(query_string)
                            perc_ident = int(hsp.identities) / float(HSP_length) * 100
                            strand = 0
                            coverage = (int(HSP_length) - int(gaps)) / float(sbjct_length)
                            perc_coverage = (int(HSP_length) - int(gaps)) / float(sbjct_length) * 100
                            cal_score = perc_ident * coverage
                            hit_id = '%s:%s..%s:%s:%f' % (
                             contig_name, query_start, query_end,
                             sbjct_header, cal_score)
                            if sbjct_start > sbjct_end:
                                tmp = sbjct_start
                                sbjct_start = sbjct_end
                                sbjct_end = tmp
                                query_string = self.reversecomplement(query_string)
                                homo_string = homo_string[::-1]
                                sbjct_string = self.reversecomplement(sbjct_string)
                                strand = 1
                            if cut_off and perc_coverage > 20 or cut_off is False:
                                best_hsp = {'evalue': hsp.expect, 
                                 'sbjct_header': sbjct_header, 
                                 'bit': bit, 
                                 'perc_ident': perc_ident, 
                                 'sbjct_length': sbjct_length, 
                                 'sbjct_start': sbjct_start, 
                                 'sbjct_end': sbjct_end, 
                                 'gaps': gaps, 
                                 'query_string': query_string, 
                                 'homo_string': homo_string, 
                                 'sbjct_string': sbjct_string, 
                                 'contig_name': contig_name, 
                                 'query_start': query_start, 
                                 'query_end': query_end, 
                                 'HSP_length': HSP_length, 
                                 'coverage': coverage, 
                                 'cal_score': cal_score, 
                                 'hit_id': hit_id, 
                                 'strand': strand, 
                                 'perc_coverage': perc_coverage}
                            if best_hsp:
                                save = 1
                                if gene_results:
                                    tmp_gene_split = gene_split
                                    tmp_results = gene_results
                                    save, gene_split, gene_results = self.compare_results(save, best_hsp, tmp_results, tmp_gene_split, allowed_overlap)
                                if save == 1:
                                    print('Saving: {}'.format(hit_id))
                                    gene_results[hit_id] = best_hsp

            result_handle.close()
            keys = list(gene_results.keys())
            for hit_id in keys:
                hit = gene_results[hit_id]
                perc_coverage = hit['perc_coverage']
                if hit['sbjct_header'] in gene_split and len(gene_split[hit['sbjct_header']]) > 1:
                    new_length = self.calculate_new_length(gene_split, gene_results, hit)
                    hit['split_length'] = new_length
                    perc_coverage = new_length / float(hit['sbjct_length']) * 100
                if perc_coverage >= min_cov:
                    if hit['coverage'] == 1:
                        self.gene_align_query[db][hit_id] = hit['query_string']
                        self.gene_align_homo[db][hit_id] = hit['homo_string']
                        self.gene_align_sbjct[db][hit_id] = hit['sbjct_string']
                    elif hit['coverage'] != 1:
                        for seq_record in SeqIO.parse(db_file, 'fasta'):
                            if seq_record.description.replace(' ', '') == hit['sbjct_header'].replace(' ', ''):
                                start_seq = str(seq_record.seq)[:int(hit['sbjct_start']) - 1]
                                end_seq = str(seq_record.seq)[int(hit['sbjct_end']):]
                                self.gene_align_sbjct[db][hit_id] = start_seq + hit['sbjct_string'] + end_seq
                                break

                        contig = ''
                        for seq_record in SeqIO.parse(inputfile, 'fasta'):
                            if seq_record.description.replace(' ', '') == hit['contig_name'].replace(' ', ''):
                                contig = str(seq_record.seq)
                                break

                        query_seq, homo_seq = self.get_query_align(hit, contig)
                        self.gene_align_query[db][hit_id] = query_seq
                        self.gene_align_homo[db][hit_id] = homo_seq
                else:
                    del gene_results[hit_id]
                    if hit['sbjct_header'] in gene_split:
                        del gene_split[hit['sbjct_header']]

            if gene_results:
                self.results[db] = gene_results
            else:
                self.results[db] = 'No hit found'

    @staticmethod
    def reversecomplement(seq):
        trans = str.maketrans('ATGC', 'TACG')
        return seq.translate(trans)[::-1]

    @staticmethod
    def compare_results(save, best_hsp, tmp_results, tmp_gene_split, allowed_overlap):
        """
            Function for comparing hits and saving only the best hit
        """
        hit_id = best_hsp['hit_id']
        new_start_query = best_hsp['query_start']
        new_end_query = best_hsp['query_end']
        new_start_sbjct = int(best_hsp['sbjct_start'])
        new_end_sbjct = int(best_hsp['sbjct_end'])
        new_score = best_hsp['cal_score']
        new_db_hit = best_hsp['sbjct_header']
        new_contig = best_hsp['contig_name']
        new_HSP = best_hsp['HSP_length']
        keys = list(tmp_results.keys())
        for hit in keys:
            hit_data = tmp_results[hit]
            old_start_query = hit_data['query_start']
            old_end_query = hit_data['query_end']
            old_start_sbjct = int(hit_data['sbjct_start'])
            old_end_sbjct = int(hit_data['sbjct_end'])
            old_score = hit_data['cal_score']
            old_db_hit = hit_data['sbjct_header']
            old_contig = hit_data['contig_name']
            old_HSP = hit_data['HSP_length']
            remove_old = 0
            if new_db_hit == old_db_hit:
                if old_contig != new_contig and new_db_hit in tmp_gene_split and hit_id not in tmp_gene_split[new_db_hit]:
                    tmp_gene_split[new_db_hit][hit_id] = 1
            elif new_start_sbjct < old_start_sbjct or new_end_sbjct > old_end_sbjct:
                tmp_gene_split[old_db_hit][hit_id] = 1
                if hit not in tmp_gene_split[old_db_hit]:
                    tmp_gene_split[old_db_hit][hit] = 1
            if new_contig == old_contig:
                pass
            print('Same contig: {} == {}'.format(new_contig, old_contig))
            print('\t{} vs {}'.format(new_db_hit, old_db_hit))
            hit_union_length = max(old_end_query, new_end_query) - min(old_start_query, new_start_query)
            hit_lengths_sum = old_end_query - old_start_query + (new_end_query - new_start_query)
            overlap_len = hit_lengths_sum - hit_union_length
            if overlap_len < allowed_overlap:
                print('\tignore overlap ({}): {}'.format(overlap_len, new_db_hit))
                continue
                print('\toverlap found ({}): {}'.format(overlap_len, new_db_hit))
                if old_start_query == new_start_query and old_end_query == new_end_query:
                    if best_hsp['perc_ident'] > hit_data['perc_ident']:
                        remove_old = 1
                        if new_db_hit in tmp_gene_split and hit_id not in tmp_gene_split[new_db_hit]:
                            tmp_gene_split[new_db_hit][hit_id] = 1
                    else:
                        if best_hsp['perc_ident'] == hit_data['perc_ident']:
                            if new_db_hit in tmp_gene_split and hit_id not in tmp_gene_split[new_db_hit]:
                                tmp_gene_split[new_db_hit][hit_id] = 1
                        else:
                            save = 0
                            if new_db_hit in tmp_gene_split and hit_id in tmp_gene_split[new_db_hit]:
                                del tmp_gene_split[new_db_hit][hit_id]
                            break
                elif hit_union_length <= hit_lengths_sum:
                    print('\t{} <= {}'.format(hit_union_length, hit_lengths_sum))
                    print('\t\tScores: {} cmp {}'.format(new_score, old_score))
                    if new_score > old_score:
                        remove_old = 1
                        if new_db_hit in tmp_gene_split and hit_id not in tmp_gene_split[new_db_hit]:
                            tmp_gene_split[new_db_hit][hit_id] = 1
                if new_score == old_score:
                    if int(best_hsp['perc_coverage']) == int(hit_data['perc_coverage']) and new_HSP > old_HSP:
                        remove_old = 1
                    else:
                        if int(best_hsp['perc_coverage']) == int(hit_data['perc_coverage']) and old_HSP > new_HSP:
                            save = 0
                        elif int(best_hsp['perc_coverage']) == int(hit_data['perc_coverage']) and old_HSP == new_HSP:
                            pass
                        if new_db_hit in tmp_gene_split and hit_id not in tmp_gene_split[new_db_hit]:
                            tmp_gene_split[new_db_hit][hit_id] = 1
                else:
                    if new_db_hit in tmp_gene_split and hit_id in tmp_gene_split[new_db_hit]:
                        del tmp_gene_split[new_db_hit][hit_id]
                    save = 0
                    break
                if remove_old == 1:
                    del tmp_results[hit]
                    if old_db_hit in tmp_gene_split and hit in tmp_gene_split[old_db_hit]:
                        del tmp_gene_split[old_db_hit][hit]

        return (
         save, tmp_gene_split, tmp_results)

    @staticmethod
    def calculate_new_length(gene_split, gene_results, hit):
        """
            Function for calcualting new length if the gene is split on
            several contigs
        """
        first = 1
        for split in gene_split[hit['sbjct_header']]:
            new_start = int(gene_results[split]['sbjct_start'])
            new_end = int(gene_results[split]['sbjct_end'])
            if first == 1:
                new_length = int(gene_results[split]['HSP_length'])
                old_start = new_start
                old_end = new_end
                first = 0
                continue
                if new_start < old_start:
                    new_length = new_length + (old_start - new_start)
                    old_start = new_start
                if new_end > old_end:
                    new_length = new_length + (new_end - old_end)
                    old_end = new_end

        return new_length

    @staticmethod
    def get_query_align(hit, contig):
        """
            Function for extracting extra seqeunce data to the query
            alignment if the full reference length are not covered
        """
        query_seq = hit['query_string']
        homo_seq = hit['homo_string']
        sbjct_start = int(hit['sbjct_start'])
        sbjct_end = int(hit['sbjct_end'])
        query_start = int(hit['query_start'])
        query_end = int(hit['query_end'])
        length = int(hit['sbjct_length'])
        if sbjct_start != 1:
            missing = sbjct_start - 1
            if query_start >= missing and hit['strand'] != 1 or hit['strand'] == 1 and missing <= len(contig) - query_end:
                if hit['strand'] == 1:
                    start_pos = query_end
                    end_pos = query_end + missing
                    chars = contig[start_pos:end_pos]
                    chars = Blaster.reversecomplement(chars)
                else:
                    start_pos = query_start - missing - 1
                    end_pos = query_start - 1
                    chars = contig[start_pos:end_pos]
                query_seq = chars + str(query_seq)
        else:
            if hit['strand'] == 1:
                if query_end == len(contig):
                    query_seq = '-' * missing + str(query_seq)
                else:
                    start_pos = query_end
                    chars = contig[start_pos:]
                    chars = Blaster.reversecomplement(chars)
                    query_seq = '-' * (missing - len(chars)) + chars + str(query_seq)
            else:
                if query_start < 3:
                    query_seq = '-' * missing + str(query_seq)
                else:
                    end_pos = query_start - 2
                    chars = contig[0:end_pos]
                    query_seq = '-' * (missing - len(chars)) + chars + str(query_seq)
            spaces = ' ' * missing
            homo_seq = str(spaces) + str(homo_seq)
        if sbjct_end < length:
            missing = length - sbjct_end
            if missing <= len(contig) - query_end and hit['strand'] != 1 or hit['strand'] == 1 and query_start >= missing:
                if hit['strand'] == 1:
                    start_pos = query_start - missing - 1
                    end_pos = query_start - 1
                    chars = contig[start_pos:end_pos]
                    chars = Blaster.reversecomplement(chars)
                else:
                    start_pos = query_end
                    end_pos = query_end + missing
                    chars = contig[start_pos:end_pos]
                query_seq = query_seq + chars
        else:
            if hit['strand'] == 1:
                if query_start < 3:
                    query_seq = query_seq + '-' * missing
                else:
                    end_pos = query_start - 2
                    chars = contig[0:end_pos]
                    chars = Blaster.reversecomplement(chars)
                    query_seq = query_seq + chars + '-' * (missing - len(chars))
            else:
                if query_end == len(contig):
                    query_seq = query_seq + '-' * missing
                else:
                    start_pos = query_end
                    chars = contig[start_pos:]
                    query_seq = query_seq + chars + '-' * (missing - len(chars))
            spaces = ' ' * int(missing)
            homo_seq = str(homo_seq) + str(spaces)
        return (
         query_seq, homo_seq)