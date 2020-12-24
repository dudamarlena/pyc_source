# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/learning/optimize.py
# Compiled at: 2018-04-24 04:48:32
import sys, time, math
from dnutils import logs
try:
    import numpy
    from scipy.optimize import fmin_bfgs, fmin_cg, fmin_ncg, fmin_tnc, fmin_l_bfgs_b, fsolve, fmin_slsqp, fmin, fmin_powell
except:
    sys.stderr.write('Warning: Failed to import SciPy/NumPy (http://www.scipy.org)! Parameter learning with PyMLNs is disabled.\n')

class DirectDescent(object):
    """
    Naive gradient descent optimization.
    """

    def __init__(self, wt, learner, gtol=0.001, maxiter=None, learningRate=0.1, **params):
        self.learner = learner
        self.wt = wt
        self.gtol = gtol
        self.maxiter = iter
        self.learningRate = learningRate
        if self.learningRate < 0.0 or self.learningRate >= 1.0:
            raise Exception('learning rate must lie in [0,1[: %s' % self.learningRate)

    def run(self):
        log = logs.getlogger(self.__class__.__name__)
        norm = 1
        alpha = 1.0
        step = 1
        log.info('starting optimization with %s... (alpha=%f)' % (self.__class__.__name__, alpha))
        f_ = None
        while True:
            grad = self.learner.grad(self.wt)
            norm = numpy.linalg.norm(grad)
            f_ = self.learner.f(self.wt)
            print
            print '|grad| =', norm
            if norm < self.gtol or self.maxiter is not None and step > self.maxiter:
                break
            exitNow = False
            w_ = None
            smaller = False
            bigger = False
            f_opt = f_
            while not exitNow:
                w = self.wt + grad * alpha
                print
                f = self.learner.f(w, verbose=True)
                if f_ < f:
                    if f_opt < f:
                        self.wt = numpy.array(list(w))
                        f_ = f
                        alpha *= 1 + self.learningRate
                        exitNow = True
                    bigger = True
                    w_ = numpy.array(list(w))
                elif f_ > f:
                    if bigger:
                        if f_opt < f:
                            self.wt = w_
                            f_ = f
                        exitNow = True
                    alpha *= 1.0 - self.learningRate
                    smaller = True
                else:
                    exitNow = True
                f_ = f

            print
            print 'alpha =', alpha

        return self.wt


class DiagonalNewton(object):

    def __init__(self, wt, problem, gtol=0.01, maxSteps=None):
        self.problem = problem
        self.wt = wt
        self.gtol = gtol
        self.maxSteps = maxSteps

    def run(self):
        p = self.problem
        grad_fct = lambda wt: p.grad(wt)
        wt = numpy.matrix(self.wt).transpose()
        wtarray = numpy.asarray(wt.transpose())[0]
        N = len(wt)
        l = 0.5
        g = numpy.asmatrix(grad_fct(wtarray)).transpose()
        d = numpy.sign(g)
        dT = d.transpose()
        step = 1
        while self.maxSteps is None or step <= self.maxSteps:
            normg = numpy.linalg.norm(g)
            if normg <= self.gtol:
                print '\nThreshold reached after %d steps. final gradient: %s (norm: %f <= %f)' % (step, g.transpose(), normg, self.gtol)
                break
            H = -p.hessian(wtarray)
            sgrad = numpy.asmatrix(numpy.zeros(N)).transpose()
            for i in xrange(N):
                v = H[i][i]
                if v == 0.0:
                    sgrad[i] = g[i] = 0.0
                else:
                    sgrad[i] = g[i] / v

            delta_predict = dT * (g + H * g) / 2.0
            alpha_numerator = dT * g
            alpha_q = dT * H * d
            while True:
                alpha = numpy.float(alpha_numerator / (alpha_q + l * dT * d))
                wt_old = numpy.matrix(wt)
                wt += alpha * sgrad
                wtarray = numpy.asarray(wt.transpose())[0]
                g = numpy.asmatrix(grad_fct(wtarray)).transpose()
                d = numpy.sign(g)
                dT = d.transpose()
                delta_actual = dT * g
                frac = delta_actual / delta_predict
                if frac > 0.75:
                    l /= 2.0
                elif frac < 0.25:
                    if l != 0.0:
                        l *= 4.0
                    else:
                        l = 1e-05
                if delta_actual >= 0:
                    print
                    print 'step %d' % step
                    print 'H:\n%s' % H
                    print '|g|: %f' % normg
                    print 'sgrad: %s' % sgrad.transpose()
                    print 'delta_a: %f' % delta_actual
                    print 'delta_p: %f' % delta_predict
                    print 'lambda: %.18f' % l
                    print 'alpha: %f' % alpha
                    print 'old wt: %s' % wt_old.transpose()
                    print 'new wt: %s' % wt.transpose()
                    break
                else:
                    print 'delta_a=%f, adjusted lambda to %f' % (delta_actual, l)
                    wt = wt_old

            step += 1

        return numpy.asarray(wt.transpose())[0]


