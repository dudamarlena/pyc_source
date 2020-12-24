# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/parser.py
# Compiled at: 2016-11-29 20:56:28
"""

DataSpecParser class.

Kisuk Lee <kisuklee@mit.edu>, 2016
"""
import ConfigParser
from vector import Vec3d

class Parser(object):
    """
    Parser class.
    """

    def __init__(self, dspec_path, net_spec, params, auto_mask=True):
        """Initialize a Parser object.

        Args:
            dspec_path: Data spec path.
            net_spec: Net spec, a dictionary containing layer-data name pairs.
            params: Parameter dictionary.
        """
        config = ConfigParser.ConfigParser()
        config.read(dspec_path)
        self._config = config
        self.net_spec = net_spec
        self.params = params
        self.auto_mask = auto_mask
        self.dparams = self._parse_dataset_params(config)

    def parse_dataset(self, dataset_id):
        """
        TODO(kisuk): Documentation.

        Args:
            dataset_id:

        Returns:
            dataset: ConfigParser object containing dataset info.
        """
        config = ConfigParser.ConfigParser()
        section = 'dataset'
        if self._config.has_section(section):
            config.add_section(section)
            for name in self.net_spec.keys():
                if self._config.has_option(section, name):
                    data = self._config.get(section, name)
                    config.set(section, name, data)
                    self.parse_data(config, name, data, dataset_id)

        else:
            raise RuntimeError('dataset section does not exist.')
        self._treat_affinity(config)
        self._treat_border(config)
        dparams = dict()
        dparams['dataset_id'] = dataset_id
        for k, v in self.dparams.iteritems():
            dparams[k] = v[dataset_id]

        return (config, dparams)

    def parse_data(self, config, name, data, idx):
        """
        TODO(kisuk): Documentation.

        Args:
            config:
            name:
            data:
            idx:
        """
        if self._config.has_section(data):
            config.add_section(data)
            for option, value in self._config.items(data):
                config.set(data, option, value)

        else:
            raise RuntimeError('data section [%s] does not exist.' % data)
        if config.has_option(data, 'file'):
            value = config.get(data, 'file')
            if not self._config.has_option('files', value):
                raise AssertionError
                flist = self._config.get('files', value).split('\n')
                config.set(data, 'file', flist[idx])
            fov = self.net_spec[name][-3:]
            config.set(data, 'fov', fov)
            config.has_option(data, 'offset') or config.set(data, 'offset', (0, 0,
                                                                             0))
        if self.auto_mask and 'label' in data:
            self._add_mask(config, name, data, idx)

    def _parse_dataset_params(self, config):
        """
        TODO(kisuk): Documentation.
        """
        ret = dict()
        if config.has_section('params'):
            opts = config.options('params')
            for opt in opts:
                ret[opt] = eval(config.get('params', opt))

        return ret

    def _add_mask(self, config, name, data, idx):
        """Add mask for label.

        Each label is supposed to have corresponding mask, an equal-sized
        volume with postive real values. During training, cost and gradient
        volumes are element-wise multiplied by mask.

        Args:
            config: ConfigParser object containing dataset info.
            name: Layer name for label.
            data: Section name for label data.
            idx: Dataset ID.
        """
        if not config.has_section(data):
            raise AssertionError
            name = name + '_mask'
            mask = data + '_mask'
            config.set('dataset', name, mask)
            config.add_section(mask)
            for option, value in config.items(data):
                if option == 'file':
                    continue
                elif option == 'mask':
                    assert self._config.has_option('files', value)
                    flist = self._config.get('files', value).split('\n')
                    option = 'file'
                    value = flist[idx]
                config.set(mask, option, value)

            config.has_option(mask, 'file') or config.set(mask, 'shape', '(z,y,x)')
            config.set(mask, 'filler', "{'type':'one'}")

    def _is_affinity(self, config, data):
        """Check if data is affinity."""
        ret = False
        if config.has_section(data):
            if config.has_option(data, 'transform'):
                tf = config.get(data, 'transform')
                if 'affinitize' in tf:
                    ret = True
        return ret

    def _has_affinity(self, config):
        """Check if dataset contains affinity data."""
        ret = False
        for _, data in config.items('dataset'):
            if self._is_affinity(config, data):
                ret = True
                break

        return ret

    def _treat_affinity(self, config):
        """
        TODO(kisuk): Documentation.
        """
        if self._has_affinity(config):
            for _, data in config.items('dataset'):
                assert config.has_section(data)
                assert config.has_option(data, 'fov')
                fov = config.get(data, 'fov')
                fov = tuple(x + 1 for x in fov)
                config.set(data, 'fov', fov)

    def _treat_border(self, config):
        """
        TODO(kisuk): Documentation.
        """
        border_func = self.params.get('border', None)
        if border_func is not None:
            if border_func['type'] is 'mirror_border':
                for _, data in config.items('dataset'):
                    if 'image' not in data:
                        continue
                    assert config.has_section(data)
                    assert config.has_option(data, 'offset')
                    offset = config.get(data, 'offset')
                    if config.has_option(data, 'preprocess'):
                        pp = config.get(data, 'Preprocess') + '\n'
                    else:
                        pp = ''
                    pp += str(border_func)
                    config.set(data, 'preprocess', pp)
                    fov = border_func['fov']
                    offset = Vec3d(offset) - Vec3d(fov) / 2
                    config.set(data, 'offset', tuple(offset))

            else:
                msg = 'unknown border mode [%s].' % border_func['type']
                raise RuntimeError(msg)
        return


if __name__ == '__main__':
    dspec_path = 'test_spec/zfish.spec'
    fov = (9, 109, 109)
    net_spec = dict(input=(18, 208, 208), label=(10, 100, 100))
    params = dict()
    params['border'] = dict(type='mirror_border', fov=fov)
    params['augment'] = [dict(type='flip')]
    params['drange'] = [0]
    p = Parser(dspec_path, net_spec, params)
    config, dparams = p.parse_dataset(0)
    assert dparams['dataset_id'] == 0
    print dparams
    f = open('zfish_dataset0.spec', 'w')
    config.write(f)
    f.close()