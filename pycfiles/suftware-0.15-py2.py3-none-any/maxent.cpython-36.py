# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/suftware_release_0P13/suftware/src/maxent.py
# Compiled at: 2018-04-12 11:57:16
# Size of source mod 2**32: 13939 bytes
import scipy as sp, numpy as np
from scipy.linalg import solve, det, norm
import suftware.src.utils as utils
from suftware.src.utils import ControlledError
PHI_STD_REG = utils.PHI_STD_REG

def coeffs_to_field(coeffs, kernel):
    """ For maxent algorithm. """
    G = kernel.shape[0]
    kernel_dim = kernel.shape[1]
    if not len(coeffs) == kernel_dim:
        raise ControlledError('/coeffs_to_field/ coeffs must have length %d: len(coeffs) = %d' % (kernel_dim, len(coeffs)))
    if not all(np.isreal(coeffs)):
        raise ControlledError('/coeffs_to_field/ coeffs is not real: coeffs = %s' % coeffs)
    if not all(np.isfinite(coeffs)):
        raise ControlledError('/coeffs_to_field/ coeffs is not finite: coeffs = %s' % coeffs)
    kernel_mat = sp.mat(kernel)
    coeffs_col = sp.mat(coeffs).T
    field_col = kernel_mat * coeffs_col
    return sp.array(field_col).ravel()


def action_per_datum_from_coeffs(coeffs, R, kernel, phi0=False, regularized=False):
    """ For optimizer. Computes action from coefficients. """
    G = kernel.shape[0]
    kernel_dim = kernel.shape[1]
    if not len(coeffs) == kernel_dim:
        raise ControlledError('/action_per_datum_from_coeffs/ coeffs must have length %d: len(coeffs) = %d' % (kernel_dim, len(coeffs)))
    if not all(np.isreal(coeffs)):
        raise ControlledError('/action_per_datum_from_coeffs/ coeffs is not real: coeffs = %s' % coeffs)
    if not all(np.isfinite(coeffs)):
        raise ControlledError('/action_per_datum_from_coeffs/ coeffs is not finite: coeffs = %s' % coeffs)
    if not isinstance(phi0, np.ndarray):
        phi0 = np.zeros(G)
    else:
        if not all(np.isreal(phi0)):
            raise ControlledError('/action_per_datum_from_coeffs/ phi0 is not real: phi0 = %s' % phi0)
    if not all(np.isfinite(phi0)):
        raise ControlledError('/action_per_datum_from_coeffs/ phi0 is not finite: phi0 = %s' % phi0)
    if not isinstance(regularized, bool):
        raise ControlledError('/action_per_datum_from_coeffs/ regularized must be a boolean: regularized = %s' % type(regularized))
    phi = coeffs_to_field(coeffs, kernel)
    quasiQ = utils.field_to_quasiprob(phi + phi0)
    current_term = sp.sum(R * phi)
    nonlinear_term = sp.sum(quasiQ)
    s = current_term + nonlinear_term
    if regularized:
        s += 0.5 / G * sum(phi ** 2) / PHI_STD_REG ** 2
    if not np.isreal(s):
        raise ControlledError('/action_per_datum_from_coeffs/ s is not real: s = %s' % s)
    if not np.isfinite(s):
        raise ControlledError('/action_per_datum_from_coeffs/ s is not finite: s = %s' % s)
    return s


