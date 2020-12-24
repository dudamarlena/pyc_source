# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/cmdline.py
# Compiled at: 2020-04-01 11:09:31
# Size of source mod 2**32: 22861 bytes
__doc__ = ' THIS MODULE CONTAINS ALL THE SHARED WRAPPER FUNCTIONS '
import sys, os
from subprocess import Popen, PIPE
from pipes import quote
from time import time, sleep
from datetime import timedelta
from .utility import debug, open_, mkpath

class ProgramList(object):
    """ProgramList"""

    def __init__(self):
        """ """
        self.timer = -time()
        self.list = []

    def __getitem__(self, key):
        """ """
        return getattr(self, key)

    def add_program(self, prog_obj):
        """ """
        setattr(self, prog_obj.name, prog_obj)
        self.list.append(prog_obj.name)
        return prog_obj

    def empty_list(self, forcefully=False):
        """ """
        removed = [self.remove_program(name, forcefully=forcefully) for name in self.list]
        if all(removed):
            return True
        else:
            return False

    def remove_name_from_list(self, name):
        """  """
        self.list[:] = (ent for ent in self.list if ent != name)

    def remove_program(self, name, forcefully=False):
        """ """
        if name in self.list:
            if name in dir(self):
                prog_obj = getattr(self, name)
                if prog_obj.status != 'Executing' or forcefully:
                    delattr(self, name)
                    self.remove_name_from_list(name)
                    return True
                else:
                    debug.log('Warning: Program %s status %s!' % (
                     name, prog_obj.status))
                    return False
            else:
                self.remove_name_from_list(name)
                return True
        else:
            self.remove_name_from_list(name)
            return True

    def add2list(self, prog_obj):
        """ """
        setattr(self, prog_obj.name, prog_obj)
        self.list.append(prog_obj.name)

    def exists(self, name):
        """ Checks whether the program exists in the program list. """
        return name in dir(self)

    def return_timer(self, name, status, timer):
        """ Return a text formatted timer """
        timer_template = '%s  %s  %s : %s : %9s'
        t = str(timedelta(0, timer)).split(',')[(-1)].strip().split(':')
        if len(t) == 4:
            h, m, s = int(t[0]) * 24 + int(t[1]), int(t[2]), float(t[3])
        else:
            if len(t) == 3:
                h, m, s = int(t[0]), int(t[1]), float(t[2])
            else:
                h, m, s = 0, 0, str(t)
        return timer_template % (
         name[:20].ljust(20),
         status[:7].ljust(7),
         '%3d' % h if h != 0 else ' --',
         '%2d' % m if m != 0 else '--',
         '%.6f' % s if isinstance(s, float) else s)

    def print_timers(self):
        """ PRINT EXECUTION TIMES FOR THE LIST OF PROGRAMS """
        self.timer += time()
        total_time = self.timer
        tmp = '*  %s  *'
        debug.log('', '* ' * 29, tmp % (' ' * 51), tmp % ('%s  %s  %s' % ('Program Name'.ljust(20), 'Status'.ljust(7), 'Execute Time (H:M:S)')), tmp % ('=' * 51))
        for name in self.list:
            if self.exists(name):
                timer = getattr(self, name).get_time()
                status = getattr(self, name).get_status()
                self.timer -= timer
                debug.log(tmp % self.return_timer(name, status, timer))
            else:
                debug.log(tmp % ('%s  %s -- : -- : --' % (name[:20].ljust(20), '                ')))

        debug.log(tmp % self.return_timer('Wrapper', '', self.timer), tmp % ('=' * 51), tmp % self.return_timer('Total', '', total_time), tmp % (' ' * 51), '* ' * 29, '')


