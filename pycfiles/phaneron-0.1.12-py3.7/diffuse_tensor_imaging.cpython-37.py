# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phaneron/diffuse_tensor_imaging.py
# Compiled at: 2019-09-03 05:18:33
# Size of source mod 2**32: 3461 bytes
"""Provides a class that wraps the API exposed by the braynsDTI plug-in"""

class DiffuseTensorImaging:
    __doc__ = 'DiffuseTensorImaging is a class that wraps the API exposed by the braynsDTI plug-in'

    def __init__(self, client):
        """
        Create a new Diffuse Tensor Imaging instance
        """
        self._client = client.rockets_client

    def add_streamlines(self, name, guids, streamlines, radius=1, opacity=1):
        """
        Adds streamlines to the scene. All streamlines are added into a single model
        :param str name: Name of the model
        :param float streamlines: Streamlines
        :param float radius: Radius of the streamlines
        :param float opacity: Opacity of the streamlines
        :return: Result of the request submission
        :rtype: str
        """
        count = 0
        indices = list()
        vertices = list()
        for points in streamlines:
            indices.append(count)
            count = count + len(points)
            for point in points:
                for coordinate in point:
                    vertices.append(float(coordinate))

        params = dict()
        params['name'] = name
        params['gids'] = guids
        params['indices'] = indices
        params['vertices'] = vertices
        params['radius'] = radius
        params['opacity'] = opacity
        return self._client.request('streamlines', params=params)

    def set_spike_simulation(self, model_id, gids, timestamps, dt, end_time, time_scale=1.0, decay_speed=0.1, rest_intensity=0.25, spike_intensity=0.75):
        params = dict()
        params['modelId'] = model_id
        params['gids'] = gids
        params['timestamps'] = timestamps
        params['dt'] = dt
        params['endTime'] = end_time
        params['timeScale'] = time_scale
        params['decaySpeed'] = decay_speed
        params['restIntensity'] = rest_intensity
        params['spikeIntensity'] = spike_intensity
        return self._client.request('spikeSimulation', params=params)

    def load_streamlines(self, connection_string, sql_statement, name, radius=1.0, color_scheme=0, nb_max_points=1000000.0):
        params = dict()
        params['connectionString'] = connection_string
        params['sqlStatement'] = sql_statement
        params['name'] = name
        params['radius'] = radius
        params['colorScheme'] = color_scheme
        params['nbMaxPoints'] = nb_max_points
        return self._client.request('loadStreamlines', params)