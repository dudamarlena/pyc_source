# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/_py2f.py
# Compiled at: 2018-10-28 11:56:52
"""
Functions to create fortran code.

Needed for exporting trained network to fortran source.
"""

def flines(string=' '):
    if string == '':
        string == ' '
    lines = string.splitlines()
    fstr = ''
    for line in lines:
        fstr += '      ' + line + '\n'

    return fstr


def fcomment(string=' ', lstrip=False):
    if string == '':
        string == ' '
    lines = string.splitlines()
    fstr = ''
    for line in lines:
        if lstrip:
            line = line.lstrip()
        fstr += 'c' + '     ' + line + '\n'

    return fstr


def addfline(string=' '):
    if string == '':
        string == ' '
    return '     & ' + string + '\n'


def f2pyline(string=' '):
    if string == '':
        string == ' '
    return 'cf2py ' + string + '\n'


def fval2string(val, ftyp):
    if 'INTEGER' in ftyp:
        return '%i' % val
    if 'REAL' in ftyp:
        return '%+.7e' % val
    if 'DOUBLE' in ftyp:
        return ('%+.15e' % val).replace('e', 'd')


def farray(arr, fname):
    shp = arr.shape
    if len(shp) == 1:
        fshp = '(%i)' % shp[0]
    else:
        fshp = str(shp)
    from numpy import dtype
    if arr.dtype == dtype('int'):
        ftyp = 'INTEGER '
    else:
        if arr.dtype == dtype('float32'):
            ftyp = 'REAL '
        else:
            if arr.dtype == dtype('float64'):
                ftyp = 'DOUBLE PRECISION '
            else:
                raise TypeError('Unsupported array type: %s'(arr.dtype))
            declaration = flines(ftyp + fname + fshp)
            indexes = [ [i] for i in range(shp[0]) ]
            findexes = [ [i + 1] for i in range(shp[0]) ]
            try:
                for idx in shp[1:]:
                    newindexes = []
                    newfindexes = []
                    for i in range(idx):
                        for j in xrange(len(indexes)):
                            newindexes += [indexes[j] + [i]]
                            newfindexes += [findexes[j] + [i + 1]]

                    indexes = newindexes[:]
                    findexes = newfindexes[:]

            except:
                pass

        indexes = [ tuple(i) for i in indexes ]
        if len(shp) == 1:
            findexes = [ '(%i)' % idx[0] for idx in findexes ]
        else:
            findexes = [ str(tuple(idx)) for idx in findexes ]
        definition = ''
        for i in xrange(len(indexes)):
            fval = fval2string(arr[indexes[i]], ftyp)
            definition += flines(fname + findexes[i] + ' = ' + fval)

    return (
     declaration, definition)


def fnumber(number, fname):
    typ = type(number).__name__
    if typ == 'int':
        ftyp = 'INTEGER '
    elif typ == 'float':
        ftyp = 'DOUBLE PRECISION '
    else:
        raise TypeError('Unsupported variable type')
    fval = fval2string(number, ftyp)
    declaration = flines(ftyp + fname)
    definition = flines(fname + ' = ' + fval)
    return (
     declaration, definition)


def fstring(string, fname):
    typ = type(string).__name__
    if typ == 'str':
        length = len(string)
        ftyp = 'CHARACTER*%i ' % length
    else:
        raise TypeError('Provide a string')
    declaration = flines(ftyp + fname)
    definition = flines(fname + ' = ' + "'" + string + "'")
    return (
     declaration, definition)


def fexport(variable, fname):
    if type(variable).__name__ == 'ndarray':
        return farray(variable, fname)
    if type(variable).__name__ in ('int', 'float'):
        return fnumber(variable, fname)
    if type(variable).__name__ == 'str':
        return fstring(variable, fname)