def gradient_per_datum_from_coeffs(coeffs, R, kernel, phi0=False, regularized=False):
    """ For optimizer. Computes gradient from coefficients. """
    G = kernel.shape[0]
    kernel_dim = kernel.shape[1]
    if not len(coeffs) == kernel_dim:
        raise ControlledError('/gradient_per_datum_from_coeffs/ coeffs must have length %d: len(coeffs) = %d' % (kernel_dim, len(coeffs)))
    if not all(np.isreal(coeffs)):
        raise ControlledError('/gradient_per_datum_from_coeffs/ coeffs is not real: coeffs = %s' % coeffs)
    if not all(np.isfinite(coeffs)):
        raise ControlledError('/gradient_per_datum_from_coeffs/ coeffs is not finite: coeffs = %s' % coeffs)
    if not isinstance(phi0, np.ndarray):
        phi0 = np.zeros(G)
    else:
        if not all(np.isreal(phi0)):
            raise ControlledError('/gradient_per_datum_from_coeffs/ phi0 is not real: phi0 = %s' % phi0)
    if not all(np.isfinite(phi0)):
        raise ControlledError('/gradient_per_datum_from_coeffs/ phi0 is not finite: phi0 = %s' % phi0)
    if not isinstance(regularized, bool):
        raise ControlledError('/gradient_per_datum_from_coeffs/ regularized must be a boolean: regularized = %s' % type(regularized))
    phi = coeffs_to_field(coeffs, kernel)
    quasiQ = utils.field_to_quasiprob(phi + phi0)
    R_row = sp.mat(R)
    quasiQ_row = sp.mat(quasiQ)
    kernel_mat = sp.mat(kernel)
    mu_R_row = R_row * kernel_mat
    mu_quasiQ_row = quasiQ_row * kernel_mat
    grad_row = mu_R_row - mu_quasiQ_row
    if regularized:
        reg_row = 1.0 / G * sp.mat(phi) / PHI_STD_REG ** 2
        mu_reg_row = reg_row * kernel_mat
        grad_row += mu_reg_row
    grad_array = sp.array(grad_row).ravel()
    if not all(np.isreal(grad_array)):
        raise ControlledError('/gradient_per_datum_from_coeffs/ grad_array is not real: grad_array = %s' % grad_array)
    if not all(np.isfinite(grad_array)):
        raise ControlledError('/gradient_per_datum_from_coeffs/ grad_array is not finite: grad_array = %s' % grad_array)
    return sp.array(grad_row).ravel()


def hessian_per_datum_from_coeffs(coeffs, R, kernel, phi0=False, regularized=False):
    """ For optimizer. Computes hessian from coefficients. """
    G = kernel.shape[0]
    kernel_dim = kernel.shape[1]
    if not len(coeffs) == kernel_dim:
        raise ControlledError('/hessian_per_datum_from_coeffs/ coeffs must have length %d: len(coeffs) = %d' % (kernel_dim, len(coeffs)))
    if not all(np.isreal(coeffs)):
        raise ControlledError('/hessian_per_datum_from_coeffs/ coeffs is not real: coeffs = %s' % coeffs)
    if not all(np.isfinite(coeffs)):
        raise ControlledError('/hessian_per_datum_from_coeffs/ coeffs is not finite: coeffs = %s' % coeffs)
    if not isinstance(phi0, np.ndarray):
        phi0 = np.zeros(G)
    else:
        if not all(np.isreal(phi0)):
            raise ControlledError('/hessian_per_datum_from_coeffs/ phi0 is not real: phi0 = %s' % phi0)
    if not all(np.isfinite(phi0)):
        raise ControlledError('/hessian_per_datum_from_coeffs/ phi0 is not finite: phi0 = %s' % phi0)
    if not isinstance(regularized, bool):
        raise ControlledError('/hessian_per_datum_from_coeffs/ regularized must be a boolean: regularized = %s' % type(regularized))
    phi = coeffs_to_field(coeffs, kernel)
    quasiQ = utils.field_to_quasiprob(phi + phi0)
    kernel_mat = sp.mat(kernel)
    H = sp.mat(sp.diag(quasiQ))
    if regularized:
        H += 1.0 / G * sp.diag(np.ones(G)) / PHI_STD_REG ** 2
    hessian_mat = kernel_mat.T * H * kernel_mat
    return sp.array(hessian_mat)


def compute_maxent_prob_1d(R, kernel, h=1.0, report_num_steps=False, phi0=False):
    if not isinstance(phi0, np.ndarray):
        phi0 = np.zeros(R.size)
    else:
        assert all(np.isreal(phi0))
    field, num_corrector_steps, num_backtracks = compute_maxent_field(R, kernel, report_num_steps=True, phi0=phi0)
    Q = utils.field_to_prob(field + phi0) / h
    if report_num_steps:
        return (Q, num_corrector_steps, num_backtracks)
    else:
        return Q


