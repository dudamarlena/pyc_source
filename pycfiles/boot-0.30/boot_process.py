# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/boot_process.py
# Compiled at: 2012-08-07 13:02:17
import time, glob, os
from subprocess import Popen, PIPE, STDOUT
import directory

def comp_and_sim(conn):
    """ Process to compile and simulate a vhdl design. This process is initiated 
        as soon as boot starts and it keeps running in background in a while 
        loop untill a trigger command is sent via its communication pipe.
    """
    COMPILATION_ERROR = False
    GTK_ALREADY_UP = False
    Compile = False
    Simulate = False
    while True:
        time.sleep(0.3)
        if conn.poll():
            wd, tl_file, _SOCKET_ID, GHDL_SIM_OPT, Compile, Simulate = conn.recv()
        if Compile:
            Compile = False
            COMPILATION_ERROR = False
            conn.send('CLEAR ALL\n')
            conn.send('Begin compiling\n')
            directory.dir_make_sure(wd, 'clean_all_files')
            my_cmd = 'ghdl -clean --workdir=' + wd + '/build'
            p = Popen(my_cmd.split(' '), shell=False, stdout=PIPE, stderr=STDOUT)
            p.wait()
            print 'All GHDL files cleaned with process id:', p.pid
            all_vhdl_files = glob.glob(os.path.join(wd, '*.vhd')) + glob.glob(os.path.join(wd, '*.vhdl'))
            print 'Checking all VHDL files in:', wd
            for x in all_vhdl_files:
                conn.send('Checking: ' + x.replace(wd + '/', ' ') + '\n')

            my_cmd = 'ghdl -a --workdir=' + wd + '/build ' + (' ').join(all_vhdl_files)
            p = Popen(my_cmd.split(' '), shell=False, stdout=PIPE, stderr=STDOUT)
            p.wait()
            print 'All vhdl files checked with process id:', p.pid
            for line in p.stdout.readlines():
                line = line.replace(wd + '/', ' ')
                conn.send(line)

            tl_entity = tl_file.split('.vhd')[0]
            print 'Compiling top-level design file:', tl_entity
            my_cmd = 'ghdl -e --workdir=' + wd + '/build ' + tl_entity
            p = Popen(my_cmd.split(' '), shell=False, stdout=PIPE, stderr=STDOUT)
            p.wait()
            print 'All vhdl files compiled with process id:', p.pid
            for line in p.stdout.readlines():
                line = line.replace(wd + '/', ' ')
                conn.send(line)
                if 'compilation error' in line:
                    COMPILATION_ERROR = True
                else:
                    COMPILATION_ERROR = False

            if not COMPILATION_ERROR:
                print 'Moving simulation file:', tl_entity
                my_cmd = 'mv ' + tl_entity + ' ' + wd + '/build'
                p = Popen(my_cmd.split(' '), shell=False, stdout=PIPE, stderr=STDOUT)
                p.wait()
                print 'All build files moved with process id:', p.pid
            conn.send('End compiling.\n')
        if Simulate and not COMPILATION_ERROR:
            Simulate = False
            conn.send('Begin simulation.\n')
            tl_entity = tl_file.split('.vhd')[0]
            print 'Simulating top-level design:', tl_entity
            my_cmd = wd + '/build/' + tl_entity + ' ' + GHDL_SIM_OPT + ' --vcd=' + wd + '/build/simul_output.vcd'
            p = Popen(my_cmd.split(' '), shell=False, stdout=PIPE, stderr=STDOUT)
            p.wait()
            print 'GHLD simulation files generated with process id:', p.pid
            for line in p.stdout.readlines():
                line = line.replace(wd + '/', ' ')
                conn.send(line)

            if GTK_ALREADY_UP:
                try:
                    _txt = 'Reloading GTKWAVE simulation file in process id:'
                    print _txt, p1.pid
                    cmd = 'gtkwave::reLoadFile\n'
                    p1.stdin.write(cmd)
                    p1.stdin.flush()
                except:
                    pass

            else:
                cmd = 'gtkwave --rcfile=' + wd + '/build/gtkwaverc' + ' --xid=' + _SOCKET_ID + ' -W'
                p1 = Popen(cmd.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
                print 'Started GHDL simulation process id:', p1.pid
                while 'Interpreter id is gtkwave' not in p1.stdout.readline():
                    time.sleep(0.1)

                print 'gtkwave is up.'
                GTK_ALREADY_UP = True
                time.sleep(0.3)
                print 'Loading simulation interface with file:', tl_entity + '.vcd'
                cmd = 'gtkwave::loadFile "' + wd + '/build/simul_output.vcd"\n'
                p1.stdin.write(cmd)
                p1.stdin.flush()
                time.sleep(0.3)
            COMPILATION_ERROR = False
            conn.send('End processing\n')

    return 0