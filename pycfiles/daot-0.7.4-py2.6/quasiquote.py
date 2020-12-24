# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\builtins\quasiquote.py
# Compiled at: 2011-11-10 02:08:10
from dao import builtin
from dao.builtin import Builtin, Function
from dao.term import CommandCall
from dao.solve import DaoSyntaxError, mycont

def evaluate_quasiquote_list_cont(solver, cont, exps):

    @mycont(cont)
    def quasi_cont(result, solver):
        if len(exps) == 0:
            yield (
             cont, result)
        else:
            element0 = exps[0]
            left_cont = evaluate_quasiquote_list_cont(solver, cont, exps[1:])
            if element0 == ():
                yield (
                 left_cont, result + ((), ))
                return
                if isinstance(element0, tuple) or element0 == unquote or element0 == unquote_slice:
                    raise DaoSyntaxError
                else:
                    yield (
                     left_cont, result + (element0,))
                    return
            elif len(element0) == 2:
                if element0[0] == unquote:

                    @mycont(quasi_cont)
                    def gather_cont(value, solver):
                        yield (left_cont, result + (value,))

                    yield (solver.cont(element0[1], gather_cont), True)
                    return
                if element0[0] == unquote_slice:

                    @mycont(quasi_cont)
                    def gather_cont(value, solver):
                        yield (left_cont, result + value)

                    yield (solver.cont(element0[1], gather_cont), True)
                    return
            elif element0[0] == unquote or element0[0] == unquote_slice:
                raise DaoSyntaxError

            @mycont(quasi_cont)
            def gather_cont(value, solver):
                yield (left_cont, result + (value,))

            yield (evaluate_quasiquote_list_cont(solver, gather_cont, element0), ())

    return quasi_cont


@builtin.macro('quasiquote')
def quasiquote(solver, cont, item):
    if not isinstance(item, tuple) or item == ():
        yield (
         cont, item)
        return
    if len(item) == 2:
        if item[0] == unquote:
            yield (
             solver.cont(item[1], cont), True)
            return
        if item[0] == unquote_slice:
            raise DaoSyntaxError
    elif item[0] == unquote or item[0] == unquote_slice:
        raise DaoSyntaxError
    yield (evaluate_quasiquote_list_cont(solver, cont, item), ())


@builtin.macro('unquote')
def unquote(solver, cont, *args):
    raise DaoSyntaxError


@builtin.macro('unquote_slice')
def unquote_slice(solver, cont, *args):
    raise DaoSyntaxError