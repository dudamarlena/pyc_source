# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/MEEGbuddy/read_dig_monatage.py
# Compiled at: 2019-02-12 17:24:47
# Size of source mod 2**32: 10352 bytes


def read_dig_montage(hsp=None, hpi=None, elp=None, point_names=None, unit='auto', fif=None, egi=None, bvct=None, transform=True, dev_head_t=False):
    r"""Read subject-specific digitization montage from a file.

    Parameters

    ----------

    hsp : None | str | array, shape (n_points, 3)

        If str, this corresponds to the filename of the headshape points.

        This is typically used with the Polhemus FastSCAN system.

        If numpy.array, this corresponds to an array of positions of the

        headshape points in 3d. These points are assumed to be in the native

        digitizer space and will be rescaled according to the unit parameter.

    hpi : None | str | array, shape (n_hpi, 3)

        If str, this corresponds to the filename of Head Position Indicator

        (HPI) points. If numpy.array, this corresponds to an array

        of HPI points. These points are in device space, and are only

        necessary if computation of a ``dev_head_t`` by the

        :class:`DigMontage` is required.

    elp : None | str | array, shape (n_fids + n_hpi, 3)

        If str, this corresponds to the filename of electrode position

        points. This is typically used with the Polhemus FastSCAN system.

        If numpy.array, this corresponds to an array of digitizer points in

        the same order. These points are assumed to be in the native digitizer

        space and will be rescaled according to the unit parameter.

    point_names : None | list

        A list of point names for elp (required if elp is defined).

        Typically this would be like::

            ('nasion', 'lpa', 'rpa', 'CHPI001', 'CHPI002', 'CHPI003')

    unit : 'auto' | 'm' | 'cm' | 'mm'

        Unit of the digitizer files (hsp and elp). If not 'm', coordinates will

        be rescaled to 'm'. Default is 'auto', which assumes 'm' for \*.hsp and

        \*.elp files and 'mm' for \*.txt files, corresponding to the known

        Polhemus export formats.

    fif : str | None

        FIF file from which to read digitization locations.

        If str (filename), all other arguments are ignored.

        .. versionadded:: 0.12

    egi : str | None

        EGI MFF XML coordinates file from which to read digitization locations.

        If str (filename), all other arguments are ignored.

        .. versionadded:: 0.14

    bvct : srt | None

        BVCT XML coordinates file from which to read digitization locations.

        (BrainVision)

        If str (filename), all other arguments are ignored.

    transform : bool

        If True (default), points will be transformed to Neuromag space

        using :meth:`DigMontage.transform_to_head`.

        The fidicuals (nasion, lpa, and rpa) must be specified.

        This is useful for points captured using a device that does

        not automatically convert points to Neuromag head coordinates

        (e.g., Polhemus FastSCAN).

    dev_head_t : bool

        If True, a Dev-to-Head transformation matrix will be added to the

        montage using :meth:`DigMontage.compute_dev_head_t`.

        To get a proper `dev_head_t`, the hpi and the elp points

        must be in the same order. If False (default), no transformation

        will be added to the montage.

    Returns

    -------

    montage : instance of DigMontage

        The digitizer montage.

    See Also

    --------

    DigMontage

    Montage

    read_montage

    Notes

    -----

    All digitized points will be transformed to head-based coordinate system

    if transform is True and fiducials are present.

    .. versionadded:: 0.9.0

    """
    if fif is not None:
        if dev_head_t or not transform:
            raise ValueError('transform must be True and dev_head_t must be False for FIF dig montage')
        if not all(x is None for x in (hsp, hpi, elp, point_names, egi, bvct)):
            raise ValueError('hsp, hpi, elp, point_names, egi, bvct must all be None if fif is not None')
        _check_fname(fif, overwrite='read', must_exist=True)
        f, tree = fiff_open(fif)[:2]
        with f as (fid):
            dig = _read_dig_fif(fid, tree)
        hsp = list()
        hpi = list()
        elp = list()
        point_names = list()
        fids = dict()
        dig_ch_pos = dict()
        for d in dig:
            if d['kind'] == FIFF.FIFFV_POINT_CARDINAL:
                _check_frame(d, 'head')
                fids[_cardinal_ident_mapping[d['ident']]] = d['r']
            else:
                if d['kind'] == FIFF.FIFFV_POINT_HPI:
                    _check_frame(d, 'head')
                    hpi.append(d['r'])
                    elp.append(d['r'])
                    point_names.append('HPI%03d' % d['ident'])
                else:
                    if d['kind'] == FIFF.FIFFV_POINT_EXTRA:
                        _check_frame(d, 'head')
                        hsp.append(d['r'])
                    else:
                        if d['kind'] == FIFF.FIFFV_POINT_EEG:
                            _check_frame(d, 'head')
                            dig_ch_pos['EEG%03d' % d['ident']] = d['r']

        fids = [fids.get(key) for key in ('nasion', 'lpa', 'rpa')]
        hsp = np.array(hsp) if len(hsp) else None
        elp = np.array(elp) if len(elp) else None
        coord_frame = 'head'
    else:
        if egi is not None:
            if not all(x is None for x in (hsp, hpi, elp, point_names, fif, bvct)):
                raise ValueError('hsp, hpi, elp, point_names, fif, bvct must all be None if egi is not None')
            _check_fname(egi, overwrite='read', must_exist=True)
            root = ElementTree.parse(egi).getroot()
            ns = root.tag[root.tag.index('{'):root.tag.index('}') + 1]
            sensors = root.find('%ssensorLayout/%ssensors' % (ns, ns))
            fids = dict()
            dig_ch_pos = dict()
            fid_name_map = {'Nasion':'nasion', 
             'Right periauricular point':'rpa', 
             'Left periauricular point':'lpa'}
            scale = dict(mm=0.001, cm=0.01, auto=0.01, m=1)
            if unit not in scale:
                raise ValueError('Unit needs to be one of %s, not %r' % (
                 sorted(scale.keys()), unit))
            for s in sensors:
                name, number, kind = s[0].text, int(s[1].text), int(s[2].text)
                coordinates = np.array([float(s[3].text), float(s[4].text),
                 float(s[5].text)])
                coordinates *= scale[unit]
                if kind == 0:
                    dig_ch_pos['EEG %03d' % number] = coordinates
                else:
                    if kind == 1:
                        dig_ch_pos['EEG %03d' % (len(dig_ch_pos.keys()) + 1)] = coordinates
                    else:
                        if kind == 2:
                            fid_name = fid_name_map[name]
                            fids[fid_name] = coordinates
                        else:
                            warn('Unknown sensor type %s detected. Skipping sensor...Proceed with caution!' % kind)

            fids = [fids[key] for key in ('nasion', 'lpa', 'rpa')]
            coord_frame = 'unknown'
        else:
            if bvct is not None:
                if not all(x is None for x in (hsp, hpi, elp, point_names, fif, egi)):
                    raise ValueError('hsp, hpi, elp, point_names, fif, egi must all be None if bvct is not None')
                _check_fname(bvct, overwrite='read', must_exist=True)
                root = ElementTree.parse(bvct).getroot()
                sensors = root.find('CapTrakElectrodeList')
                fids = {}
                dig_ch_pos = {}
                fid_name_map = {'Nasion':'nasion', 
                 'RPA':'rpa',  'LPA':'lpa'}
                scale = dict(mm=0.001, cm=0.01, auto=0.001, m=1)
                if unit not in scale:
                    raise ValueError('Unit needs to be one of %s, not %r' % (
                     sorted(scale.keys()), unit))
                for s in sensors:
                    name = s.find('Name').text
                    fid = name in fid_name_map
                    coordinates = np.array([float(s.find('X').text),
                     float(s.find('Y').text),
                     float(s.find('Z').text)])
                    coordinates *= scale[unit]
                    if fid:
                        fid_name = fid_name_map[name]
                        fids[fid_name] = coordinates
                    else:
                        dig_ch_pos[name] = coordinates

                fids = [fids[key] for key in ('nasion', 'lpa', 'rpa')]
                coord_frame = 'unknown'
            else:
                fids = [None] * 3
                dig_ch_pos = None
                scale = dict(mm=0.001, cm=0.01, auto=0.001, m=1)
                if unit not in scale:
                    raise ValueError('Unit needs to be one of %s, not %r' % (
                     sorted(scale.keys()), unit))
                if isinstance(hsp, string_types):
                    hsp = _read_dig_points(hsp, unit=unit)
                else:
                    if hsp is not None:
                        hsp *= scale[unit]
                if isinstance(hpi, string_types):
                    ext = op.splitext(hpi)[(-1)]
                    if ext in ('.txt', '.mat'):
                        hpi = _read_dig_points(hpi, unit='m')
                    else:
                        if ext in ('.sqd', '.mrk'):
                            from ..io.kit import read_mrk
                            hpi = read_mrk(hpi)
                        else:
                            raise ValueError('HPI file with extension *%s is not supported. Only *.txt, *.sqd and *.mrk are supported.' % ext)
                if isinstance(elp, string_types):
                    elp = _read_dig_points(elp, unit=unit)
                else:
                    if elp is not None:
                        if scale[unit]:
                            elp *= scale[unit]
                    coord_frame = 'unknown'
                out = DigMontage(hsp, hpi, elp, point_names, (fids[0]), (fids[1]), (fids[2]), dig_ch_pos=dig_ch_pos,
                  coord_frame=coord_frame)
                if fif is None:
                    if transform:
                        out.transform_to_head()
        if dev_head_t:
            out.compute_dev_head_t()
    return out