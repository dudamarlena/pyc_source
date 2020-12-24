# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/Merge.dataset.py
# Compiled at: 2019-12-11 00:39:51
# Size of source mod 2**32: 2775 bytes
import os, argparse, glob
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-t', help='trait name',
  type=str,
  default='ARG',
  metavar='trait name')
parser.add_argument('--r', help='input directory or folder of your previous results by Traits_WGD.py',
  type=str,
  default='Result',
  metavar='Result',
  nargs='+')
files_to_merge = dict()
args = parser.parse_args()
result_dir = args.r[0]
merge_dir = os.path.join(result_dir, 'merge')
try:
    os.mkdir(merge_dir)
except OSError:
    pass

print('merge results can be found in %s' % merge_dir)
merge_dir = os.path.join(merge_dir, 'summary')
try:
    os.mkdir(merge_dir)
except OSError:
    pass

merge_list = [
 args.t + '.all.traits.aa.fasta', args.t + '.all.traits.dna.fasta',
 args.t + '.all.traits.dna.txt', args.t + '.all.traits.aa.txt',
 args.t + '.all.16S.fasta']
result_dir = os.path.join(result_dir, 'summary')
summary_files = glob.glob(os.path.join(result_dir, args.t + '.all.traits.*.summarize.*.txt'))
for files in summary_files:
    merge_list.append(os.path.split(files)[(-1)])

for result_dir in args.r:
    result_dir = os.path.join(result_dir, 'summary')
    extra_file = glob.glob(os.path.join(result_dir, args.t + '.all.traits.dna.extra*.fasta'))
    if extra_file != []:
        if args.t + '.all.traits.dna.extra500.fasta' not in files_to_merge:
            files_to_merge.setdefault(args.t + '.all.traits.dna.extra500.fasta', [
             extra_file[0]])
        else:
            files_to_merge[(args.t + '.all.traits.dna.extra500.fasta')].append(extra_file[0])
    for file_name in merge_list:
        try:
            ftest = open(os.path.join(result_dir, file_name), 'r')
            if file_name not in files_to_merge:
                files_to_merge.setdefault(file_name, [
                 os.path.join(result_dir, file_name)])
            else:
                files_to_merge[file_name].append(os.path.join(result_dir, file_name))
        except IOError:
            pass

for file_name in files_to_merge:
    os.system('cat %s > %s' % (' '.join(files_to_merge[file_name]), os.path.join(merge_dir, file_name)))