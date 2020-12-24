# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\evolutionary_algorithm.py
# Compiled at: 2018-04-26 12:25:04
# Size of source mod 2**32: 65938 bytes
"""
Evolutionary Algorithms are population based stochastic global optimization
methods.

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from warnings import warn
try:
    from mpi4py import MPI
except ImportError:
    mpi_exist = False
else:
    mpi_exist = True
__all__ = ['Evolutionary']

class Evolutionary:
    __doc__ = "\n    Evolutionary Algorithm optimizer.\n    \n    This optimizer minimizes an objective function using Differential\n    Evolution (DE), Particle Swarm Optimization (PSO), Competitive Particle\n    Swarm Optimization (CPSO), Covariance Matrix Adaptation - Evolution\n    Strategy (CMA-ES), or VD-CMA.\n    \n    Parameters\n    ----------\n    func : callable\n        Objective function. If necessary, the variables required for its\n        computation should be passed in 'args' and/or 'kwargs'.\n    lower : ndarray, optional, default None\n        Search space lower boundary.\n    upper : ndarray, optional, default None\n        Search space upper boundary.\n    n_dim : int, optional, default 1\n        Search space dimension. Only used if 'lower' and 'upper' are not\n        provided.\n    popsize : int, optional, default 10\n        Population size.\n    max_iter : int, optional, default 100\n        Maximum number of iterations.\n    eps1 : scalar, optional, default 1e-8\n        Minimum change in best individual.\n    eps2 : scalar, optional, default 1e-8\n        Minimum objective function precision.\n    constrain : bool, optional, default True\n        Constrain to search space if an individual leave the search space.\n    snap : bool, optional, default False\n        Save the positions and energy of all individuals at each iteration\n        in a 3-D array with shape (n_dim, popsize, max_iter) and 2-D array\n        with shape (popsize, max_iter) in attributes 'models' and 'energy'.\n    random_state : int, optional, default None\n        Seed for random number generator.\n    mpi : bool, default False\n        Enable MPI parallelization.\n    args : list or tuple, optional, default ()\n        Arguments passed to func.\n    kwargs : dict, optional, default {}\n        Keyworded arguments passed to func.\n    "
    _ATTRIBUTES = [
     'solution', 'fitness', 'n_iter', 'n_eval', 'flag']

    def __init__(self, func, lower=None, upper=None, n_dim=1, popsize=10, max_iter=100, eps1=1e-08, eps2=1e-08, constrain=True, snap=False, random_state=None, mpi=False, args=(), kwargs={}):
        if not hasattr(func, '__call__'):
            raise ValueError('func is not callable')
        else:
            self._func = lambda x: func(x, *args, **kwargs)
        if lower is None:
            if upper is not None:
                raise ValueError('lower is not defined')
        if upper is None:
            if lower is not None:
                raise ValueError('upper is not defined')
        if lower is not None:
            if upper is not None:
                if len(lower) != len(upper):
                    raise ValueError('lower and upper must have the same length')
                if np.any(upper < lower):
                    raise ValueError('upper must be greater than lower')
                self._lower = np.array(lower)
                self._upper = np.array(upper)
                self._n_dim = len(lower)
            else:
                self._lower = np.full(n_dim, -100.0)
                self._upper = np.full(n_dim, 100.0)
                self._n_dim = n_dim
        else:
            if not isinstance(max_iter, int) or max_iter <= 0:
                raise ValueError('max_iter must be a positive integer, got %s' % max_iter)
            else:
                self._max_iter = max_iter
            if not isinstance(popsize, float) and not isinstance(popsize, int) or popsize < 2:
                raise ValueError('popsize must be an integer > 1, got %s' % popsize)
            else:
                self._popsize = int(popsize)
            if not isinstance(eps1, float) and not isinstance(eps1, int) or eps1 < 0.0:
                raise ValueError('eps1 must be positive, got %s' % eps1)
            else:
                self._eps1 = eps1
        if not isinstance(eps2, float):
            if not isinstance(eps2, int):
                raise ValueError('eps2 must be an integer or float, got %s' % eps2)
            else:
                self._eps2 = eps2
            if not isinstance(constrain, bool):
                raise ValueError('constrain must be either True or False, got %s' % constrain)
            else:
                self._constrain = constrain
            if not isinstance(snap, bool):
                raise ValueError('snap must be either True or False, got %s')
            else:
                self._snap = snap
            if random_state is not None:
                if random_state >= 0:
                    np.random.seed(random_state)
            raise isinstance(mpi, bool) or ValueError('mpi must be either True or False, got %s' % mpi)
        else:
            self._mpi = mpi
        if mpi:
            if not mpi_exist:
                raise ValueError('mpi4py is not installed or not properly installed')
        if not isinstance(args, (list, tuple)):
            raise ValueError('args must be a list or a tuple')
        if not isinstance(kwargs, dict):
            raise ValueError('kwargs must be a dictionary')

    def __repr__(self):
        attributes = ['%s: %s' % (attr.rjust(13), self._print_attr(attr)) for attr in self._ATTRIBUTES]
        if self._solver == 'cpso':
            attributes.append('%s: %s' % ('n_restart'.rjust(13), self._print_attr('n_restart')))
        if self._mpi:
            attributes.append('%s: %s seconds' % ('t_serial'.rjust(13), self._print_attr('t_serial')))
            attributes.append('%s: %s seconds' % ('t_parallel'.rjust(13), self._print_attr('t_parallel')))
        return '\n'.join(attributes) + '\n'

    def _print_attr(self, attr):
        ATTRIBUTES = self._ATTRIBUTES + ['n_restart']
        if self._mpi:
            ATTRIBUTES += ['t_serial', 't_parallel']
        else:
            if attr not in ATTRIBUTES:
                raise ValueError('attr should be in %s' % ATTRIBUTES)
            elif attr == 'solution':
                param = '\n'
                for i in range(self._n_dim):
                    tmp = '%.8g' % self._xopt[i]
                    if self._xopt[i] >= 0.0:
                        tmp = ' ' + tmp
                    param += '\t\t%s\n' % tmp

                return param[:-1]
        if attr == 'fitness':
            return '%.8g' % self._gfit
        if attr == 'n_iter':
            return '%d' % self._n_iter
        if attr == 'n_eval':
            return '%d' % self._n_eval
        if attr == 'n_restart':
            return '%d' % self._n_restart
        if attr == 'flag':
            return '%s' % self.flag
        if attr == 't_serial':
            return '%.8g' % np.sum(self._time_serial)
        if attr == 't_parallel':
            return '%.8g' % np.sum(self._time_parallel)

    def optimize(self, solver='cpso', xstart=None, sync=True, w=0.7298, c1=1.49618, c2=1.49618, gamma=1.0, F=0.5, CR=0.1, strategy='best2', sigma=0.5, mu_perc=0.5):
        """
        Minimize an objective function using Differential Evolution (DE),
        Particle Swarm Optimization (PSO), Competitive Particle Swarm
        Optimization (CPSO), Covariance Matrix Adaptation - Evolution
        Strategy (CMA-ES), or VD-CMA.
        
        Parameters
        ----------
        solver : {'de', 'pso', 'cpso', 'cmaes', 'vdcma'}, default 'cpso'
            Optimization method.
            - 'de', Differential Evolution.
            - 'pso', Particle Swarm Optimization.
            - 'cpso', Competitive Particle Swarm Optimization.
            - 'cmaes', Covariance Matrix Adaptation - Evolution Strategy.
            - 'vdcma', VD-CMA.
        xstart : None or ndarray, optional, default None
            Initial positions of the population or mean (if solver = 'cmaes').
        sync : bool, optional, default True
            Synchronize population, the best individual is updated after each
            iteration which allows the parallelization. Only used if 'solver'
            is 'pso', 'cpso', or 'de'.
        w : scalar, optional, default 0.7298
            Inertial weight. Only used when solver = {'pso', 'cpso'}.
        c1 : scalar, optional, default 1.49618
            Cognition parameter. Only used when solver = {'pso', 'cpso'}.
        c2 : scalar, optional, default 1.49618
            Sociability parameter. Only used when solver = {'pso', 'cpso'}.
        gamma : scalar, optional, default 1.
            Competitivity parameter. Only used when solver = 'cpso'.
        F : scalar, optional, default 0.5
            Differential weight. Only used when solver = 'de'.
        CR : scalar, optional, default 0.1
            Crossover probability. Only used when solver = 'de'.
        strategy : {'rand1', 'rand2', 'best1', 'best2'}, optional, default 'best2'
            Mutation strategy.
            - 'rand1', mutate a random vector by adding one scaled difference vector.
            - 'rand2', mutate a random vector by adding two scaled difference vectors.
            - 'best1', mutate the best vector by adding one scaled difference vector.
            - 'best2', mutate the best vector by adding two scaled difference vectors.
        sigma : scalar, optional, default 0.5
            Step size. Only used when solver = {'cmaes', 'vdcma'}.
        mu_perc : scalar, optional, default 0.5
            Number of parents as a percentage of population size. Only used
            when solver = {'cmaes', 'vdcma'}.
            
        Returns
        -------
        xopt : ndarray
            Optimal solution found by the optimizer.
        gfit : scalar
            Objective function value of the optimal solution.
        
        Examples
        --------
        Import the module and define the objective function (Rosenbrock):
        
        >>> import numpy as np
        >>> from stochopy import Evolutionary
        >>> f = lambda x: 100*np.sum((x[1:]-x[:-1]**2)**2)+np.sum((1-x[:-1])**2)
        
        Define the search space boundaries in 5-D:
        
        >>> n_dim = 5
        >>> lower = np.full(n_dim, -5.12)
        >>> upper = np.full(n_dim, 5.12)
        
        Initialize the Evolutionary Algorithm optimizer:
        
        >>> popsize = 30
        >>> max_iter = 1000
        >>> ea = Evolutionary(f, lower = lower, upper = upper,
                              popsize = popsize, max_iter = max_iter)
        
        Differential Evolution:
        
        >>> xopt, gfit = ea.optimize(solver = "de", F = 0.5, CR = 0.1)
        
        Particle Swarm Optimization:
        
        >>> xopt, gfit = ea.optimize(solver = "pso")
        
        Covariance Matrix Adaptation - Evolution Strategy:
        
        >>> xopt, gfit = ea.optimize(solver = "cmaes")
        """
        if not isinstance(solver, str) or solver not in ('cpso', 'pso', 'de', 'cmaes',
                                                         'vdcma'):
            raise ValueError("solver must either be 'cpso', 'pso', 'de', 'cmaes' or 'vdcma', got %s" % solver)
        elif not isinstance(sync, bool):
            raise ValueError('sync must either be True or False')
        else:
            if self._mpi:
                if solver in ('cpso', 'pso', 'de'):
                    if not sync:
                        raise ValueError('cannot use MPI with asynchrone population')
            else:
                self._solver = solver
                self._n_eval = 0
                self._n_restart = 0
                self._init_models()
                self._mu_scale = 0.5 * (self._upper + self._lower)
                self._std_scale = 0.5 * (self._upper - self._lower)
                if self._mpi:
                    self._mpi_comm = MPI.COMM_WORLD
                    self._mpi_rank = self._mpi_comm.Get_rank()
                    self._mpi_size = self._mpi_comm.Get_size()
                    self._time_serial = np.zeros(self._max_iter)
                    self._time_parallel = np.zeros(self._max_iter)
                else:
                    self._mpi_rank = 0
                self._mpi_size = 1
            if solver == 'pso':
                xopt, gfit = self._cpso(w=w, c1=c1, c2=c2, gamma=0.0, xstart=xstart,
                  sync=sync)
            else:
                if solver == 'cpso':
                    xopt, gfit = self._cpso(w=w, c1=c1, c2=c2, gamma=gamma, xstart=xstart,
                      sync=sync)
                else:
                    if solver == 'de':
                        xopt, gfit = self._de(F=F, CR=CR, strategy=strategy, xstart=xstart,
                          sync=sync)
                    else:
                        if solver == 'cmaes':
                            xopt, gfit = self._cmaes(sigma=sigma, mu_perc=mu_perc, xstart=xstart)
                        elif solver == 'vdcma':
                            xopt, gfit = self._vdcma(sigma=sigma, mu_perc=mu_perc, xstart=xstart)
        return (
         xopt, gfit)

    def _standardize(self, models):
        return (models - self._mu_scale) / self._std_scale

    def _unstandardize(self, models):
        return models * self._std_scale + self._mu_scale

    def _init_models(self):
        self._models = np.zeros((self._popsize, self._n_dim, self._max_iter))
        self._energy = np.zeros((self._popsize, self._max_iter))

    def _eval_models(self, models, it):
        n = models.shape[0]
        if self._mpi:
            starttime_parallel = MPI.Wtime()
            fit = np.zeros(n)
            fit_mpi = np.zeros_like(fit)
            self._mpi_comm.Barrier()
            self._mpi_comm.Bcast([models, MPI.DOUBLE], root=0)
            for i in np.arange(self._mpi_rank, n, self._mpi_size):
                fit_mpi[i] = self._func(self._unstandardize(models[i]))

            self._mpi_comm.Barrier()
            self._mpi_comm.Allreduce([fit_mpi, MPI.DOUBLE], [fit, MPI.DOUBLE], op=(MPI.SUM))
            self._time_parallel[it - 1] = MPI.Wtime() - starttime_parallel
        else:
            fit = np.array([self._func(self._unstandardize(models[i])) for i in range(n)])
        self._n_eval += n
        return fit

    def _constrain_de(self, models):
        """
        Random constraint for Differential Evolution. Parameters of models that
        are in the infeasible space are regenerated uniformly.
        """
        models = np.where(np.logical_or(models < -1.0, models > 1.0), np.random.uniform(-1.0, 1.0, models.shape), models)
        return models

    def _constrain_cpso(self, models, models_old):
        """
        Shrinking approach for Particle Swarm Optimization and Competitive PSO.
        Velocity vector amplitude is shrinked for models that are in the
        infeasible space. This approach preserves the trajectory of the
        particles.
        """
        maskl = models < -1.0
        masku = models > 1.0
        if np.any(maskl):
            if np.any(masku):
                beta_l = np.min((models_old[maskl] + 1.0) / (models_old[maskl] - models[maskl]))
                beta_u = np.min((models_old[masku] - 1.0) / (models_old[masku] - models[masku]))
                beta = min(beta_l, beta_u)
                models = models_old + beta * (models - models_old)
        if np.any(maskl) and not np.any(masku):
            beta = np.min((models_old[maskl] + 1.0) / (models_old[maskl] - models[maskl]))
            models = models_old + beta * (models - models_old)
        else:
            if not np.any(maskl) and np.any(masku):
                beta = np.min((models_old[masku] - 1.0) / (models_old[masku] - models[masku]))
                models = models_old + beta * (models - models_old)
        return models

    def _constrain_cma(self, arxvalid, arx, xmean, xold, sigma, diagC, mueff, it, bnd_weights, dfithist, validfitval, iniphase):
        """
        Box constraint handling by adding a penalty term that quantifies the
        distance of the parameters from the feasible parameter space.
        """
        arxvalid = np.where(arxvalid < -1.0, -np.ones_like(arxvalid), arxvalid)
        arxvalid = np.where(arxvalid > 1.0, np.ones_like(arxvalid), arxvalid)
        arfitness = self._eval_models(arxvalid, it)
        perc = np.percentile(arfitness, [25, 75])
        delta = (perc[1] - perc[0]) / self._n_dim / np.mean(diagC) / sigma ** 2
        if delta == 0:
            delta = np.min(dfithist[(dfithist > 0.0)])
        else:
            if not validfitval:
                dfithist = np.array([])
                validfitval = True
            if len(dfithist) < 20 + 3.0 * self._n_dim / self._popsize:
                dfithist = np.append(dfithist, delta)
            else:
                dfithist = np.append(dfithist[1:len(dfithist) + 1], delta)
        ti = np.logical_or(xmean < -1.0, xmean > 1.0)
        tx = np.where(xmean < -1.0, -np.ones_like(xmean), xmean)
        tx = np.where(xmean > 1.0, np.ones_like(xmean), xmean)
        if iniphase:
            if np.any(ti):
                bnd_weights.fill(2.0002 * np.median(dfithist))
                if validfitval:
                    if it > 2:
                        iniphase = False
        if np.any(ti):
            tx = xmean - tx
            idx = np.logical_and(ti, np.abs(tx) > 3.0 * max(1.0, np.sqrt(self._n_dim / mueff)) * sigma * np.sqrt(diagC))
            idx = np.logical_and(idx, np.sign(tx) == np.sign(xmean - xold))
            bnd_weights = np.array([w * 1.2 ** min(1.0, mueff / 10.0 / self._n_dim) if i else w for i, w in zip(idx, bnd_weights)])
        bnd_scale = np.exp(0.9 * (np.log(diagC) - np.mean(np.log(diagC))))
        arfitness += np.dot((arxvalid - arx) ** 2, bnd_weights / bnd_scale)
        return (arfitness, arxvalid, bnd_weights, dfithist, validfitval, iniphase)

    def _de_mutation(self, X, F, gbest, strategy, sync, i=None):
        if sync:
            idx = [list(range(self._popsize)) for i in range(self._popsize)]
            for i, l in enumerate(idx):
                l.remove(i)
                l = np.random.shuffle(l)

            idx = np.transpose(idx)
        else:
            idx = list(range(self._popsize))
            idx.remove(i)
            np.random.shuffle(idx)
            idx = np.array(idx)
        if strategy == 'rand1':
            X1 = np.array(X[idx[0], :])
            X2 = np.array(X[idx[1], :])
            X3 = np.array(X[idx[2], :])
            V = X1 + F * (X2 - X3)
        else:
            if strategy == 'rand2':
                X1 = np.array(X[idx[0], :])
                X2 = np.array(X[idx[1], :])
                X3 = np.array(X[idx[2], :])
                X4 = np.array(X[idx[3], :])
                X5 = np.array(X[idx[4], :])
                V = X1 + F * (X2 + X3 - X4 - X5)
            else:
                if strategy == 'best1':
                    X1 = np.array(X[idx[0], :])
                    X2 = np.array(X[idx[1], :])
                    V = gbest + F * (X1 - X2)
                else:
                    if strategy == 'best2':
                        X1 = np.array(X[idx[0], :])
                        X2 = np.array(X[idx[1], :])
                        X3 = np.array(X[idx[2], :])
                        X4 = np.array(X[idx[3], :])
                        V = gbest + F * (X1 + X2 - X3 - X4)
        return V

    def _de(self, F=0.5, CR=0.1, strategy='best2', xstart=None, sync=True):
        """
        Minimize an objective function using Differential Evolution (DE).
        
        Parameters
        ----------
        F : scalar, optional, default 0.5
            Differential weight.
        CR : scalar, optional, default 0.1
            Crossover probability.
        strategy : {'rand1', 'rand2', 'best1', 'best2'}, optional, default 'best2'
            Mutation strategy.
            - 'rand1', mutate a random vector by adding one scaled difference vector.
            - 'rand2', mutate a random vector by adding two scaled difference vectors.
            - 'best1', mutate the best vector by adding one scaled difference vector.
            - 'best2', mutate the best vector by adding two scaled difference vectors.
        xstart : None or ndarray, optional, default None
            Initial positions of the population.
        sync : bool, optional, default True
            Synchronize population, the best individual is updated after each
            iteration which allows the parallelization.
            
        Returns
        -------
        xopt : ndarray
            Optimal solution found by the optimizer.
        gfit : scalar
            Objective function value of the optimal solution.
        
        References
        ----------
        .. [1] R. Storn and K. Price, *Differential Evolution - A Simple and
               Efficient Heuristic for global Optimization over Continuous
               Spaces*, Journal of Global Optimization, 1997, 11(4): 341-359
        """
        self._check_inputs(F, CR, strategy, xstart)
        if self._mpi:
            starttime_serial = MPI.Wtime()
        else:
            if xstart is None:
                X = np.random.uniform(-1.0, 1.0, (self._popsize, self._n_dim))
            else:
                X = self._standardize(xstart)
        pfit = self._eval_models(X, 1)
        pbestfit = np.array(pfit)
        self._n_eval = self._popsize
        if self._snap:
            self._init_models()
            self._models[:, :, 0] = self._unstandardize(X)
            self._energy[:, 0] = np.array(pbestfit)
        gbidx = np.argmin(pbestfit)
        gfit = pbestfit[gbidx]
        gbest = np.array(X[gbidx, :])
        if self._mpi:
            self._time_serial[0] = MPI.Wtime() - starttime_serial
        it = 1
        converge = False
        while not converge:
            if self._mpi:
                starttime_serial = MPI.Wtime()
            it += 1
            r1 = np.random.rand(self._popsize, self._n_dim)
            if sync:
                V = self._de_mutation(X, F, gbest, strategy, sync)
                mask = np.zeros_like(r1, dtype=bool)
                irand = np.random.randint((self._n_dim), size=(self._popsize))
                for i in range(self._popsize):
                    mask[(i, irand[i])] = True

                mask = np.logical_or(mask, r1 <= CR)
                U = np.where(mask, V, X)
                if self._constrain:
                    U = self._constrain_de(U)
                pfit = self._eval_models(U, it)
                idx = pfit < pbestfit
                pbestfit[idx] = pfit[idx]
                X[idx] = U[idx]
                gbidx = np.argmin(pbestfit)
                if np.linalg.norm(gbest - X[gbidx]) <= self._eps1:
                    if pbestfit[gbidx] <= self._eps2:
                        converge = True
                        xopt = self._unstandardize(X[gbidx])
                        gfit = pbestfit[gbidx]
                        self._flag = 0
                if pbestfit[gbidx] <= self._eps2:
                    converge = True
                    xopt = self._unstandardize(X[gbidx])
                    gfit = pbestfit[gbidx]
                    self._flag = 1
                else:
                    if it >= self._max_iter:
                        converge = True
                        xopt = self._unstandardize(X[gbidx])
                        gfit = pbestfit[gbidx]
                        self._flag = -1
                    else:
                        gbest = np.array(X[gbidx])
                        gfit = pbestfit[gbidx]
            else:
                for i in range(self._popsize):
                    V = self._de_mutation(X, F, gbest, strategy, sync, i)
                    mask = np.zeros((self._n_dim), dtype=bool)
                    irand = np.random.randint(self._n_dim)
                    mask[irand] = True
                    mask = np.logical_or(mask, r1[i] <= CR)
                    U = np.where(mask, V, X[i])
                    if self._constrain:
                        U = self._constrain_de(U)
                    pfit[i] = self._func(self._unstandardize(U))
                    self._n_eval += 1
                    if pfit[i] <= pbestfit[i]:
                        X[i] = np.array(U)
                        pbestfit[i] = pfit[i]
                        if pfit[i] <= gfit:
                            if np.linalg.norm(gbest - X[i]) <= self._eps1 and pfit[i] <= self._eps2:
                                converge = True
                                xopt = self._unstandardize(X[i])
                                gfit = pbestfit[i]
                                self._flag = 0
                        if pfit[i] <= self._eps2:
                            converge = True
                            xopt = self._unstandardize(X[i])
                            gfit = pbestfit[i]
                            self._flag = 1
                        else:
                            gbest = np.array(X[i])
                            gfit = pfit[i]

                if not converge:
                    if it >= self._max_iter:
                        converge = True
                        xopt = self._unstandardize(gbest)
                        self._flag = -1
                if self._snap:
                    self._models[:, :, it - 1] = self._unstandardize(X)
                    self._energy[:, it - 1] = np.array(pbestfit)
                if self._mpi:
                    self._time_serial[it - 1] = MPI.Wtime() - starttime_serial

        self._xopt = xopt
        self._gfit = gfit
        self._n_iter = it
        if self._mpi:
            self._time_serial = self._time_serial[:it] - self._time_parallel[:it]
            self._time_parallel = self._time_parallel[:it]
        if self._snap:
            self._models = self._models[:, :, :it]
            self._energy = self._energy[:, :it]
        return (
         xopt, gfit)

    def _cpso(self, w=0.7298, c1=1.49618, c2=1.49618, gamma=1.0, xstart=None, sync=True):
        """
        Minimize an objective function using Competitive Particle Swarm
        Optimization (CPSO). Set gamma = 0. for classical PSO.
        
        Parameters
        ----------
        w : scalar, optional, default 0.7298
            Inertial weight.
        c1 : scalar, optional, default 1.49618
            Cognition parameter.
        c2 : scalar, optional, default 1.49618
            Sociability parameter.
        gamma : scalar, optional, default 1.
            Competitivity parameter.
        xstart : None or ndarray, optional, default None
            Initial positions of the population.
        sync : bool, optional, default True
            Synchronize population, the best individual is updated after each
            iteration which allows the parallelization.
            
        Returns
        -------
        xopt : ndarray
            Optimal solution found by the optimizer.
        gfit : scalar
            Objective function value of the optimal solution.
        
        References
        ----------
        .. [1] J. Kennedy and R. Eberhart, *Particle swarm optimization*,
               Proceedings of ICNN'95 - International Conference on Neural
               Networks, 1995, 4: 1942-1948
        .. [2] F. Van Den Bergh, *An analysis of particle swarm optimizers*,
               University of Pretoria, 2001
        .. [3] K. Luu, M. Noble, A. Gesret, N. Belayouni and P.-F. Roux,
               *A parallel competitive Particle Swarm Optimization for
               non-linear first arrival traveltime tomography and uncertainty
               quantification*, Computers & Geosciences, 2018, 113: 81-93
        """
        self._check_inputs(w, c1, c2, gamma, xstart)
        if self._mpi:
            starttime_serial = MPI.Wtime()
        else:
            if xstart is None:
                X = np.random.uniform(-1.0, 1.0, (self._popsize, self._n_dim))
            else:
                X = self._standardize(xstart)
        pbest = np.array(X)
        V = np.zeros((self._popsize, self._n_dim))
        pfit = self._eval_models(X, 1)
        pbestfit = np.array(pfit)
        self._n_eval = self._popsize
        if self._snap:
            self._init_models()
            self._models[:, :, 0] = self._unstandardize(X)
            self._energy[:, 0] = np.array(pbestfit)
        gbidx = np.argmin(pbestfit)
        gfit = pbestfit[gbidx]
        gbest = np.array(X[gbidx])
        delta = np.log(1.0 + 0.003 * self._popsize) / np.max((0.2, np.log(0.01 * self._max_iter)))
        if self._mpi:
            self._time_serial[0] = MPI.Wtime() - starttime_serial
        it = 1
        converge = False
        while not converge:
            if self._mpi:
                starttime_serial = MPI.Wtime()
            it += 1
            r1 = np.random.rand(self._popsize, self._n_dim)
            r2 = np.random.rand(self._popsize, self._n_dim)
            if sync:
                V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest - X)
                if self._constrain:
                    X = np.array([self._constrain_cpso(X[i, :] + V[i, :], X[i, :]) for i in range(self._popsize)])
                else:
                    X += V
                pfit = self._eval_models(X, it)
                idx = pfit < pbestfit
                pbestfit[idx] = np.array(pfit[idx])
                pbest[idx] = np.array(X[idx])
                gbidx = np.argmin(pbestfit)
                if np.linalg.norm(gbest - pbest[gbidx]) <= self._eps1:
                    if pbestfit[gbidx] <= self._eps2:
                        converge = True
                        xopt = self._unstandardize(pbest[gbidx])
                        gfit = pbestfit[gbidx]
                        self._flag = 0
                if pbestfit[gbidx] <= self._eps2:
                    converge = True
                    xopt = self._unstandardize(pbest[gbidx])
                    gfit = pbestfit[gbidx]
                    self._flag = 1
                else:
                    if it >= self._max_iter:
                        converge = True
                        xopt = self._unstandardize(pbest[gbidx])
                        gfit = pbestfit[gbidx]
                        self._flag = -1
                    else:
                        gbest = np.array(pbest[gbidx])
                        gfit = pbestfit[gbidx]
            else:
                for i in range(self._popsize):
                    V[i] = w * V[i] + c1 * r1[i] * (pbest[i] - X[i]) + c2 * r2[i] * (gbest - X[i])
                    if self._constrain:
                        X[i] = self._constrain_cpso(X[i] + V[i], X[i])
                    else:
                        X[i] += V[i]
                    pfit[i] = self._func(self._unstandardize(X[i]))
                    self._n_eval += 1
                    if pfit[i] <= pbestfit[i]:
                        pbest[i] = np.array(X[i])
                        pbestfit[i] = pfit[i]
                        if pfit[i] <= gfit:
                            if np.linalg.norm(gbest - X[i]) <= self._eps1 and pfit[i] <= self._eps2:
                                converge = True
                                xopt = self._unstandardize(X[i])
                                gfit = pbestfit[i]
                                self._flag = 0
                        if pfit[i] <= self._eps2:
                            converge = True
                            xopt = self._unstandardize(X[i])
                            gfit = pbestfit[i]
                            self._flag = 1
                        else:
                            gbest = np.array(X[i])
                            gfit = pfit[i]

                if not converge:
                    if it >= self._max_iter:
                        converge = True
                        xopt = self._unstandardize(gbest)
                        self._flag = -1
                if self._snap:
                    self._models[:, :, it - 1] = self._unstandardize(X)
                    self._energy[:, it - 1] = np.array(pfit)
                if not converge:
                    if gamma > 0.0:
                        swarm_radius = np.max([np.linalg.norm(X[i] - gbest) for i in range(self._popsize)])
                        swarm_radius /= np.sqrt(4.0 * self._n_dim)
                        if swarm_radius < delta:
                            inorm = it / self._max_iter
                            nw = int((self._popsize - 1.0) / (1.0 + np.exp(11.11111111111111 * (inorm - gamma + 0.5))))
                            if nw > 0:
                                self._n_restart += 1
                                idx = pbestfit.argsort()[:-nw - 1:-1]
                                V[idx] = np.zeros((nw, self._n_dim))
                                X[idx] = np.random.uniform(-1.0, 1.0, (nw, self._n_dim))
                                pbest[idx] = np.array(X[idx])
                                pbestfit[idx] = np.full(nw, 1e+30)
                if self._mpi:
                    self._time_serial[it - 1] = MPI.Wtime() - starttime_serial

        self._xopt = np.array(xopt)
        self._gfit = gfit
        self._n_iter = it
        if self._mpi:
            self._time_serial = self._time_serial[:it] - self._time_parallel[:it]
            self._time_parallel = self._time_parallel[:it]
        if self._snap:
            self._models = self._models[:, :, :it]
            self._energy = self._energy[:, :it]
        return (
         xopt, gfit)

    def _cmaes(self, sigma=0.5, mu_perc=0.5, xstart=None):
        """
        Minimize an objective function using Covariance Matrix Adaptation
        - Evolution Strategy (CMA-ES).
        
        Parameters
        ----------
        sigma : scalar, optional, default 0.5
            Step size.
        mu_perc : scalar, optional, default 0.5
            Number of parents as a percentage of population size.
        xstart : None or ndarray, optional, default None
            Initial position of the mean.
            
        Returns
        -------
        xopt : ndarray
            Optimal solution found by the optimizer.
        gfit : scalar
            Objective function value of the optimal solution.
        
        References
        ----------
        .. [1] N. Hansen, *The CMA evolution strategy: A tutorial*, Inria,
               Université Paris-Saclay, LRI, 2011, 102: 1-34
        """
        self._check_inputs(sigma, mu_perc, xstart)
        if self._snap:
            self._init_models()
            self._means = np.zeros((self._max_iter, self._n_dim))
        else:
            if xstart is None:
                xmean = np.random.uniform(-1.0, 1.0, self._n_dim)
            else:
                if np.asarray(xstart).ndim == 1:
                    xmean = self._standardize(xstart)
                else:
                    arfitness = self._eval_models(self._standardize(xstart), 1)
                    xmean = self._standardize(xstart[np.argmin(arfitness)])
        xold = np.empty_like(xmean)
        mu = int(mu_perc * self._popsize)
        weights = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
        weights /= np.sum(weights)
        mueff = np.sum(weights) ** 2 / np.sum(weights ** 2)
        cc = (4.0 + mueff / self._n_dim) / (self._n_dim + 4.0 + 2.0 * mueff / self._n_dim)
        cs = (mueff + 2.0) / (self._n_dim + mueff + 5.0)
        c1 = 2.0 / ((self._n_dim + 1.3) ** 2 + mueff)
        cmu = min(1.0 - c1, 2.0 * (mueff - 2.0 + 1.0 / mueff) / ((self._n_dim + 2.0) ** 2 + mueff))
        damps = 1.0 + 2.0 * max(0.0, np.sqrt((mueff - 1.0) / (self._n_dim + 1.0)) - 1.0) + cs
        pc = np.zeros(self._n_dim)
        ps = np.zeros(self._n_dim)
        B = np.eye(self._n_dim)
        D = np.ones(self._n_dim)
        C = np.eye(self._n_dim)
        invsqrtC = np.eye(self._n_dim)
        chind = np.sqrt(self._n_dim) * (1.0 - 1.0 / (4.0 * self._n_dim) + 1.0 / (21.0 * self._n_dim ** 2))
        bnd_weights = np.zeros(self._n_dim)
        dfithist = np.array([1.0])
        self._n_eval = 0
        it = 0
        eigeneval = 0
        arbestfitness = np.zeros(self._max_iter)
        ilim = int(10 + 30 * self._n_dim / self._popsize)
        insigma = sigma
        validfitval = False
        iniphase = True
        converge = False
        while not converge:
            if self._mpi:
                starttime_serial = MPI.Wtime()
            else:
                it += 1
                arx = np.array([xmean + sigma * np.dot(B, D * np.random.randn(self._n_dim)) for i in range(self._popsize)])
                arxvalid = np.array(arx)
                if self._constrain:
                    arfitness, arxvalid, bnd_weights, dfithist, validfitval, iniphase = self._constrain_cma(arxvalid, arx, xmean, xold, sigma, np.diag(C), mueff, it, bnd_weights, dfithist, validfitval, iniphase)
                else:
                    arfitness = self._eval_models(arxvalid, it)
                if self._snap:
                    self._models[:, :, it - 1] = self._unstandardize(arxvalid)
                    self._energy[:, it - 1] = np.array(arfitness)
                    self._means[it - 1, :] = self._unstandardize(xmean)
                arindex = np.argsort(arfitness)
                xold = np.array(xmean)
                xmean = np.dot(weights, arx[arindex[:mu], :])
                arbestfitness[it - 1] = arfitness[arindex[0]]
                ps = (1.0 - cs) * ps + np.sqrt(cs * (2.0 - cs) * mueff) * np.dot(invsqrtC, xmean - xold) / sigma
                if np.linalg.norm(ps) / np.sqrt(1.0 - (1.0 - cs) ** (2.0 * self._n_eval / self._popsize)) / chind < 1.4 + 2.0 / (self._n_dim + 1.0):
                    hsig = 1.0
                    pc = (1.0 - cc) * pc + np.sqrt(cc * (2.0 - cc) * mueff) * (xmean - xold) / sigma
                else:
                    hsig = 0.0
                    pc = (1.0 - cc) * pc
                artmp = (arx[arindex[:mu], :] - np.tile(xold, (mu, 1))) / sigma
                if hsig:
                    C = (1.0 - c1 - cmu) * C + c1 * np.outer(pc, pc) + cmu * np.dot(np.dot(artmp.transpose(), np.diag(weights)), artmp)
                else:
                    C = (1.0 - c1 - cmu) * C + c1 * (np.outer(pc, pc) + cc * (2.0 - cc) * C) + cmu * np.dot(np.dot(artmp.transpose(), np.diag(weights)), artmp)
                sigma *= np.exp(cs / damps * (np.linalg.norm(ps) / chind - 1.0))
                if self._n_eval - eigeneval > self._popsize / (c1 + cmu) / self._n_dim / 10.0:
                    eigeneval = self._n_eval
                    C = np.triu(C) + np.triu(C, 1).transpose()
                    D, B = np.linalg.eigh(C)
                    idx = np.argsort(D)
                    D = D[idx]
                    B = B[:, idx]
                    D = np.sqrt(D)
                    invsqrtC = np.dot(np.dot(B, np.diag(1.0 / D)), B.transpose())
                if it >= self._max_iter:
                    converge = True
                    self._flag = -1
                if not converge:
                    if np.linalg.norm(xold - xmean) <= self._eps1:
                        if arfitness[arindex[0]] < self._eps2:
                            converge = True
                            self._flag = 0
                if not converge:
                    if arfitness[arindex[0]] <= self._eps2:
                        converge = True
                        self._flag = 1
                i = int(np.floor(np.mod(it, self._n_dim)))
                if not converge:
                    if np.all(np.abs(0.1 * sigma * B[:, i] * D[i]) < 1e-10):
                        converge = True
                        self._flag = 2
                if not converge:
                    if np.any(0.2 * sigma * np.sqrt(np.diag(C)) < 1e-10):
                        converge = True
                        self._flag = 3
                if not converge:
                    if np.max(D) > 10000000.0 * np.min(D):
                        converge = True
                        self._flag = 4
                if not converge:
                    if it >= ilim:
                        if np.max(arbestfitness[it - ilim:it + 1]) - np.min(arbestfitness[it - ilim:it + 1]) < 1e-10:
                            converge = True
                            self._flag = 5
                if not converge:
                    if np.any(sigma * np.sqrt(np.diag(C)) > 1000.0 * insigma):
                        converge = True
                        self._flag = 6
                if not converge:
                    if it > 2:
                        if np.max(np.append(arfitness, arbestfitness)) - np.min(np.append(arfitness, arbestfitness)) < 1e-12:
                            converge = True
                            self._flag = 7
                if not converge:
                    if np.all(sigma * np.max(np.append(np.abs(pc), np.sqrt(np.diag(C)))) < 1e-11 * insigma):
                        converge = True
                        self._flag = 8
            if self._mpi:
                self._time_serial[it - 1] = MPI.Wtime() - starttime_serial

        xopt = self._unstandardize(arxvalid[arindex[0]])
        gfit = arfitness[arindex[0]]
        self._xopt = np.array(xopt)
        self._gfit = gfit
        self._n_iter = it
        if self._mpi:
            self._time_serial = self._time_serial[:it] - self._time_parallel[:it]
            self._time_parallel = self._time_parallel[:it]
        if self._snap:
            self._models = self._models[:, :, :it]
            self._energy = self._energy[:, :it]
            self._means = self._means[:it, :]
        return (
         xopt, gfit)

    def _vdcma(self, sigma=0.5, mu_perc=0.5, xstart=None):
        """
        Minimize an objective function using VD-CMA.
        
        Parameters
        ----------
        sigma : scalar, optional, default 0.5
            Step size.
        mu_perc : scalar, optional, default 0.5
            Number of parents as a percentage of population size.
        xstart : None or ndarray, optional, default None
            Initial position of the mean.
            
        Returns
        -------
        xopt : ndarray
            Optimal solution found by the optimizer.
        gfit : scalar
            Objective function value of the optimal solution.
        
        References
        ----------
        .. [1] Y. Akimoto, A. Auger and N. Hansen, *Comparison-Based Natural
               Gradient Optimization in High Dimension*, Proceedings of the
               2014 conference on Genetic and evolutionary computation, 2014,
               373-380
        """
        self._check_inputs(sigma, mu_perc, xstart)
        if self._snap:
            self._init_models()
            self._means = np.zeros((self._max_iter, self._n_dim))
        else:
            if xstart is None:
                xmean = np.random.uniform(-1.0, 1.0, self._n_dim)
            else:
                if np.asarray(xstart).ndim == 1:
                    xmean = self._standardize(xstart)
                else:
                    arfitness = self._eval_models(self._standardize(xstart), 1)
                    xmean = self._standardize(xstart[np.argmin(arfitness)])
        xold = np.empty_like(xmean)
        mu = int(mu_perc * self._popsize)
        weights = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
        weights /= np.sum(weights)
        mueff = np.sum(weights) ** 2 / np.sum(weights ** 2)
        cc = (4.0 + mueff / self._n_dim) / (self._n_dim + 4.0 + 2.0 * mueff / self._n_dim)
        cfactor = (self._n_dim - 5.0) / 6.0
        c1 = cfactor * 2.0 / ((self._n_dim + 1.3) ** 2 + mueff)
        cmu = min(1.0 - c1, cfactor * 2.0 * (mueff - 2.0 + 1.0 / mueff) / ((self._n_dim + 2.0) ** 2 + mueff))
        flg_injection = False
        cs = 0.3
        ds = np.sqrt(self._n_dim)
        dx = np.zeros(self._n_dim)
        ps = 0.0
        dvec = np.ones(self._n_dim)
        vvec = np.random.normal(0.0, 1.0, self._n_dim) / np.sqrt(self._n_dim)
        norm_v2 = np.dot(vvec, vvec)
        norm_v = np.sqrt(norm_v2)
        vn = vvec / norm_v
        vnn = vn ** 2
        pc = np.zeros(self._n_dim)
        bnd_weights = np.zeros(self._n_dim)
        dfithist = np.array([1.0])
        self._n_eval = 0
        it = 0
        arbestfitness = np.zeros(self._max_iter)
        ilim = int(10 + 30 * self._n_dim / self._popsize)
        insigma = sigma
        validfitval = False
        iniphase = True
        converge = False
        while not converge:
            if self._mpi:
                starttime_serial = MPI.Wtime()
            else:
                it += 1
                arz = np.random.randn(self._popsize, self._n_dim)
                ary = dvec * (arz + (np.sqrt(1.0 + norm_v2) - 1.0) * np.outer(np.dot(arz, vn), vn))
                if flg_injection:
                    ddx = dx / dvec
                    mnorm = (ddx ** 2).sum() - np.dot(ddx, vvec) ** 2 / (1.0 + norm_v2)
                    dy = np.linalg.norm(np.random.randn(self._n_dim)) / np.sqrt(mnorm) * dx
                    ary[0] = dy
                    ary[1] = -dy
                arx = xmean + sigma * ary
                arxvalid = np.array(arx)
                diagC = np.diag(np.dot(np.dot(np.diag(dvec), np.eye(self._n_dim) + np.outer(vvec, vvec)), np.diag(dvec)))
                if self._constrain:
                    arfitness, arxvalid, bnd_weights, dfithist, validfitval, iniphase = self._constrain_cma(arxvalid, arx, xmean, xold, sigma, diagC, mueff, it, bnd_weights, dfithist, validfitval, iniphase)
                else:
                    arfitness = self._eval_models(arxvalid, it)
                if self._snap:
                    self._models[:, :, it - 1] = self._unstandardize(arxvalid)
                    self._energy[:, it - 1] = np.array(arfitness)
                    self._means[it - 1, :] = self._unstandardize(xmean)
                arindex = np.argsort(arfitness)
                dx = np.dot(weights, arx[arindex[:mu]]) - np.sum(weights) * xmean
                xold = np.array(xmean)
                xmean += dx
                arbestfitness[it - 1] = arfitness[arindex[0]]
                if flg_injection:
                    alpha_act = np.where(arindex == 1)[0][0] - np.where(arindex == 0)[0][0]
                    alpha_act /= self._popsize - 1.0
                    ps += cs * (alpha_act - ps)
                    sigma *= np.exp(ps / ds)
                    hsig = ps < 0.5
                else:
                    flg_injection = True
                    hsig = True
                pc = (1.0 - cc) * pc + hsig * np.sqrt(cc * (2.0 - cc) * mueff) * np.dot(weights, ary[arindex[:mu]])
                gamma = 1.0 / np.sqrt(1.0 + norm_v2)
                alpha = np.sqrt(norm_v2 ** 2 + (1.0 + norm_v2) / max(vnn) * (2.0 - gamma)) / (2.0 + norm_v2)
                if alpha < 1.0:
                    beta = (4.0 - (2.0 - gamma) / max(vnn)) / (1.0 + 2.0 / norm_v2) ** 2
                else:
                    alpha = 1.0
                    beta = 0.0
                bsca = 2.0 * alpha ** 2 - beta
                avec = 2.0 - (bsca + 2.0 * alpha ** 2) * vnn
                invavnn = vnn / avec
                if cmu == 0.0:
                    pvec_mu = np.zeros(self._n_dim)
                    qvec_mu = np.zeros(self._n_dim)
                else:
                    pvec_mu, qvec_mu = self._pvec_and_qvec(vn, norm_v2, ary[arindex[:mu]] / dvec, weights)
                if c1 == 0.0:
                    pvec_one = np.zeros(self._n_dim)
                    qvec_one = np.zeros(self._n_dim)
                else:
                    pvec_one, qvec_one = self._pvec_and_qvec(vn, norm_v2, pc / dvec)
                pvec = cmu * pvec_mu + hsig * c1 * pvec_one
                qvec = cmu * qvec_mu + hsig * c1 * qvec_one
                if cmu + c1 > 0.0:
                    ngv, ngd = self._ngv_ngd(dvec, vn, vnn, norm_v, norm_v2, alpha, avec, bsca, invavnn, pvec, qvec)
                    upfactor = 1.0
                    upfactor = min(upfactor, 0.7 * norm_v / np.sqrt(np.dot(ngv, ngv)))
                    upfactor = min(upfactor, 0.7 * (dvec / np.abs(ngd)).min())
                else:
                    ngv = np.zeros(self._n_dim)
                    ngd = np.zeros(self._n_dim)
                    upfactor = 1.0
                vvec += upfactor * ngv
                dvec += upfactor * ngd
                norm_v2 = np.dot(vvec, vvec)
                norm_v = np.sqrt(norm_v2)
                vn = vvec / norm_v
                vnn = vn ** 2
                if it >= self._max_iter:
                    converge = True
                    self._flag = -1
                if not converge:
                    if np.linalg.norm(xold - xmean) <= self._eps1:
                        if arfitness[arindex[0]] < self._eps2:
                            converge = True
                            self._flag = 0
                if not converge:
                    if arfitness[arindex[0]] <= self._eps2:
                        converge = True
                        self._flag = 1
                if not converge:
                    if np.any(0.2 * sigma * np.sqrt(diagC) < 1e-10):
                        converge = True
                        self._flag = 3
                if not converge:
                    if it >= ilim:
                        if np.max(arbestfitness[it - ilim:it + 1]) - np.min(arbestfitness[it - ilim:it + 1]) < 1e-10:
                            converge = True
                            self._flag = 5
                if not converge:
                    if np.any(sigma * np.sqrt(diagC) > 1000.0 * insigma):
                        converge = True
                        self._flag = 6
                if not converge:
                    if it > 2:
                        if np.max(np.append(arfitness, arbestfitness)) - np.min(np.append(arfitness, arbestfitness)) < 1e-12:
                            converge = True
                            self._flag = 7
                if not converge:
                    if np.all(sigma * np.max(np.append(np.abs(pc), np.sqrt(diagC))) < 1e-11 * insigma):
                        converge = True
                        self._flag = 8
            if self._mpi:
                self._time_serial[it - 1] = MPI.Wtime() - starttime_serial

        arindex = np.argsort(arfitness)
        xopt = self._unstandardize(arxvalid[arindex[0]])
        gfit = arfitness[arindex[0]]
        self._xopt = np.array(xopt)
        self._gfit = gfit
        self._n_iter = it
        if self._mpi:
            self._time_serial = self._time_serial[:it] - self._time_parallel[:it]
            self._time_parallel = self._time_parallel[:it]
        if self._snap:
            self._models = self._models[:, :, :it]
            self._energy = self._energy[:, :it]
            self._means = self._means[:it, :]
        return (
         xopt, gfit)

    @staticmethod
    def _pvec_and_qvec(vn, norm_v2, y, weights=None):
        y_vn = np.dot(y, vn)
        if weights is None:
            pvec = y ** 2 - norm_v2 / (1.0 + norm_v2) * (y_vn * (y * vn)) - 1.0
            qvec = y_vn * y - 0.5 * (y_vn ** 2 + 1.0 + norm_v2) * vn
        else:
            pvec = np.dot(weights, y ** 2 - norm_v2 / (1.0 + norm_v2) * (y_vn * (y * vn).T).T - 1.0)
            qvec = np.dot(weights, (y_vn * y.T).T - np.outer(0.5 * (y_vn ** 2 + 1.0 + norm_v2), vn))
        return (
         pvec, qvec)

    @staticmethod
    def _ngv_ngd(dvec, vn, vnn, norm_v, norm_v2, alpha, avec, bsca, invavnn, pvec, qvec):
        rvec = pvec - alpha / (1.0 + norm_v2) * ((2.0 + norm_v2) * (qvec * vn) - norm_v2 * np.dot(vn, qvec) * vnn)
        svec = rvec / avec - bsca * np.dot(rvec, invavnn) / (1.0 + bsca * np.dot(vnn, invavnn)) * invavnn
        ngv = qvec / norm_v - alpha / norm_v * ((2.0 + norm_v2) * (vn * svec) - np.dot(svec, vnn) * vn)
        ngd = dvec * svec
        return (ngv, ngd)

    def _check_inputs(self, *args):
        if self._solver == 'de':
            F, CR, strategy, xstart = args
            if self._popsize <= 3:
                if strategy not in ('rand2', 'best2'):
                    self._popsize = 4
                    warn('\npopsize cannot be lower than 4 for DE, popsize set to 4', UserWarning)
            if self._popsize <= 4:
                if strategy == 'best2':
                    self._popsize = 5
                    warn('\npopsize cannot be lower than 5 for DE, popsize set to 5', UserWarning)
            if self._popsize <= 5:
                if strategy == 'rand2':
                    self._popsize = 6
                    warn('\npopsize cannot be lower than 6 for DE, popsize set to 6', UserWarning)
            if not isinstance(F, float) and not isinstance(F, int) or not 0.0 <= F <= 2.0:
                raise ValueError('F must be an integer or float in [ 0, 2 ], got %s' % F)
            if not isinstance(CR, float) and not isinstance(CR, int) or not 0.0 <= CR <= 1.0:
                raise ValueError('CR must be an integer or float in [ 0, 1 ], got %s' % CR)
            if strategy not in ('rand1', 'rand2', 'best1', 'best2'):
                raise ValueError("strategy should either be 'rand1', 'rand2', 'best1' or 'best2'")
            if xstart is not None:
                if isinstance(xstart, np.ndarray):
                    if xstart.shape != (self._popsize, self._n_dim):
                        raise ValueError('xstart must be a ndarray of shape [ %d, %d ], got [ %d, %d ]' % (
                         self._popsize, self._n_dim, xstart.shape[0], xstart.shape[1]))
        else:
            if self._solver in ('pso', 'cpso'):
                w, c1, c2, gamma, xstart = args
                if not isinstance(w, float) and not isinstance(w, int) or not 0.0 <= w <= 1.0:
                    raise ValueError('w must be an integer or float in [ 0, 1 ], got %s' % w)
                if not isinstance(c1, float) and not isinstance(c1, int) or not 0.0 <= c1 <= 4.0:
                    raise ValueError('c1 must be an integer or float in [ 0, 4 ], got %s' % c1)
                if not isinstance(c2, float) and not isinstance(c2, int) or not 0.0 <= c2 <= 4.0:
                    raise ValueError('c2 must be an integer or float in [ 0, 4 ], got %s' % c2)
                if not isinstance(gamma, float) and not isinstance(gamma, int) or not 0.0 <= gamma <= 2.0:
                    raise ValueError('gamma must be an integer or float in [ 0, 2 ], got %s' % gamma)
                if xstart is not None:
                    if isinstance(xstart, np.ndarray):
                        if xstart.shape != (self._popsize, self._n_dim):
                            raise ValueError('xstart must be a ndarray of shape [ %d, %d ], got [ %d, %d ]' % (
                             self._popsize, self._n_dim, xstart.shape[0], xstart.shape[1]))
            elif self._solver in ('cmaes', 'vdcma'):
                sigma, mu_perc, xstart = args
                if self._popsize <= 3:
                    self._popsize = 4
                    warn('\npopsize cannot be lower than 4 for %s, popsize set to 4' % self._solver.upper(), UserWarning)
                if not isinstance(sigma, float) and not isinstance(sigma, int) or sigma <= 0.0:
                    raise ValueError('sigma must be positive, got %s' % sigma)
                if not isinstance(mu_perc, float) and not isinstance(mu_perc, int) or not 0.0 < mu_perc <= 1.0:
                    raise ValueError('mu_perc must be an integer or float in ] 0, 1 ], got %s' % mu_perc)
                if xstart is not None:
                    if isinstance(xstart, (list, np.ndarray)):
                        if np.asarray(xstart).ndim not in (1, 2):
                            raise ValueError('xstart must be a 1-D or 2-D ndarray')
                if np.asarray(xstart).ndim == 1 and len(xstart) != self._n_dim:
                    raise ValueError('xstart must be a list or ndarray of length %d, got %d' % (self._n_dim, len(xstart)))
                elif np.asarray(xstart).ndim == 2:
                    if xstart.shape != (self._popsize, self._n_dim):
                        raise ValueError('xstart must be a ndarray of shape [ %d, %d ], got [ %d, %d ]' % (
                         self._popsize, self._n_dim, xstart.shape[0], xstart.shape[1]))

    @property
    def xopt(self):
        """
        ndarray of shape (n_dim)
        Optimal solution found by the optimizer.
        """
        return self._xopt

    @property
    def gfit(self):
        """
        scalar
        Objective function value of the optimal solution.
        """
        return self._gfit

    @property
    def flag(self):
        """
        int
        Stopping criterion.
        """
        if self._flag == -1:
            return 'maximum number of iterations is reached'
        else:
            if self._flag == 0:
                return 'best individual position changes less than eps1 (%g)' % self._eps1
            else:
                if self._flag == 1:
                    return 'fitness is lower than threshold eps2 (%g)' % self._eps2
                else:
                    if self._flag == 2:
                        return 'NoEffectAxis'
                    else:
                        if self._flag == 3:
                            return 'NoEffectCoord'
                        if self._flag == 4:
                            return 'ConditionCov'
                        if self._flag == 5:
                            return 'EqualFunValues'
                    if self._flag == 6:
                        return 'TolXUp'
                if self._flag == 7:
                    return 'TolFun'
            if self._flag == 8:
                return 'TolX'

    @property
    def n_iter(self):
        """
        int
        Number of iterations required to reach stopping criterion.
        """
        return self._n_iter

    @property
    def n_eval(self):
        """
        int
        Number of function evaluations performed.
        """
        return self._n_eval

    @property
    def models(self):
        """
        ndarray of shape (popsize, n_dim, n_iter)
        Models explored by every individuals at each iteration. Available only
        when snap = True.
        """
        return self._models

    @property
    def energy(self):
        """
        ndarray of shape (popsize, n_iter)
        Energy of models explored by every individuals at each iteration.
        Available only when snap = True.
        """
        return self._energy

    @property
    def means(self):
        """
        ndarray of shape (n_iter, n_dim)
        Mean models at every iterations. Available only when
        solver = {'cmaes', 'vdcma'} and snap = True.
        """
        return self._means

    @property
    def time_serial(self):
        """
        ndarray of length n_iter
        Sequential computation time in seconds at each iteration.
        """
        return self._time_serial

    @property
    def time_parallel(self):
        """
        ndarray of length n_iter
        Parallel computation time in seconds at each iteration.
        """
        return self._time_parallel