# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/f0/paul/Projects/Tools/Psicons/psicons.core/psicons/core/commands.py
# Compiled at: 2011-08-01 12:43:27
__doc__ = '\nNew scons commands.\n\nThe process of installing a new tool or module for use by SCons is fiddly, \ninvolves copying libraries in a tool directory, registering \ntheir use in build files, voids the ease of using ``easy_install`` and makes \ndevelopment a pain. Thus, these additional "commands" are real scons commands, so\nmuch as functions that generate commands. But they are easy to use.\n\n\n'
__docformat__ = 'restructuredtext en'
import impl

def External(env, exe, args=[], infiles=[], output=[], depends=[], capture_stdout=None):
    """
        Create a task for doing analysis with an external (fixed) program.
        
        :Parameters:
                env : Environment
                        The environment created for the build
                exe : str
                        name of executable to be called
                args : str or list
                        either a string that is used to pass arguments to the executable 
                        (e.g. ``"--foo 5 -t one.txt"``) or a list of strings that can be joined to
                        do the same (e.g. ``["--foo", "5", "-t", "one.txt"]``).
                infiles : str or list
                        a string or list of strings giving the paths of the files that this
                        task depends on. 
                output : str or list
                        a string or list of strings giving the paths of the files that this
                        task produces.
                capture_stdout : None or str
                        Record the output of the tool. If a string is provided, this will be
                        used as the path of the file to save it in.
        
        This is a command that runs an executable, intended for processing input
        datafiles to output data files. It calls the named executable with the
        passed arguments. Infiles and any others listed in `depends` are recorded
        as dependencies. outfiles and the captured output are listed as outputs.
        These will be used in dependency tracking.
        
        """
    infiles = impl.make_list(infiles or [])
    args = impl.make_list(args or [])
    cmdline = exe % {'args': (' ').join(args), 
       'infiles': (' ').join(infiles)}
    output = impl.make_list(output or [])
    new_command = env.Command(output, infiles, cmdline)
    depends = depends + infiles
    env.Depends(new_command, depends)
    return new_command


def Script(env, path, interpreter=None, args=[], infiles=[], output=[], depends=[], capture_stdout=None):
    """
        Create a task for running a local script.
        
        :Parameters:
                path : str
                        Pathway to the script
                interpreter
                        Interpreter to run the script with. If None, assume it is python.
                        
                

        This is a command that runs a local script, intended for processing input
        datafiles to output data files. It work like `External`, except that the 
        script itself is made a dependency for this step. Thus ,alterations in the
        script will trigger rerunning. All undescribed parameters are as per `External`.
        
        For example::
        
                >>> env = SconsEnv()
                >>> make_clean_data = Script ('Scripts/clean.py',
                        ...     args = ['--save-as', 'output.txt'],
                        ...     infiles = ['indata.txt'],
                        ...     output = 'output.txt',
                ...     )
                >>> type_data = Script ('count_types.pl',
                ...             interpreter = 'perl',
                ...             args = ['--use-types', 'type_data.csv'],
                ...             infiles = ['clean_data.txt'],
                ...             depends = 'type_config.txt',
                ...             capture_stdout='captured-types.txt',
                ...     )
        
        """
    interpreter = interpreter or '$PY'
    infiles = impl.make_list(infiles or [])
    args = impl.make_list(args or [])
    cmdline = (' ').join([interpreter, path] + args + infiles)
    if capture_stdout:
        cmdline = (' ').join([cmdline, '>', capture_stdout])
        output.append(capture_stdout)
    new_command = env.Command(output, [
     path] + infiles, cmdline)
    depends = depends + infiles
    env.Depends(new_command, depends)
    return new_command


if __name__ == '__main__':
    import doctest
    doctest.testmod()