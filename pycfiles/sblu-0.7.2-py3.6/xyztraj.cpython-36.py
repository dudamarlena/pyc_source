# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/xyztraj.py
# Compiled at: 2019-04-09 13:30:31
# Size of source mod 2**32: 2840 bytes
from typing import Iterator, List
import numpy as np

def _rot_matrix_from_quaternion(q: np.ndarray) -> np.ndarray:
    """Create rotation matrix from quaternion"""
    assert q.shape == (4, )
    m = np.zeros((3, 3), dtype=(np.float))
    r, i, j, k = q
    m[(0, 0)] = 1 - 2 * (j ** 2 + k ** 2)
    m[(1, 1)] = 1 - 2 * (i ** 2 + k ** 2)
    m[(2, 2)] = 1 - 2 * (i ** 2 + j ** 2)
    m[(0, 1)] = 2 * (i * j - k * r)
    m[(0, 2)] = 2 * (i * k + j * r)
    m[(1, 0)] = 2 * (i * j + k * r)
    m[(1, 2)] = 2 * (j * k - i * r)
    m[(2, 0)] = 2 * (i * k - j * r)
    m[(2, 1)] = 2 * (j * k + i * r)
    return m


class XYZParticle:
    __doc__ = '\n    A class presenting single particle from rigid-body XYZ trajectory.\n\n    Parameters\n    ----------\n    line : str\n        The line from XYZ file to parse.\n\n    Attributes\n    ----------\n    type_ : int\n        Particle type.\n    t : np.ndarray\n        Translation vector, array of shape (3,).\n    q : np.ndarray\n        Rotation quaternion, in order (w, x, y, z), array of shape (4,).\n    '

    def __init__(self, line: str):
        tokens = line.split()
        self.type_ = int(tokens[0])
        tokens_f = [float(i) for i in tokens[1:]]
        assert len(tokens_f) == 7
        self.t = np.array(tokens_f[:3])
        self.q = np.array(tokens_f[3:])

    @property
    def r(self) -> np.ndarray:
        """Rotation matrix (computed)"""
        return _rot_matrix_from_quaternion(self.q)


class XYZFrame:
    __doc__ = '\n    A class presenting single frame from rigid-body XYZ trajectory.\n\n    Parameters\n    ----------\n    comment : str\n        The comment from XYZ file.\n    particles : list of XYZParticle\n        The list of particles in this frame.\n    '

    def __init__(self, comment: str, particles: List[XYZParticle]):
        self.comment = comment
        self.particles = particles


def _non_empty(x: str) -> bool:
    """Return True iff `x` contains any printable characters."""
    return len(x.strip()) > 0


def xyz_stream(file_stream: Iterator[str]) -> Iterator[XYZFrame]:
    """Iterate over frames in XYZ rigid-body file.

    Parameters
    ----------
    file_stream : iterator yielding strings
        Any way to iterate over lines of XYZ rigid-body file.

    Yields
    ------
    XYZFrame
        Single XYZ trajectory frame.

    Examples
    --------
    >>> with open('trajectory.xyz') as f_traj:
    >>>    for frame_id, frame in enumerate(xyz_stream(f_traj)):
    >>>        print('Frame #{} has {} particles.'.format(frame_id, len(frame.particles)))
    """
    lines_good = filter(_non_empty, file_stream)
    for line in lines_good:
        num_particles = int(line)
        comment = next(lines_good).strip()
        particles = [XYZParticle(next(lines_good)) for _ in range(num_particles)]
        yield XYZFrame(comment=comment, particles=particles)