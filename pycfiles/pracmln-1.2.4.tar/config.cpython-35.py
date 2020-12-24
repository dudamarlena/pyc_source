# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/utils/config.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 2771 bytes
from dnutils import logs
logger = logs.getlogger(__name__)
fixed_width_font = ('Monospace', -12)
learn_config_pattern = '%s.learn.conf'
query_config_pattern = '%s.query.conf'
global_config_filename = '.pracmln.conf'
learnwts_mln_filemask = '*.mln'
learnwts_db_filemask = '*.db'

def learnwts_output_filename(infile, method, dbfile):
    if infile[:3] == 'in.':
        infile = infile[3:]
    elif infile[:4] == 'wts.':
        infile = infile[4:]
    if infile[-4:] == '.mln':
        infile = infile[:-4]
    if dbfile[-3:] == '.db':
        dbfile = dbfile[:-3]
    return 'learnt.%s.%s-%s.mln' % (method, dbfile, infile)


learnwts_full_report = True
learnwts_report_bottom = True
learnwts_edit_outfile_when_done = False
query_mln_filemask = '*.mln'
emln_filemask = '*.emln'
query_db_filemask = ['*.db', '*.blogdb']

def query_output_filename(mlnfile, method, dbfile):
    if mlnfile[:4] == 'wts.':
        mlnfile = mlnfile[4:]
    if mlnfile[-4:] == '.mln':
        mlnfile = mlnfile[:-4]
    if dbfile[-3:] == '.db':
        dbfile = dbfile[:-3]
    return '%s.%s-%s.results' % (method, dbfile, mlnfile)


query_edit_outfile_when_done = False