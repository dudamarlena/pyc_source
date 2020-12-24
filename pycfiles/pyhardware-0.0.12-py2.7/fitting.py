# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\curve\fitting.py
# Compiled at: 2013-10-05 03:48:04
import pandas, scipy.optimize, numpy, collections, math
LAMBDA = 1.064e-06

class FitFunctions(object):

    def lorentz(self, scale, x0, y0, bandwidth):
        x = self.x()
        return scale / (1 + (x - x0) / bandwidth * ((x - x0) / bandwidth)) + y0

    def linear(self, x0, slope):
        x = self.x()
        return slope * (x - x0)

    def lorentzSB(self, scale, x0, y0, bandwidth, SBwidth, SBscale):
        x = self.x()
        return y0 + scale * (1 / (1 + (x - x0) / bandwidth * ((x - x0) / bandwidth)) + SBscale / (1 + ((x - x0 - SBwidth) / bandwidth) ** 2) + SBscale / (1 + ((x - x0 + SBwidth) / bandwidth) ** 2))

    def gaussianbeam(self, x0, w0):
        x = self.x()
        return w0 * ((x - x0) ** 2 / math.pi ** 2 / w0 ** 4 * LAMBDA ** 2 + 1) ** 0.5

    def _guessgaussianbeam(self):
        tempfit = Fit(data=self.data, func='linear', maxiter=10)
        res = tempfit.getparams()
        params = dict(x0=res['x0'], w0=LAMBDA / math.pi / res['slope'])
        return params

    def _guesslorentz(self):
        x0 = float(self.x()[self.data.argmax()])
        max = self.data.max()
        min = self.data.min()
        bw = 0.1 * (self.x().max() - self.x().min())
        fit_params = {'x0': x0, 'y0': min, 'scale': max - min, 'bandwidth': bw}
        return fit_params

    def _guesslorentzSB(self):
        x0 = float(self.x()[self.data.argmax()])
        max = self.data.max()
        min = self.data.min()
        bw = 0.1 * (self.x().max() - self.x().min())
        fit_params = {'x0': x0, 'y0': min, 'scale': max - min, 'bandwidth': bw, 'SBwidth': 1.8 * bw, 
           'SBscale': 0.3}
        return fit_params

    def _guesslinear(self):
        max = self.data.max()
        min = self.data.min()
        slope = (max - min) / (self.x().max() - self.x().min())
        x0 = self.x().mean() - self.data.mean() / slope
        fit_params = {'x0': x0, 'slope': slope}
        return fit_params


