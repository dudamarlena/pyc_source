# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/utils/solver.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 15365 bytes
"""SAT solver integrated with CNFgen.

Of course it does not implement an actual sat solver, but tries to use
solvers installed on the machine. For the full list of supported
solvers, see

  `cnfformula.utils.solver.supported_satsolvers`
"""
import sys
__all__ = [
 'supported_satsolvers', 'is_satisfiable', 'have_satsolver']

def _satsolve_filein_fileout(F, cmd='minisat', verbose=0):
    """Test CNF satisfiability using a minisat-style solver.

    This also works fine using `glucose` instead of `minisat`, or any
    other solver which uses the same I/O conventions of `minisat`.

    Parameters
    ----------
    F  : a CNF formula
    
    cmd : string
        the command line used to invoke the SAT solver.

    verbose: int
       0 or less means no output. 1 shows the command line actually
       run. 2 outputs the solver output. (default: 0)

    Examples:
    ---------
    _satsolve_filein_fileout(F,cmd='minisat -no-pre')
    _satsolve_filein_fileout(F,cmd='glucose -pre')

    The first call tests F using `minisat` without formula
    preprocessing. The second does it using `glucose` with
    preprocessing.

    Returns:
    --------
    A pair (answer,witness) where answer is either True when F is
    satisfiable, or False otherwise. If F is satisfiable the witness
    is a satisfiable assignment in form of a dictionary, otherwise it
    is None.

    Notes:
    ------
    `minisat` writes its output on a file. If the formula is
    unsatisfiable then the output file contains just the line "UNSAT",
    but if it is satisfiable it contains the line "SAT" and on a new
    line the assignment, encoded as literal values, e.g., "-1 2 3 -4 -5 ..."
    """
    import subprocess, os, tempfile
    cnf = tempfile.NamedTemporaryFile(delete=False)
    sat = tempfile.NamedTemporaryFile(delete=False)
    cnf.write(F.dimacs().encode('ascii'))
    cnf.close()
    sat.close()
    output = b''
    try:
        try:
            final_command = cmd + ' ' + cnf.name + ' ' + sat.name
            if verbose >= 1:
                print(('$ ' + final_command), file=(sys.stderr))
            p = subprocess.Popen(args=(cmd.split() + [cnf.name, sat.name]), stdin=(subprocess.PIPE),
              stdout=(subprocess.PIPE))
            output, _ = p.communicate()
            sat = open((sat.name), 'r', encoding='ascii')
            foutput = sat.read().split()
            sat.close()
        except OSError:
            pass

    finally:
        os.unlink(cnf.name)
        os.unlink(sat.name)

    result = None
    witness = None
    output = output.decode('ascii')
    if verbose >= 2:
        print(output, file=(sys.stderr))
    else:
        if len(foutput) == 0:
            raise RuntimeError('Error during SAT solver call: {}.\n'.format(' '.join([cmd, cnf.name, sat.name])))
        else:
            if foutput[0] == 'SAT':
                result = True
                witness = [int(v) for v in foutput[1:] if v != '0']
                witness = {F._index2name[abs(v)]:v > 0 for v in witness}
            else:
                if foutput[0] == 'UNSAT':
                    result = False
                else:
                    raise RuntimeError('Error during SAT solver call: {}.\n'.format(' '.join([cmd, cnf.name, sat.name])))
    return (
     result, result and witness or None)


