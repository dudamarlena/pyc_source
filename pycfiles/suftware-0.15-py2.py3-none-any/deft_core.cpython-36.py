# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/suftware_release_0P13/suftware/src/deft_core.py
# Compiled at: 2018-04-12 13:07:25
# Size of source mod 2**32: 33758 bytes
import scipy as sp, numpy as np
from scipy.sparse import csr_matrix, diags, spdiags
from scipy.sparse.linalg import spsolve, eigsh
from scipy.linalg import det, eigh, solve, eigvalsh, inv
import scipy.optimize as opt, time, sys
if sys.version_info[0] == 3:
    import suftware.src.utils as utils, suftware.src.supplements as supplements, suftware.src.maxent as maxent
else:
    import utils, supplements, maxent
from suftware.src.utils import ControlledError
T_MAX = 40
T_MIN = -40
PHI_MAX = utils.PHI_MAX
PHI_MIN = utils.PHI_MIN
MAX_DS = -0.001
PHI_STD_REG = utils.PHI_STD_REG

class Results:
    pass


class MAP_curve_point:

    def __init__(self, t, phi, Q, log_E, sample_mean, sample_mean_std_dev, details=False):
        self.t = t
        self.phi = phi
        self.Q = Q
        self.log_E = log_E
        self.sample_mean = sample_mean
        self.sample_mean_std_dev = sample_mean_std_dev


class MAP_curve:

    def __init__(self):
        self.points = []
        self._is_sorted = False

    def add_point(self, t, phi, Q, log_E, sample_mean, sample_mean_std_dev, details=False):
        point = MAP_curve_point(t, phi, Q, log_E, sample_mean, sample_mean_std_dev, details)
        self.points.append(point)
        self._is_sorted = False

    def sort(self):
        self.points.sort(key=(lambda x: x.t))
        self._is_sorted = True

    def get_points(self):
        if not self._is_sorted:
            self.sort()
        return self.points

    def get_maxent_point(self):
        if not self._is_sorted:
            self.sort()
        p = self.points[0]
        if not p.t == -sp.Inf:
            raise ControlledError('/MAP_curve/ Not getting MaxEnt point: t = %f' % p.t)
        return p

    def get_histogram_point(self):
        if not self._is_sorted:
            self.sort()
        p = self.points[(-1)]
        if not p.t == sp.Inf:
            raise ControlledError('/MAP_curve/ Not getting histogram point: t = %f' % p.t)
        return p

    def get_log_evidence_ratios(self, finite=True):
        log_Es = sp.array([p.log_E for p in self.points])
        ts = sp.array([p.t for p in self.points])
        if finite:
            indices = (log_Es > -np.Inf) * (ts > -np.Inf) * (ts < np.Inf)
            return (
             log_Es[indices], ts[indices])
        else:
            return (
             log_Es, ts)


def action(phi, R, Delta, t, N, phi_in_kernel=False, regularized=False):
    if not all(np.isreal(phi)):
        raise ControlledError('/action/ phi is not real: phi = %s' % phi)
    else:
        if not all(np.isfinite(phi)):
            raise ControlledError('/action/ phi is not finite: phi = %s' % phi)
        else:
            if not np.isreal(t):
                raise ControlledError('/action/ t is not real: t = %s' % t)
            else:
                if not isinstance(phi_in_kernel, bool):
                    raise ControlledError('/action/ phi_in_kernel must be a boolean: phi_in_kernel = %s' % type(phi_in_kernel))
                else:
                    if not isinstance(regularized, bool):
                        raise ControlledError('/action/ regularized must be a boolean: regularized = %s' % type(regularized))
                    G = 1.0 * len(R)
                    quasiQ = utils.field_to_quasiprob(phi)
                    quasiQ_col = sp.mat(quasiQ).T
                    Delta_sparse = Delta.get_sparse_matrix()
                    phi_col = sp.mat(phi).T
                    R_col = sp.mat(R).T
                    ones_col = sp.mat(sp.ones(int(G))).T
                    if phi_in_kernel:
                        S_mat = G * R_col.T * phi_col + G * ones_col.T * quasiQ_col
                    else:
                        S_mat = 0.5 * sp.exp(-t) * phi_col.T * Delta_sparse * phi_col + G * R_col.T * phi_col + G * ones_col.T * quasiQ_col
                if regularized:
                    S_mat += 0.5 * (phi_col.T * phi_col) / (N * PHI_STD_REG ** 2)
            S = S_mat[(0, 0)]
            raise np.isreal(S) or ControlledError('/action/ S is not real at t = %s: S = %s' % (t, S))
        raise np.isfinite(S) or ControlledError('/action/ S is not finite at t = %s: S = %s' % (t, S))
    return S


