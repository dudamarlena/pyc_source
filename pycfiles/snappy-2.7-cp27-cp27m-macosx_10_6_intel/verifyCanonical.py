# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/verify/verifyCanonical.py
# Compiled at: 2019-07-15 23:56:54
from __future__ import print_function
from ..sage_helper import _within_sage, sage_method
from .cuspCrossSection import RealCuspCrossSection
from .squareExtensions import find_shapes_as_complex_sqrt_lin_combinations
from . import verifyHyperbolicity
from . import exceptions
from ..exceptions import SnapPeaFatalError
from ..snap import t3mlite as t3m
if _within_sage:
    from sage.rings.real_mpfi import RealIntervalField
    from sage.rings.complex_interval_field import ComplexIntervalField
    from ..pari import prec_dec_to_bits, prec_bits_to_dec
__all__ = ['FindExactShapesError',
 'interval_checked_canonical_triangulation',
 'exactly_checked_canonical_retriangulation',
 'verified_canonical_retriangulation',
 'default_interval_bits_precs',
 'default_exact_bits_prec_and_degrees']
default_interval_bits_precs = [
 53, 212]
default_exact_bits_prec_and_degrees = [(212, 10),
 (1000, 20),
 (2000, 20)]
_num_tries_canonize = 3
_max_tries_verify_penalty = 9

class FindExactShapesError(RuntimeError):
    """
    Raised when snap failed to find the exact shapes using the LLL-algorithm
    for a manifold.
    """
    pass


@sage_method
def interval_checked_canonical_triangulation(M, bits_prec=None):
    """
    Given a canonical triangulation of a cusped (possibly non-orientable)
    manifold M, return this triangulation if it has tetrahedral cells and can
    be verified using interval arithmetics with the optional, given precision.
    Otherwise, raises an Exception.
    
    It fails when we call it on something which is not the canonical
    triangulation::

       sage: from snappy import Manifold
       sage: M = Manifold("m015")
       sage: interval_checked_canonical_triangulation(M) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
       Traceback (most recent call last):
       ...
       TiltProvenPositiveNumericalVerifyError: Numerical verification that tilt is negative has failed, tilt is actually positive. This is provably not the proto-canonical triangulation: 0.164542163...? <= 0

    It verifies the canonical triangulation::

       sage: M.canonize()
       sage: K = interval_checked_canonical_triangulation(M)
       sage: K
       m015(0,0)

    Has a non-tetrahedral canonical cell::

      sage: M = Manifold("m137")
      sage: M.canonize()
      sage: interval_checked_canonical_triangulation(M) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
      ...
      TiltInequalityNumericalVerifyError: Numerical verification that tilt is negative has failed: 0.?e-1... < 0
    
    Has a cubical canonical cell::

       sage: M = Manifold("m412")
       sage: M.canonize()
       sage: interval_checked_canonical_triangulation(M) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
       Traceback (most recent call last):
       ...
       TiltInequalityNumericalVerifyError: Numerical verification that tilt is negative has failed: 0.?e-1... < 0
    
    """
    shapes = M.tetrahedra_shapes('rect', intervals=True, bits_prec=bits_prec)
    c = RealCuspCrossSection.fromManifoldAndShapes(M, shapes)
    verifyHyperbolicity.check_logarithmic_gluing_equations_and_positively_oriented_tets(M, shapes)
    if M.num_cusps() > 1:
        c.normalize_cusps()
    c.compute_tilts()
    for face in c.mcomplex.Faces:
        if face.Tilt > 0:
            raise exceptions.TiltProvenPositiveNumericalVerifyError(face.Tilt)
        if not face.Tilt < 0:
            raise exceptions.TiltInequalityNumericalVerifyError(face.Tilt)

    return M