def _satsolve_stdin_stdout(F, cmd='lingeling', verbose=0):
    """Test CNF satisfiability using a dimacs I/O compatible solver.

    This works fine using any other solver which respects the dimacs
    conventions for input/output. In particular it works with the
    default solver which is `lingeling`.

    Parameters
    ----------
    F  : a CNF formula
    
    cmd : string
        the command line used to invoke the SAT solver.
    
    verbose: int
       0 or less means no output. 1 shows the command line actually
       run. 2 outputs the solver output. (default: 0)

    Example:
    --------
    _satsolve_stdin_stdout(F,cmd='lingeling --plain')
    _satsolve_stdin_stdout(F,cmd='cryptominisat')

    The first call tests F using `lingeling` without formula
    preprocessing. The second does it using `march` with default settings.

    Returns:
    --------
    A pair (answer,witness) where answer is either True when F is
    satisfiable, or False otherwise. If F is satisfiable the witness
    is a satisfiable assignment in form of a dictionary, otherwise it
    is None.

    Notes:
    ------
    A solver adheres to dimacs I/O conventions if every line on the
    standard output is preceded by the 'c' character, except for the
    solution line, preceded by 's', and possibly for the assignment
    lines, each one preceded by 'v'. See example::

      c comment line
      c more comments
      s SATISFIABLE
      c other comments
      v -1 -2 -3 4 5 6
      v -7 8 9 -10 0
      c concluding comments.
    """
    import subprocess
    output = b''
    try:
        if verbose >= 1:
            print(('$ ' + cmd), file=(sys.stderr))
        p = subprocess.Popen(args=(cmd.split()), stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE))
        output, err = p.communicate(F.dimacs().encode('ascii'))
    except OSError:
        pass

    witness = []
    result = None
    output = output.decode('ascii')
    if verbose >= 2:
        print(output, file=(sys.stderr))
    for line in output.splitlines():
        if len(line) == 0:
            pass
        else:
            if line[0] == 's':
                if line.split()[1] == 'SATISFIABLE':
                    result = True
                else:
                    if line.split()[1] == 'UNSATISFIABLE':
                        result = False
                    else:
                        result = None
                if line[0] == 'v':
                    witness += [int(el) for el in line.split() if el != 'v' if el != '0']

    if result is None:
        raise RuntimeError('Error during SAT solver call: {}.\n'.format(cmd))
    witness = {F._index2name[abs(v)]:v > 0 for v in witness}
    return (
     result, result and witness or None)


def _satsolve_filein_stdout(F, cmd='sat4j', verbose=0):
    """Test CNF satisfiability using solvers that requires input file.

    This works fine using any solver which requires the input formula
    as a file but respects the dimacs conventions for the output. In
    particular it works with the default solver which is `sat4j`.

    Parameters
    ----------
    F  : a CNF formula
    
    cmd : string
        the command line used to invoke the SAT solver.
    
    verbose: int
       0 or less means no output. 1 shows the command line actually
       run. 2 outputs the solver output. (default: 0)

    Example:
    --------
    _satsolve_filein_stdout(F,cmd='sat4j')
    _satsolve_filein_stdout(F,cmd='march')

    Returns:
    --------
    A pair (answer,witness) where answer is either True when F is
    satisfiable, or False otherwise. If F is satisfiable the witness
    is a satisfiable assignment in form of a dictionary, otherwise it
    is None.

    """
    import subprocess, tempfile
    cnf = tempfile.NamedTemporaryFile(delete=False)
    cnf.write(F.dimacs().encode('ascii'))
    cnf.close()
    output = b''
    try:
        final_command = cmd + ' ' + cnf.name
        if verbose >= 1:
            print(('$ ' + final_command), file=(sys.stderr))
        p = subprocess.Popen(args=(cmd.split() + [cnf.name]), stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE))
        output, err = p.communicate()
    except OSError:
        pass

    witness = []
    result = None
    output = output.decode('ascii')
    if verbose >= 2:
        print(output, file=(sys.stderr))
    for line in output.splitlines():
        if len(line) == 0:
            pass
        else:
            if line[0] == 's':
                if line.split()[1] == 'SATISFIABLE':
                    result = True
                else:
                    if line.split()[1] == 'UNSATISFIABLE':
                        result = False
                    else:
                        result = None
                if line[0] == 'v':
                    witness += [int(el) for el in line.split() if el != 'v' if el != '0']

    if result is None:
        raise RuntimeError('Error during SAT solver call: {}.\n'.format(cmd + ' ' + cnf.name))
    witness = {F._index2name[abs(v)]:v > 0 for v in witness}
    return (
     result, result and witness or None)


_SATSOLVER_INTERFACE = {'lingeling':_satsolve_stdin_stdout, 
 'plingeling':_satsolve_stdin_stdout, 
 'precosat':_satsolve_stdin_stdout, 
 'picosat':_satsolve_stdin_stdout, 
 'march':_satsolve_filein_stdout, 
 'cryptominisat':_satsolve_stdin_stdout, 
 'minisat':_satsolve_filein_fileout, 
 'glucose':_satsolve_stdin_stdout, 
 'sat4j':_satsolve_filein_stdout}

def supported_satsolvers():
    """List the supported SAT solvers.

    Output the list of all solvers supported by CNFgen.
    """
    return list(_SATSOLVER_INTERFACE.keys())