def gradient(phi, R, Delta, t, N, regularized=False):
    if not all(np.isreal(phi)):
        raise ControlledError('/gradient/ phi is not real: phi = %s' % phi)
    else:
        if not all(np.isfinite(phi)):
            raise ControlledError('/gradient/ phi is not finite: phi = %s' % phi)
        else:
            if not np.isreal(t):
                raise ControlledError('/gradient/ t is not real: t = %s' % t)
            else:
                if not np.isfinite(t):
                    raise ControlledError('/gradient/ t is not finite: t = %s' % t)
                if not isinstance(regularized, bool):
                    raise ControlledError('/gradient/ regularized must be a boolean: regularized = %s' % type(regularized))
                G = 1.0 * len(R)
                quasiQ = utils.field_to_quasiprob(phi)
                quasiQ_col = sp.mat(quasiQ).T
                Delta_sparse = Delta.get_sparse_matrix()
                phi_col = sp.mat(phi).T
                R_col = sp.mat(R).T
                grad_col = sp.exp(-t) * Delta_sparse * phi_col + G * R_col - G * quasiQ_col
                if regularized:
                    grad_col += phi_col / (N * PHI_STD_REG ** 2)
            grad = sp.array(grad_col).ravel()
            raise all(np.isreal(grad)) or ControlledError('/gradient/ grad is not real at t = %s: grad = %s' % (t, grad))
        raise all(np.isfinite(grad)) or ControlledError('/gradient/ grad is not finite at t = %s: grad = %s' % (t, grad))
    return grad


def hessian(phi, R, Delta, t, N, regularized=False):
    if not all(np.isreal(phi)):
        raise ControlledError('/hessian/ phi is not real: phi = %s' % phi)
    else:
        if not all(np.isfinite(phi)):
            raise ControlledError('/hessian/ phi is not finite: phi = %s' % phi)
        else:
            if not np.isreal(t):
                raise ControlledError('/hessian/ t is not real: t = %s' % t)
            if not np.isfinite(t):
                raise ControlledError('/hessian/ t is not finite: t = %s' % t)
            raise isinstance(regularized, bool) or ControlledError('/hessian/ regularized must be a boolean: regularized = %s' % type(regularized))
        G = 1.0 * len(R)
        quasiQ = utils.field_to_quasiprob(phi)
        Delta_sparse = Delta.get_sparse_matrix()
        H = sp.exp(-t) * Delta_sparse + G * diags(quasiQ, 0)
        if regularized:
            H += diags(np.ones(int(G)), 0) / (N * PHI_STD_REG ** 2)
    return H


