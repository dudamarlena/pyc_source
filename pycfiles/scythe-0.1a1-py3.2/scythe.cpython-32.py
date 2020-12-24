# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scythe/scythe.py
# Compiled at: 2014-06-16 04:49:17
import imp, sys, subprocess, os, glob, getopt, re
from itertools import chain
import configparser, datetime
from helpers.grphelper import GrpParser
from helpers.scythecore import ScytheSpec
from helpers.scythecore import ScytheGroupMap, ScytheGroup
from helpers.scythecore import ScytheFrame
from helpers.scythecore import AutoVD
from helpers.fastahelper import FastaParser
from algo.algomod import AlgoHandler
from algo.algomod import EmptyScoringDctException, EmptySequenceDctException
import threading, time, queue, multiprocessing
logo = '\n          _____            __  __\n         / ___/_______  __/ /_/ /_  ___\n         \\__ \\/ ___/ / / / __/ __ \\/ _ \\\n        ___/ / /__/ /_/ / /_/ / / /  __/\n       /____/\\___/\\__, /\\__/_/ /_/\\___/\n                 /____/'

def usage():
    print('\n    ######################################\n    # scythe.py v0.1a1                   #\n    ######################################\n  usage:\n     scythe.py -i DIR -g .grpFILE --cleanup\n\n  usage with configuration file:\n     scythe.py --config configuration.scy\n\n  general options:\n    -C, --config                     use configuration file instead of\n                                     command line parameters\n    -c, --cleanup                    remove temporary files when done\n    -h, --help                       prints this\n    -i, --in_dir=DIR                 folder w/ subfolders "fa" and "loc"\n\n    -o, --out_dir=DIR                output directory [default:./]\n    -N, --num_cores=NUM              number of processors to use [default 1]\n    -v, --verbose                    be wordy\n\n algorithm options:\n    -R, --sl_ref                     find best matches to reference\n    -G, --sl_glob                    best scoring pair as seed\n    -M, --mx_sum                     optimize sum of pairwise scores\n\n\n  alignment options:\n     -O, --gap_open=FLOAT           needleall gap opening cost [default 10]\n     -E, --gap_extend=FLOAT         needleall gap extension cost\n\n  fasta options:\n    -d, --delim=STRING               split fasta headers at STRING\n    -a, --asID=INT                   use INTth part of fasta header as transcript-ID\n                                     (default:0)\n\n  further help:\n    Please see documentation.\n    ')
    sys.exit(2)


