# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sling/data/remove_domains_to_ignore.py
# Compiled at: 2018-05-09 04:07:50
to_ignore = []
with open('domains_to_ignore.txt') as (f):
    for line in f:
        to_ignore.append(line.strip())

def rewrite_hmms(hmm_file_in, hmm_file_out):
    out = open(hmm_file_out, 'w')
    hmm_file_full = open(hmm_file_in).read()
    hmms = hmm_file_full.split('//')
    for hmm in hmms:
        for line in hmm.split('\n'):
            if line.startswith('NAME'):
                toks = line.split()
                if toks[1] not in to_ignore:
                    out.write(hmm + '//\n')
                break

    out.close()


rewrite_hmms('toxins', 'toxins_new')
rewrite_hmms('RND_pump', 'RND_new')