class Program:
    """Program"""

    def __init__(self, name, path=None, timer=0, ptype=None, wdir='', queue=None, wait=False, args=None, walltime=2, mem=4, procs=1, server=None):
        debug.log('\n\nInitiating %s...' % name)
        self.path = path
        self.name = name
        self.timer = timer
        self.ptype = ptype
        self.queue = queue
        self.forcewait = wait
        self.args = []
        self.unquoted_args = []
        self.stderr = '%s.err' % name
        self.stdout = '%s.out' % name
        self.walltime = walltime
        self.mem = mem
        self.procs = procs
        self.p = None
        self.server = server
        self.status = 'Initialised'
        self.verbose = False
        if args:
            self.append_args(args)
        self.wdir = ''
        if wdir is not None:
            if wdir != '' and not os.path.exists(wdir):
                try:
                    mkpath(wdir)
                except Exception as e:
                    debug.graceful_exit('Error: The specified working directory (%s) does not exist, and could not be created!' % wdir)

                self.wdir = wdir

    def get_time(self):
        """ This function returns the amount of time used by the program
          (in seconds).
      """
        return self.timer

    def get_status(self):
        """ This function returns the amount of time used by the program
          (in seconds).
      """
        return self.status

    def get_cmd(self):
        """ This function combines and return the commanline call of the program.
      """
        cmd = []
        if self.path is not None:
            if '/' in self.path and not os.path.exists(self.path):
                debug.log('Error: path contains / but does not exist: %s' % self.path)
        else:
            if self.ptype is not None:
                if os.path.exists(self.ptype):
                    cmd.append(self.ptype)
                elif '/' not in self.ptype:
                    for path in os.environ['PATH'].split(os.pathsep):
                        path = path.strip('"')
                        ppath = os.path.join(path, self.ptype)
                        if os.path.isfile(ppath):
                            cmd.append(ppath)
                            break

                cmd.append(self.path)
                if sys.version_info < (3, 0):
                    cmd.extend([str(x) if not isinstance(x, unicode) else x.encode('utf-8') for x in [quote(str(x)) for x in self.args] + self.unquoted_args])
                else:
                    cmd.extend([str(x) for x in [quote(str(x)) for x in self.args] + self.unquoted_args])
            else:
                debug.log('Error: Program path not set!')
            return ' '.join(cmd)

    def update_timer(self, time):
        """ This function updates the program timer. """
        self.timer += time

    def append_args(self, arg):
        """ This function appends the provided arguments to the program object.
      """
        debug.log('Adding Arguments: %s' % arg)
        if isinstance(arg, (int, float)):
            self.args.append(str(arg))
        if isinstance(arg, str):
            self.args.append(arg)
        if isinstance(arg, list):
            if sys.version_info < (3, 0):
                self.args.extend([str(x) if not isinstance(x, unicode) else x.encode('utf-8') for x in arg])
        else:
            self.args.extend([str(x) for x in arg])

    def execute(self):
        """ This function Executes the program with set arguments. """
        prog_cmd = self.get_cmd().strip()
        if prog_cmd == '':
            self.status = 'Failure'
            debug.log('Error: No program to execute for %s!' % self.name)
            debug.log('Could not combine path and arguments into cmdline:\n%s %s)\n' % (
             self.path, ' '.join(self.args)))
        else:
            debug.log('\n\nExecute %s...\n%s' % (self.name, prog_cmd))
            script = '%s.sh' % self.name
            if self.wdir != '':
                script = '%s/%s' % (self.wdir, script)
            else:
                script = '%s/%s' % (os.getcwd(), script)
            with open_(script, 'w') as (f):
                f.write('#!/bin/bash\n')
                if self.wdir != '':
                    f.write('cd {workdir}\n'.format(workdir=self.wdir))
                f.write('touch {stdout} {stderr}\nchmod a+r {stdout} {stderr}\n{cmd} 1> {stdout} 2> {stderr}\nec=$?\n'.format(stdout=self.stdout, stderr=self.stderr, cmd=prog_cmd))
                if not self.forcewait:
                    f.write('if [ "$ec" -ne "0" ]; then echo "Error" >> {stderr}; else echo "Done" >> {stderr}; fi\n'.format(stderr=self.stderr))
                f.write('exit $ec\n')
            os.chmod(script, 493)
            if self.queue is not None:
                other_args = ''
                if self.forcewait:
                    other_args += '-K '
                cmd = '/usr/bin/qsub -l nodes=1:ppn={procs},walltime={hours}:00:00,mem={mem}g -r y {workdir_arg} {other_args} {cmd}'.format(procs=self.procs, hours=self.walltime, mem=self.mem, workdir_arg='-d %s' % self.wdir if self.wdir != '' else '', other_args=other_args, cmd=script)
                debug.log('\n\nTORQUE SETUP %s...\n%s\n' % (self.name, cmd))
            else:
                cmd = script
            if self.server is not None:
                cmd = 'ssh {server} {cmd}'.format(server=self.server, cmd=quote(cmd))
            self.status = 'Executing'
            self.update_timer(-time())
            if self.forcewait:
                self.p = Popen(cmd)
                ec = self.p.wait()
                if ec == 0:
                    debug.log('Program finished successfully!')
                    self.status = 'Done'
                else:
                    debug.log('Program failed on execution!')
                    self.status = 'Failure'
                self.p = None
            else:
                debug.log('CMD: %s' % cmd)
                self.p = Popen(cmd)
            self.update_timer(time())
            debug.log('timed: %s' % self.get_time())

    def wait(self, pattern='Done', interval=None, epatterns=['error', 'Error', 'STACK', 'Traceback']):
        """ This function will wait on a given pattern being shown on the last
          line of a given outputfile.

      OPTIONS
         pattern        - The string pattern to recognise when a program
                          finished properly.
         interval       - The amount of seconds to wait between checking the
                          log file.
         epatterns      - A list of string patterns to recognise when a program
                          has finished with an error.
      """
        increasing_interval = False
        if interval is None:
            increasing_interval = True
            interval = 10
        if self.wdir != '':
            stderr = '%s/%s' % (self.wdir, self.stderr)
        else:
            stderr = self.stderr
        debug.log('\nWaiting for %s to finish...' % str(self.name))
        if self.status == 'Executing':
            self.update_timer(-time())
            found = False
            if self.queue is not None:
                debug.log('   Waiting for the error log to be created (%s)...' % stderr)
                max_queued_time = 10800
                while not os.path.exists(stderr) and time() + self.timer < max_queued_time and time() + self.timer > 0:
                    debug.log('      Waiting... (max wait time left: %s seconds)' % str(max_queued_time - time() - self.timer))
                    sleep(interval)
                    if increasing_interval:
                        interval *= 1.1

                if os.path.exists(stderr):
                    if increasing_interval:
                        interval = 10
                    debug.log('\nError log created, waiting for program to finish...')
                    max_time = time() + self.walltime * 60 * 60
                    while time() < max_time:
                        with open_(stderr) as (f):
                            for l in f.readlines()[-5:]:
                                if pattern in l:
                                    found = True
                                    max_time = 0
                                    break
                                elif any([ep in l for ep in epatterns]):
                                    found = False
                                    max_time = 0
                                    break

                        if max_time > 0:
                            debug.log('      Waiting... (max wait-time left: %s seconds)' % str(max_time - time()))
                            sleep(interval)

                    if found:
                        debug.log('   Program finished successfully!')
                        self.status = 'Done'
                    else:
                        debug.log('Error: Program took too long, or finished with error!')
                        if self.verbose:
                            debug.print_out('Technical error occurred!\n', 'The service was not able to produce a result.\n', 'Please check your settings are correct, and the file type matches what you specified.\n', 'Try again, and if the problem persists please notify the technical support.\n')
                        self.status = 'Failure'
                else:
                    debug.log('Error: %s still does not exist!\n' % stderr, 'This error might be caused by the cgebase not being available!')
                    if self.verbose:
                        debug.print_out('Technical error occurred!\n', 'This error might be caused by the server not being available!\n', 'Try again later, and if the problem persists please notify the technical support.\n', 'Sorry for any inconvenience.\n')
                    self.status = 'Failure'
                if self.p is not None:
                    self.p.wait()
                    self.p = None
            else:
                if self.p is None:
                    debug.log('Program not instanciated!')
                    self.status = 'Failure'
                else:
                    ec = self.p.wait()
            if ec != 0:
                debug.log('Program failed on execution!')
                self.status = 'Failure'
            else:
                if os.path.exists(stderr):
                    with open_(stderr) as (f):
                        for l in f.readlines()[-5:]:
                            if pattern in l:
                                found = True
                                break
                            elif any([ep in l for ep in epatterns]):
                                found = False
                                break

                    if found:
                        debug.log('   Program finished successfully!')
                        self.status = 'Done'
                    else:
                        debug.log('Error: Program failed to finish properly!')
                        if self.verbose:
                            debug.print_out('Technical error occurred!\n', 'The service was not able to produce a result.\n', 'Please check your settings are correct, and the file ' + 'type matches what you specified.', 'Try again, and if ' + 'the problem persists please notify the technical ' + 'support.\n')
                        self.status = 'Failure'
                else:
                    debug.log('Error: %s does not exist!\n' % stderr, 'This error might be caused by the cgebase not being ' + 'available!')
                    if self.verbose:
                        debug.print_out('Technical error occurred!\n', 'This error might be caused by the server not being ' + 'available!\n', 'Try again later, and if the problem ' + 'persists please notify the technical support.\n', 'Sorry for any inconvenience.\n')
                    self.status = 'Failure'
                self.p = None
            self.update_timer(time())
            debug.log('   timed: %s' % self.get_time())
        else:
            debug.log('   The check-out of the program has been sorted previously.')

    def print_stdout(self):
        """ This function will read the standard out of the program and print it
      """
        if self.wdir != '':
            stdout = '%s/%s' % (self.wdir, self.stdout)
        else:
            stdout = self.stdout
        if os.path.exists(stdout):
            with open_(stdout, 'r') as (f):
                debug.print_out('\n'.join([line for line in f]))
        else:
            debug.log('Error: The stdout file %s does not exist!' % stdout)

    def find_out_var(self, varnames=[]):
        """ This function will read the standard out of the program, catch
          variables and return the values

          EG. #varname=value
      """
        if self.wdir != '':
            stdout = '%s/%s' % (self.wdir, self.stdout)
        else:
            stdout = self.stdout
        response = [
         None] * len(varnames)
        if os.path.exists(stdout):
            with open_(stdout, 'r') as (f):
                for line in f:
                    if '=' in line:
                        var = line.strip('#').split('=')
                        value = var[1].strip()
                        var = var[0].strip()
                        if var in varnames:
                            response[varnames.index(var)] = value

        else:
            debug.log('Error: The stdout file %s does not exist!' % stdout)
        return response

    def find_err_pattern(self, pattern):
        """ This function will read the standard error of the program and return
          a matching pattern if found.

          EG. prog_obj.FindErrPattern("Update of mySQL failed")
      """
        if self.wdir != '':
            stderr = '%s/%s' % (self.wdir, self.stderr)
        else:
            stderr = self.stderr
        response = []
        if os.path.exists(stderr):
            with open_(stderr, 'r') as (f):
                for line in f:
                    if pattern in line:
                        response.append(line.strip())

        else:
            debug.log('Error: The stderr file %s does not exist!' % stderr)
        return response

    def find_out_pattern(self, pattern):
        """ This function will read the standard error of the program and return
          a matching pattern if found.

          EG. prog_obj.FindErrPattern("Update of mySQL failed")
      """
        if self.wdir != '':
            stdout = '%s/%s' % (self.wdir, self.stdout)
        else:
            stdout = self.stdout
        response = []
        if os.path.exists(stdout):
            with open_(stdout, 'r') as (f):
                for line in f:
                    if pattern in line:
                        response.append(line.strip())

        else:
            debug.log('Error: The stdout file %s does not exist!' % stdout)
        return response


def cmd2list(cmd):
    """ Executes a command through the operating system and returns the output
   as a list, or on error a string with the standard error.
   EXAMPLE:
      >>> from subprocess import Popen, PIPE
      >>> CMDout2array('ls -l')
   """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    if p.returncode != 0 and stderr != '':
        return 'ERROR: %s\n' % stderr
    else:
        return stdout.split('\n')


proglist = ProgramList()