def log_ptgd_at_maxent(phi_M, R, Delta, N, Z_eval, num_Z_samples):
    if not all(np.isreal(phi_M)):
        raise ControlledError('/log_ptgd_at_maxent/ phi_M is not real: phi_M = %s' % phi_M)
    else:
        if not all(np.isfinite(phi_M)):
            raise ControlledError('/log_ptgd_at_maxent/ phi_M is not finite: phi_M = %s' % phi_M)
        else:
            kernel_dim = Delta._kernel_dim
            M = utils.field_to_prob(phi_M)
            M_on_kernel = sp.zeros([kernel_dim, kernel_dim])
            kernel_basis = Delta._kernel_basis
            lambdas = Delta._eigenvalues
            for a in range(int(kernel_dim)):
                for b in range(int(kernel_dim)):
                    psi_a = sp.ravel(kernel_basis[:, a])
                    psi_b = sp.ravel(kernel_basis[:, b])
                    M_on_kernel[(a, b)] = sp.sum(psi_a * psi_b * M)

            log_Occam_at_infty = -0.5 * sp.log(det(M_on_kernel)) - 0.5 * sp.sum(sp.log(lambdas[kernel_dim:]))
            if not np.isreal(log_Occam_at_infty):
                raise ControlledError('/log_ptgd_at_maxent/ log_Occam_at_infty is not real: log_Occam_at_infty = %s' % log_Occam_at_infty)
            if not np.isfinite(log_Occam_at_infty):
                raise ControlledError('/log_ptgd_at_maxent/ log_Occam_at_infty is not finite: log_Occam_at_infty = %s' % log_Occam_at_infty)
            log_likelihood_at_infty = -N * sp.sum(phi_M * R) - N
            if not np.isreal(log_likelihood_at_infty):
                raise ControlledError('/log_ptgd_at_maxent/ log_likelihood_at_infty is not real: log_likelihood_at_infty = %s' % log_likelihood_at_infty)
            if not np.isfinite(log_likelihood_at_infty):
                raise ControlledError('/log_ptgd_at_maxent/ log_likelihood_at_infty is not finite: log_likelihood_at_infty = %s' % log_likelihood_at_infty)
            log_ptgd_at_maxent = log_likelihood_at_infty + log_Occam_at_infty
            t = -np.inf
            num_samples = num_Z_samples
            if Z_eval == 'Lap':
                correction, w_sample_mean, w_sample_mean_std = (0.0, 1.0, 0.0)
            if Z_eval == 'Lap+Imp':
                correction, w_sample_mean, w_sample_mean_std = supplements.Laplace_approach(phi_M, R, Delta, t, N, num_samples, go_parallel=False)
            if Z_eval == 'Lap+Imp+P':
                correction, w_sample_mean, w_sample_mean_std = supplements.Laplace_approach(phi_M, R, Delta, t, N, num_samples, go_parallel=True)
            if Z_eval == 'GLap':
                correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi_M, R, Delta, t, N, num_samples, go_parallel=False, sampling=False)
            if Z_eval == 'GLap+P':
                correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi_M, R, Delta, t, N, num_samples, go_parallel=True, sampling=False)
            if Z_eval == 'GLap+Sam':
                correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi_M, R, Delta, t, N, num_samples, go_parallel=False, sampling=True)
            if Z_eval == 'GLap+Sam+P':
                correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi_M, R, Delta, t, N, num_samples, go_parallel=True, sampling=True)
            if Z_eval == 'Lap+Fey':
                correction, w_sample_mean, w_sample_mean_std = supplements.Feynman_diagrams(phi_M, R, Delta, t, N)
            raise np.isreal(correction) or ControlledError('/log_ptgd_at_maxent/ correction is not real: correction = %s' % correction)
        raise np.isfinite(correction) or ControlledError('/log_ptgd_at_maxent/ correction is not finite: correction = %s' % correction)
    log_ptgd_at_maxent += correction
    return (
     log_ptgd_at_maxent, w_sample_mean, w_sample_mean_std)


