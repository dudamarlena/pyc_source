# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phaneron/graph_explorer.py
# Compiled at: 2019-10-21 09:09:20
# Size of source mod 2**32: 5327 bytes


class GraphExplorer:
    __doc__ = 'GraphExplorer is a class that wraps the API exposed by the braynsGraph plug-in'

    def __init__(self, client):
        """Create a new Graph instance"""
        self._client = client.rockets_client

    def load_positions_from_file(self, path, mesh_file='', pdb_file='', radius=1.0, scale=[1.0, 1.0, 1.0]):
        """
        Loads node positions from file
        :param str path: Path of the file where positions are stored
        :param str mesh_file: Path of the mesh file to be placed at each position
        :param str pdb_file: Path of the protein file to be placed at each position
        :param float radius: Radius of the sphere used to represent the node
        :param float scale: Scaling to use for the positions
        :return: Result of the request submission
        :rtype: str
        """
        xs = []
        ys = []
        zs = []
        with open(path) as (f):
            for l in f:
                x, y, z = l.split()
                xs.append(float(x) * scale)
                ys.append(float(y) * scale)
                zs.append(float(z) * scale)

        params = dict()
        params['x'] = xs
        params['y'] = ys
        params['z'] = zs
        params['radius'] = radius
        params['meshFile'] = mesh_file
        params['pdbFile'] = pdb_file
        self._client.request('positions', params=params)

    def create_random_connectivity(self, min_distance=0, max_distance=1000000.0, density=1, seed=0):
        """
        Creates random connectivity between nodes
        :param float min_distance: Minimum distance between nodes to be connected
        :param float max_distance: Maximum distance between nodes to be connected
        :param float density: Nodes to skip between every new connection
        :param float seed: Random seed
        :return: Result of the request submission
        :rtype: str
        """
        params = dict()
        params['minLength'] = min_distance
        params['maxLength'] = max_distance
        params['density'] = density
        params['seed'] = density
        return self._client.request('randomConnectivity', params=params)

    def load_connectivity_from_file(self, path, matrix_id, dimension_range=(1, 1000000.0)):
        """
        :param str path: Path to the h5 file containing the connectivity data
        :param int matrix_id: Id of the matrix used to create the connections
        :param list dimension_range: Range of dimensions
        :return: Result of the request submission
        :rtype: str
        """
        params = dict()
        params['filename'] = path
        params['matrixId'] = matrix_id
        params['minDimension'] = dimension_range[0]
        params['maxDimension'] = dimension_range[1]
        return self._client.request('connectivity', params=params)

    def initialize_morphing(self, model_id, nb_steps=1000, sync_with_animation=False):
        """
        Initialize the morphing sequence
        :param model_id: Id of the model
        :param nb_steps: Number of morphing steps
        :param sync_with_animation: Specifies if morphing steps should automatically be synchronized with animation
        :return: Result of the request submission
        :rtype: str
        """
        params = dict()
        params['modelId'] = model_id
        params['nbSteps'] = nb_steps
        params['syncWithAnimation'] = sync_with_animation
        return self._client.request('initializeMorphing', params=params)

    def set_morphing_step(self, model_id, step):
        """
        Set the morphing step
        :param str model_id: Id of the model
        :param int nb_steps: Number of morphing steps
        :return: Result of the request submission
        :rtype: str
        """
        params = dict()
        params['modelId'] = model_id
        params['step'] = step
        return self._client.request('setMorphingStep', params=params)

    def set_morphing_synchronization(self, model_id, sync_with_animation):
        """
        Set the morphing step
        :param str model_id: Id of the model
        :param int nb_steps: Number of morphing steps
        :return: Result of the request submission
        :rtype: str
        """
        params = dict()
        params['modelId'] = model_id
        params['syncWithAnimation'] = sync_with_animation
        return self._client.request('setMorphingSynchronization', params=params)