@sage_method
def exactly_checked_canonical_retriangulation(M, bits_prec, degree):
    """
    Given a proto-canonical triangulation of a cusped (possibly non-orientable)
    manifold M, return its canonical retriangulation which is computed from
    exact shapes. The exact shapes are computed using snap (which uses the
    LLL-algorithm). The precision (in bits) and the maximal degree need to be
    specified (here 300 bits precision and polynomials of degree less than 4)::

       sage: from snappy import Manifold
       sage: M = Manifold("m412")
       sage: M.canonize()
       sage: K = exactly_checked_canonical_retriangulation(M, 300, 4)

    M's canonical cell decomposition has a cube, so non-tetrahedral::
    
       sage: K.has_finite_vertices()
       True

    Has 12 tetrahedra after the retrianglation::
    
      sage: K.num_tetrahedra()
      12

    Check that it fails on something which is not a proto-canonical
    triangulation::

      sage: from snappy import Manifold
      sage: M = Manifold("m015")
      sage: exactly_checked_canonical_retriangulation(M, 500, 6)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
      ...
      TiltProvenPositiveNumericalVerifyError: Numerical verification that tilt is negative has failed, tilt is actually positive. This is provably not the proto-canonical triangulation: 0.1645421638874662848910671879? <= 0
    """
    dec_prec = prec_bits_to_dec(bits_prec)
    shapes = find_shapes_as_complex_sqrt_lin_combinations(M, dec_prec, degree)
    if not shapes:
        raise FindExactShapesError()
    c = RealCuspCrossSection.fromManifoldAndShapes(M, shapes)
    c.check_polynomial_edge_equations_exactly()
    c.check_cusp_development_exactly()
    CIF = ComplexIntervalField(bits_prec)
    c.check_logarithmic_edge_equations_and_positivity(CIF)
    if M.num_cusps() > 1:
        c.normalize_cusps()
    c.compute_tilts()

    def get_opacity(tilt):
        sign, interval = tilt.sign_with_interval()
        if sign < 0:
            return True
        if sign == 0:
            return False
        if sign > 0:
            raise exceptions.TiltProvenPositiveNumericalVerifyError(interval)

    def index_of_face_corner(corner):
        face_index = t3m.simplex.comp(corner.Subsimplex).bit_length() - 1
        return 4 * corner.Tetrahedron.Index + face_index

    opacities = 4 * len(c.mcomplex.Tetrahedra) * [None]
    for face in c.mcomplex.Faces:
        opacity = get_opacity(face.Tilt)
        for corner in face.Corners:
            opacities[index_of_face_corner(corner)] = opacity

    if None in opacities:
        raise Exception('Mismatch with opacities')
    if False in opacities:
        return M._canonical_retriangulation(opacities)
    else:
        return M


def _retrying_canonize(M):
    """
    Wrapper for SnapPea kernel's function to compute the proto-canonical
    triangulation in place. It will retry the kernel function if it fails.
    Returns True if and only if the kernel function was successful eventually.
    """
    for i in range(_num_tries_canonize):
        try:
            M.canonize()
            return True
        except (RuntimeError, SnapPeaFatalError):
            M.randomize()

    return False


def _retrying_high_precision_canonize(M):
    """
    Wrapper for SnapPea kernel's function to compute the proto-canonical
    triangulation. It will retry the kernel function if it fails, switching
    to the quad-double implementation.
    Returns the proto-canonical triangulation if the kernel function was
    successful eventually. Otherwise None. The original manifold is unchanged.
    """
    Mcopy = M.copy()
    if _retrying_canonize(Mcopy):
        return Mcopy
    else:
        Mhp = M.high_precision()
        if _retrying_canonize(Mhp):
            return Mhp
        return


def _print_exception(e):
    print('%s: %s' % (type(e).__name__, e))


