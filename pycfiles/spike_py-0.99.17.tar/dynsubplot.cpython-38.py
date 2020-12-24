# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/dynsubplot.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 8170 bytes
"""
Code permitting to make easily subplot without having to anticipate the number of plot. 
Just the number of columns is needed. 
typical syntax is :
    sub = subpl(nbsub_h = 2) # suplot organized in two columns
    sub.next() # adding new subplot
    sub.plot(np.arange(6), np.arange(6)**2, 'g', label = 'one') # first plot in first subplot
    sub.title('One')
"""
from __future__ import print_function
import numpy as np, unittest

def add_meth(attr):
    """
    Evaluates methods created in dec_class. 
    Replaces pyplot method by methods which keep the arguments. 
    for example, subpl.title() will stock its arguments in the list "subpl.ltitle"
    """

    def wrapped(*args, **kwargs):
        eval('subpl.l' + attr + '.append([args[1:], kwargs])')
        if attr == 'plot':
            eval('subpl.l_num.append(subpl.numplot)')

    return classmethod(wrapped)


def add_class(l):
    """
    Each method in the list l is associated to a method defined with add_meth.
    This method as the same name as the pyplot method, but it has a different function. 
    It will append the arguments passed in the plotting code to a list "lmeth" which will contains the arguments. 
    Those
    
    """

    def dec_class(cls):
        setattr(cls, 'numplot', 0)
        for attr in l:
            setattr(cls, attr, add_meth(attr))
            setattr(cls, 'l' + attr, [])
            if attr == 'plot':
                setattr(cls, 'l_num', [])
            return cls

    return dec_class


l = [
 'title', 'xlabel', 'ylabel', 'plot', 'xticklabels', 'ax']

@add_class(l)
class subpl:
    __doc__ = '\n    Iterator for returning automatically\n    the number of the subplot iteratively.\n    nbsub_h is the number of subplot horizontally\n    which_plot is the kind of plot, fake plot or matplotlib pyplot plot.. \n    '

    def __init__(self, nbsub_h=1, which_plot=None):
        global plt
        if which_plot:
            print('using injected pyplot')
            plt = which_plot
        else:
            plt = globals()['plt']
        self.fig = plt.figure()
        subpl.numplot = 0
        self.nbsub_h = nbsub_h
        self.nbsub_v = 0
        for meth in dir(self):
            if meth[0] == 'l':
                setattr(subpl, meth, [])

    def next(self):
        """
        Increments the number of plots "subpl.numplot"
        And calculates the number of vertical lines. 
        """
        subpl.numplot += 1
        self.nbsub_v = (subpl.numplot - 1) / self.nbsub_h + 1

    def read_kargs(self, l):
        """
        """
        lkargs = ''
        for name in l:
            n = l[name]
            if type(n) == str:
                nkargs = '"' + n + '"'
            else:
                nkargs = str(n)
            lkargs += ',' + name + '=' + nkargs
        else:
            return lkargs

    def make_str_kargs(self, func, i):
        """
        Extracts the list containing the arguments from sublist [1] of each method,
        in the list "self.lmeth".
        """
        try:
            str_kargs = self.read_kargs(eval('self.l' + func + '[i][1]'))
        except:
            str_kargs = ''
        else:
            return str_kargs

    def select_pos(self, func):
        """
        
        """
        if func == 'plot':
            pos = '[i][0]'
        else:
            pos = '[numpl-1][0]'
        return pos

    def show(self):
        """
        Takes all the list of arguments from the fake methods sub.meth
        And evaluates them one after the other with the correct pyplot corresponding method. 
        """
        nbticks = None
        for i, numpl in enumerate(self.l_num):
            self.ax = self.fig.add_subplot(self.nbsub_v, self.nbsub_h, numpl)

        for func in l:
            str_kargs = self.make_str_kargs(func, i)
            pos = self.select_pos(func)
            arg = '(*self.l' + func + pos + str_kargs + ')'
            if func != 'plot':
                try:
                    expr_eval = 'self.ax.set_' + func + arg
                    eval(expr_eval)
                except:
                    pass
                else:
                    if func == 'xticklabels':
                        try:
                            nbticks = len(self.lxticklabels[(numpl - 1)][0][0]) - 1
                        except:
                            nbticks = None

            elif func == 'plot':
                expr_eval = 'self.ax.' + func + arg
                eval(expr_eval)
                if str_kargs != '':
                    plt.legend()
        else:
            if nbticks:
                if not hasattr(plt, 'FAKE'):
                    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=nbticks))
            plt.show()


class Test_dynsubplot(unittest.TestCase):
    __doc__ = '\n    Unittests for dynsubplot with four subplots.\n    First plot contains 2 plots. \n    '

    def test_dynsub(self):
        global plt
        import spike.Display.testplot as testplot
        plt = testplot.plot()
        sub = subpl(nbsub_h=2)
        sub.next()
        sub.plot((np.arange(6)), (np.arange(6) ** 2), 'g', label='one')
        sub.title('One')
        sub.ylabel('y1')
        sub.xlabel('x1')
        sub.plot((np.cos(np.arange(11))), label='two')
        sub.next()
        sub.title('Second sub')
        sub.plot((np.sin(np.arange(15))), label='three')
        sub.ylabel('y3')
        sub.next()
        sub.ylabel('y4')
        sub.title('Third')
        sub.plot((np.arange(21)), 'g', label='four')
        sub.next()
        sub.ylabel('y5')
        sub.title('Forth subplot')
        sub.plot((np.cos(np.arange(21)) - np.arange(21)), 'r', label='five')
        sub.show()
        sub = subpl(nbsub_h=2)
        sub.next()
        sub.plot((np.arange(10)), (np.arange(10) ** 3), 'g', label='one')
        sub.title('One')
        sub.ylabel('y1')
        sub.xlabel('x1')
        sub.plot((np.sin(np.arange(20))), label='two')
        sub.next()
        sub.title('Second sub')
        sub.plot((np.cos(np.arange(41))), label='three')
        sub.ylabel('y3')
        sub.show()


if __name__ == '__main__':
    unittest.main()