def log_ptgd(phi, R, Delta, t, N, Z_eval, num_Z_samples):
    if not all(np.isreal(phi)):
        raise ControlledError('/log_ptgd/ phi is not real: phi = %s' % phi)
    else:
        if not all(np.isfinite(phi)):
            raise ControlledError('/log_ptgd/ phi is not finite: phi = %s' % phi)
        else:
            if not np.isreal(t):
                raise ControlledError('/log_ptgd/ t is not real: t = %s' % t)
            else:
                if not np.isfinite(t):
                    raise ControlledError('/log_ptgd/ t is not finite: t = %s' % t)
                else:
                    G = 1.0 * len(phi)
                    alpha = 1.0 * Delta._alpha
                    kernel_dim = 1.0 * Delta._kernel_dim
                    H = hessian(phi, R, Delta, t, N)
                    H_prime = H.todense() * sp.exp(t)
                    S = action(phi, R, Delta, t, N)
                    log_det = sp.log(det(H_prime))
                    if not (np.isreal(log_det) and np.isfinite(log_det)):
                        lambdas = abs(eigvalsh(H_prime))
                        log_det = sp.sum(sp.log(lambdas))
                    if not np.isreal(log_det):
                        raise ControlledError('/log_ptgd/ log_det is not real at t = %s: log_det = %s' % (t, log_det))
                    if not np.isfinite(log_det):
                        raise ControlledError('/log_ptgd/ log_det is not finite at t = %s: log_det = %s' % (t, log_det))
                    log_ptgd = -(N / G) * S + 0.5 * kernel_dim * t - 0.5 * log_det
                    if not np.isreal(log_ptgd):
                        raise ControlledError('/log_ptgd/ log_ptgd is not real at t = %s: log_ptgd = %s' % (t, log_ptgd))
                    if not np.isfinite(log_ptgd):
                        raise ControlledError('/log_ptgd/ log_ptgd is not finite at t = %s: log_ptgd = %s' % (t, log_ptgd))
                    num_samples = num_Z_samples
                    if Z_eval == 'Lap':
                        correction, w_sample_mean, w_sample_mean_std = (0.0, 1.0, 0.0)
                    if Z_eval == 'Lap+Imp':
                        correction, w_sample_mean, w_sample_mean_std = supplements.Laplace_approach(phi, R, Delta, t, N, num_samples, go_parallel=False)
                    if Z_eval == 'Lap+Imp+P':
                        correction, w_sample_mean, w_sample_mean_std = supplements.Laplace_approach(phi, R, Delta, t, N, num_samples, go_parallel=True)
                    if Z_eval == 'GLap':
                        correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi, R, Delta, t, N, num_samples, go_parallel=False, sampling=False)
                    if Z_eval == 'GLap+P':
                        correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi, R, Delta, t, N, num_samples, go_parallel=True, sampling=False)
                    if Z_eval == 'GLap+Sam':
                        correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi, R, Delta, t, N, num_samples, go_parallel=False, sampling=True)
                    if Z_eval == 'GLap+Sam+P':
                        correction, w_sample_mean, w_sample_mean_std = supplements.GLaplace_approach(phi, R, Delta, t, N, num_samples, go_parallel=True, sampling=True)
                if Z_eval == 'Lap+Fey':
                    correction, w_sample_mean, w_sample_mean_std = supplements.Feynman_diagrams(phi, R, Delta, t, N)
            raise np.isreal(correction) or ControlledError('/log_ptgd/ correction is not real at t = %s: correction = %s' % (t, correction))
        raise np.isfinite(correction) or ControlledError('/log_ptgd/ correction is not finite at t = %s: correction = %s' % (t, correction))
    log_ptgd += correction
    details = Results()
    details.S = S
    details.N = N
    details.G = G
    details.kernel_dim = kernel_dim
    details.t = t
    details.log_det = log_det
    details.phi = phi
    return (
     log_ptgd, w_sample_mean, w_sample_mean_std)