def compute_maxent_prob_2d(R, kernel, grid_spacing=[
 1.0, 1.0], report_num_steps=False, phi0=False):
    if not isinstance(phi0, np.ndarray):
        phi0 = np.zeros(R.size)
    else:
        assert all(np.isreal(phi0))
    phi, num_corrector_steps, num_backtracks = compute_maxent_field(R, kernel, report_num_steps=True)
    h = grid_spacing[0] * grid_spacing[1]
    Q = utils.field_to_prob(phi + phi0) / h
    if report_num_steps:
        return (Q, num_corrector_steps, num_backtracks)
    else:
        return Q


def compute_maxent_field(R, kernel, report_num_steps=False, phi0=False, geo_dist_tollerance=0.001, grad_tollerance=1e-05):
    """
    Computes the maxent field from a histogram and kernel
    
    Args:
        R (numpy.narray): 
            Normalized histogram of the raw data. Should have size G
            
        kernel (numpy.ndarray): 
            Array of vectors spanning the smoothness operator kernel. Should
            have size G x kernel_dim
            
    Returns:
        
        phi: 
            The MaxEnt field. 
    """
    if not isinstance(report_num_steps, bool):
        raise ControlledError('/compute_maxent_field/ report_num_steps must be a boolean: report_num_steps = %s' % type(report_num_steps))
    else:
        if not isinstance(phi0, np.ndarray):
            phi0 = np.zeros(len(R))
        else:
            if not all(np.isreal(phi0)):
                raise ControlledError('/compute_maxent_field/ phi0 is not real: phi0 = %s' % phi0)
            else:
                if not all(np.isfinite(phi0)):
                    raise ControlledError('/compute_maxent_field/ phi0 is not finite: phi0 = %s' % phi0)
                if not isinstance(geo_dist_tollerance, float):
                    raise ControlledError('/compute_maxent_field/ geo_dist_tollerance must be a float: geo_dist_tollerance = %s' % type(geo_dist_tollerance))
                raise isinstance(grad_tollerance, float) or ControlledError('/compute_maxent_field/ grad_tollerance must be a float: grad_tollerance = %s' % type(grad_tollerance))
            G = kernel.shape[0]
            kernel_dim = kernel.shape[1]
            if kernel_dim > 1:
                coeffs = sp.zeros(kernel_dim)
            else:
                coeffs = sp.zeros(1)
        phi = coeffs_to_field(coeffs, kernel)
        phi = sp.array(phi).ravel()
        phi0 = sp.array(phi0).ravel()
        Q = utils.field_to_prob(phi + phi0)
        s = action_per_datum_from_coeffs(coeffs, R, kernel, phi0)
        num_corrector_steps = 0
        num_backtracks = 0
        while 1:
            if kernel_dim == 1:
                success = True
                break
            else:
                v = gradient_per_datum_from_coeffs(coeffs, R, kernel, phi0)
                if norm(v) < G * utils.TINY_FLOAT32:
                    break
                Lambda = hessian_per_datum_from_coeffs(coeffs, R, kernel, phi0)
                da = -sp.real(solve(Lambda, v))
                ds = sp.sum(da * v)
                if ds > 0:
                    print('Warning: ds > 0. Quitting compute_maxent_field.')
                    break
                beta = 1.0
                success = False
                while 1:
                    coeffs_new = coeffs + beta * da
                    s_new = action_per_datum_from_coeffs(coeffs_new, R, kernel, phi0)
                    if s_new <= s + 0.5 * beta * ds:
                        break
                    else:
                        if beta < 1e-20:
                            raise ControlledError('/compute_maxent_field/ phi is not converging: beta = %s' % beta)
                        else:
                            num_backtracks += 1
                            beta *= 0.5

                phi_new = coeffs_to_field(coeffs_new, kernel)
                Q_new = utils.field_to_prob(phi_new + phi0)
                if utils.geo_dist(Q_new, Q) < geo_dist_tollerance:
                    if np.linalg.norm(v) < grad_tollerance:
                        success = True
                        break
                if s_new - s > 0:
                    print('Warning: action has increased. Terminating steps.')
                    success = False
                    break
                else:
                    num_corrector_steps += 1
                coeffs = coeffs_new
                s = s_new
                Q = Q_new
                phi = phi_new

        if not success:
            print('gradident norm == %f' % np.linalg.norm(v))
            print('gradient tollerance == %f' % grad_tollerance)
            print('Failure! Trying Maxent again!')
    if report_num_steps:
        return (phi, num_corrector_steps, num_backtracks)
    else:
        return (
         phi, success)