def parseConfig(pathconfig):
    global GLOBMAX
    global GLOBSUM
    VERBOSE = False
    CF_MODE = 'Mode'
    CF_MODE_use_ensembl = 'use_ensembl'
    CF_MODE_use_local_files = 'use_local_files'
    CF_PATHS = 'Paths'
    CF_PATHS_fasta_directory = 'fasta_directory'
    CF_PATHS_loc_directory = 'loc_directory'
    CF_PATHS_grp_file = 'grp_file'
    CF_PATHS_output_directory = 'output_directory'
    CF_CLEANUP = 'Cleanup'
    CF_CLEANUP_clean_up_directories = 'clean_up_directories'
    CF_RUN = 'Run_options'
    CF_RUN_num_CPU = 'num_CPU'
    CF_RUN_split_input = 'split_input'
    CF_PENALTIES = 'Penalties'
    CF_PENALTIES_gap_open_cost = 'gap_open_cost'
    CF_PENALTIES_gap_extend_cost = 'gap_extend_cost'
    CF_PENALTIES_substitution_matrix = 'substitution_matrix'
    CF_ALGORITHM = 'Algorithm'
    CF_ALGORITHM_use_global_max = 'use_sl_glob'
    CF_ALGORITHM_use_default = 'use_sl_ref'
    CF_ALGORITHM_use_global_sum = 'use_mx_sum'
    CF_FASTAHEADER = 'Fasta_header'
    CF_FASTAHEADER_delimiter = 'fasta_header_delimiter'
    CF_FASTAHEADER_part = 'fasta_header_part'
    config = configparser.ConfigParser()
    config.read(pathconfig)
    if config.get(CF_ALGORITHM, CF_ALGORITHM_use_global_max) != 'yes':
        GLOBMAX = False
    else:
        GLOBMAX = True
    if config.get(CF_ALGORITHM, CF_ALGORITHM_use_global_sum) != 'yes':
        GLOBSUM = False
    else:
        GLOBSUM = True
    if config.get(CF_ALGORITHM, CF_ALGORITHM_use_default) != 'yes':
        SL_REF = False
    else:
        SL_REF = True
    if sum([GLOBMAX, GLOBSUM, SL_REF]) > 1:
        sys.stderr.write('Problem with you config file. Please select one algorithm.\n')
        sys.exit(1)
    else:
        if sum([GLOBMAX, GLOBSUM, SL_REF]) < 1:
            sys.stderr.write('Problem with you config file. Please select one algorithm ( ...  = "yes").\n')
            sys.exit(1)
        if config.get(CF_CLEANUP, CF_CLEANUP_clean_up_directories) != 'yes':
            cleanUp = False
        else:
            cleanUp = True
    groups = config.get(CF_PATHS, CF_PATHS_grp_file)
    namesList = None
    faDir = config.get(CF_PATHS, CF_PATHS_fasta_directory)
    inDir = faDir
    outDir = config.get(CF_PATHS, CF_PATHS_output_directory)
    locDir = config.get(CF_PATHS, CF_PATHS_loc_directory)
    fastaList = os.listdir(faDir)
    delim = config.get(CF_FASTAHEADER, CF_FASTAHEADER_delimiter)
    asID = int(config.get(CF_FASTAHEADER, CF_FASTAHEADER_part))
    gapOpen = config.get(CF_PENALTIES, CF_PENALTIES_gap_open_cost)
    gapExtend = config.get(CF_PENALTIES, CF_PENALTIES_gap_extend_cost)
    numCPU = int(config.get(CF_RUN, CF_RUN_num_CPU))
    faFileList = os.listdir(faDir)
    namesList = os.listdir(faDir)
    namesList = [n[0:3] for n in namesList]
    runScythe(groups=groups, delim=delim.strip('"'), asID=asID, faFileList=faFileList, namesList=namesList, cleanUp=cleanUp, inDir=inDir, outDir=outDir, gapOpen=gapOpen, gapExtend=gapExtend, locDir=locDir, faDir=faDir, numCPU=numCPU)
    return


def makeFasta(listofspecies, group, frame, stopAfter, gapOpen, gapExtend, task, startAt=None):
    groupList = [g for i, g in enumerate(group.groups) if int(i) < stopAfter and int(i) >= startAt]
    print('group', groupList)
    singles = {}
    skip = {}
    allSpec = set()
    pattern = re.compile('(.*)\\s+([a-zA-Z0-9_.]*)\\s+[a-zA-Z0-9_.]*\\s+\\((.*)\\)')
    outfile = None
    sp = {}
    ah = AlgoHandler()
    for l in listofspecies:
        sp[l.name] = l

    for g in groupList:
        seqDct = {}
        spl = list(group.groups[g])
        allSpec = set(spl)
        singles[g] = set()
        for s in spl:
            outfile = frame._fat + '.'.join([str(g), s, 'fa'])
            out = open(outfile, 'w')
            spa = group.groups[g][s]
            if len(spa) == 1:
                singles[g].add(s)
            for locus in spa:
                try:
                    out.write(sp[s].sequences[locus].toFasta())
                    seqDct[sp[s].sequences[locus].name] = sp[s].sequences[locus]
                except KeyError as ke:
                    print('Are all gene models in your fasta files? - KeyError for ', ke)
                    return (None, None)

            out.close()

        if len(singles[g]) == len(spl):
            print('SKIP ', g)
            skip[g] = True
        else:
            skip[g] = False
        if skip[g]:
            print('SKIP', g)
            return (
             (
              seqDct, set([x.name for x in seqDct.values()]), 'SKIP'), str(g))
        else:
            avd = None
            avd = AutoVD()
            spl = list(set(group.groups[g]))
            for i in range(0, len(spl)):
                for j in range(i + 1, len(spl)):
                    outfile = frame._fat + '.'.join([str(g), spl[i], 'fa'])
                    fileA = outfile
                    outfile = frame._fat + '.'.join([str(g), spl[j], 'fa'])
                    fileB = outfile
                    outfile = frame._sr + '.'.join([str(g), spl[i], spl[(i + 1)], 'needle'])
                    try:
                        task = frame.callNeedleAll(fileA, fileB, outfile=outfile, stdout=True, gapOpen=gapOpen, gapExtend=gapExtend)
                        fulldata = task.stdout.read()
                        assert task.wait() == 0
                        task.stdout.close()
                    except AssertionError as ae:
                        sys.stderr.write(ae)
                        data = '#'
                        sys.stderr.write('WARNING:', fileA, fileB, 'excluded')
                        frame.writeLog('error', 'WARNING:' + fileA + ' ' + fileB + ' excluded, AssertionError')
                        return (None, None)

                    data = fulldata.decode('utf-8')
                    for l in data.split('\n'):
                        if l.startswith('#'):
                            break
                        else:
                            tmp = pattern.findall(l)
                            if tmp:
                                res = tmp[0]
                                score = int(float(res[2]) * 10)
                                avd[res[0]][res[1]] = score
                                avd[res[1]][res[0]] = score
                                continue

            if GLOBSUM:
                r = ah.mx_sum(scoringDct=avd, sequenceDct=seqDct)
                R = str(g)
                return (
                 r, R)
            if GLOBMAX:
                r = ah.sl_glob(scoringDct=avd, sequenceDct=seqDct)
                R = str(g)
                return (
                 r, R)
            r, R = ah.sl_ref(scoringDct=avd, sequenceDct=seqDct), str(g)
            return (r, R)

    return


