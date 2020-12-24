# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\commands.py
# Compiled at: 2013-01-14 06:47:43
"""Drop-in replacement for old commands.getstatusoutput()."""

def getstatusoutput(cmd, **kwargs):
    r"""
    Return (status, output) of executing cmd in a shell. Output includes errors.
    
    http://stackoverflow.com/questions/1193583/what-is-the-multiplatform-alternative-to-subprocess-getstatusoutput-older-comman
    
    >>> getstatusoutput("echo test")
    (0, 'test\n')
    
    Keyword arguments are passed to subprocess.Popen(). This is useful e.g. to 
    set the current directory for the command.
    
    The returned output also includes error messages, as described in 
    http://docs.python.org/library/commands.html#commands.getstatusoutput
    To verify this, execute a command that redirects its output to the 
    standard error stream.
    
    >>> status, output = getstatusoutput("echo test 1>&2")
    >>> output.strip()
    'test'
    """
    import subprocess
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True, **kwargs)
    output = ('').join(pipe.stdout.readlines())
    sts = pipe.returncode
    if sts is None:
        sts = 0
    return (
     sts, output)


if __name__ == '__main__':
    import doctest
    doctest.testmod()