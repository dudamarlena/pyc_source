# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gentex/template.py
# Compiled at: 2019-10-04 13:17:54
# Size of source mod 2**32: 23620 bytes
import numpy as np

class Template:
    __doc__ = "Class template for generating lists of template voxels\n\n    Parameters\n    ----------\n\n    type: string\n        Required by constructor. The type of template currently available types are:\n\n            - 'RectBox' - rectangular box (1,2,3,4 dimensions) template origin is center of box\n\n            - 'RectShell' - shell of rectangular box (1,2,3,4 dimensions) template origin is center of shell\n\n            - 'Ellipsoid' - ellispoid (1,2,3,4 dimensions) template origin is center of ellipsoid\n\n            - 'EllipsoidShell' - ellipsoidal shell (1,2,3,4 dimensions) template origin is center of shell\n\n            - 'Line' - linear template template origin is first point of line\n\n            - 'Notch' - notch template template origin is point about which notch is built\n\n            - 'Cone' - cone template template origin is start of half cone\n\n    sizes:  1D int array (can be empty)\n        Attributes of sizes required for constructing template\n\n    dimension: int\n        Dimension of template\n\n    inculsion: bool\n        Whether or not to include anchor point (i.e. [0], [0,0],...)\n\n    handedness: 1D int array\n        If there are axial asymetries in the template (e.g. Notch) can pass in a vector with +1 for 'right' and -1\n        for 'left' (default is [1], or [1,1], or...)\n\n    axbase: List of ints (each list of length = dimension)\n        Basis vector specifying axis, when appropriate, for direction of template (can be empty) - component lengths\n        will be ignored; only whether the component is zero or nonzero, and the sign will be\n        considered (i.e. only co-ordinate axes and '45 degree' lines will be considered as template axes), so e.g::\n\n            [1,0] ~ [10,0] ~ x-axis in 2D\n            [0,1,0] ~ [0,33,0] ~ y-axis in 3D\n            [1,-1] ~ [30,-20] ~ [108,-1] ~ 135 degree axis in 2\n\n        if axbase is empty template will pick axes according to following conventions:\n\n            - templates requiring single axis specification (e.g. line, notch, cone) will always use positivedirection of first dimension\n\n            - templates requiring multiple axis specification, e.g. rectangular parallelipipeds and ellipsoids will choose:\n\n                - largest dimension (e.g. semi-major axis) in positive direction of first dimension\n\n                - next largest dimension (e.g. semi-minor axis) in positive direction of second dimension\n\n                - etc.\n\n    anchoff: list of ints\n        Offset of anchor point from template [0,0,0] in template (usually assume [0,0,0])\n\n    shift: List of int\n        List of ints to use if you\n        want to shift all points in offset array - useful, e.g.\n        if you want to build cooccurence arrays from offset\n        templates - build one template (set of offsets with no shift\n        and another with an appropriate shift; those can each be passed\n        to the feature space cluster algorithm, then those\n        to the cooccurence matrix builder, and that to the texture\n        measure generator.\n    "

    def __init__(self, type, sizes, dimension, inclusion, handedness=None, axbase=None, anchoff=None, shift=None):
        self.type = type
        self.sizes = sizes
        self.dim = dimension
        self.me = inclusion
        self.handedness = handedness
        self.offsets = []
        self.axbase = axbase
        self.anchoff = anchoff
        self.shift = shift
        if self.handedness is None:
            if self.dim == 1:
                self.handedness = [
                 1]
            if self.dim == 2:
                self.handedness = [
                 1, 1]
            if self.dim == 3:
                self.handedness = [
                 1, 1, 1]
            if self.dim == 4:
                self.handedness = [
                 1, 1, 1, 1]
        if self.axbase is None:
            if self.dim == 1:
                self.axbase = [
                 1]
            if self.dim == 2:
                self.axbase = [
                 1, 0]
            if self.dim == 3:
                self.axbase = [
                 1, 0, 0]
            if self.dim == 4:
                self.axbase = [
                 1, 0, 0, 0]
        if self.anchoff is None:
            if self.dim == 1:
                self.anchoff = [
                 0]
            if self.dim == 2:
                self.anchoff = [
                 0, 0]
            if self.dim == 3:
                self.anchoff = [
                 0, 0, 0]
            if self.dim == 4:
                self.anchoff = [
                 0, 0, 0, 0]
        if self.shift is None:
            if self.dim == 1:
                self.shift = [
                 0]
            if self.dim == 2:
                self.shift = [
                 0, 0]
            if self.dim == 3:
                self.shift = [
                 0, 0, 0]
            if self.dim == 4:
                self.shift = [
                 0, 0, 0, 0]
            if type == 'RectBox':
                if len(self.sizes) != self.dim:
                    print(f"sizes array is of length {len(self.sizes)} but must be of length {self.dim} for type {type}")
                else:
                    lims = np.zeros((self.dim, 2), int)
                    for i in range(self.dim):
                        lims[(i, 0)] = -(self.sizes[0] / 2)
                        if self.sizes[0] % 2 == 0:
                            lims[(i, 1)] = self.sizes[0] / 2
                        else:
                            lims[(i, 1)] = self.sizes[0] / 2 + 1

                    if self.dim == 1:
                        for i in range(lims[(0, 0)], lims[(0, 1)]):
                            self.offsets.append([i])

                        if [
                         0] in self.offsets:
                            self.offsets.remove([0])
                    if self.dim == 2:
                        for i in range(lims[(0, 0)], lims[(0, 1)]):
                            for j in range(lims[(1, 0)], lims[(1, 1)]):
                                self.offsets.append([i, j])

                        if [
                         0, 0] in self.offsets:
                            self.offsets.remove([0, 0])
                    if self.dim == 3:
                        for i in range(lims[(0, 0)], lims[(0, 1)]):
                            for j in range(lims[(1, 0)], lims[(1, 1)]):
                                for k in range(lims[(2, 0)], lims[(2, 1)]):
                                    self.offsets.append([i, j, k])

                        if [
                         0, 0, 0] in self.offsets:
                            self.offsets.remove([0, 0, 0])
                if self.dim == 4:
                    for i in range(lims[(0, 0)], lims[(0, 1)]):
                        for j in range(lims[(1, 0)], lims[(1, 1)]):
                            for k in range(lims[(2, 0)], lims[(2, 1)]):
                                for t in range(lims[(3, 0)], lims[(3, 1)]):
                                    self.offsets.append([i, j, k, t])

                    if [
                     0, 0, 0, 0] in self.offsets:
                        self.offsets.remove([0, 0, 0, 0])
        elif type == 'RectShell':
            if len(self.sizes) != self.dim:
                print(f"sizes array is of length {len(self.sizes)} but must be of length {self.dim} for type {type}")
            if self.dim == 1:
                sub = self.sizes[0] / 2
                for i in range(self.sizes[0]):
                    if not i == 0:
                        if i == self.sizes[0] - 1:
                            pass
                        self.offsets.append([i - sub])

            if self.dim == 2:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        if not (i == 0 or i == self.sizes[0] - 1 or j == 0):
                            if j == self.sizes[1] - 1:
                                pass
                            self.offsets.append([i - sub0, j - sub1])

            if self.dim == 3:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            if not (i == 0 or i == self.sizes[0] - 1 or j == 0 or j == self.sizes[1] - 1 or k == 0):
                                if k == self.sizes[2] - 1:
                                    pass
                                self.offsets.append([i - sub0, j - sub1, k - sub2])

            if self.dim == 4:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                sub3 = self.sizes[3] / 2
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            for t in range(self.sizes[3]):
                                if not (i == 0 or i == self.sizes[0] - 1 or j == 0 or j == self.sizes[1] - 1 or k == 0 or k == self.sizes[2] - 1 or t == 0):
                                    if t == self.sizes[3] - 1:
                                        pass
                                    self.offsets.append([i - sub0, j - sub1, k - sub2, t - sub3])

        elif type == 'Ellipsoid':
            if len(self.sizes) != self.dim:
                print(f"sizes array is of length {len(self.sizes)} but must be of length {self.dim} for type {type}")
            if self.dim == 1:
                sub = self.sizes[0] / 2
                for i in range(self.sizes[0]):
                    self.offsets.append([i - sub])

            if self.dim == 2:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        bounder = (i - sub0) * (i - sub0) / s02 + (j - sub1) * (j - sub1) / s12
                        if bounder <= 1.0:
                            self.offsets.append([i - sub0, j - sub1])

            if self.dim == 3:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                s22 = self.sizes[2] * self.sizes[2]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            bounder = (i - sub0) * (i - sub0) / s02 + (j - sub1) * (j - sub1) / s12 + (k - sub2) * (k - sub2) / s22
                            if bounder <= 1.0:
                                self.offsets.append([i - sub0, j - sub1, k - sub2])

            if self.dim == 4:
                print
        elif type == 'EllipsoidShell':
            if len(self.sizes) != self.dim:
                print(f"sizes array is of length {len(self.sizes)} but must be of length {self.dim} for type {type}")
            if self.dim == 1:
                sub = self.sizes[0] / 2
                for i in range(self.sizes[0]):
                    if not i == 0:
                        if i == self.sizes[0] - 1:
                            pass
                        self.offsets.append([i - sub])

            if self.dim == 2:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        bounder = (i - sub0) * (i - sub0) / s02 + (j - sub1) * (j - sub1) / s12
                        if bounder > 0.9 and bounder < 1.1:
                            self.offsets.append([i - sub0, j - sub1])

            if self.dim == 3:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                s22 = self.sizes[2] * self.sizes[2]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            bounder = (i - sub0) * (i - sub0) / s02 + (j - sub1) * (j - sub1) / s12 + (k - sub2) * (k - sub2) / s22
                            if bounder > 0.9 and bounder < 1.1:
                                self.offsets.append([i - sub0, j - sub1, k - sub2])

            if self.dim == 4:
                print('Sorry 4D ellipsoidal shells not yet implemented')
        elif type == 'Line':
            if len(self.sizes) != 1:
                print(f"sizes array is of length {len(self.sizes)} but must be of length {self.dim} for type {type}")
            proto = np.sign(self.axbase)
            for i in range(1, self.sizes[0] + 1):
                self.offsets.append(list(i * proto))

        else:
            if type == 'Notch':
                if len(self.sizes) != 1:
                    print(f"sizes array is of length {len(self.sizes)} but must be of length {self.dim} for type {type}")
                else:
                    proto = list(np.sign(self.axbase))
                    if self.dim == 1:
                        print
                    if self.dim == 2:
                        protoset = [
                         [
                          1, 0], [-1, 0], [0, 1], [0, -1]]
                        if proto not in protoset:
                            proto = [
                             1, 0]
                        if proto == [1, 0]:
                            for i in range(self.sizes[0] + 1):
                                for j in range(-self.sizes[0], self.sizes[0] + 1):
                                    if not i > 0:
                                        if j <= 0:
                                            pass
                                        self.offsets.append([i, j])

                        if proto == [-1, 0]:
                            for i in range(-self.sizes[0], 1):
                                for j in range(-self.sizes[0], self.sizes[0] + 1):
                                    if not i < 0:
                                        if j <= 0:
                                            pass
                                        self.offsets.append([i, j])

                        if proto == [0, 1]:
                            for i in range(-self.sizes[0], self.sizes[0] + 1):
                                for j in range(self.sizes[0] + 1):
                                    if not j > 0:
                                        if i >= 0:
                                            pass
                                        self.offsets.append([i, j])

                        if proto == [0, -1]:
                            for i in range(-self.sizes[0], self.sizes[0] + 1):
                                for j in range(-self.sizes[0], 1):
                                    if not j < 0:
                                        if i >= 0:
                                            pass
                                        self.offsets.append([i, j])

                    if self.dim == 3:
                        protoset = [
                         [
                          1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
                        if proto not in protoset:
                            proto = [
                             1, 0, 0]
                        if proto == [1, 0, 0]:
                            for i in range(self.sizes[0] + 1):
                                for j in range(-self.sizes[0], self.sizes[0] + 1):
                                    for k in range(-self.sizes[0], self.sizes[0] + 1):
                                        if i > 0 or i >= 0 and j > 0 or j >= 0:
                                            if k > 0:
                                                pass
                                            self.offsets.append([i, j, k])

                        if proto == [-1, 0, 0]:
                            for i in range(-self.sizes[0], self.sizes[0]):
                                for j in range(-self.sizes[0], self.sizes[0] + 1):
                                    for k in range(-self.sizes[0], self.sizes[0] + 1):
                                        if i < 0 or i <= 0 and j < 0 or j <= 0:
                                            if k < 0:
                                                pass
                                            self.offsets.append([i, j, k])

                        if proto == [0, 1, 0]:
                            for j in range(self.sizes[0] + 1):
                                for k in range(-self.sizes[0], self.sizes[0] + 1):
                                    for i in range(-self.sizes[0], self.sizes[0] + 1):
                                        if j > 0 or j >= 0 and i > 0 or i >= 0:
                                            if k < 0:
                                                pass
                                            self.offsets.append([i, j, k])

                        if proto == [0, -1, 0]:
                            for j in range(-self.sizes[0], self.sizes[0]):
                                for k in range(-self.sizes[0], self.sizes[0] + 1):
                                    for i in range(-self.sizes[0], self.sizes[0] + 1):
                                        if j < 0 or j <= 0 and i > 0 or i >= 0:
                                            if k < 0:
                                                pass
                                            self.offsets.append([i, j, k])

                        if proto == [0, 0, 1]:
                            for k in range(self.sizes[0] + 1):
                                for i in range(-self.sizes[0], self.sizes[0] + 1):
                                    for j in range(-self.sizes[0], self.sizes[0] + 1):
                                        if k > 0 or k >= 0 and j < 0 or j <= 0:
                                            if i > 0:
                                                pass
                                            self.offsets.append([i, j, k])

                        if proto == [0, 0, -1]:
                            for k in range(-self.sizes[0], self.sizes[0]):
                                for i in range(-self.sizes[0], self.sizes[0] + 1):
                                    for j in range(-self.sizes[0], self.sizes[0] + 1):
                                        if k < 0 or k <= 0 and j > 0 or j >= 0:
                                            if i < 0:
                                                pass
                                            self.offsets.append([i, j, k])

                if self.dim == 4:
                    print
            elif type == 'Cone':
                if len(self.sizes) != 1:
                    print(f"sizes array is of length {len(self.sizes)} but must be of length {self.dim} for type {type}")
                else:
                    proto = list(np.sign(self.axbase))
                    if self.dim == 1:
                        for i in range(self.sizes[0]):
                            self.offsets.append([i])

                    if self.dim == 2:
                        protoset = [
                         [
                          1, 0], [-1, 0], [0, 1], [0, -1]]
                        if proto not in protoset:
                            proto = [
                             1, 0]
                        if proto == [1, 0]:
                            for i in range(self.sizes[0]):
                                for j in range(-i, i + 1):
                                    self.offsets.append([i, j])

                        if proto == [-1, 0]:
                            for i in range(self.sizes[0]):
                                for j in range(-i, i + 1):
                                    self.offsets.append([-i, j])

                        if proto == [0, 1]:
                            for j in range(self.sizes[0]):
                                for i in range(-j, j + 1):
                                    self.offsets.append([i, j])

                        if proto == [0, -1]:
                            for j in range(self.sizes[0]):
                                for i in range(-j, j + 1):
                                    self.offsets.append([i, -j])

                    if self.dim == 3:
                        protoset = [
                         [
                          1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
                        if proto not in protoset:
                            proto = [
                             1, 0, 0]
                        if proto == [1, 0, 0]:
                            for i in range(self.sizes[0]):
                                for j in range(-i, i + 1):
                                    for k in range(-i, i + 1):
                                        self.offsets.append([i, j, k])

                        if proto == [-1, 0, 0]:
                            for i in range(self.sizes[0]):
                                for j in range(-i, i + 1):
                                    for k in range(-i, i + 1):
                                        self.offsets.append([-i, j, k])

                        if proto == [0, 1, 0]:
                            for j in range(self.sizes[0]):
                                for k in range(-j, j + 1):
                                    for i in range(-j, j + 1):
                                        self.offsets.append([i, j, k])

                        if proto == [0, -1, 0]:
                            for j in range(self.sizes[0]):
                                for k in range(-j, j + 1):
                                    for i in range(-j, j + 1):
                                        self.offsets.append([i, -j, k])

                        if proto == [0, 0, 1]:
                            for k in range(self.sizes[0]):
                                for i in range(-k, k + 1):
                                    for j in range(-k, k + 1):
                                        self.offsets.append([i, j, k])

                        if proto == [0, 0, -1]:
                            for k in range(self.sizes[0]):
                                for i in range(-k, k + 1):
                                    for j in range(-k, k + 1):
                                        self.offsets.append([i, j, -k])

                if self.dim == 4:
                    protoset = [[0, 0, 0, 1], [0, 0, 0, -1]]
                    if proto not in protoset:
                        proto = [
                         0, 0, 0, 1]
                    if proto == [0, 0, 0, 1]:
                        for t in range(self.sizes[0]):
                            for i in range(-t, t + 1):
                                for j in range(-t, t + 1):
                                    for k in range(-t, t + 1):
                                        self.offsets.append([i, j, k, t])

                    if proto == [0, 0, 0, -1]:
                        for t in range(self.sizes[0]):
                            for i in range(-t, t + 1):
                                for j in range(-t, t + 1):
                                    for k in range(-t, t + 1):
                                        self.offsets.append([i, j, k, -t])

            else:
                print(f"Type {type} unknow")
        for i in range(len(self.offsets)):
            self.offsets[i] = list(np.array(self.offsets[i]) + np.array(self.shift))

        if inclusion:
            if self.anchoff not in self.offsets:
                self.offsets.append(self.anchoff)
        if not inclusion:
            if self.anchoff in self.offsets:
                self.offsets.remove(self.anchoff)
        tempoff = []
        for off in self.offsets:
            tempoff.append(list(np.array(off) * np.array(self.handedness)))

        self.offsets = tempoff