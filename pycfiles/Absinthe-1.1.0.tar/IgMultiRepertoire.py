# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgMultiRepertoire/IgMultiRepertoire.py
# Compiled at: 2019-04-23 02:08:32
from __future__ import print_function
import os, sys, math
from multiprocessing import Queue, cpu_count
from abseqPy.config import AUX_FOLDER
from abseqPy.IgMultiRepertoire.AbSeqWorker import AbSeqWorker, AbSeqWorkerException, ResourcePool
from abseqPy.IgRepertoire.IgRepertoire import IgRepertoire
from abseqPy.argsParser import parseYAML, parseArgs

class IgMultiRepertoire:

    def __init__(self, args):
        self.result = Queue()
        self.buffer = []
        if args.yaml is not None:
            outdirs = set()
            for yamlArg in parseYAML(args.yaml):
                arg = parseArgs(yamlArg)
                arg.outdir = os.path.abspath(arg.outdir) + os.path.sep
                outdirs.add(arg.outdir)
                arg.log = os.path.join(arg.outdir, AUX_FOLDER, arg.name, arg.name + '.log')
                self.buffer.append(IgRepertoire(**vars(arg)))

        else:
            args.log = os.path.join(args.outdir, AUX_FOLDER, args.name, ('{}.log').format(args.name))
            self.buffer.append(IgRepertoire(**vars(args)))
        self.sampleCount = len(self.buffer)
        availCPUs = cpu_count()
        requestedCPU = sum([ s.threads for s in self.buffer ])
        if availCPUs and requestedCPU > availCPUs:
            cappedCPU = math.floor(availCPUs * 0.8)
            print(('Detected {} available CPUs but jobs are running {} processes in total.').format(availCPUs, requestedCPU))
            print(('Capping total processes to {}.').format(cappedCPU))
            print("Please refer to abseqPy's README, under the 'Gotcha' section to learn more about this message.")
            perSampleProcess = int(math.floor(cappedCPU * 1.0 / len(self.buffer)))
            for sample in self.buffer:
                sample.threads = max(perSampleProcess, 1)
                sample.args['threads'] = sample.threads

            assert sum([ s.threads for s in self.buffer ]) <= cappedCPU or all([ s.threads == 1 for s in self.buffer ])
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.result.close()
        self.result.join_thread()

    def start(self):
        resourcePool = ResourcePool(0)
        workers = [ AbSeqWorker(rep, self.result, resourcePool) for rep in self.buffer ]
        try:
            try:
                for w in workers:
                    w.start()

                for i in range(self.sampleCount):
                    res = self.result.get()
                    if isinstance(res, tuple):
                        raise AbSeqWorkerException(*res)
                    self.buffer.append(res)

                for w in workers:
                    w.join()

            except AbSeqWorkerException as e:
                print(('\n\n{}').format(e.errors), file=sys.stderr)
                print('\n\nSomething went horribly wrong while trying to run AbSeq!', file=sys.stderr)
                print('GeneralWorker stacktrace:', file=sys.stderr)
                print('-' * 120, file=sys.stderr)
                print(e.tracebackMsg, file=sys.stderr)
                print('-' * 120, file=sys.stderr)
                raise e
            except Exception as e:
                raise e

        finally:
            for w in workers:
                w.terminate()