# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\utils\math\minimizebnd.py
# Compiled at: 2019-06-20 20:12:17
# Size of source mod 2**32: 10492 bytes
"""
Module with port from Matlab fminsearchbnd, but applied to SciPy's minimize fcn
===============================================================================

 :minimizebnd(): scipy.minimize() wrapper that allows contrained parameters on 
                 unconstrained methods(port of Matlab's fminsearchbnd). 
                 Starting, lower and upper bounds values can also be provided 
                 as a dict.

===============================================================================
"""
from luxpy import np, minimize, vec_to_dict
__all__ = [
 'minimizebnd']

def minimizebnd(fun, x0, args=(), method='nelder-mead', use_bnd=True, bounds=(None, None), options=None, x0_vsize=None, x0_keys=None, **kwargs):
    """
    Minimization function that allows for bounds on any type of method in 
    SciPy's minimize function by transforming the parameters values 
    | (see Matlab's fminsearchbnd). 
    | Starting values, and lower and upper bounds can also be provided as a dict.
    
    Args:
        :x0: 
            | parameter starting values
            | If x0_keys is None then :x0: is vector else, :x0: is dict and
            | x0_size should be provided with length/size of values for each of 
              the keys in :x0: to convert it to a vector.                
        :use_bnd:
            | True, optional
            | False: omits bounds and defaults to regular minimize function.
        :bounds:
            | (lower, upper), optional
            | Tuple of lists or dicts (x0_keys is None) of lower and upper bounds 
              for each of the parameters values.
        :kwargs: 
            | allows input for other type of arguments (e.g. in OutputFcn)
         
    Note:
        For other input arguments, see ?scipy.minimize()
         
    Returns:
        :res: 
            | dict with minimize() output. 
            | Additionally, function value, fval, of solution is also in :res:,
              as well as a vector or dict (if x0 was dict) 
              with final solutions (res['x'])
        
        
    """
    if isinstance(x0, dict):
        x0, vsize = vec_to_dict(dic=x0, vsize=x0_vsize, keys=x0_keys)
    else:
        if use_bnd == False:
            res = minimize(fun, x0, args=args, options=options, **kwargs)
            res['fval'] = fun(res['x'], *args)
            if x0_keys is None:
                res['x_final'] = res['x']
            else:
                res['x_final'] = vec_to_dict(vec=(res['x']), vsize=x0_vsize, keys=x0_keys)
            return res
        else:
            LB, UB = bounds
            if isinstance(LB, dict):
                LB, vsize = vec_to_dict(dic=LB, vsize=x0_vsize, keys=x0_keys)
            if isinstance(UB, dict):
                UB, vsize = vec_to_dict(dic=UB, vsize=x0_vsize, keys=x0_keys)
            xsize = x0.shape
            x0 = x0.flatten()
            n = x0.shape[0]
            if LB is None:
                LB = -np.inf * np.ones(n)
            else:
                LB = LB.flatten()
            if UB is None:
                UB = np.inf * np.ones(n)
            else:
                UB = UB.flatten()
            if (n != LB.shape[0]) | (n != UB.shape[0]):
                raise Exception('minimizebnd(): x0 is incompatible in size with either LB or UB.')
            if options is None:
                options = {}
        params = {}
        params['args'] = args
        params['LB'] = LB
        params['UB'] = UB
        params['fun'] = fun
        params['n'] = n
        params['OutputFcn'] = None
        params['BoundClass'] = np.zeros(n)
        for i in range(n):
            k = np.isfinite(LB[i]) + 2 * np.isfinite(UB[i])
            params['BoundClass'][i] = k
            if (k == 3) & (LB[i] == UB[i]):
                params['BoundClass'][i] = 4

        x0u = x0
        k = 0
        for i in range(n):
            if params['BoundClass'][i] == 1:
                if x0[i] <= LB[i]:
                    x0u[k] = 0
                else:
                    x0u[k] = np.sqrt(x0[i] - LB[i])
            elif params['BoundClass'][i] == 2:
                if x0[i] >= UB[i]:
                    x0u[k] = 0
                else:
                    x0u[k] = np.sqrt(UB[i] - x0[i])
            elif params['BoundClass'][i] == 2:
                if x0[i] <= LB[i]:
                    x0u[k] = -np.pi / 2
                else:
                    if x0[i] >= UB[i]:
                        x0u[k] = np.pi / 2
                    else:
                        x0u[k] = 2 * (x0[i] - LB[i]) / (UB[i] - LB[i]) - 1
                        x0u[k] = 2 * np.pi + np.asin(np.hstack((-1, np.hstack((1, x0u[k]).min()))).max())
            elif params['BoundClass'][i] == 0:
                x0u[k] = x0[i]
            else:
                if params['BoundClass'][i] != 4:
                    k += 1

        if k <= n:
            x0u = x0u[:k + 1]
    if x0u.shape[0] == 0:
        x = xtransform(x0u, params)
        x = x.reshape(xsize)
        fval = (params['fun'])(x, *params['args'])
        output = {'success': False}
        output['x'] = x
        output['iterations'] = 0
        output['funcount'] = 1
        output['algorithm'] = method
        output['message'] = 'All variables were held fixed by the applied bounds'
        output['status'] = 0
        return output
    else:

        def outfun_wrapper(x, **kwargs):
            xtrans = xtransform(x, params)
            stop = (params['OutputFcn'])(xtrans, **kwargs)
            return stop

        if 'OutputFcn' in options:
            if options['OutputFcn'] is not None:
                params['OutputFcn'] = options['OutputFcn']
                options['OutputFcn'] = outfun_wrapper
        res = minimize(intrafun, x0u, args=params, method=method, options=options)
        fval = intrafun(res['x'], params)
        x = xtransform(res['x'], params)
        x = x.reshape(xsize)
        res['fval'] = fval
        res['x'] = x
        if x0_keys is None:
            res['x_final'] = res['x']
        else:
            res['x_final'] = vec_to_dict(vec=(res['x']), vsize=x0_vsize, keys=x0_keys)
        return res


def intrafun(x, params):
    """
    Transforms variables, then calls original function.
    """
    xtrans = xtransform(x, params)
    fval = (params['fun'])(xtrans, *params['args'])
    return fval


def xtransform(x, params):
    """
    Converts unconstrained variables into their original domains.
    """
    xtrans = np.zeros(params['n'])
    k = 0
    for i in range(params['n']):
        if params['BoundClass'][i] == 1:
            xtrans[i] = params['LB'][i] + x[k] ** 2
        else:
            if params['BoundClass'][i] == 2:
                xtrans[i] = params['UB'][i] - x[k] ** 2
            else:
                if params['BoundClass'][i] == 3:
                    xtrans[i] = (np.sin(x[k]) + 1) / 2
                    xtrans[i] = xtrans[i] * (params['UB'][i] - params['LB'][i]) + params['LB'][i]
                    xtrans[i] = np.hstack((params['LB'][i], np.hstack((params['UB'][i], xtrans[i])).min())).max()
                else:
                    if params['BoundClass'][i] == 4:
                        xtrans[i] = params['LB'][i]
                    else:
                        if params['BoundClass'][i] == 0:
                            xtrans[i] = x[k]
        if params['BoundClass'][i] != 4:
            k += 1

    return xtrans