class ConsumerProc(multiprocessing.Process):
    counter = 0

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        ConsumerProc.counter += 1

    def run(self):
        SEMAPHORE.acquire()
        proc_name = self.name
        print('started\n', ConsumerProc.counter)
        while True:
            next_task = self.task_queue.get()
            if next_task == 'done':
                print('exit', self.name)
                break
            r, R = next_task.call()
            self.result_queue.put((r, R))

        SEMAPHORE.release()
        return ()


class Task(object):

    def __init__(self, listofspecies, group, frame, stopAfter, gapOpen, gapExtend, task, startAt):
        self.listofspecies = listofspecies
        self.group = group
        self.frame = frame
        self.stopAfter = stopAfter
        self.gapOpen = gapOpen
        self.gapExtend = gapExtend
        self.task = task
        self.startAt = startAt

    def call(self):
        r, R = makeFasta(listofspecies=self.listofspecies, group=self.group, frame=self.frame, stopAfter=self.stopAfter, gapOpen=self.gapOpen, gapExtend=self.gapExtend, task=self.task, startAt=self.startAt)
        return (r, R)


def runScythe(groups, delim, asID, namesList, cleanUp, faFileList, inDir, outDir, gapOpen, gapExtend, locDir=None, faDir=None, numCPU=1, startAt=0):
    global SEMAPHORE
    global outDctOg
    global outDctSp
    timeStarted = time.time()
    print('Started {}\n'.format(timeStarted))
    print('NUM_CPU', numCPU)
    SEMAPHORE = multiprocessing.BoundedSemaphore(numCPU)
    print(delim, asID, locDir, faDir, inDir)
    specsList = []
    grpMapList = []
    if locDir:
        if not locDir.endswith(os.sep):
            locDir = locDir + os.sep
    if faDir:
        if not faDir.endswith(os.sep):
            faDir = faDir + os.sep
    if locDir:
        locFileList = os.listdir(locDir)
    else:
        locFileList = os.listdir(inDir + os.sep + 'loc')
    if groups:
        if locDir:
            locfl = [locDir + x for x in locFileList]
        else:
            locfl = [inDir + os.sep + 'loc' + os.sep + x for x in locFileList]
        dct = GrpParser().groupDct(groups, locf=locfl)
    else:
        usage()
    for n, f in zip(namesList, faFileList):
        print(n, f, 'match')
        if locDir:
            locFileList = os.listdir(locDir)
        else:
            locFileList = os.listdir(inDir + os.sep + 'loc' + os.sep)
        locFileListtmp = locFileList
        pf = '.'.join(f.split('.')[:-1])
        pf = pf.split('_')[0]
        locFileList = [x for x in locFileList if x.startswith(pf)]
        if len(locFileList) < len(faFileList):
            locFileList = [x for x in locFileListtmp if x.startswith(pf[0:3])]
        n = n.strip()
        if locDir:
            specsList.append(ScytheSpec(name=n, format='loc', source=locDir + locFileList[0], fasta=faDir + f))
        else:
            specsList.append(ScytheSpec(name=n, format='loc', source=inDir + os.sep + 'loc' + os.sep + locFileList[0], fasta=inDir + os.sep + 'fa' + os.sep + f))
        if locDir:
            grpMapList.append(ScytheGroupMap(name=n, locfile=locDir + locFileList[0], dct=dct, separator=delim, asID=asID))
        else:
            grpMapList.append(ScytheGroupMap(name=n, locfile=inDir + os.sep + 'loc' + os.sep + locFileList[0], dct=dct, separator=delim, asID=asID))

    for g in grpMapList:
        g.free()

    for sp in specsList:
        sp.fillLociCDS()
        sp.fillSequences(sep=delim, asID=asID)
        sp.fillDefForm()

    grp = ScytheGroup('tmpgrp', grpMapList)
    frame = ScytheFrame(path=outDir)
    frame.mkAllDirs()
    outfiles = {}
    outfilesGroups = {}
    outDctSp = {}
    outDctOg = {}
    for s in specsList:
        outfile = frame._srfa + '.'.join([s.name, 'fa'])
        outDctSp[frame._srfa + '.'.join([s.name, 'fa'])] = []
        outfile = frame._srfa + '.'.join([s.name, 'skipped.fa'])
        outDctSp[frame._srfa + '.'.join([s.name, 'skipped.fa'])] = []

    taskQueue = multiprocessing.JoinableQueue()
    resQueue = multiprocessing.JoinableQueue()
    num_consumers = numCPU
    consumers = [ConsumerProc(taskQueue, resQueue) for i in range(num_consumers)]
    for c in consumers:
        c.start()

    num_jobs = len(grp.groups)
    print('{} groups are being processed.\n'.format(num_jobs))
    for i in range(0, num_jobs):
        taskQueue.put(Task(listofspecies=specsList, group=grp, frame=frame, stopAfter=i + 1, gapOpen=gapOpen, gapExtend=gapExtend, task='needleall', startAt=i))

    for i in range(0, num_consumers):
        taskQueue.put('done')

    resQueue.join()
    taskQueue.close()
    inMem = 0
    while num_jobs:
        r, R = resQueue.get()
        num_jobs -= 1
        inMem += 1
        if r[2] == 'SKIP':
            outfileGroup = frame._srofa + '.'.join([R, 'skipped', 'fa'])
            outDctOg[outfileGroup] = []
        else:
            outfileGroup = frame._srofa + '.'.join([R, 'fa'])
            outDctOg[outfileGroup] = []
        for s in specsList:
            tmp = r[1]
            ok = [x for x in tmp if x in s.cds]
            if ok:
                ok = ok[0]
                if not r[2] == 'SKIP':
                    outDctSp[(frame._srfa + '.'.join([s.name, 'fa']))].append(r[0][ok].toFasta())
                    outDctOg[(frame._srofa + '.'.join([R, 'fa']))].append(r[0][ok].toFasta())
                else:
                    outDctSp[(frame._srfa + '.'.join([s.name, 'skipped.fa']))].append(r[0][ok].toFasta())
                    outDctOg[(frame._srofa + '.'.join([R, 'skipped', 'fa']))].append(r[0][ok].toFasta())
                    continue

        if inMem >= 10:
            inMem = 0
            print('Writing files\n')
            for g in outDctOg:
                with open(g, 'w') as (gh):
                    for e in outDctOg[g]:
                        gh.write(e)

            print('...\n')
            for g in outDctSp:
                with open(g, 'a') as (gh):
                    for e in outDctSp[g]:
                        gh.write(e)

            outDctOg.clear()
            for k in outDctSp:
                outDctSp[k] = []

            continue

    print('Writing files...\n')
    for g in outDctOg:
        with open(g, 'w') as (gh):
            for e in outDctOg[g]:
                gh.write(e)

    print('...\n')
    for g in outDctSp:
        with open(g, 'a') as (gh):
            for e in outDctSp[g]:
                gh.write(e)

    print('Cleaning up... \n')
    if cleanUp:
        frame.cleanUp()
    timeEnded = time.time()
    print('Time: ', timeEnded, '\n')
    print('Time taken: {}\n'.format(timeEnded - timeStarted))
    print('Done.\n')


