# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mpathic/src/io_local.py
# Compiled at: 2018-07-12 00:29:59
import pandas as pd, os
from mpathic.src import qc
from mpathic.src import utils
from mpathic.src.utils import ControlledError, handle_errors
from mpathic import SortSeqError
import sys
from Bio import SeqIO
from mpathic.src.utils import clean_SortSeqError

def format_fasta(s):
    """Function which takes in the raw fastq format and returns only the sequence"""
    location = s.find('\n')
    s = s[location + 1:]
    s = s.replace('\n', '')
    return s


def load_text(file_arg):
    """
    General function used to load data from a text file
    """
    file_handle = validate_file_for_reading(file_arg)
    try:
        df = pd.io.parsers.read_csv(file_handle, delim_whitespace=True, comment='#', skip_blank_lines=True, engine='c')
    except:
        raise SortSeqError('Could not interpret text file %s as dataframe.' % repr(file_handle))

    return df.dropna(axis=0, how='all')


def validate_file_for_reading(file_arg):
    """ Checks that a specified file exists and is readable. Returns a valid file handle given a file name or handle
    """
    if type(file_arg) == str:
        if not os.path.isfile(file_arg):
            raise SortSeqError('Cannot find file: %s' % file_arg)
        if not os.access(file_arg, os.R_OK):
            raise SortSeqError('Can find but cannot read from file: %s' % file_arg)
        file_handle = open(file_arg, 'r')
    elif type(file_arg) == file:
        if file_arg.closed:
            raise SortSeqError('File object is already closed.')
        file_handle = file_arg
    else:
        raise SortSeqError('file_arg is neigher a name or handle.')
    return file_handle


def validate_file_for_writing(file_arg):
    """ Checks that a specified file can be written
    """
    if type(file_arg) == str:
        file_handle = open(file_arg, 'w')
        if not os.access(file_arg, os.W_OK):
            raise SortSeqError('Cannot write to file: %s' % file_arg)
    elif type(file_arg) == file:
        file_handle = file_arg
    else:
        raise SortSeqError('file_arg is neigher a name or handle.')
    return file_handle


@handle_errors
def load_dataset(file_arg, file_type='text', seq_type=None):
    """
    Method that loads a dataset via a file and
    returns a pandas dataframe.

    parameters
    ----------

    file_arg: (string)
        String specifying the location of the input file containing
        the dataset file.

    file_type: (string)
        String specifying type of file. Valid choices include
        'fasta','fastq', and 'text'.

    seq_type: (string)
        String that specifies type of sequence. Valid choices
        include 'dna', 'rna', 'protein' and (possibly None).

    return
    -------

    (dataframe)
        Pandas dataframe is returned.
    """
    if file_arg == 'sort_seq_data.txt':
        file_arg = './mpathic/data/sortseq/full-0/data.txt'
    file_handle = validate_file_for_reading(file_arg)
    if file_type not in ('text', 'fasta', 'fastq'):
        raise SortSeqError('Argument file_type, = %s, is not valid, valid arguments include text, fasta, fastq.' % str(file_type))
    if seq_type and seq_type not in qc.seqtypes:
        raise SortSeqError('seq_type %s is invalid' % str(seq_type))
    if file_type == 'fasta':
        if not seq_type:
            raise SortSeqError('Seqtype unspecified while fasta file.')
        colname = qc.seqtype_to_seqcolname_dict[seq_type]
        df = pd.io.parsers.read_csv(file_arg, lineterminator='>', engine='c', names='s')
        df.rename(columns={'s': colname}, inplace=True)
        df.loc[:, colname] = df.loc[:, colname].apply(format_fasta)
    elif file_type == 'fastq':
        if not seq_type:
            seq_type = 'dna'
        if seq_type != 'dna':
            raise SortSeqError('seq_type=%s is incompatible with file_type="fastq"' % seq_type)
        colname = qc.seqtype_to_seqcolname_dict[seq_type]
        temp_df = pd.io.parsers.read_csv(file_arg, engine='c', names='s')
        temp_df.rename(columns={'s': colname}, inplace=True)
        df = pd.DataFrame(columns=[colname])
        df.loc[:, colname] = temp_df.loc[1::4, colname]
        df.reset_index(inplace=True, drop=True)
    elif file_type == 'text':
        df = load_text(file_arg)
        if seq_type:
            colname = qc.seqtype_to_seqcolname_dict[seq_type]
        if seq_type and colname not in df.columns:
            raise SortSeqError('Column %s is not in dataframe' % str(colname))
    else:
        raise SortSeqError('Unrecognized filetype %s' % file_type)
    if not df.shape[0] >= 1:
        SortSeqError('No data was loaded.')
    if any([ qc.is_col_type(col, ['seqs', 'tag']) for col in df.columns ]):
        ct_cols = [ col for col in df.columns if qc.is_col_type(col, 'cts') ]
        if len(ct_cols) == 0:
            df['ct'] = 1
        elif 'ct' not in ct_cols:
            df['ct'] = df.loc[:, ct_cols].sum(axis=1)
    return qc.validate_dataset(df, fix=True)


