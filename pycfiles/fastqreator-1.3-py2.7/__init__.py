# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/fastqreator/__init__.py
# Compiled at: 2016-12-07 23:02:30
import os, sys, io
SEQGO = 'BEGIN_SEQUENCE'
HEADER = 'BEGIN_COMMENT'
GO = 'BEGIN_DNA'
STOP = 'END_DNA'
SEQSTOP = 'END_SEQUENCE'
DIRPATH = ' '
INFILE = ' '
INPUT = ' '
seq_1 = ' '
seq_2 = ' '
score_1 = ' '
score_2 = ' '
nuc_acids = [
 'A', 'C', 'G', 'T', 'U', 'R', 'Y', 'K', 'M',
 'S', 'W', 'B', 'D', 'H', 'V', 'N', '-']
ascii_scale = [
 '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>',
 '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\',
 ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
 '{', '|', '}', '~']
in_files = []
out_files = []
crpt_files = []
usr_flags = []

def dirOrFile(INFILE):
    if os.path.isdir(INFILE):
        print '\t[*]\tUsing Directory: %s' % INFILE
        for filename in os.listdir(INFILE):
            if filename.endswith('.phd.1'):
                in_files.append(filename)

    elif os.path.isfile(INFILE):
        print '\t[*]\tReading File: %s' % INFILE


def checkFile(line):
    if SEQGO in line:
        pass
    elif SEQGO not in line:
        print '\t\t[-] ERROR_5: Check source file, missing %s.' % SEQGO
        sys.exit(5)
    else:
        print '\t\t[-] ERROR_2 in source file.'
        sys.exit(2)


def readData(line, f, dna_seq, q_score):
    if STOP in line:
        for line in f:
            pass

    elif any(s in line for s in nuc_acids):
        CHAR = line[:1]
        dna_seq.append(CHAR)
        SCORE = int(line.split()[1])
        q_score.append(ascii_scale[SCORE])
        return (
         q_score, dna_seq)


def writeNewFile(INFILE, dna_seq, q_score, TITLE):
    OUTFILE = INFILE[:-6] + '.fastq'
    dna_string = ('').join(dna_seq)
    if 'NNNNN' in dna_string:
        crpt_files.append(OUTFILE)
        return
    tmp_line = '@' + TITLE
    first_line = tmp_line.rstrip()
    ascii_scale = ('').join(q_score)
    with io.FileIO(OUTFILE, 'w+') as (fout):
        try:
            fout.write(first_line + '\n' + dna_string + '\n' + '+\n' + ascii_scale + '\n')
        except IOError:
            print '\t\t[-] Error, cannot open %s for writing.' % OUTFILE
        else:
            out_files.append(OUTFILE)


def fileGen(FILE):
    dna_seq = []
    q_score = []
    TITLE_MARKER = 'CHROMAT_FILE:'
    TITLE = ' '
    with open(FILE, 'r') as (f):
        for line in f:
            if SEQGO in line:
                checkFile(line)
            elif TITLE_MARKER in line:
                TITLE = line[14:]
            elif GO in line:
                for line in f:
                    readData(line, f, dna_seq, q_score)

    writeNewFile(FILE, dna_seq, q_score, TITLE)


def getInput():
    global DIRPATH
    global INFILE
    for i in sys.argv:
        if i.startswith('-'):
            usr_flags.append(i)
        if i.endswith('.phd.1') or i.endswith('.fastq'):
            print 'Found file.'
            in_files.append(i)
        elif not i.endswith('.py') and i.endswith('/'):
            print '\t[*]\tNo PHRED files found, directory was passed.'
            INFILE = i
            DIRPATH = i
        elif None:
            print "If passing a directory, please include the tailing '/'"

    return INFILE


def concatFiles(file_1, file_2):
    OUTF = '@' + file_1 + '&' + file_2
    for file in (file_1, file_2):
        with open(file) as (f):
            COUNT = 0
            for i, line in enumerate(f):
                COUNT += 1
                if i == 2:
                    if COUNT == 1:
                        d[seq_1] = line
                    elif COUNT == 2:
                        d[seq_2] = line
                elif i == 4:
                    if COUNT == 1:
                        d[score_1] = line
                    elif COUNT == 2:
                        d[score_2] = line

    with io.FileIO(OUTF.lstrip('@'), 'w+') as (fout):
        try:
            fout.write(OUTF + '\n' + seq_1 + seq_2 + '\n' + '+ \n' + score_1 + score_2 + '\n')
        except IOError:
            print '\t\t[-] Error, cannot open %s for writing.' % OUTF
        else:
            print '\n\t\tComplete. Check working directory for %s.\n' % OUTF


getInput()
if not usr_flags:
    FLAGS = (' ').join(usr_flags)
    print '\t[*]\tRunning with flags: %s' % FLAGS
    dirOrFile(INFILE)
    if len(in_files) > 1:
        for i in in_files:
            INPUT = DIRPATH + i
            fileGen(INPUT)

    elif len(in_files) == 1:
        print 'Using one input file: %s' % INFILE
        INFILE = in_files[0]
        fileGen(INFILE)
    else:
        print '\t\t[-] Error: Parse found neither a populated nor empty in_files list.'
    print '\t[+]\t[%d] files were created under %s' % (len(out_files), DIRPATH)
    with io.FileIO(DIRPATH + 'invalid_source_log', 'w+') as (log_crpt):
        try:
            COUNT = 0
            for i in crpt_files:
                log_crpt.write(crpt_files[COUNT] + '\n')
                COUNT += 1

        except IOError:
            print "Could not write 'invalid_source_files'."
        else:
            print "\t[*]\t[%d] Invalid 'NNNNN' input files have been logged in 'invalid_source-files'." % len(crpt_files)

elif '-C' or '-c' in usr_flags:
    if len(in_files) == 1:
        print '\t\t[-] ERROR: Concatenatio requires two input files.'
        sys.exit(1)
    else:
        print in_files
        d = {}
        concatFiles(in_files[0], in_files[1])
elif '-h' in sur_flags:
    with io.FileIO('README', 'r') as (help):
        print help