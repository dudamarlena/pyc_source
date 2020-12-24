# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\vvio\wavefront.py
# Compiled at: 2016-03-22 04:56:47
# Size of source mod 2**32: 12224 bytes
""" Module wavefront

This module produces functionality to read and write wavefront (.OBJ) files.

http://en.wikipedia.org/wiki/Wavefront_.obj_file

The wavefront format is quite powerfull and allows a wide variety of surfaces
to be described.

This implementation does only supports mesh stuff, so no nurbs etc. Further,
material properties are ignored, although this might be implemented later,

The classes are written with compatibility of Python3 in mind.

"""
import visvis as vv, numpy as np, time

class WavefrontReader(object):

    def __init__(self, f):
        self._f = f
        self._v = []
        self._vn = []
        self._vt = []
        self._vertices = []
        self._normals = []
        self._texcords = []
        self._faces = []
        self._facemap = {}

    @classmethod
    def read(cls, fname, check='ignored'):
        """ read(fname)
        
        This classmethod is the entry point for reading OBJ files.
        
        Parameters
        ----------
        fname : string
            The name of the file to read.
        
        """
        t0 = time.time()
        f = open(fname, 'rb')
        try:
            try:
                reader = WavefrontReader(f)
                while True:
                    reader.readLine()

            except EOFError:
                pass

        finally:
            f.close()

        mesh = reader.finish()
        return mesh

    def readLine(self):
        """ The method that reads a line and processes it.
        """
        line = self._f.readline().decode('ascii', 'ignore')
        if not line:
            raise EOFError()
        line = line.strip()
        if line.startswith('v '):
            self._v.append(self.readTuple(line))
        else:
            if line.startswith('vt '):
                self._vt.append(self.readTuple(line, 3))
            else:
                if line.startswith('vn '):
                    self._vn.append(self.readTuple(line))
                else:
                    if line.startswith('f '):
                        self._faces.append(self.readFace(line))
                    else:
                        if line.startswith('#'):
                            pass
                        else:
                            if line.startswith('mtllib '):
                                print('Notice reading .OBJ: material properties are ignored.')
                            else:
                                if line.startswith('g ') or line.startswith('s '):
                                    pass
                                else:
                                    if line.startswith('o '):
                                        pass
                                    else:
                                        if line.startswith('usemtl '):
                                            pass
                                        else:
                                            if not line.strip():
                                                pass
                                            else:
                                                print('Notice reading .OBJ: ignoring %s command.' % line.strip())

    def readTuple(self, line, n=3):
        """ Reads a tuple of numbers. e.g. vertices, normals or teture coords.
        """
        numbers = [num for num in line.split(' ') if num]
        return [float(num) for num in numbers[1:n + 1]]

    def readFace(self, line):
        """ Each face consists of three or more sets of indices. Each set
        consists of 1, 2 or 3 indices to vertices/normals/texcords.
        """
        indexSets = [num for num in line.split(' ') if num][1:]
        final_face = []
        for indexSet in indexSets:
            final_index = self._facemap.get(indexSet)
            if final_index is not None:
                final_face.append(final_index)
                continue
                final_index = len(self._vertices)
                final_face.append(final_index)
                self._facemap[indexSet] = final_index
                indices = [i for i in indexSet.split('/')]
                vertex_index = self._absint(indices[0], len(self._v))
                self._vertices.append(self._v[vertex_index])
                if self._texcords is not None:
                    if len(indices) > 1 and indices[1]:
                        texcord_index = self._absint(indices[1], len(self._vt))
                        self._texcords.append(self._vt[texcord_index])
                    else:
                        if self._texcords:
                            print('Warning reading OBJ: ignoring texture coordinates because it is not specified for all faces.')
                        self._texcords = None
                    if self._normals is not None:
                        if len(indices) > 2 and indices[2]:
                            normal_index = self._absint(indices[2], len(self._vn))
                            self._normals.append(self._vn[normal_index])
                        else:
                            if self._normals:
                                print('Warning reading OBJ: ignoring normals because it is not specified for all faces.')
                            self._normals = None

        if self._faces and len(self._faces[0]) != len(final_face):
            raise RuntimeError('Visvis requires that all faces are either triangles or quads.')
        return final_face

    def _absint(self, i, ref):
        i = int(i)
        if i > 0:
            return i - 1
        else:
            return ref + i

    def finish(self):
        """ Converts gathere lists to numpy arrays and creates 
        BaseMesh instance.
        """
        self._vertices = np.array(self._vertices, 'float32')
        if self._normals:
            self._normals = np.array(self._normals, 'float32')
        else:
            self._normals = None
        if self._texcords:
            self._texcords = np.array(self._texcords, 'float32')
        else:
            self._texcords = None
        if self._faces:
            self._faces = np.array(self._faces, 'uint32')
        else:
            self._vertices = np.array(self._v, 'float32')
            self._faces = None
        return vv.BaseMesh(self._vertices, self._faces, self._normals, self._texcords)


