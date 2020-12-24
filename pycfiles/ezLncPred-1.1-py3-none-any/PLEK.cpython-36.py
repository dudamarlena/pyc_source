# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/PLEK/PLEK.py
# Compiled at: 2019-12-09 21:34:58
# Size of source mod 2**32: 18301 bytes
__all__ = [
 '']
import os, sys, traceback, getpass, time, re
from threading import Thread
from subprocess import *
from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style

class SVMScaleThread(Thread):

    def __init__(self, range_file, svm_origin, svm_scaled, script_dir):
        Thread.__init__(self)
        self.range_file = range_file
        self.svm_origin = svm_origin
        self.svm_scaled = svm_scaled
        self.script_dir = script_dir

    def run(self):
        cmdline = (self.script_dir + '../tools/libsvm/svm-scale -r {0} {1} > {2} ').format(self.range_file, self.svm_origin, self.svm_scaled)
        os.system(cmdline)


class SVMPredictThread(Thread):

    def __init__(self, svm_scaled, svm_model, predicted, script_dir):
        Thread.__init__(self)
        self.svm_scaled = svm_scaled
        self.svm_model = svm_model
        self.predicted = predicted
        self.script_dir = script_dir

    def run(self):
        cmdline = (self.script_dir + '../tools/libsvm/svm-predict {0} {1} {2} ').format(self.svm_scaled, self.svm_model, self.predicted)
        os.system(cmdline)


class GridOption:

    def __init__(self, options):
        dirname = os.path.dirname(__file__)
        self.svmtrain_pathname = os.path.join(dirname, 'svm-train')
        self.svmpredict_pathname = os.path.join(dirname, 'svm-predict')
        self.svmscale_pathname = os.path.join(dirname, 'svm-scale')
        self.pos_file = ''
        self.neg_file = ''
        self.prefix = 'plek_output_'
        self.svmrangefile = dirname + '/PLEK.range'
        self.is_posneg_balanced = 0
        self.thread_count = 5
        self.modelfile = dirname + '/PLEK.model'
        self.kmer = 5
        self.min_seq_length = 200
        self.unkown = 0
        self.is_recompile = 0
        self.input_type = 1
        self.isoutmsg = 0
        self.isrmtempfile = 1
        self.script_dir = dirname + '/'
        self.parse_options(options)

    def parse_options(self, options):
        args = options
        if type(options) == str:
            options = options.split()
        i = 0
        pass_through_options = []
        script_name = args[0]
        while i < len(options):
            if options[i] == '--input' or options[i] == '-i':
                i = i + 1
                self.pos_file = options[i]
                self.unkown = 1
            else:
                if options[i] == '--thread':
                    i = i + 1
                    self.thread_count = options[i]
                else:
                    if options[i] == '--output' or options[i] == '-o':
                        i = i + 1
                        self.prefix = options[i]
                    else:
                        if options[i] == '--size' or options[i] == '-z':
                            i = i + 1
                            self.min_seq_length = options[i]
                        else:
                            if options[i] == '--isoutmsg':
                                i = i + 1
                                self.isoutmsg = options[i]
                            else:
                                if options[i] == '--isrmtempfile':
                                    i = i + 1
                                    self.isrmtempfile = options[i]
                                else:
                                    if options[i] == '-pos':
                                        i = i + 1
                                        self.pos_file = options[i]
                                    else:
                                        if options[i] == '-neg':
                                            i = i + 1
                                            self.neg_file = options[i]
                                        else:
                                            if options[i] == '-range':
                                                i = i + 1
                                                self.svmrangefile = options[i]
                                            else:
                                                if options[i] == '-k':
                                                    i = i + 1
                                                    self.kmer = options[i]
                                                else:
                                                    if options[i] == '-model':
                                                        i = i + 1
                                                        self.modelfile = options[i]
                                                    else:
                                                        if options[i] == '-balance':
                                                            self.is_posneg_balanced = 1
                                                        else:
                                                            if options[i] == '-isrecompile':
                                                                i = i + 1
                                                                self.is_recompile = options[i]
                                                            else:
                                                                pass_through_options.append(options[i])
            i = i + 1

        self.pass_through_string = ' '.join(pass_through_options)