@sage_method
def verified_canonical_retriangulation(M, interval_bits_precs=default_interval_bits_precs, exact_bits_prec_and_degrees=default_exact_bits_prec_and_degrees, verbose=False):
    """
    Given some triangulation of a cusped (possibly non-orientable) manifold ``M``,
    return its canonical retriangulation. Return ``None`` if it could not certify
    the result.

    To compute the canonical retriangulation, it first prepares the manifold 
    (filling all Dehn-filled cusps and trying to find a proto-canonical
    triangulation).
    It then tries to certify the canonical triangulation using interval
    arithmetics. If this fails, it uses snap (using `LLL-algorithm 
    <http://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm>`_)
    to guess
    exact representations of the shapes in the shape field and then certifies
    that it found the proto-canonical triangulation and determines the
    transparent faces to construct the canonical retriangulation.

    The optional arguments are:

    - ``interval_bits_precs``:
      a list of precisions used to try to
      certify the canonical triangulation using intervals. By default, it
      first tries to certify using 53 bits precision. If it failed, it tries
      212 bits precision next. If it failed again, it moves on to trying exact
      arithmetics.

    - ``exact_bits_prec_and_degrees``:
      a list of pairs (precision, maximal degree) used when the LLL-algorithm
      is trying to find the defining polynomial of the shape field.
      Similar to ``interval_bits_precs``, each pair is tried until we succeed.

    - ``verbose``:
      If ``True``, print out additional information.

    The exact arithmetics can take a long time. To circumvent it, use
    ``exact_bits_prec_and_degrees = None``.

    More information on the canonical retriangulation can be found in the
    SnapPea kernel ``canonize_part_2.c`` and in Section 3.1 of 
    `Fominykh, Garoufalidis, Goerner, Tarkaev, Vesnin <http://arxiv.org/abs/1502.00383>`_.

    Canonical cell decompostion of ``m004`` has 2 tetrahedral cells::

       sage: from snappy import Manifold
       sage: M = Manifold("m004")
       sage: K = verified_canonical_retriangulation(M)
       sage: K.has_finite_vertices()
       False
       sage: K.num_tetrahedra()
       2

    Canonical cell decomposition of ``m137`` is not tetrahedral::

       sage: M = Manifold("m137")
       sage: K = verified_canonical_retriangulation(M)
       sage: K.has_finite_vertices()
       True
       sage: K.num_tetrahedra()
       18
    
    Canonical cell decomposition of ``m412`` is a cube and has exactly 8
    symmetries::

       sage: M = Manifold("m412")
       sage: K = verified_canonical_retriangulation(M)
       sage: K.has_finite_vertices()
       True
       sage: K.num_tetrahedra()
       12
       sage: len(K.isomorphisms_to(K))
       8

    `Burton's example <http://arxiv.org/abs/1311.7615>`_ of ``x101`` and ``x103`` which are actually isometric but
    SnapPea fails to show so. We certify the canonical retriangulation and
    find them isomorphic::

       sage: M = Manifold('x101'); K = verified_canonical_retriangulation(M)
       sage: N = Manifold('x103'); L = verified_canonical_retriangulation(N)
       sage: len(K.isomorphisms_to(L)) > 0
       True

    Avoid potentially expensive exact arithmetics (return ``None`` because it has
    non-tetrahedral cells so interval arithmetics can't certify it)::

       sage: M = Manifold("m412")
       sage: verified_canonical_retriangulation(M, exact_bits_prec_and_degrees = None)
    """
    tries_penalty_left = _max_tries_verify_penalty
    while tries_penalty_left > 0:
        try:
            return _verified_canonical_retriangulation(M, interval_bits_precs, exact_bits_prec_and_degrees, verbose)
        except (ZeroDivisionError,
         exceptions.TiltProvenPositiveNumericalVerifyError,
         exceptions.EdgeEquationExactVerifyError) as e:
            if verbose:
                _print_exception(e)
                print("Failure: In verification of result of SnapPea kernel's proto_canonize", end='')
                if isinstance(e, ZeroDivisionError):
                    print(' probably due to flat tetrahedra.')
                if isinstance(e, exceptions.TiltProvenPositiveNumericalVerifyError):
                    print(' due to provably positive tilts.')
                if isinstance(e, exceptions.EdgeEquationExactVerifyError):
                    print(' probably due to snap giving wrong number field.')
                print('Next step: Retrying with randomized triangulation.')
            M = M.copy()
            M.randomize()
            if isinstance(e, ZeroDivisionError):
                tries_penalty_left -= 1
            else:
                tries_penalty_left -= 3
        except exceptions.VerifyErrorBase as e:
            if verbose:
                _print_exception(e)
                print("Failure: In verification of result of SnapPea kernel's proto_canonize.")
                print('Next step: Give up.')
            return

    return