def have_satsolver(solvers=None):
    """Test whether we can run SAT solvers.

    Parameters
    ----------
    `solvername` : string / list of strings, optional
        the names of the solvers to be tested.

    If `solvers` is None then all supported solvers are tested.
    If `solvers` is a list of strings all solvers in the list are tested.
    If `solvers` is a string then only that solver is tested.

    Raises
    ------
    `TypeError` if `solvers` is not of the right type.
    """
    import subprocess
    if solvers is None:
        solvers = supported_satsolvers()
    else:
        if type(solvers) == str:
            solvers = [
             solvers]
        else:
            if any([type(s) != str for s in solvers]):
                raise TypeError("'solvers' type must be either 'str' or 'list(str)'.")
    for solvername in solvers:
        try:
            subprocess.Popen(args=[solvername, '--help'], stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE))
        except OSError:
            pass
        else:
            return True

    return False


def is_satisfiable(F, cmd=None, sameas=None, verbose=0):
    """Determines whether a CNF is satisfiable or not.

    The satisfiability is determined using an external sat solver.  If
    no command line is specified, the known solvers are tried in
    succession until one is found.

    Parameters
    ----------
    F: a CNF formula object
       check the satisfiablility of this formula

    cmd: string,optional
       the actual command line used to invoke the SAT solver

    sameas: string, optional
       use the interface of one of the supported solvers, indicated in
       input. Useful when the solver ont the command line is not supported.

    verbose: int
       0 or less means no output. 1 shows the command line actually
       run. 2 outputs the solver output. (default: 0)

    Examples
    --------
    >>> is_satisfiable(F)                                               # doctest: +SKIP
    >>> is_satisfiable(F,cmd='minisat -no-pre')                         # doctest: +SKIP
    >>> is_satisfiable(F,cmd='glucose -pre')                            # doctest: +SKIP
    >>> is_satisfiable(F,cmd='lingeling --plain')                       # doctest: +SKIP
    >>> is_satisfiable(F,cmd='sat4j')                                   # doctest: +SKIP
    >>> is_satisfiable(F,cmd='my-hacked-minisat -pre',sameas='minisat') # doctest: +SKIP
    >>> is_satisfiable(F,cmd='patched-lingeling',sameas='lingeling')    # doctest: +SKIP

    Returns
    -------
    A pair (answer,witness) where answer is either True when F is
    satisfiable, or False otherwise. If F is satisfiable the witness
    is a satisfiable assignment in form of a dictionary, otherwise it
    is None.

    Raises
    ------
    RuntimeError
       if it is not possible to correctly invoke the solver needed.
    ValueError 
       if `sameas` is set and does not match the name of a supported solver.
    TypeError
       if F is not a CNF object.
    
    Supported solvers:
    ------------------
    See `cnfformula.utils.solver.supported_satsolvers`

    Drop-in solver replacements:
    ----------------------------

    It is possible to use any drop-in replacement for these solvers,
    but in this case more information is needed on how to communicate
    with the solver. In particular `minisat` does not respect
    the standard `dimacs` I/O conventions, and that holds also for
    `glucose` which is a drop-in replacement of `minisat`.

    For the supported solver we can pick the right interface, but for
    other solvers it is impossible to guess. We suggest to use one of

    >>> is_satisfiable(F,cmd='minisat-style-solver',sameas='minisat')  # doctest: +SKIP
    >>> is_satisfiable(F,cmd='dimacs-style-solver',sameas='lingeling') # doctest: +SKIP

    """
    import cnfformula
    if not isinstance(F, cnfformula.CNF):
        raise TypeError("'F' is not a CNF formula object.")
    else:
        if sameas is not None:
            if sameas not in supported_satsolvers():
                raise ValueError("'{}' is not a supported sat solver.".format(sameas))
        else:
            if cmd is None or len(cmd.split()) == 0:
                solver_cmds = supported_satsolvers()
                sameas = None
            else:
                if cmd.split()[0] not in supported_satsolvers():
                    if sameas is None:
                        raise RuntimeError("Solver '{}' is not supported, use 'sameas' option (see docs).".format(cmd.split()[0]))
                solver_cmds = [
                 cmd]
        for solver_cmd in solver_cmds:
            solver = solver_cmd.split()[0]
            s_func = _SATSOLVER_INTERFACE[(sameas or solver)]
            if not have_satsolver(solvers=[solver]):
                continue
            else:
                return s_func(F, solver_cmd, verbose=verbose)

        if len(solver_cmds) == 1:
            raise RuntimeError("Solver '{}' is not installed or is unusable.".format(solver_cmds[0].split()[0]))
        else:
            raise RuntimeError('No usable solver found.')