class Fit(FitFunctions):

    def __init__(self, data, func, fixed_params={}, manualguess_params={}, autoguessfunction='', verbosemode=True, maxiter=100):
        self.data = data
        self.sqerror = float('nan')
        self.verbosemode = verbosemode
        self.stepcount = 0
        self.maxiter = maxiter
        self.fitfunctions = FitFunctions()
        self.commentstring = ''
        self.fixed_params = collections.OrderedDict(fixed_params)
        self.manualguess_params = collections.OrderedDict(manualguess_params)
        self.func = func
        self.fn = self.__getattribute__(self.func)
        self.autoguessfunction = autoguessfunction
        if self.autoguessfunction == '':
            self.fn_guess = self.__getattribute__('_guess' + self.func)
        else:
            self.fn_guess = self.__getattribute__(self.autoguessfunction)
        self.autoguess_params = self.fn_guess()
        self.fit_params = collections.OrderedDict()
        for key in self.fn.func_code.co_varnames[1:self.fn.func_code.co_argcount]:
            if key in self.fixed_params:
                pass
            elif key in self.manualguess_params:
                self.fit_params[key] = self.manualguess_params[key]
            else:
                self.fit_params[key] = self.autoguess_params[key]

        self.comment('Square sum of data: ' + str((self.data ** 2).sum()))
        self.comment('Calling fit function with following guesses: ')
        self.comment(str(dict(self.getparams())))
        res = self.fit()
        self.comment('Return of fit optimisation function: ')
        self.comment(str(res))

    def getparams(self):
        params = self.fit_params.copy()
        params.update(self.fixed_params)
        return params

    def sqerror(self):
        return self.squareerror(self.fit_params.values())

    def squareerror(self, kwds):
        for index, key in enumerate(self.fit_params):
            self.fit_params[key] = float(kwds[index])

        self.sqerror = float(((self.fn(**self.getparams()) - self.data.values) ** 2).sum())
        return self.sqerror

    def comment(self, string):
        if self.verbosemode is True:
            print string
        self.commentstring += str(string) + '\r\n'

    def x(self):
        return numpy.array(self.data.index, dtype=float)

    def fit(self):
        res = scipy.optimize.minimize(fun=self.squareerror, x0=self.fit_params.values(), args=(), method='BFGS', jac=False, hess=None, hessp=None, bounds=None, constraints=(), tol=0.1, callback=self.printstatus, options={'maxiter': self.maxiter, 'disp': self.verbosemode})
        self.comment('Fit completed with sqerror = ' + str(self.sqerror))
        self.comment('Obtained parameter values: ')
        self.comment(dict(self.getparams()))
        self.comment('Fit completed with sqerror = ' + str(self.sqerror))
        self.fitdata = pandas.Series(data=self.fn(**self.getparams()), index=self.x(), name='fitfunction: ' + self.func)
        return res

    def getoversampledfitdata(self, numbersamples):
        datasafe = self.data
        maxindex = self.x().max()
        print maxindex
        minindex = self.x().min()
        print minindex
        newindex = numpy.array(numpy.linspace(minindex, maxindex, numbersamples), dtype=float)
        self.data = pandas.Series(data=newindex, index=newindex)
        self.fitdata = pandas.Series(data=self.fn(**self.getparams()), index=self.x(), name='fitfunction: ' + self.func)
        self.data = datasafe
        return self.fitdata

    def printstatus(self, dummy):
        self.stepcount += 1
        self.comment('Step ' + str(self.stepcount) + ' with sqerror = ' + str(self.sqerror))
        self.comment(dict(self.getparams()))
        self.comment('dummy: ' + str(dummy))

    def _guesslorentzSBfromlorentzOld_tobedeleted(self):
        self.comment('Estimating first fit parameters from simple lorentz fit')
        tempfit = Fit(data=self.data, func='lorentz', autoguessfunction='', fixed_params=self.fixed_params, manualguess_params=self.manualguess_params, verbosemode=self.verbosemode, maxiter=20)
        tempfit_params = tempfit.getparams()
        self.comment('')
        self.comment('Estimating remaining fit parameters from lorentzSB fit with fixed previously determined parameters')
        tempfit = Fit(data=self.data, func='lorentzSB', autoguessfunction='', fixed_params=tempfit_params, manualguess_params=self.manualguess_params, verbosemode=self.verbosemode, maxiter=20)
        fit_params = tempfit.getparams()
        return fit_params

    def _guesslorentzSBguessfixfromlorentzSB(self):
        """use the more evolved guess from guesslorentzSBfixfromlorentz"""
        self.comment('perform guesslorentzSBfixfromlorentz...')
        tempfit = Fit(data=self.data, func='lorentzSB', autoguessfunction='_guesslorentzSBfixfromlorentz', fixed_params=self.fixed_params, manualguess_params=self.manualguess_params, verbosemode=self.verbosemode, maxiter=15)
        fit_params = tempfit.getparams()
        self.fixed_params['bandwidth'] = fit_params['bandwidth']
        self.fixed_params['SBwidth'] = fit_params['SBwidth']
        return fit_params

    def _guesslorentzSBguessfromlorentzSB(self):
        """use the more evolved guess from guesslorentzSBfixfromlorentz"""
        self.comment('perform guesslorentzSBfixfromlorentz...')
        tempfit = Fit(data=self.data, func='lorentzSB', autoguessfunction='_guesslorentzSBfixfromlorentz', fixed_params=self.fixed_params, manualguess_params=self.manualguess_params, verbosemode=self.verbosemode, maxiter=15)
        fit_params = tempfit.getparams()
        return fit_params

    def _guesslorentzSBfixfromlorentz(self):
        self.comment('Estimating first fit parameters from simple lorentz fit')
        tempfit = Fit(data=self.data, func='lorentz', autoguessfunction='_guesslorentz', fixed_params=self.fixed_params, manualguess_params=self.manualguess_params, verbosemode=self.verbosemode, maxiter=15)
        tempfit_params = tempfit.getparams()
        bwguess = tempfit_params.pop('bandwidth')
        tempfit_params.update(self.fixed_params)
        self.fixed_params = tempfit_params.copy()
        fitparams = collections.OrderedDict({'bandwidth': bwguess / 2.0, 'SBwidth': 1.1 * bwguess, 
           'SBscale': 0.25})
        self.comment('Prefit for parameter guess obtained the following results: ')
        self.comment('Fixed: ' + str(self.fixed_params))
        self.comment('Manual: ' + str(self.manualguess_params))
        self.comment('Automatic: ' + str(fitparams))
        return fitparams