def _verified_canonical_retriangulation(M, interval_bits_precs, exact_bits_prec_and_degrees, verbose):
    num_complete_cusps = 0
    num_incomplete_cusps = 0
    for cusp_info in M.cusp_info():
        if cusp_info['complete?']:
            num_complete_cusps += 1
        else:
            num_incomplete_cusps += 1

    if not num_complete_cusps:
        if verbose:
            print('Failure: Due to no unfilled cusp.')
            print('Next step: Give up.')
        return
    if num_incomplete_cusps:
        Mfilled = M.filled_triangulation()
    else:
        Mfilled = M
    Mcopy = _retrying_high_precision_canonize(Mfilled)
    if not Mcopy:
        if verbose:
            print("Failure: In SnapPea kernel's proto_canonize()")
            print('Next step: Give up.')
        return
    if interval_bits_precs:
        for interval_bits_prec in interval_bits_precs:
            if verbose:
                print('Method: Intervals with interval_bits_prec = %d' % interval_bits_prec)
            try:
                return interval_checked_canonical_triangulation(Mcopy, interval_bits_prec)
            except (RuntimeError, exceptions.NumericalVerifyError) as e:
                if verbose:
                    _print_exception(e)
                    if isinstance(e, exceptions.NumericalVerifyError):
                        print('Failure: Could not verify proto-canonical triangulation.')
                    else:
                        print('Failure: Could not find verified interval.')
                    print('Next step: trying different method/precision.')

    if exact_bits_prec_and_degrees:
        for bits_prec, degree in exact_bits_prec_and_degrees:
            if verbose:
                print('Method: Exact, using LLL with bits_prec = %d, degree = %d' % (
                 bits_prec, degree))
            try:
                return exactly_checked_canonical_retriangulation(Mcopy, bits_prec, degree)
            except FindExactShapesError as e:
                if verbose:
                    _print_exception(e)
                    print('Failure: Could not find exact shapes.')
                    print('Next step: trying different method/precision')

    return


_known_canonical_retriangulations = [
 ('m004', b'\x02\x0e\x01\x01\x01-\x1b\x87'),
 ('m412', b'\x0c\x80\xac\xff\x07\x05\x07\t\n\t\x08\t\n\x0b\x0b\n\x0b\xe4\xe4\xe4\xe4\xe4\xe1\xe1\xe1\xe1\xe1\xe1\xe1\xe1'),
 ('m137', b'\x12\x00\xb0\xfa\xaf\x0f\x04\t\x0b\x08\x07\x07\n\x0c\x0e\r\n\x0f\x0f\r\x11\x11\x10\x10\x11\xb4\xe4\xe1\xe1\xe1\xb4\xe1\xe1\xb1\xe1\xb4\xe4\xe4\xe1\xb1\xe1\xe1\xb4\xe1')]

def _test_against_known_canonical_retriangulations():
    from snappy import Manifold
    for name, bytes_ in _known_canonical_retriangulations:
        M = Manifold(name)
        K = verified_canonical_retriangulation(M)
        L = Manifold('empty')
        L._from_bytes(bytes_)
        if not len(K.isomorphisms_to(L)):
            raise Exception('%s failed' % name)