def main(options):

    def getModel(model, saveDir):
        print(Fore.CYAN + Style.BRIGHT + '------------------------------Start Loading----------------------------\n')
        modelAbsPath = saveDir + model
        print(modelAbsPath)
        if os.path.exists(modelAbsPath):
            print(Fore.CYAN + Style.BRIGHT + '----------------------------------Loading Completed-------------------------\n')
            return True
        else:
            choice = input(Fore.GREEN + Style.BRIGHT + 'Loading Failed! Do you want to download ' + model + ' from remote repository (51M) ? [y/n]' + '\x1b[39m')
            if choice == 'y':
                downURL = 'http://120.27.208.220/lncRNAPredModels/PLEK.model.tgz'
                downComm = 'wget -nv --show-progress -O ' + modelAbsPath + '.tgz ' + downURL
                os.system(downComm)
                print(Fore.CYAN + Style.BRIGHT + '\n-------------------------------Download Succeed!Now Decompressing---------------------------\n')
                extractComm = 'tar -xzf ' + modelAbsPath + '.tgz' + ' -C ' + saveDir
                os.system(extractComm)
                rmComm = 'rm ' + modelAbsPath + '.tgz'
                os.system(rmComm)
                if os.path.exists(modelAbsPath):
                    print(Fore.CYAN + Style.BRIGHT + '-----------------------------------------Loading Succeed----------------------------------------\n')
                    return True
            else:
                print(Fore.RED + Style.BRIGHT + '-----------------------------------------Loading Failed----------------------------------------\n')
            return False

    def file_id_by_lineid(totalcount, filecount, n):
        countperfile = totalcount / filecount
        for i in range(1, filecount):
            if n > (i - 1) * countperfile:
                if n <= i * countperfile:
                    return i

        return filecount

    def compile_c(_options):
        print('[{0}] Compiling svm, svm-train, svm-predict, svm-scale'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        os.system('g++ -c ' + _options.script_dir + 'svm.cpp -o ' + _options.script_dir + 'svm.o')
        os.system('LNAG=C gcc -g -Wall ' + _options.script_dir + 'svm-train.c ' + _options.script_dir + 'svm.o -o ' + _options.script_dir + 'svm-train -lstdc++ -lm')
        os.system('LNAG=C gcc -g -Wall ' + _options.script_dir + 'svm-predict.c ' + _options.script_dir + 'svm.o -o ' + _options.script_dir + 'svm-predict  -lstdc++ -lm')
        os.system('LNAG=C gcc -g -Wall ' + _options.script_dir + 'svm-scale.c ' + _options.script_dir + 'svm.o -o ' + _options.script_dir + 'svm-scale  -lstdc++ -lm')
        print('[{0}] Compiling PLEK_main, PLEK_spsn'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        os.system('LNAG=C gcc -g -Wall ' + _options.script_dir + 'PLEK_main.c -o ' + _options.script_dir + 'PLEK -lm')
        os.system('LNAG=C gcc -g -Wall ' + _options.script_dir + 'PLEK_spsn.c -o ' + _options.script_dir + 'PLEK_spsn -lm ')

    if len(sys.argv) < 2:
        exit_with_help()
    options = sys.argv
    script_dir = os.path.split(os.path.realpath(__file__))[0]
    saveDir = script_dir
    if getModel('/PLEK.model', saveDir):
        try:
            print('[{0}] Beginning PLEK run (Version 1.2) '.format(time.strftime('%Y-%m-%d %H:%M:%S')))
            _options = GridOption(options)
            cmdline = None
            if _options.is_recompile or not os.path.isfile(_options.script_dir + 'PLEK'):
                compile_c(_options)
            if not os.path.isfile(_options.modelfile):
                print('Building model')
                os.system('cat ' + _options.script_dir + 'PLEK.model0 ' + _options.script_dir + 'PLEK.model1 ' + _options.script_dir + 'PLEK.model2 > ' + _options.modelfile)
                if not os.path.isfile(_options.modelfile):
                    print("ERROR: No such file '" + _options.modelfile + "'")
                    sys.exit(1)
            svm_file = str(_options.prefix) + '_allsvm'
            print('[{0}] PLEK is running'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
            print('[{0}] Calculating k-mer usage'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
            if _options.pos_file != '':
                if _options.neg_file != '':
                    if _options.is_posneg_balanced == 1:
                        _options.input_type = 1
                        if not os.path.isfile(_options.pos_file):
                            print("ERROR: No such file '" + _options.pos_file + "'")
                            sys.exit(1)
                        if not os.path.isfile(_options.neg_file):
                            print("ERROR: No such file '" + _options.neg_file + "'")
                            sys.exit(1)
                        cmdline = (_options.script_dir + 'PLEK -s 1 -d 5 -p {0} -n {1} -o {2} -k {3} -l {4}  -b -isoutmsg {5} -isrmtempfile {6}').format(_options.pos_file, _options.neg_file, _options.prefix, _options.kmer, _options.min_seq_length, _options.isoutmsg, _options.isrmtempfile)
            if _options.pos_file != '':
                if _options.neg_file != '':
                    if _options.is_posneg_balanced == 0:
                        _options.input_type = 2
                        if not os.path.isfile(_options.pos_file):
                            print("ERROR: No such file '" + _options.pos_file + "'")
                            sys.exit(1)
                        if not os.path.isfile(_options.neg_file):
                            print("ERROR: No such file '" + _options.neg_file + "'")
                            sys.exit(1)
                        cmdline = (_options.script_dir + 'PLEK   -s 1 -d 5 -p {0} -n {1} -o {2} -k {3} -l {4}  -b -isoutmsg {5} -isrmtempfile {6}').format(_options.pos_file, _options.neg_file, _options.prefix, _options.kmer, _options.min_seq_length, _options.isoutmsg, _options.isrmtempfile)
            if _options.pos_file != '':
                if _options.neg_file == '':
                    _options.input_type = 3
                    if _options.unkown == 1:
                        _options.input_type = 4
                    if not os.path.isfile(_options.pos_file):
                        print("ERROR: No such file '" + _options.pos_file + "'")
                        sys.exit(1)
                    cmdline = (_options.script_dir + 'PLEK   -s 1 -d 5 -p {0} -o {1}  -k {2} -l {3}  -isoutmsg {4} -isrmtempfile {5}').format(_options.pos_file, _options.prefix, _options.kmer, _options.min_seq_length, _options.isoutmsg, _options.isrmtempfile)
            if _options.pos_file == '':
                if _options.neg_file != '':
                    _options.input_type = 5
                    if not os.path.isfile(_options.neg_file):
                        print("ERROR: No such file '" + _options.neg_file + "'")
                        sys.exit(1)
                    cmdline = (_options.script_dir + 'PLEK   -s 1 -d 5  -n {0} -o {1} -k {2} -l {3}  -isoutmsg {4} -isrmtempfile {5}').format(_options.neg_file, _options.prefix, _options.kmer, _options.min_seq_length, _options.isoutmsg, _options.isrmtempfile)
            os.system(cmdline)
            count = -1
            for count, line in enumerate(open(svm_file, 'rU')):
                count += 1

            file_count = int(_options.thread_count)
            file_array = []
            for fn in range(1, file_count + 1):
                fp = open(_options.prefix + '_temp_' + str(fn), 'w')
                file_array.append(fp)

            if not os.path.isfile(svm_file):
                print("ERROR: No such file '" + svm_file + "'")
                sys.exit(1)
            fv = open(svm_file, 'r')
            n = 1
            for line in fv:
                file_id = file_id_by_lineid(count, file_count, n)
                file_p = file_array[(file_id - 1)]
                file_p.write(line)
                n += 1

            for fn in range(1, file_count + 1):
                file_p = file_array[(fn - 1)]
                file_p.close()

            fv.close()
            print('[{0}] Scaling data'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
            scale_array = []
            print('svmrangefile is ', _options.svmrangefile)
            print('prefix is ', _options.prefix)
            print('script dir is ', _options.script_dir)
            for fn in range(1, file_count + 1):
                scale_obj = SVMScaleThread(_options.svmrangefile, _options.prefix + '_temp_' + str(fn), _options.prefix + '_temp_' + str(fn) + '_scaled', _options.script_dir)
                scale_array.append(scale_obj)
                scale_obj.start()

            for fn in range(1, file_count + 1):
                scale_obj = scale_array[(fn - 1)]
                scale_obj.join()

            if _options.isrmtempfile == 1:
                for fn in range(1, file_count + 1):
                    os.remove(_options.prefix + '_temp_' + str(fn))

            print('[{0}] Predicting'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
            predict_array = []
            for fn in range(1, file_count + 1):
                predict_obj = SVMPredictThread(_options.prefix + '_temp_' + str(fn) + '_scaled', _options.modelfile, _options.prefix + '_temp_' + str(fn) + '_predicted', _options.script_dir)
                predict_array.append(predict_obj)
                predict_obj.start()

            for fn in range(1, file_count + 1):
                predict_obj = predict_array[(fn - 1)]
                predict_obj.join()

            if _options.isrmtempfile == 1:
                for fn in range(1, file_count + 1):
                    os.remove(_options.prefix + '_temp_' + str(fn) + '_scaled')

            f_final = open(_options.prefix + '_predicted', 'w')
            for fn in range(1, file_count + 1):
                f_predicted = open(_options.prefix + '_temp_' + str(fn) + '_predicted')
                for line in f_predicted:
                    f_final.write(line)

                f_predicted.close()
                f_final.flush()

            f_final.close()
            if _options.input_type == 2 or _options.input_type == 3 or _options.input_type == 5 or _options.input_type == 4:
                cmdline = (_options.script_dir + 'PLEK_spsn  -svm {0} -predict {1} -desc {2} -descclass {3} -output {4} -input_type {5}  -isoutmsg {6} -isrmtempfile {7}').format(svm_file, _options.prefix + '_predicted', _options.prefix + '_allsvmdesc', _options.prefix + '_result', _options.prefix + '_logs', _options.input_type, _options.isoutmsg, _options.isrmtempfile)
                os.system(cmdline)
            if _options.isrmtempfile == 1:
                os.remove(_options.prefix + '_logs')
            os.rename(_options.prefix + '_result', _options.prefix)
            if _options.isrmtempfile == 1:
                for fn in range(1, file_count + 1):
                    os.remove(_options.prefix + '_temp_' + str(fn) + '_predicted')

            print('[{0}] Run complete'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
            print('\tResult file: {0}'.format(_options.prefix))
            Total_count = 0
            Noncoding_count = 0
            for line in open(_options.prefix, 'r'):
                Total_count = Total_count + 1
                if re.compile('^Non-coding').match(line):
                    Noncoding_count = Noncoding_count + 1

            print('\tCoding: {0}/{1}={2}%, Non-coding: {3}/{4}={5}%'.format(Total_count - Noncoding_count, Total_count, 1.0 * (Total_count - Noncoding_count) / Total_count * 100, Noncoding_count, Total_count, 1.0 * Noncoding_count / Total_count * 100))
        except (IOError, ValueError) as e:
            sys.stderr.write(str(e) + '\n')
            sys.stderr.write('Try "python {0}" for more information.\n'.format(sys.arg[0]))
            sys.exit(1)