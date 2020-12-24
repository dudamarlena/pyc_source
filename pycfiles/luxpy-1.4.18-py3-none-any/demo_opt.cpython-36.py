# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\utils\math\DEMO\demo_opt.py
# Compiled at: 2019-01-31 20:33:19
# Size of source mod 2**32: 24335 bytes
"""
Module for demo_opt
==================================================================

 :demo_opt(): | Multi-objective optimization using the DEMO.
              | This function uses the Differential Evolution for Multi-objective 
              | Optimization (a.k.a. DEMO) to solve a multi-objective problem. The 
              | result is a set of nondominated points that are (hopefully) very close
              | to the true Pareto front.

 :fobjeval(): | Evaluates the objective function.

 :mutation(): | Performs mutation in the individuals.
 
 :recombination(): | Performs recombination in the individuals.
 
 :repair(): | Truncates the population to be in the feasible region.
 
 :selection(): | Selects the next population.
 
 :init_options(): | Initialize options dict.
 
 :ndset(): | Finds the nondominated set of a set of objective points.
 
 :crowdingdistance(): Computes the crowding distance of a nondominated front.

 :dtlz2():  | DTLZ2 problem: This function represents a hyper-sphere.
            | Using k = 10, the number of dimensions must be n = (M - 1) + k.
            | The Pareto optimal solutions are obtained when the last k variables of x
            | are equal to 0.5.
            
 :dtlz_range(): | Returns the decision range of a DTLZ function
                 | The range is simply [0,1] for all variables. What varies is the number 
                 | of decision variables in each problem. The equation for that is
                 | n = (M-1) + k
                 | wherein k = 5 for DTLZ1, 10 for DTLZ2-6, and 20 for DTLZ7.

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, plt, Axes3D, put_args_in_db, getdata
if __name__ == '__main__':
    np.set_printoptions(formatter={'float': lambda x: '{0:0.4f}'.format(x)})
__all__ = ['demo_opt', 'fobjeval', 'mutation', 'recombination', 'repair', 'selection', 'init_options', 'ndset', 'crowdingdistance', 'dtlz2', 'dtlz_range']

def demo_opt(f, args=(), xrange=None, options={}):
    """
    DEMO_OPT: Multi-objective optimization using the DEMO
    This function uses the Differential Evolution for Multi-objective 
    Optimization (a.k.a. DEMO) to solve a multi-objective problem. The 
    result is a set of nondominated points that are (hopefully) very close
    to the true Pareto front.

    Args:
      :f: 
          | handle to objective function.
          | The output must be, for each point, a column vector of size m x 1, 
          | with m > 1 the number of objectives.
      :args: (), optional
          | Input arguments required for f.
      :xrange: None, optional
          | ndarray with lower and upperbounds.
          | If n is the dimension, it will be a n x 2 matrix, such that the 
          | first column contains the lower bounds, 
          | and the second, the upper bounds.
          | None defaults to no bounds ( [-Inf, Inf] ndarray).
      :options: 
          | None, optional
          | dict with internal parameters of the algorithm.
          | None initializes default values.
          | keys:
          | - 'F': the scale factor to be used in the mutation (default: 0.5);
          | - 'CR': the crossover factor used in the recombination (def.: 0.3);
          | - 'mu': the population size (number of individuals) (def.: 100);
          | - 'kmax': maximum number of iterations (def.: 300);
          | - 'display': 'on' to display the population while the algorithm is
          |         being executed, and 'off' to not (default: 'off');
          | If any of the parameters is not set, the default ones are used
          | instead.

    Returns: fopt, xopt
          :fopt: the m x mu_opt ndarray with the mu_opt best objectives
          :xopt: the n x mu_opt ndarray with the mu_opt best individuals
    """
    options = init_options(options=options)
    n = xrange.shape[0]
    P = {'x': np.random.rand(n, options['mu'])}
    P['f'] = fobjeval(f, P['x'], args, xrange)
    m = P['f'].shape[0]
    k = 0
    Pfirst = P.copy()
    axh = None
    while k <= options['kmax']:
        if options['display'] == True:
            if (k == 0) & (m < 4):
                fig = plt.gcf()
                fig.show()
                fig.canvas.draw()
            if m == 2:
                axh = plt.axes()
                plt.plot(P['f'][0], P['f'][1], 'o')
                plt.title('Objective values during the execution')
                plt.xlabel('f_1')
                plt.ylabel('f_2')
                fig.canvas.draw()
                del axh.lines[0]
            elif m == 3:
                axh = plt.axes(projection='3d')
                axh.plot3D(P['f'][0], P['f'][1], P['f'][2], 'o')
                plt.title('Objective values during the execution')
                axh.set_xlabel('f_1')
                axh.set_ylabel('f_2')
                axh.set_zlabel('f_3')
                fig.canvas.draw()
                plt.pause(0.01)
                del axh.lines[0]
        O = {'x': mutation(P['x'], options)}
        O['x'] = recombination(P['x'].copy(), O['x'], options)
        O['x'] = repair(O['x'])
        O['f'] = fobjeval(f, O['x'], args, xrange)
        P = selection(P, O, options)
        print('Iteration #{:1.0f} of {:1.0f}'.format(k, options['kmax']))
        k += 1

    Xmin = xrange[:, 0][:, None]
    Xmax = xrange[:, 1][:, None]
    Xun = (Xmax - Xmin) * P['x'] + Xmin
    ispar = ndset(P['f'])
    fopt = P['f'][:, ispar]
    xopt = Xun[:, ispar]
    return (
     fopt, xopt)


def fobjeval(f, x, args, xrange):
    """
    Evaluates the objective function.
    Since the population is normalized, this function unnormalizes it and
    computes the objective values.

    Args:
       :f: 
           | handle to objective function.
           | The output must be, for each point, a column vector of size m x 1, 
           | with m > 1 the number of objectives.
       :x: 
           | a n x mu ndarray with mu individuals (points) and n variables 
           | (dimension size)
       :args: 
          | Input arguments required for f.
       :options:
           | the dict with the parameters of the algorithm.

    Returns:
       :phi: 
           | a m x mu ndarray with the m objective values of the mu
           | individuals
    """
    mu = x.shape[1]
    Xmin = xrange[:, 0][:, None]
    Xmax = xrange[:, 1][:, None]
    Xun = (Xmax - Xmin) * x + Xmin
    if bool(()) == False:
        phi = f(Xun)
    else:
        phi = f(Xun, **args)
    return phi


def mutation(Xp, options):
    """
    Performs mutation in the individuals.
    The mutation is one of the operators responsible for random changes in
    the individuals. Each parent x will have a new individual, called trial
    vector u, after the mutation.
    To do that, pick up two random individuals from the population, x2 and
    x3, and creates a difference vector v = x2 - x3. Then, chooses another
    point, called base vector, xb, and creates the trial vector by

       u = xb + F*v = xb + F*(x2 - x3)

    wherein F is an internal parameter, called scale factor.

    Args:
       :Xp: 
           | a n x mu ndarray with mu "parents" and of dimension n
       :options: 
           | the dict with the internal parameters

    Returns:
       :Xo: 
           | a n x mu ndarray with the mu mutated individuals (of dimension n)
    """
    A = np.arange(options['mu']).repeat(options['mu']).reshape(options['mu'], options['mu']).T
    A = np.reshape(A[(np.eye(A.shape[0]) == False)], (options['mu'], options['mu'] - 1))
    J = np.argsort((np.random.rand)(*A.shape), axis=1)
    Ilin = J * options['mu'] + np.arange(options['mu'])[:, None]
    A = A.T.flatten()[Ilin].reshape(A.shape)
    xbase = Xp[:, A[:, 0]]
    v = Xp[:, A[:, 1]] - Xp[:, A[:, 2]]
    Xo = xbase + options['F'] * v
    return Xo


def recombination(Xp, Xm, options):
    """
    Performs recombination in the individuals.
    The recombination combines the information of the parents and the
    mutated individuals (also called "trial vectors") to create the
    offspring. Assuming x represents the i-th parent, and u the i-th trial
    vector (obtained from the mutation), the offspring xo will have the
    following j-th coordinate: xo_j = u_j if rand_j <= CR, x_j otherwise
    wherein rand_j is a number drawn from a uniform distribution from 0 to
    1, and CR is called the crossover factor. To prevent mere copies, at
    least one coordinate is guaranteed to belong to the trial vector.

   Args:
      :Xp: 
          | a n x mu ndarray with the mu parents
      :Xm: 
          | a n x mu ndarray with the mu mutated points
      :options: 
          | the dict with the internal parameters

   Returns:
      Xo: 
          | a n x mu ndarray with the recombinated points (offspring)
   """
    n = Xp.shape[0]
    aux = np.random.rand(n, options['mu']) <= options['CR']
    auxs = aux.sum(axis=0) == 0
    indc = np.where(auxs)[0]
    indr = np.random.randint(0, n, auxs.sum())
    aux[(indr, indc)] = True
    Xo = Xp
    Xo[aux] = Xm[aux]
    return Xo


def repair(Xo):
    """
    Truncates the population to be in the feasible region.
    """
    Xo = np.clip(Xo, 0, 1)
    return Xo


def selection(P, O, options):
    """
    Selects the next population.
    Each parent is compared to its offspring. If the parent dominates its 
    child, then it goes to the next population. If the offspring dominates 
    the parent, that new member is added. However, if they are incomparable
    (there is no mutual domination), them both are sent to the next 
    population. After that, the new set of individuals must be truncated to 
    mu, wherein mu is the original number of points.
    This is accomplished by the use of "non-dominated sorting", that is,
    ranks the individual in fronts of non-domination, and within each
    front, measures them by using crowding distance. With regard to these
    two metrics, the best individuals are kept in the new population.

   Args:
      :P: 
          | a dict with the parents (x and f)
      :O: 
          | a dict with the offspring
      :options: 
          | the dict with the algorithm's parameters

   Returns:
      :Pnew: 
          | the new population (a dict with x and f)
   """
    aux1 = (P['f'] <= O['f']).all(axis=0)
    aux2 = (P['f'] < O['f']).any(axis=0)
    auxp = np.logical_and(aux1, aux2)
    aux1 = (P['f'] >= O['f']).all(axis=0)
    aux2 = (P['f'] > O['f']).any(axis=0)
    auxo = np.logical_and(aux1, aux2)
    auxpo = np.logical_and(~auxp, ~auxo)
    R = {'f': np.hstack((P['f'][:, auxp].copy(), O['f'][:, auxo].copy(), P['f'][:, auxpo].copy(), O['f'][:, auxpo].copy()))}
    R['x'] = np.hstack((P['x'][:, auxp].copy(), O['x'][:, auxo].copy(), P['x'][:, auxpo].copy(), O['x'][:, auxpo].copy()))
    Pnew = {'x': np.atleast_2d([])}
    Pnew['f'] = np.atleast_2d([])
    while 1:
        ispar = ndset(R['f'])
        if Pnew['f'].shape[1] + ispar.sum() < options['mu']:
            Pnew['f'] = np.hstack((Pnew['f'], R['f'][:, ispar].copy())) if Pnew['f'].size else R['f'][:, ispar].copy()
            Pnew['x'] = np.hstack((Pnew['x'], R['x'][:, ispar].copy())) if Pnew['x'].size else R['x'][:, ispar].copy()
            R['f'] = np.delete((R['f']), ispar, axis=1)
            R['x'] = np.delete((R['x']), ispar, axis=1)
        else:
            Frem = R['f'][:, ispar].copy()
            Xrem = R['x'][:, ispar].copy()
            break

    aux = Pnew['f'].shape[1] + Frem.shape[1] - options['mu']
    if aux == 0:
        Pnew['x'] = np.hstack((Pnew['x'], Xrem.copy()))
        Pnew['f'] = np.hstack((Pnew['f'], Frem.copy()))
    else:
        if aux > 0:
            for ii in range(aux):
                cdist = crowdingdistance(Frem)
                imin = cdist.argmin()
                Frem = np.delete(Frem, imin, axis=1)
                Xrem = np.delete(Xrem, imin, axis=1)

            Pnew['x'] = np.hstack((Pnew['x'], Xrem.copy())) if Pnew['x'].size else Xrem.copy()
            Pnew['f'] = np.hstack((Pnew['f'], Frem.copy())) if Pnew['f'].size else Frem.copy()
        else:
            raise Exception('Run to the hills! This is not supposed to happen!')
    return Pnew


def init_options(options={}, F=None, CR=None, kmax=None, mu=None, display=None):
    """
    Initialize options dict.
    If input arg is None, the default value is used. 
    
    Args:
        :options: {}, optional
         | Dict with options
         | {} initializes dict to default values.
        :F: scale factor, optional
        :CR: crossover factor, optional
        :kmax: maximum number of iterations, optional
        :mu: population size, optional
        :display: show or not the population during execution, optional
        
    Returns:
        :options: dict with options.
    """
    args = locals().copy()
    if bool(options) == False:
        options = {'F':0.5, 
         'CR':0.3,  'kmax':300,  'mu':100,  'display':False}
    return put_args_in_db(options, args)


def ndset(F):
    """
    Finds the nondominated set of a set of objective points.

    Args:
      F: 
          | a m x mu ndarray with mu points and m objectives

   Returns:
      :ispar: 
          | a mu-length vector with true in the nondominated points
    """
    mu = F.shape[1]
    f1 = np.transpose((F[(Ellipsis, None)]), axes=[0, 2, 1])
    f1 = np.repeat(f1, mu, axis=1)
    f2 = np.repeat((F[(Ellipsis, None)]), mu, axis=2)
    aux1 = (f1 <= f2).all(axis=0, keepdims=True)
    aux2 = (f1 < f2).any(axis=0, keepdims=True)
    auxf1 = np.logical_and(aux1, aux2)
    aux1 = (f1 >= f2).all(axis=0, keepdims=True)
    aux2 = (f1 > f2).any(axis=0, keepdims=True)
    auxf2 = np.logical_and(aux1, aux2)
    dom = np.zeros((1, mu, mu), dtype=int)
    dom[auxf1] = 1
    dom[auxf2] = -1
    ispar = (dom != -1).all(axis=1)
    ispar = ispar.flatten()
    return ispar


def crowdingdistance(F):
    """
    Computes the crowding distance of a nondominated front.
    The crowding distance gives a measure of how close the individuals are
    with regard to its neighbors. The higher this value, the greater the
    spacing. This is used to promote better diversity in the population.

    Args:
       F: 
           | an m x mu ndarray with mu individuals and m objectives

    Returns:
       cdist: 
           | a m-length column vector
    """
    m, mu = F.shape
    if mu == 2:
        cdist = np.vstack((np.inf, np.inf))
        return cdist
    else:
        Is = F.argsort(axis=1)
        Fs = np.sort(F, axis=1)
        C = Fs[:, 2:] - Fs[:, :-2]
        C = np.hstack((np.inf * np.ones((m, 1)), C, np.inf * np.ones((m, 1))))
        Aux = np.arange(m).repeat(mu).reshape(m, mu)
        ind = np.ravel_multi_index((Aux.flatten(), Is.flatten()), (m, mu))
        C2 = C.flatten().copy()
        C2[ind] = C2.flatten()
        C = C2.reshape((m, mu))
        den = np.repeat(((Fs[:, -1] - Fs[:, 0])[:, None]), mu, axis=1)
        cdist = (C / den).sum(axis=0)
        cdist = cdist.flatten()
        return cdist


def dtlz2(x, M):
    """
    DTLZ2 multi-objective function
    This function represents a hyper-sphere.
    Using k = 10, the number of dimensions must be n = (M - 1) + k.
    The Pareto optimal solutions are obtained when the last k variables of x
    are equal to 0.5.
    
    Args:
        :x: 
            | a n x mu ndarray with mu points and n dimensions
        :M: 
            | a scalar with the number of objectives
    
       Returns:
          f: 
            | a m x mu ndarray with mu points and their m objectives computed at
            | the input
    """
    k = 10
    n = M - 1 + k
    if x.shape[0] != n:
        raise Exception('Using k = 10, it is required that the number of dimensions be n = (M - 1) + k = {:1.0f} in this case.'.format(n))
    xm = x[n - k:, :].copy()
    g = ((xm - 0.5) ** 2).sum(axis=0)
    f = np.empty((M, x.shape[1]))
    f[0, :] = (1 + g) * np.prod((np.cos(np.pi / 2 * x[:M - 1, :])), axis=0)
    for ii in range(1, M - 1):
        f[ii, :] = (1 + g) * np.prod((np.cos(np.pi / 2 * x[:M - ii - 1, :])), axis=0) * np.sin(np.pi / 2 * x[M - ii - 1, :])

    f[M - 1, :] = (1 + g) * np.sin(np.pi / 2 * x[0, :])
    return f


def dtlz_range(fname, M):
    """
    Returns the decision range of a DTLZ function
    The range is simply [0,1] for all variables. What varies is the number 
    of decision variables in each problem. The equation for that is
    n = (M-1) + k
    wherein k = 5 for DTLZ1, 10 for DTLZ2-6, and 20 for DTLZ7.
    
    Args:
        :fname: 
            | a string with the name of the function ('dtlz1', 'dtlz2' etc.)
        :M: 
            | a scalar with the number of objectives
    
       Returns:
          :lim: 
              | a n x 2 matrix wherein the first column is the lower limit 
               (0), and the second column, the upper limit of search (1)
    """
    fname = fname.lower()
    if len(fname) < 5 or fname[:4] != 'dtlz' or float(fname[4]) > 7:
        raise Exception('Sorry, the function {:s} is not implemented.'.format(fname))
    else:
        if fname == 'dtlz1':
            k = 5
        else:
            if fname == 'dtlz7':
                k = 20
            else:
                k = 10
    n = M - 1 + k
    lim = np.hstack((np.zeros((n, 1)), np.ones((n, 1))))
    return lim


if __name__ == '__main__':
    k = 10
    opts = init_options(display=True)
    f = lambda x: dtlz2(x, k)
    xrange = dtlz_range('dtlz2', k)
    fopt, xopt = demo_opt(f, xrange=xrange, options=opts)
    mu = xopt.shape[1]
    xlast = 0.5 * np.ones((k, mu))
    d = ((xopt[-1 - k:-1, :] - xlast) ** 2).sum(axis=0)
    print('min(d): {:1.3f}'.format(d.min()))
    print('mean(d): {:1.3f}'.format(d.mean()))
    print('max(d): {:1.3f}'.format(d.max()))