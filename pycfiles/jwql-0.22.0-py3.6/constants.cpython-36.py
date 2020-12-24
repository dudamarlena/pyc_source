# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/utils/constants.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 7004 bytes
"""Globally defined and used variables for the ``jwql`` project.

Authors
-------

    - Johannes Sahlmann

Use
---
    This variables within this module are intended to be directly
    imported, e.g.:
    ::

        from jwql.utils.constants import JWST_INSTRUMENT_NAMES

References
----------

    Many variables were transferred from an earlier version of
    ``utils.py``
"""
import inflection
AMPLIFIER_BOUNDARIES = {'nircam':{'1':[
   (0, 512, 1), (0, 2048, 1)], 
  '2':[
   (512, 1024, 1), (0, 2048, 1)], 
  '3':[
   (1024, 1536, 1), (0, 2048, 1)], 
  '4':[
   (1536, 2048, 1), (0, 2048, 1)]}, 
 'niriss':{'1':[
   (0, 2048, 1), (0, 512, 1)], 
  '2':[
   (0, 2048, 1), (512, 1024, 1)], 
  '3':[
   (0, 2048, 1), (1024, 1536, 1)], 
  '4':[
   (0, 2048, 1), (1536, 2048, 1)]}, 
 'fgs':{'1':[
   (0, 512, 1), (0, 2048, 1)], 
  '2':[
   (512, 1024, 1), (0, 2048, 1)], 
  '3':[
   (1024, 1536, 1), (0, 2048, 1)], 
  '4':[
   (1536, 2048, 1), (0, 2048, 1)]}, 
 'nirspec':{'1':[
   (0, 512, 1), (0, 2048, 1)], 
  '2':[
   (512, 1024, 1), (0, 2048, 1)], 
  '3':[
   (1024, 1536, 1), (0, 2048, 1)], 
  '4':[
   (1536, 2048, 1), (0, 2048, 1)]}, 
 'miri':{'1':[
   (0, 1032, 4), (0, 1024, 1)], 
  '2':[
   (1, 1032, 4), (0, 1024, 1)], 
  '3':[
   (2, 1032, 4), (0, 1024, 1)], 
  '4':[
   (3, 1032, 4), (0, 1024, 1)]}}
ANOMALIES = [
 'snowball', 'cosmic_ray_shower', 'crosstalk', 'data_transfer_error', 'diffraction_spike',
 'excessive_saturation', 'ghost', 'guidestar_failure', 'persistence', 'satellite_trail', 'other']
ANOMALY_CHOICES = [(anomaly, inflection.titleize(anomaly)) for anomaly in ANOMALIES]
FOUR_AMP_SUBARRAYS = [
 'WFSS128R', 'WFSS64R', 'WFSS128C', 'WFSS64C']
GENERIC_SUFFIX_TYPES = [
 'uncal', 'cal', 'rateints', 'rate', 'trapsfilled', 'i2d',
 'x1dints', 'x1d', 's2d', 's3d', 'dark', 'crfints',
 'crf', 'ramp', 'fitopt', 'bsubints', 'bsub', 'cat']
GUIDER_SUFFIX_TYPES = [
 'stream', 'stacked_uncal', 'image_uncal', 'stacked_cal', 'image_cal']
INSTRUMENT_MONITOR_DATABASE_TABLES = {'dark_monitor': ['nircam_dark_dark_current', 'nircam_dark_pixel_stats', 'nircam_dark_query_history']}
JWST_DATAPRODUCTS = [
 'IMAGE', 'SPECTRUM', 'SED', 'TIMESERIES', 'VISIBILITY',
 'EVENTLIST', 'CUBE', 'CATALOG', 'ENGINEERING', 'NULL']
JWST_INSTRUMENT_NAMES = sorted(['niriss', 'nircam', 'nirspec', 'miri', 'fgs'])
JWST_INSTRUMENT_NAMES_SHORTHAND = {'gui':'fgs', 
 'mir':'miri', 
 'nis':'niriss', 
 'nrc':'nircam', 
 'nrs':'nirspec'}
JWST_INSTRUMENT_NAMES_MIXEDCASE = {'fgs':'FGS', 
 'miri':'MIRI', 
 'nircam':'NIRCam', 
 'niriss':'NIRISS', 
 'nirspec':'NIRSpec'}
JWST_INSTRUMENT_NAMES_UPPERCASE = {key:value.upper() for key, value in JWST_INSTRUMENT_NAMES_MIXEDCASE.items()}
JWST_MAST_SERVICES = ['Mast.Jwst.Filtered.{}'.format(value.title()) for value in JWST_INSTRUMENT_NAMES]
MONITORS = {'fgs':[
  ('Bad Pixel Monitor', '#')], 
 'miri':[
  ('Dark Current Monitor', '#'),
  ('Data Trending', '/miri/miri_data_trending'),
  ('Bad Pixel Monitor', '#'),
  ('Cosmic Ray Monitor', '#'),
  ('Photometry Monitor', '#'),
  ('TA Failure Monitor', '#'),
  ('Blind Pointing Accuracy Monitor', '#'),
  ('Filter and Calibration Lamp Monitor', '#'),
  ('Thermal Emission Monitor', '#')], 
 'nircam':[
  ('Bias Monitor', '#'),
  ('Readnoise Monitor', '#'),
  ('Gain Level Monitor', '#'),
  ('Mean Dark Current Rate Monitor', '#'),
  ('Photometric Stability Monitor', '#')], 
 'niriss':[
  ('Bad Pixel Monitor', '#'),
  ('Readnoise Monitor', '#'),
  ('AMI Calibrator Monitor', '#'),
  ('TSO RMS Monitor', '#')], 
 'nirspec':[
  ('Optical Short Monitor', '#'),
  ('Target Acquisition Monitor', '#'),
  ('Data Trending', '/nirspec/nirspec_data_trending'),
  ('Detector Health Monitor', '#'),
  ('Ref Pix Monitor', '#'),
  ('Internal Lamp Monitor', '#'),
  ('Instrument Model Updates', '#'),
  ('Failed-open Shutter Monitor', '#')]}
NIRCAM_CORONAGRAPHY_SUFFIX_TYPES = [
 'psfstack', 'psfalign', 'psfsub']
NIRCAM_FOUR_AMP_SUBARRAYS = [
 'WFSS128R', 'WFSS64R']
NIRCAM_LONGWAVE_DETECTORS = [
 'NRCA5', 'NRCB5']
NIRCAM_SHORTWAVE_DETECTORS = [
 'NRCA1', 'NRCA2', 'NRCA3', 'NRCA4',
 'NRCB1', 'NRCB2', 'NRCB3', 'NRCB4']
NIRCAM_SUBARRAYS_ONE_OR_FOUR_AMPS = [
 'SUBGRISMSTRIPE64', 'SUBGRISMSTRIPE128', 'SUBGRISMSTRIPE256']
NIRISS_AMI_SUFFIX_TYPES = [
 'amiavg', 'aminorm', 'ami']
SUBARRAYS_ONE_OR_FOUR_AMPS = [
 'SUBGRISMSTRIPE64', 'SUBGRISMSTRIPE128', 'SUBGRISMSTRIPE256']
TIME_SERIES_SUFFIX_TYPES = [
 'phot', 'whtlt']
FILE_SUFFIX_TYPES = GUIDER_SUFFIX_TYPES + GENERIC_SUFFIX_TYPES + TIME_SERIES_SUFFIX_TYPES + NIRCAM_CORONAGRAPHY_SUFFIX_TYPES + NIRISS_AMI_SUFFIX_TYPES