def compute_predictor_step(phi, R, Delta, t, N, direction, resolution, DT_MAX):
    if not all(np.isreal(phi)):
        raise ControlledError('/compute_predictor_step/ phi is not real: phi = %s' % phi)
    else:
        if not all(np.isfinite(phi)):
            raise ControlledError('/compute_predictor_step/ phi is not finite: phi = %s' % phi)
        else:
            if not np.isreal(t):
                raise ControlledError('/compute_predictor_step/ t is not real: t = %s' % t)
            else:
                if not np.isfinite(t):
                    raise ControlledError('/compute_predictor_step/ t is not finite: t = %s' % t)
                else:
                    if not (direction == 1 or direction == -1):
                        raise ControlledError('/compute_predictor_step/ direction must be just a sign: direction = %s' % direction)
                    else:
                        Q = utils.field_to_prob(phi)
                        G = 1.0 * len(Q)
                        H = hessian(phi, R, Delta, t, N)
                        rho = G * spsolve(H, Q - R)
                        if not all(np.isreal(rho)):
                            raise ControlledError('/compute_predictor_step/ rho is not real at t = %s: rho = %s' % (t, rho))
                        if not all(np.isfinite(rho)):
                            raise ControlledError('/compute_predictor_step/ rho is not finite at t = %s: rho = %s' % (t, rho))
                        denom = sp.sqrt(sp.sum(rho * Q * rho))
                        if not np.isreal(denom):
                            raise ControlledError('/compute_predictor_step/ denom is not real at t = %s: denom = %s' % (t, denom))
                        if not np.isfinite(denom):
                            raise ControlledError('/compute_predictor_step/ denom is not finite at t = %s: denom = %s' % (t, denom))
                        raise denom > 0 or ControlledError('/compute_predictor_step/ denom is not positive at t = %s: denom = %s' % (t, denom))
                    dt = direction * resolution / denom
                    while abs(dt) > DT_MAX:
                        dt /= 2.0

                    phi_new = phi + rho * dt
                    t_new = t + dt
                    raise all(np.isreal(phi_new)) or ControlledError('/compute_predictor_step/ phi_new is not real at t_new = %s: phi_new = %s' % (t_new, phi_new))
                raise all(np.isfinite(phi_new)) or ControlledError('/compute_predictor_step/ phi_new is not finite at t_new = %s: phi_new = %s' % (t_new, phi_new))
            raise np.isreal(t_new) or ControlledError('/compute_predictor_step/ t_new is not real: t_new = %s' % t_new)
        raise np.isfinite(t_new) or ControlledError('/compute_predictor_step/ t_new is not finite: t_new = %s' % t_new)
    return (phi_new, t_new)


def compute_corrector_step(phi, R, Delta, t, N, tollerance, report_num_steps=False):
    if not all(np.isreal(phi)):
        raise ControlledError('/compute_corrector_step/ phi is not real: phi = %s' % phi)
    else:
        if not all(np.isfinite(phi)):
            raise ControlledError('/compute_corrector_step/ phi is not finite: phi = %s' % phi)
        else:
            if not np.isreal(t):
                raise ControlledError('/compute_corrector_step/ t is not real: t = %s' % t)
            raise np.isfinite(t) or ControlledError('/compute_corrector_step/ t is not finite: t = %s' % t)
        raise isinstance(report_num_steps, bool) or ControlledError('/compute_corrector_step/ report_num_steps must be a boolean: report_num_steps = %s' % type(report_num_steps))
    Q = utils.field_to_prob(phi)
    S = action(phi, R, Delta, t, N)
    num_corrector_steps = 0
    num_backtracks = 0
    while True:
        v = gradient(phi, R, Delta, t, N)
        H = hessian(phi, R, Delta, t, N)
        dphi = -spsolve(H, v)
        if not all(np.isreal(dphi)):
            raise ControlledError('/compute_corrector_step/ dphi is not real at t = %s: dphi = %s' % (t, dphi))
        if not all(np.isfinite(dphi)):
            raise ControlledError('/compute_corrector_step/ dphi is not finite at t = %s: dphi = %s' % (t, dphi))
        dS = sp.sum(dphi * v)
        if dS > MAX_DS:
            break
        beta = 1.0
        while 1:
            if beta < 1e-50:
                raise ControlledError('/compute_corrector_step/ phi is not converging at t = %s: beta = %s' % (t, beta))
            phi_new = phi + beta * dphi
            if any(phi_new < PHI_MIN) or any(phi_new > PHI_MAX):
                num_backtracks += 1
                beta *= 0.5
            else:
                S_new = action(phi_new, R, Delta, t, N)
                if S_new - S <= 0.5 * beta * dS:
                    break
                else:
                    num_backtracks += 1
                    beta *= 0.5
                    continue

        if not all(np.isreal(phi_new)):
            raise ControlledError('/compute_corrector_step/ phi_new is not real at t = %s: phi_new = %s' % (t, phi_new))
        if not all(np.isfinite(phi_new)):
            raise ControlledError('/compute_corrector_step/ phi_new is not finite at t = %s: phi_new = %s' % (t, phi_new))
        Q_new = utils.field_to_prob(phi_new)
        gd = utils.geo_dist(Q_new, Q)
        if gd < tollerance:
            break
        elif S_new - S > 0:
            raise ControlledError('/compute_corrector_step/ S_new > S at t = %s: terminating corrector steps' % t)
        else:
            phi = phi_new
            Q = Q_new
            S = S_new
            num_corrector_steps += 1

    if report_num_steps:
        return (phi, num_corrector_steps, num_backtracks)
    else:
        return phi


