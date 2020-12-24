# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nbc\nbc.py
# Compiled at: 2019-10-28 07:32:32
# Size of source mod 2**32: 5204 bytes
import os, sys, subprocess
from tqdm import tqdm
from nbconvert import nbconvertapp, RSTExporter
from options import nbc_options
from data.load_data import DataLoader
opt = nbc_options.Options().parse()
app = nbconvertapp.NbConvertApp()
loader = DataLoader()

class Converter:

    def __init__(self):
        self.os = opt.os
        self.cwd = os.getcwd()
        self.dir = os.path.abspath(os.path.dirname(__file__))
        self.expy = os.path.join(os.environ['USERPROFILE'], '.expy')
        self.home = os.environ['USERPROFILE']
        self.input = self.init_input()
        self.output = self.init_output()
        self.template = self.init_template()
        self.path = self.init_path()

    def init_input(self):
        all_file = [os.path.join(self.cwd, f) for f in opt.input] if opt.input else []
        if opt.input == opt.all:
            opt.no_convert = True
        elif opt.input:
            all_dir = [os.path.join(self.cwd, d) for d in opt.input if os.path.isdir(os.path.join(self.cwd, d))]
        else:
            if opt.all:
                all_dir = [os.path.join(self.cwd, d) for d in opt.all if os.path.isdir(os.path.join(self.cwd, d))]
            else:
                all_dir = [self.cwd] if opt.all == [] else []
        for d in all_dir:
            all_file += [os.path.join(d, f) for f in os.listdir(d)]

        return [f for f in all_file if f[-6:] == '.ipynb' if os.path.isfile(f)]

    def init_output(self):
        if opt.to:
            return opt.to
        if opt.output:
            return opt.output
        return 'pdf'

    def init_template(self):
        loader()
        if opt.template:
            if os.path.isfile(os.path.join(self.cwd, opt.template[0])):
                return os.path.join(self.cwd, opt.template[0])
            raise ValueError('No such file\t%s.' % os.path.join(self.cwd, opt.template[0]))
        if opt.template == []:
            return
        if self.output == 'pdf':
            return loader.latex_temp
        if self.output == 'html':
            return loader.html_temp
        return

    def init_path(self):
        path = opt.path if opt.path else self.cwd
        if opt.path is None:
            return
        return path

    def __call__(self):
        if opt.install_tex:
            self.install_tex()
        else:
            if opt.install_pandoc:
                self.install_pandoc()
            if opt.reset_template:
                loader.nofile_list = loader.file_list
                loader()
            if opt.debug:
                self.debug()
            if type(opt.rm) == type([]):
                self.remove_file()
            opt.no_convert or self.convert()
            print('Finished')

    def convert(self):
        input = self.input
        output = opt.output if opt.output else '%s.%s' % (opt.input, self.output)
        for filename in input if opt.hide_bar else tqdm(input):
            args = [
             filename,
             '--to=%s' % self.output]
            if opt.no_input:
                args.append('--no-input')
            if self.template:
                args.append('--template=%s' % self.template)
            if self.path:
                args.append('--output-dir=%s' % self.path)
            app.initialize(args)
            app.start()

    def debug(self):
        print('test:\t', opt.test, '\ntype:\t', type(opt.test))

    def install_tex(self):
        if opt.os in ('posix', 'Debian', 'Ubuntu'):
            subprocess.run('sudo apt install texlive-xetex texlive-fonts-recommended texlive-generic-recommended')
        if opt.os in ('Windows', 'nt'):
            print('\n\tPlease install [MikTex](http://www.miktex.org/)\n')
        if opt.os in ('Mac', 'Darwin'):
            print('\n\tPlease install [MacTex](http://tug.org/mactex/)\n')

    def install_pandoc--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              opt
                2  LOAD_ATTR                os
                4  LOAD_STR                 'posix'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  LOAD_STR                 'Debian'
               12  POP_JUMP_IF_TRUE     14  'to 14'
             14_0  COME_FROM            12  '12'
             14_1  COME_FROM             8  '8'

 L.  95        14  LOAD_GLOBAL              subprocess
               16  LOAD_METHOD              run
               18  LOAD_STR                 'sudo apt install pandoc'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_TOP          
               24  JUMP_FORWARD         34  'to 34'

 L.  96        26  LOAD_GLOBAL              print
               28  LOAD_STR                 '\n\tPlease install [Pandoc](https://pandoc.org/installing.html)\n'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  POP_TOP          
             34_0  COME_FROM            24  '24'

Parse error at or near `JUMP_FORWARD' instruction at offset 24

    def remove_file(self):
        opt.no_convert = True
        all_file = [os.path.join(self.cwd, f) for f in opt.rm] if opt.rm else []
        if opt.all:
            all_dir = [os.path.join(self.cwd, d) for d in opt.all if os.path.isdir(os.path.join(self.cwd, d))]
        else:
            if opt.rm:
                all_dir = [os.path.join(self.cwd, d) for d in opt.rm if os.path.isdir(os.path.join(self.cwd, d))]
            else:
                all_dir = [self.cwd] if opt.all == [] else []
        for d in all_dir:
            all_file += [os.path.join(d, f) for f in os.listdir(d)]

        all_file = [f for f in all_file if f[-len(self.output):] == self.output if os.path.isfile(f)]
        for f in all_file:
            print('\t%s' % f)

        print('already delete this file ?\t[y/n]')
        val = input()
        if val in ('y', 'yes'):
            try:
                for f in tqdm(all_file):
                    os.remove(f)

            except:
                pass

        print('Finished.')


def main():
    conv = Converter()
    conv()


if __name__ == '__main__':
    main()