def load_contigs_from_fasta(file_arg, model_df, chunksize=10000, circular=False):
    L = model_df.shape[0]
    contig_list = []
    inloc = validate_file_for_reading(file_arg)
    for i, record in enumerate(SeqIO.parse(inloc, 'fasta')):
        name = record.name if record.name else 'contig_%d' % i
        full_contig_str = str(record.seq)
        if circular:
            full_contig_str += full_contig_str[:L - 1]
        start = 0
        end = start + chunksize + L - 1
        while end < len(full_contig_str):
            contig_str = full_contig_str[start:end]
            contig_list.append((contig_str, name, start))
            start += chunksize
            end = start + chunksize + L - 1

        contig_str = full_contig_str[start:]
        contig_list.append((contig_str, name, start))

    return contig_list


@handle_errors
def load_model(file_arg):
    if file_arg == 'crp_model.txt':
        file_arg = './mpathic/data/sortseq/full-0/crp_model.txt'
    return load(file_arg, file_type='model')


def load_filelist(file_arg):
    return load(file_arg, file_type='filelist')


def load_tagkey(file_arg):
    return load(file_arg, file_type='tagkey')


def load_profile_ct(file_arg):
    return load(file_arg, file_type='profile_ct')


def load_profile_freq(file_arg):
    return load(file_arg, file_type='profile_freq')


def load_profile_mut(file_arg):
    return load(file_arg, file_type='profile_mut')


def load_profile_info(file_arg):
    return load(file_arg, file_type='profile_info')


def load_meanstd(file_arg):
    return load(file_arg, file_type='meanstd')


def load_sitelist(file_arg):
    return load(file_arg, file_type='sitelist')


def load(file_arg, file_type, **kwargs):
    """ Loads file of any specified type
    """
    validate_func_dict = {'model': qc.validate_model, 
       'filelist': qc.validate_filelist, 
       'tagkey': qc.validate_tagkey, 
       'profile_ct': qc.validate_profile_ct, 
       'profile_freq': qc.validate_profile_freq, 
       'profile_mut': qc.validate_profile_mut, 
       'profile_info': qc.validate_profile_info, 
       'meanstd': qc.validate_meanstd, 
       'sitelist': qc.validate_sitelist}
    df = load_text(file_arg)
    if 'dataset' in file_type:
        raise SortSeqError('file_type %s is not supported in load()' % file_type)
    if file_type not in validate_func_dict.keys():
        raise SortSeqError('Unrecognized file_type %s' % file_type)
    func = validate_func_dict[file_type]
    return func(df, fix=True, **kwargs)


def write(df, file_arg, fast=False):
    """ Writes a data frame to specified file, given as name or handle
    """
    file_handle = validate_file_for_writing(file_arg)
    if fast:
        df.to_csv(file_handle, sep='\t', float_format='%10.6f')
    else:
        pd.set_option('max_colwidth', int(1000000.0))
        df_string = df.to_string(index=False, col_space=5, float_format=utils.format_string)
        file_handle.write(df_string + '\n')
        file_handle.close()