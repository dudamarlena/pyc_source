# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Alister/miniconda3/envs/obsea/lib/python3.7/site-packages/obsea/gis.py
# Compiled at: 2019-11-19 06:21:45
# Size of source mod 2**32: 5480 bytes
"""
GIS module.

Used to process AIS data, build ship trajectories and retreive route passing
close to a recording instrument.

"""
import numpy as np, pandas as pd
import cartopy.crs as ccrs
from shapely.geometry import Point, LineString
import xarray as xr

def read_ais(ais, timedelta):
    """
    Create a GeoSerie of tracks from AIS data.

    Parameters
    ----------
    ais : DataFrame
        The AIS data with time stored in the 'timestamp' column
        and position in a 'lon and 'lat' column.
    timegap : Timedelta
        The maximum time gap accepted between two AIS logs.

    Returns
    -------
    tracks : GeoSerie
        A GeoSerie containing Linestrings indexed by its MMSI.

    """
    df = ais.copy()
    td = timedelta / pd.Timedelta(1, 's')
    df = df.sort_values(['mmsi', 'timestamp'])
    df['time'] = (df.timestamp - np.datetime64(0, 's')) / np.timedelta64(1, 's')
    df['dt'] = df.groupby('mmsi')['time'].apply(lambda x: x.diff())
    df['i'] = df.groupby('mmsi')['dt'].apply(lambda x: (x > td).cumsum())
    df = df.groupby(['mmsi', 'i']).filter(lambda x: x.shape[0] > 1)
    tracks = df.groupby([
     'mmsi', 'i']).apply(lambda x: LineString(x[['lon', 'lat', 'time']].values)).reset_index('i',
      drop=True)
    return tracks


def trim_track(track, t_start, t_end):
    """
    Temporally trim a track.

    Parameters
    ----------
    track : LineString
        Moving source trajectory.
    t_start : float
        Specify the start time (POSIX timestamp in seconds).
    t_end : float
        Specify the end time (POSIX timestamp in seconds).

    Returns
    -------
    LineString
        Trimed moving source trajectory.

    """
    xyt = np.asarray(track.coords)
    mask = (xyt[:, -1] > t_start) & (xyt[:, -1] < t_end)
    if mask.sum() < 2:
        return np.nan
    return LineString(xyt[mask])


def select_tracks(tracks, station, radius, cpa):
    """
    Select tracks passing close to some interest point.

    Parameters
    ----------
    tracks : GeoSerie
        Tracks from which the selection must be done.
    station : Obspy Station
        Station of interest.
    radius : float
        Tracks are intersected in with a disk with radius is given but that
        value (in metres).
    cpa : float
        Tracks passing farther than this are rejected (in metres).

    Returns
    -------
    df : GeoDataFrame
        The selected tracks in the local azimuthal equidistant projection
        as a GeoDataFrame containing tracks and related statistics.

    """
    tracks = tracks.copy()
    t_start = station.start_date.timestamp
    t_end = station.end_date.timestamp
    tracks = tracks.apply(lambda track: trim_track(track, t_start, t_end))
    tracks = tracks[(~tracks.isna())]
    crs = ccrs.AzimuthalEquidistant(station.longitude, station.latitude)
    tracks = tracks.apply(lambda track: LineString((crs.transform_points)(ccrs.PlateCarree(), *np.array(track.coords).T)))
    centre = Point(0, 0)
    cpa_mask = tracks.apply(centre.distance) <= cpa
    tracks = tracks[cpa_mask]
    area = centre.buffer(radius)
    tracks = tracks.apply(area.intersection)
    if len(tracks) == 0:
        return
    tracks = tracks.apply(pd.Series).stack().reset_index(level=1,
      drop=True).apply(lambda track: LineString(sorted((track.coords), key=(lambda point: point[(-1)]))))
    cpa_mask = tracks.apply(centre.distance) <= cpa
    tracks = tracks[cpa_mask]
    return tracks


def track2xarr(track):
    """
    Convert a track to a DataArray.

    Parameters
    ----------
    track : LineString
        Moving source trajectory as a LineString.

    Returns
    -------
    xarray.DataArray
        Moving source trajectory as a DataArray.

    """
    x, y, t = np.array(track.coords).T
    data = x + complex(0.0, 1.0) * y
    track = xr.DataArray(data=data, coords={'time': t}, dims='time')
    _, index = np.unique((track['time']), return_index=True)
    track = track.isel(time=index)
    return track


def correct_track(track, B):
    """
    Correct the accoustic center.

    Change the track positions by B in the opposite direction of the ship
    heading. For now works only for rectilinear trajectories.

    Parameters
    ----------
    track : xr.DataArray
        The track to correct.
    B : float
        The amount of correction.

    Returns
    -------
    xr.DataArray
        The corrected track
    """
    v, r0 = np.polyfit(track.time, track.values, 1)
    u = v / np.abs(v)
    track = track - u * B
    return track