def ffnetrecall(net, fname):
    """
    Takes ffnet network instance and returns string representing
    fortran source of the recalling routine.
    """
    netroutine = flines('SUBROUTINE ' + fname + '(input, output)')
    descr = net.call.__doc__
    descr += 'Arguments:\n'
    descr += '    input - 1-d array of length %i\n' % len(net.inno)
    descr += '    output - 1-d array of length %i\n' % len(net.outno)
    descr = fcomment(descr, lstrip=True)
    declarations = ''
    definitions = ''
    n = len(net.conec)
    u = len(net.units)
    i = len(net.inno)
    o = len(net.outno)
    arrs = [
     'conec', 'inno', 'outno', 'weights', 'eni', 'deo']
    for name in arrs:
        deftuple = fexport(net.__dict__[name], name)
        declarations += deftuple[0]
        definitions += deftuple[1] + fcomment()

    declarations += flines('DOUBLE PRECISION units(%i)' % u)
    declarations += flines('DOUBLE PRECISION input(%i)' % i)
    declarations += flines('DOUBLE PRECISION output(%i)' % o)
    callnet = flines('CALL normcall( weights, conec, %i, units, %i, ' % (n, u))
    callnet += addfline('inno, %i, outno, %i, eni, deo, input, output )' % (i, o))
    routine = fcomment('-' * 66) + netroutine + fcomment('-' * 66) + descr + fcomment('-' * 66) + declarations + fcomment() + f2pyline('intent(in) input') + f2pyline('intent(out) output') + fcomment() + definitions + callnet + fcomment() + flines('END')
    return routine


def ffnetdiff(net, fname):
    """
    Takes ffnet network instance and returns string representing
    fortran source of the network derivative routine.
    """
    netroutine = flines('SUBROUTINE ' + fname + '(input, deriv)')
    descr = net.derivative.__doc__
    descr += 'Arguments:\n'
    descr += '    input - 1-d array of length %i\n' % len(net.inno)
    descr += '    deriv - 2-d array of the shape (%i, %i)\n' % (
     len(net.outno), len(net.inno))
    descr = fcomment(descr, lstrip=True)
    declarations = ''
    definitions = ''
    n = len(net.conec)
    u = len(net.units)
    i = len(net.inno)
    o = len(net.outno)
    dn = len(net.dconecno)
    arrs = [
     'conec', 'dconecno', 'dconecmk', 'inno', 'outno',
     'weights', 'eni', 'ded']
    for name in arrs:
        deftuple = fexport(net.__dict__[name], name)
        declarations += deftuple[0]
        definitions += deftuple[1] + fcomment()

    declarations += flines('DOUBLE PRECISION units(%i)' % u)
    declarations += flines('DOUBLE PRECISION input(%i)' % i)
    declarations += flines('DOUBLE PRECISION deriv(%i, %i)' % (o, i))
    callnet = flines('CALL normdiff( weights, conec, %i, dconecno, %i, ' % (n, dn))
    callnet += addfline('dconecmk, units, %i, inno, %i, outno, %i, ' % (u, i, o))
    callnet += addfline('eni, ded, input, deriv)')
    routine = fcomment('-' * 66) + netroutine + fcomment('-' * 66) + descr + fcomment('-' * 66) + declarations + fcomment() + f2pyline('intent(in) input') + f2pyline('intent(out) deriv') + fcomment() + definitions + callnet + fcomment() + flines('END')
    return routine


def fheader(net, version=''):
    inlimits = ''
    outlimits = ''
    for i, line in enumerate(net.inlimits):
        inlimits += flines('%i --> %s' % (i + 1, str(line)))

    for o, line in enumerate(net.outlimits):
        outlimits += flines('%i --> %s' % (o + 1, str(line)))

    header = "##################################################################\nTHIS FILE IS AUTOMATICALLY GENERATED WITH:\n\nffnet-%s, feed-forward neural network for python\nhttp://ffnet.sourceforge.net\n\nCopyright (C) 2006 by Marek Wojciechowski\n<mwojc@p.lodz.pl>\n\nDistributed under the terms of the GNU General Public License:\nhttp://www.gnu.org/copyleft/gpl.html\n##################################################################\n\nNETWORK SPECIFICATION\n%s\n\nINPUT LIMITS\n%s\nOUTPUT LIMITS\n%s\nNOTE: You need 'ffnet.f' file distributed with ffnet-%s\n      sources to get the below routines to work.\n" % (version, net.__repr__(), inlimits, outlimits, version)
    header = fcomment(header)
    return header