def compute_map_curve(N, R, Delta, Z_eval, num_Z_samples, t_start, DT_MAX, print_t, tollerance, resolution, max_log_evidence_ratio_drop):
    """ Traces the map curve in both directions

    Args:

        R (numpy.narray):
            The data histogram

        Delta (Smoothness_operator instance):
            Effectiely defines smoothness

        resolution (float):
            Specifies max distance between neighboring points on the
            MAP curve

    Returns:

        map_curve (list): A list of MAP_curve_points

    """
    G = Delta.get_G()
    alpha = Delta._alpha
    kernel_basis = Delta.get_kernel_basis()
    kernel_dim = Delta.get_kernel_dim()
    map_curve = MAP_curve()
    R = R / sum(R)
    phi_R = utils.prob_to_field(R)
    log_E_R = -np.Inf
    t_R = np.Inf
    w_sample_mean_R = 1.0
    w_sample_mean_std_R = 0.0
    map_curve.add_point(t_R, phi_R, R, log_E_R, w_sample_mean_R, w_sample_mean_std_R)
    phi_infty, success = maxent.compute_maxent_field(R, kernel_basis)
    M = utils.field_to_prob(phi_infty)
    log_ptgd_M, w_sample_mean_M, w_sample_mean_std_M = log_ptgd_at_maxent(phi_infty, R, Delta, N, Z_eval, num_Z_samples)
    log_E_M = 0
    t_M = -sp.Inf
    map_curve.add_point(t_M, phi_infty, M, log_E_M, w_sample_mean_M, w_sample_mean_std_M)
    log_E_max = -np.Inf
    phi_start = compute_corrector_step(phi_infty, R, Delta, t_start, N, tollerance)
    Q_start = utils.field_to_prob(phi_start)
    log_ptgd_start, w_sample_mean_start, w_sample_mean_std_start = log_ptgd(phi_start, R, Delta, t_start, N, Z_eval, num_Z_samples)
    log_E_start = log_ptgd_start - log_ptgd_M
    log_E_max = log_E_start if log_E_start > log_E_max else log_E_max
    if print_t:
        print('t = %.2f' % t_start)
    map_curve.add_point(t_start, phi_start, Q_start, log_E_start, w_sample_mean_start, w_sample_mean_std_start)
    break_t_loop = [
     True, True]
    for direction in (-1, 1):
        phi = phi_start
        t = t_start
        Q = Q_start
        log_E = log_E_start
        w_sample_mean = w_sample_mean_start
        w_sample_mean_std_dev = w_sample_mean_std_start
        if direction == -1:
            Q_end = M
        else:
            Q_end = R
        log_ptgd0 = log_ptgd_start
        slope = np.sign(0)
        while utils.geo_dist(Q_end, Q) <= resolution:
            if direction == -1:
                pass
            else:
                break
            phi_pre, t_new = compute_predictor_step(phi, R, Delta, t, N, direction, resolution, DT_MAX)
            if any(phi_pre > PHI_MAX) or any(phi_pre < PHI_MIN):
                phi_pre = phi
            phi_new = compute_corrector_step(phi_pre, R, Delta, t_new, N, tollerance)
            Q_new = utils.field_to_prob(phi_new)
            log_ptgd_new, w_sample_mean_new, w_sample_mean_std_new = log_ptgd(phi_new, R, Delta, t_new, N, Z_eval, num_Z_samples)
            log_E_new = log_ptgd_new - log_ptgd_M
            t = t_new
            Q = Q_new
            phi = phi_new
            log_E = log_E_new
            w_sample_mean = w_sample_mean_new
            w_sample_mean_std = w_sample_mean_std_new
            log_E_max = log_E if log_E > log_E_max else log_E_max
            if log_E_new < log_E_max - max_log_evidence_ratio_drop:
                if direction == -1:
                    break_t_loop[0] = False
                else:
                    break_t_loop[1] = False
                if print_t:
                    print('t = %.2f' % t)
                map_curve.add_point(t, phi, Q, log_E, w_sample_mean, w_sample_mean_std)
                break
            slope_new = np.sign(log_ptgd_new - log_ptgd0)
            if t < T_MIN:
                break_t_loop[0] = False
                break
            else:
                if t > T_MAX:
                    break_t_loop[1] = False
                    break
                else:
                    if direction == 1:
                        if t > 0:
                            if np.sign(slope_new * slope) < 0:
                                if log_ptgd_new > log_ptgd0:
                                    break_t_loop[1] = False
                                    break
            if direction == 1:
                if np.sign(slope_new * slope) < 0:
                    if log_ptgd_new > log_ptgd0 + max_log_evidence_ratio_drop:
                        break_t_loop[1] = False
                        break
            log_ptgd0 = log_ptgd_new
            slope = slope_new
            if print_t:
                print('t = %.2f' % t)
            map_curve.add_point(t, phi, Q, log_E, w_sample_mean, w_sample_mean_std)

    map_curve.sort()
    map_curve.t_start = t_start
    map_curve.break_t_loop = break_t_loop
    return map_curve