class SciPyOpt(object):
    """
    Wrapper around the optimization techniques implemented by SciPy.
    """

    def __init__(self, optimizer, wt, problem, verbose=False, **optParams):
        self.wt = wt
        self.problem = problem
        self.optParams = optParams
        self.optimizer = optimizer
        self.verbose = verbose

    def run(self):
        optimizer = self.optimizer
        p = self.problem
        f = p.f
        grad = p.grad
        f = lambda wt: numpy.float64(p.f(wt))
        grad = lambda wt: numpy.array(map(numpy.float64, p.grad(wt)))
        neg_f = lambda wt: -f(wt)
        neg_grad = lambda wt: -grad(wt)
        if not p.usef:
            neg_f = lambda wt: -p._fDummy(wt)
        log = logs.getlogger(self.__class__.__name__)
        if optimizer == 'bfgs':
            params = dict(filter(lambda (k, v): k in ('gtol', 'epsilon', 'maxiter'), self.optParams.iteritems()))
            if self.verbose:
                print 'starting optimization with %s... %s' % (optimizer, params)
            wt, f_opt, grad_opt, Hopt, func_calls, grad_calls, warn_flags = fmin_bfgs(neg_f, self.wt, fprime=neg_grad, full_output=True, **params)
            if self.verbose:
                print 'optimization done with %s...' % optimizer
                print 'f-opt: %.16f\nfunction evaluations: %d\nwarning flags: %d\n' % (-f_opt, func_calls, warn_flags)
        elif optimizer == 'cg':
            params = dict(filter(lambda (k, v): k in ('gtol', 'epsilon', 'maxiter'), self.optParams.iteritems()))
            log.info('starting optimization with %s... %s' % (optimizer, params))
            wt, f_opt, func_calls, grad_calls, warn_flags = fmin_cg(neg_f, self.wt, fprime=neg_grad, args=(), full_output=True, **params)
            log.info('optimization done with %s...' % optimizer)
            log.info('f-opt: %.16f\nfunction evaluations: %d\nwarning flags: %d\n' % (-f_opt, func_calls, warn_flags))
        elif optimizer == 'ncg':
            params = dict(filter(lambda (k, v): k in ('avextol', 'epsilon', 'maxiter'), self.optParams.iteritems()))
            log.info('starting optimization with %s... %s' % (optimizer, params))
            wt, f_opt, func_calls, grad_calls, warn_flags = fmin_ncg(neg_f, self.wt, fprime=neg_grad, args=(), full_output=True, **params)
            log.info('optimization done with %s...' % optimizer)
            log.info('f-opt: %.16f\nfunction evaluations: %d\nwarning flags: %d\n' % (-f_opt, func_calls, warn_flags))
        elif optimizer == 'fmin':
            params = dict(filter(lambda (k, v): k in ('xtol', 'ftol', 'maxiter'), self.optParams.iteritems()))
            log.info('starting optimization with %s... %s' % (optimizer, params))
            wt = fmin(neg_f, self.wt, args=(), full_output=True, **params)
            log.info('optimization done with %s...' % optimizer)
        elif optimizer == 'powell':
            params = dict(filter(lambda (k, v): k in ('xtol', 'ftol', 'maxiter'), self.optParams.iteritems()))
            log.info('starting optimization with %s... %s' % (optimizer, params))
            wt = fmin_powell(neg_f, self.wt, args=(), full_output=True, **params)
            log.info('optimization done with %s...' % optimizer)
        elif optimizer == 'l-bfgs-b':
            params = dict(filter(lambda (k, v): k in ('gtol', 'epsilon', 'maxiter', 'bounds'), self.optParams.iteritems()))
            log.info('starting optimization with %s... %s' % (optimizer, params))
            if 'bounds' in params:
                params['bounds'] = (
                 params['bounds'],) * len(self.wt)
            wt, f_opt, d = fmin_l_bfgs_b(neg_f, self.wt, fprime=neg_grad, **params)
            log.info('optimization done with %s...' % optimizer)
            log.info('f-opt: %.16f\n' % -f_opt)
        else:
            raise Exception("Unknown optimizer '%s'" % optimizer)
        return wt