def main():
    global GLOBMAX
    global GLOBSUM
    global SL_REF
    global VERBOSE
    VERBOSE = None
    GLOBMAX = False
    GLOBSUM = False
    SL_REF = False
    cleanUp = False
    groups = None
    namesList = None
    inDir = None
    outDir = './'
    fastaList = None
    gffList = None
    delim = None
    asID = 0
    gapOpen = str(10)
    gapExtend = str(0.5)
    isUsingConfig = False
    numCPU = 1
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'C:i:g:o:d:a:O:E:N:RGMcvh', [
         'config=',
         'in_dir=',
         'groups=',
         'out_dir=',
         'delim=',
         'asID=',
         'gap_open=',
         'gap_extend=',
         'num_cores = ',
         'sl_ref',
         'sl_glob',
         'mx_sum',
         'cleanup',
         'verbose',
         'help'])
    except getopt.GetoptError as err:
        print(str(err))
        print(logo)
        usage()

    for o, a in opts:
        if o in ('-C', '--config'):
            print(logo)
            parseConfig(a)
            isUsingConfig = True
        elif o in ('-i', '--in_dir'):
            inDir = a
            if not inDir.endswith(os.sep):
                inDir = inDir + os.sep
        elif o in ('-o', '--outdir'):
            outDir = a
        elif o in ('-d', '--delim'):
            delim = a
        elif o in ('-a', '--asID'):
            asID = int(a)
        elif o in ('-g', '--groups'):
            groups = a
        elif o in ('-v', '--verbose'):
            VERBOSE = True
        elif o in ('-c', '--cleanup'):
            cleanUp = True
        elif o in ('-R', '--sl_ref'):
            SL_REF = True
        elif o in ('-G', '--sl_glob'):
            GLOBMAX = True
        elif o in ('-M', '--mx_sum'):
            GLOBSUM = True
        elif o in ('-O', '--gap_open'):
            gapOpen = a
        elif o in ('-E', '--gap_extend'):
            gapExtend = a
        elif o in ('-N', '--num_cores'):
            numCPU = int(a)
        elif o in ('-h', '--help'):
            usage()
        elif not False:
            raise AssertionError('unhandled option')

    if not isUsingConfig:
        if VERBOSE:
            for o, a in opts:
                if o in ('-v', '--verbose', '-c', '--cleanup'):
                    print(o, 'set')
                else:
                    print(o, 'set to', a)

        if not (inDir and groups):
            print(logo)
            usage()
        try:
            print(os.listdir(inDir + 'fa'))
            print(os.listdir(inDir + 'loc'))
        except OSError as e:
            sys.stderr.write(str(e))
            print("Please provide a directory containing folders 'fa' with fasta files and 'loc' with .loc files.\nAlternatively, use Scythe with gui or configuration file\n")
            usage()

        faFileList = os.listdir(inDir + 'fa')
        namesList = os.listdir(inDir + 'fa')
        namesList = [n[0:3] for n in namesList]
        locDir = inDir + 'loc' + os.sep
        locFileList = os.listdir(locDir)
        faDir = inDir + 'fa' + os.sep
        faFileList = os.listdir(faDir)
        print('debug', locDir, locFileList)
        if len(faFileList) != len(namesList) or len(locFileList) != len(namesList):
            sys.stderr.write("Number of files doesn't match. Please check {} and {}\n".format(locDir, faDir))
            usage()
        runScythe(groups=groups, delim=delim, asID=asID, faFileList=faFileList, namesList=namesList, cleanUp=cleanUp, inDir=faDir, outDir=outDir, gapOpen=gapOpen, gapExtend=gapExtend, locDir=locDir, faDir=faDir, numCPU=numCPU)
    return


class ThreadedScythe(multiprocessing.Process):

    def __init__(self, queue, argdct):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.argdct = argdct

    def run(self):
        try:
            runScythe(**self.argdct)
            self.queue.put(1)
        except Exception as e:
            sys.stderr.write(str(e))
            sys.exit(1)


if __name__ == '__main__':
    main()