def run(counts_array, Delta, Z_eval, num_Z_samples, t_start, DT_MAX, print_t, tollerance, resolution, num_pt_samples, fix_t_at_t_star, max_log_evidence_ratio_drop, details=False):
    """
    The core algorithm of DEFT, used for both 1D and 2D density estmation.

    Args:
        counts_array (numpy.ndarray):
            A scipy array of counts. All counts must be nonnegative.

        Delta (Smoothness_operator instance):
            An operator providing the definition of 'smoothness' used by DEFT
    """
    if not isinstance(details, bool):
        raise ControlledError('/deft_core._run/ details must be a boolean: details = %s' % type(details))
    else:
        G = Delta.get_G()
        kernel_dim = Delta.get_kernel_dim()
        if not len(counts_array) == G:
            raise ControlledError('/deft_core._run/ counts_array must have length %d: len(counts_array) = %d' % (
             G, len(counts_array)))
        if not all(counts_array >= 0):
            raise ControlledError('/deft_core._run/ counts_array is not non-negative: counts_array = %s' % counts_array)
        if not sum(counts_array > 0) > kernel_dim:
            raise ControlledError('/deft_core._run/ Only %d elements of counts_array contain data, less than kernel dimension %d' % (
             sum(counts_array > 0), kernel_dim))
        N = sum(counts_array)
        R = 1.0 * counts_array / N
        start_time = time.clock()
        map_curve = compute_map_curve(N, R, Delta, Z_eval, num_Z_samples, t_start, DT_MAX, print_t, tollerance, resolution, max_log_evidence_ratio_drop)
        end_time = time.clock()
        map_curve_compute_time = end_time - start_time
        if print_t:
            print('MAP curve computation took %.2f sec' % map_curve_compute_time)
        points = map_curve.points
        log_Es = sp.array([p.log_E for p in points])
        log_E_max = log_Es.max()
        ibest = log_Es.argmax()
        star = points[ibest]
        Q_star = np.copy(star.Q)
        t_star = star.t
        phi_star = np.copy(star.phi)
        map_curve.i_star = ibest
        if not num_pt_samples == 0:
            Q_samples, phi_samples, phi_weights = supplements.posterior_sampling(points, R, Delta, N, G, num_pt_samples, fix_t_at_t_star)
        results = Results()
        results.phi_star = phi_star
        results.Q_star = Q_star
        results.R = R
        results.map_curve = map_curve
        results.map_curve_compute_time = map_curve_compute_time
        results.G = G
        results.N = N
        results.t_star = t_star
        results.i_star = ibest
        results.counts = counts_array
        results.tollerance = tollerance
        results.resolution = resolution
        results.points = points
        maxent_point = results.map_curve.get_maxent_point()
        results.M = maxent_point.Q / np.sum(maxent_point.Q)
        results.num_pt_samples = num_pt_samples == 0 or num_pt_samples
        results.Q_samples = Q_samples
        results.phi_samples = phi_samples
        results.phi_weights = phi_weights
    return results