class WavefrontWriter(object):

    def __init__(self, f):
        self._f = f

    @classmethod
    def write(cls, fname, mesh, name='', bin='ignored'):
        """ write(fname, mesh, name='')
        
        This classmethod is the entry point for writing mesh data to OBJ.
        
        Parameters
        ----------
        fname : string
            The filename to write to.
        mesh : Mesh data
            Can be vv.BaseMesh, vv.Pointset, or np.ndarray.
        name : string
            The name of the object (e.g. 'teapot')
        
        """
        f = open(fname, 'wb')
        try:
            try:
                writer = WavefrontWriter(f)
                writer.writeMesh(mesh, name)
            except EOFError:
                pass

        finally:
            f.close()

    def writeLine(self, text):
        """ Simple writeLine function to write a line of code to the file.
        The encoding is done here, and a newline character is added.
        """
        text += '\n'
        self._f.write(text.encode('ascii'))

    def writeTuple(self, val, what):
        """ Writes a tuple of numbers (on one line).
        """
        val = val[:3]
        val = ' '.join([str(v) for v in val])
        self.writeLine('%s %s' % (what, val))

    def writeFace(self, val, what='f'):
        """ Write the face info to the net line.
        """
        val = [v + 1 for v in val]
        if self._hasValues and self._hasNormals:
            val = ' '.join(['%i/%i/%i' % (v, v, v) for v in val])
        else:
            if self._hasNormals:
                val = ' '.join(['%i//%i' % (v, v) for v in val])
            else:
                if self._hasValues:
                    val = ' '.join(['%i/%i' % (v, v) for v in val])
                else:
                    val = ' '.join(['%i' % v for v in val])
        self.writeLine('%s %s' % (what, val))

    def writeMesh(self, mesh, name=''):
        """ Write the given mesh instance.
        """
        self._hasNormals = mesh._normals is not None
        self._hasValues = mesh._values is not None
        self._hasFaces = mesh._faces is not None
        faces = mesh._GetFaces()
        N = mesh._vertices.shape[0]
        stats = []
        stats.append('%i vertices' % N)
        if self._hasValues:
            stats.append('%i texcords' % N)
        else:
            stats.append('no texcords')
        if self._hasNormals:
            stats.append('%i normals' % N)
        else:
            stats.append('no normals')
        stats.append('%i faces' % faces.shape[0])
        self.writeLine('# Wavefront OBJ file')
        self.writeLine('# Created by visvis (a Python visualization toolkit).')
        self.writeLine('#')
        if name:
            self.writeLine('# object %s' % name)
        else:
            self.writeLine('# unnamed object')
        self.writeLine('# %s' % ', '.join(stats))
        self.writeLine('')
        for i in range(N):
            self.writeTuple(mesh._vertices[i], 'v')

        if self._hasNormals:
            for i in range(N):
                self.writeTuple(mesh._normals[i], 'vn')

        if self._hasValues:
            for i in range(N):
                self.writeTuple(mesh._values[i], 'vt')

        for i in range(faces.shape[0]):
            self.writeFace(faces[i])