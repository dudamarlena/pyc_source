# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/sella/internal.py
# Compiled at: 2020-01-27 12:43:28
# Size of source mod 2**32: 12139 bytes
from __future__ import division
import warnings, numpy as np
from scipy.optimize import minimize
from .internal_cython import get_internal, cart_to_internal
from ase.data import covalent_radii, vdw_radii

class Internal(object):

    def __init__(self, atoms, angles=False, dihedrals=False, extra_bonds=None):
        self.extra_bonds = []
        if extra_bonds is not None:
            self.extra_bonds = extra_bonds
        self.use_angles = angles
        self.use_dihedrals = dihedrals
        self._mask = None
        self.atoms = atoms
        self._pos_old = np.zeros_like(self.atoms.get_positions())
        self.path = None
        self.v0 = None
        self.v1 = None

    def get_internal(self):
        self.c10y, self.nbonds, self.bonds, self.angles, self.dihedrals = get_internal(self._atoms, self.use_angles, self.use_dihedrals, self.extra_bonds)
        self.nb = len(self.bonds)
        if self.use_angles:
            self.na = len(self.angles)
        else:
            self.na = 0
        if self.use_dihedrals:
            self.nd = len(self.dihedrals)
        else:
            self.nd = 0
        self.ninternal = self.nb + self.na + self.nd
        self._mask = np.ones((self.ninternal), dtype=(np.uint8))
        self._p = None
        self._B = None
        self._D = None

    @property
    def atoms(self):
        return self._atoms

    @atoms.setter
    def atoms(self, new_atoms):
        self._atoms = new_atoms.copy()
        self.natoms = len(self._atoms)
        self.get_internal()
        for ind0 in range(self.natoms):
            ind1 = min(self.c10y[ind0, :self.nbonds[ind0]])
            tmp = set(self.c10y[ind1, :self.nbonds[ind1]])
            tmp.discard(ind0)
            if tmp:
                ind2 = min(tmp)
                break

    def _calc_internal(self, gradient=False, curvature=False):
        mask = np.ones((self.ninternal), dtype=(np.uint8))
        self._p, _, _ = cart_to_internal(self.atoms.positions, self.bonds, self.angles, self.dihedrals, mask)
        added = True
        while added:
            added = False
            for i, thetai in enumerate(self._p[self.nb:self.nb + self.na]):
                if np.pi - thetai < np.pi / 20:
                    a, b, c = self.angles[i]
                    for j, k in self.bonds:
                        if j == a:
                            if k == c:
                                break
                    else:
                        self.extra_bonds.append(tuple(sorted((a, c))))
                        added = True

            if added:
                self.get_internal()
                self._p, _, _ = cart_to_internal(self.atoms.positions, self.bonds, self.angles, self.dihedrals, self._mask)

        collinear = []
        self._mask = np.ones((self.ninternal), dtype=(np.uint8))
        for i, thetai in enumerate(self._p[self.nb:self.nb + self.na]):
            if np.pi - thetai < np.pi / 20:
                collinear.append(i)

        for i, di in enumerate(self.dihedrals):
            for j in collinear:
                a, b, c = self.angles[j]
                if a in di and b in di and c in di:
                    self._mask[self.nb + self.na + i] = False
                    break

        self._p, self._B, self._D = cart_to_internal(self.atoms.positions, self.bonds, self.angles, self.dihedrals, self._mask, gradient, curvature)
        self._pos_old = self.atoms.positions.copy()

    @property
    def p(self):
        if self._p is not None:
            if np.all(self.atoms.positions == self._pos_old):
                return self._p
        self._calc_internal()
        self._B = None
        self._D = None
        return self._p

    @p.setter
    def p(self, target):
        nba = self.nb + self.na
        dp = target - self.p
        dp[nba:] = (dp[nba:] + np.pi) % (2 * np.pi) - np.pi
        lvecs, lams, rvecs = np.linalg.svd((self.B), full_matrices=False)
        indices = [i for i, lam in enumerate(lams) if abs(lam) > 1e-12]
        dx = rvecs[indices, :].T @ (lvecs[:, indices].T @ dp / lams[indices])
        self.v0 = dx.copy()
        dxnorm = np.linalg.norm(dx)
        dx_max = 0.001
        if dxnorm <= dx_max:
            self.path = [
             self.atoms.get_positions().copy()]
            self.atoms.positions += dx.reshape((-1, 3))
            self.path.append(self.atoms.get_positions().copy())
            self.v1 = dx.copy()
            return
        nsteps = int(np.ceil(dxnorm / dx_max))
        dt = dxnorm / nsteps
        v = dx / dxnorm
        a = -rvecs[indices, :].T @ (lvecs[:, indices].T @ self.D.ddot(v, v) / lams[indices])
        self.path = [self.atoms.get_positions().copy()]
        nscf = 100
        ndiis = 5
        viter = np.zeros((len(dx), nscf))
        errors = np.zeros((len(dx), nscf))
        p = self.p.copy()
        for _ in range(nsteps):
            vhalf = v + a * dt / 2
            self.atoms.positions += (vhalf * dt).reshape((-1, 3))
            D = self.D
            self.path.append(self.atoms.get_positions().copy())
            v = vhalf.copy()
            lvecs, lams, rvecs = np.linalg.svd((self.B), full_matrices=False)
            indices = [i for i, lam in enumerate(lams) if abs(lam) > 1e-12]
            for i in range(nscf):
                vlast = v.copy()
                viter[:, i] = v
                a = -rvecs[indices, :].T @ (lvecs[:, indices].T @ self.D.ddot(v, v) / lams[indices])
                errors[:, i] = vhalf + a * dt / 2 - v
                if i <= 1:
                    v = vhalf + a * dt / 2
                    continue
                nhist = min(i + 1, ndiis)
                A = np.ones((nhist + 1, nhist + 1))
                A[:nhist, :nhist] = errors[:, i + 1 - nhist:i + 1].T @ errors[:, i + 1 - nhist:i + 1]
                A[(-1, -1)] = 0
                rhs = np.zeros(nhist + 1)
                rhs[-1] = 1
                cs = np.linalg.lstsq(A, rhs, rcond=None)[0]
                v = viter[:, i + 1 - nhist:i + 1] @ cs[:nhist]
                if np.linalg.norm(v - vlast) < 1e-12:
                    break
            else:
                print(np.linalg.norm(v - vlast))
                raise RuntimeError('Failed to converge Coriolis forces')

        self.v1 = dxnorm * v.copy()

    def xpolate(self, alpha):
        """Interpolate/extrapolate most recent trajectory"""
        if self.path is None:
            raise RuntimeError('No path to interpolate/extrapolate!')
        else:
            if alpha < 0:
                self.atoms.positions = self.path[0]
                self.p = self.p + alpha * self.B @ self.v0
            else:
                if 0 < alpha < 1:
                    nsteps = len(self.path) - 1
                    beta = alpha * nsteps
                    idx = int(beta)
                    beta -= idx
                    self.atoms.positions = self.path[(idx + 1)] * beta + self.path[idx] * (1 - beta)
                else:
                    self.atoms.positions = self.path[(-1)]
                    self.p = self.p + (1 - alpha) * self.B @ self.v1
        return self.p

    @property
    def B(self):
        if self._B is not None:
            if np.all(self.atoms.positions == self._pos_old):
                return self._B
        self._calc_internal(gradient=True)
        self._D = None
        return self._B

    @property
    def D(self):
        if self._D is not None:
            if np.all(self.atoms.positions == self._pos_old):
                return self._D
        self._calc_internal(gradient=True, curvature=True)
        return self._D

    def guess_hessian(self, g0):
        D = self.D
        B = self.B
        rcov = np.zeros(len(self.atoms))
        for i, atom in enumerate(self.atoms):
            rcov[i] = covalent_radii[atom.number]

        rho = {}
        for i, (a, b) in enumerate(self.bonds):
            rho[tuple(sorted((a, b)))] = np.exp(-self.atoms.get_distance(a, b) / (rcov[a] + rcov[b]) + 1.0)

        H0 = np.zeros(self.nb + self.na + self.nd)
        n = 0
        start = 0
        for i, (a, b) in enumerate(self.bonds):
            if not self._mask[i]:
                pass
            else:
                H0[n] = 45 * rho[tuple(sorted((a, b)))]
                n += 1

        start += self.nb
        for i, (a, b, c) in enumerate(self.angles):
            if not self._mask[(start + i)]:
                continue
            rhoab = rho[tuple(sorted((a, b)))]
            rhobc = rho[tuple(sorted((b, c)))]
            H0[n] = 4 * rhoab * rhobc
            n += 1

        start += self.na
        for i, (a, b, c, d) in enumerate(self.dihedrals):
            if not self._mask[(start + i)]:
                pass
            else:
                rhoab = rho[tuple(sorted((a, b)))]
                rhobc = rho[tuple(sorted((b, c)))]
                rhocd = rho[tuple(sorted((c, d)))]
                H0[n] = 0.15 * rhoab * rhobc * rhocd
                n += 1

        H = np.diag(H0[:n])
        lvecs, lams, rvecs = np.linalg.svd(B, full_matrices=False)
        indices = [i for i, lam in enumerate(lams) if abs(lam) > 1e-12]
        Binv = rvecs[indices, :].T @ (lvecs[:, indices].T / lams[(indices, np.newaxis)])
        Hcart = B.T @ H @ B + D.ldot(Binv.T @ g0)
        return Hcart