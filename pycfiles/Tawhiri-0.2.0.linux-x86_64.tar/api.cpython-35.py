# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/tawhiri/api.py
# Compiled at: 2016-11-26 12:39:04
# Size of source mod 2**32: 10320 bytes
"""
Provide the HTTP API for Tawhiri.
"""
from flask import Flask, jsonify, request, g
from datetime import datetime
import time, strict_rfc3339
from tawhiri import solver, models
from tawhiri.dataset import Dataset as WindDataset
from ruaumoko import Dataset as ElevationDataset
app = Flask(__name__)
API_VERSION = 1
LATEST_DATASET_KEYWORD = 'latest'
PROFILE_STANDARD = 'standard_profile'
PROFILE_FLOAT = 'float_profile'

def ruaumoko_ds():
    if not hasattr('ruaumoko_ds', 'once'):
        ds_loc = app.config.get('ELEVATION_DATASET', ElevationDataset.default_location)
        ruaumoko_ds.once = ElevationDataset(ds_loc)
    return ruaumoko_ds.once


def _rfc3339_to_timestamp(dt):
    """
    Convert from a RFC3339 timestamp to a UNIX timestamp.
    """
    return strict_rfc3339.rfc3339_to_timestamp(dt)


def _timestamp_to_rfc3339(dt):
    """
    Convert from a UNIX timestamp to a RFC3339 timestamp.
    """
    return strict_rfc3339.timestamp_to_rfc3339_utcoffset(dt)


class APIException(Exception):
    __doc__ = '\n    Base API exception.\n    '
    status_code = 500


class RequestException(APIException):
    __doc__ = '\n    Raised if request is invalid.\n    '
    status_code = 400


class InvalidDatasetException(APIException):
    __doc__ = '\n    Raised if the dataset specified in the request is invalid.\n    '
    status_code = 404


class PredictionException(APIException):
    __doc__ = '\n    Raised if the solver raises an exception.\n    '
    status_code = 500


class InternalException(APIException):
    __doc__ = '\n    Raised when an internal error occurs.\n    '
    status_code = 500


class NotYetImplementedException(APIException):
    __doc__ = '\n    Raised when the functionality has not yet been implemented.\n    '
    status_code = 501


def parse_request(data):
    """
    Parse the request.
    """
    req = {'version': API_VERSION}
    req['launch_latitude'] = _extract_parameter(data, 'launch_latitude', float, validator=lambda x: -90 <= x <= 90)
    req['launch_longitude'] = _extract_parameter(data, 'launch_longitude', float, validator=lambda x: 0 <= x < 360)
    req['launch_datetime'] = _extract_parameter(data, 'launch_datetime', _rfc3339_to_timestamp)
    req['launch_altitude'] = _extract_parameter(data, 'launch_altitude', float, ignore=True)
    if req['launch_altitude'] is None:
        try:
            req['launch_altitude'] = ruaumoko_ds().get(req['launch_latitude'], req['launch_longitude'])
        except Exception:
            raise InternalException('Internal exception experienced whilst ' + "looking up 'launch_altitude'.")

    req['profile'] = _extract_parameter(data, 'profile', str, PROFILE_STANDARD)
    launch_alt = req['launch_altitude']
    if req['profile'] == PROFILE_STANDARD:
        req['ascent_rate'] = _extract_parameter(data, 'ascent_rate', float, validator=lambda x: x > 0)
        req['burst_altitude'] = _extract_parameter(data, 'burst_altitude', float, validator=lambda x: x > launch_alt)
        req['descent_rate'] = _extract_parameter(data, 'descent_rate', float, validator=lambda x: x > 0)
    else:
        if req['profile'] == PROFILE_FLOAT:
            req['ascent_rate'] = _extract_parameter(data, 'ascent_rate', float, validator=lambda x: x > 0)
            req['float_altitude'] = _extract_parameter(data, 'float_altitude', float, validator=lambda x: x > launch_alt)
            req['stop_datetime'] = _extract_parameter(data, 'stop_datetime', _rfc3339_to_timestamp, validator=lambda x: x > req['launch_datetime'])
        else:
            raise RequestException("Unknown profile '%s'." % req['profile'])
    req['dataset'] = _extract_parameter(data, 'dataset', _rfc3339_to_timestamp, LATEST_DATASET_KEYWORD)
    return req


def _extract_parameter(data, parameter, cast, default=None, ignore=False, validator=None):
    """
    Extract a parameter from the POST request and raise an exception if any
    parameter is missing or invalid.
    """
    if parameter not in data:
        if default is None and not ignore:
            raise RequestException("Parameter '%s' not provided in request." % parameter)
        return default
        try:
            result = cast(data[parameter])
        except Exception:
            raise RequestException("Unable to parse parameter '%s': %s." % (
             parameter, data[parameter]))

        if validator is not None and not validator(result):
            raise RequestException("Invalid value for parameter '%s': %s." % (
             parameter, data[parameter]))
        return result


def run_prediction(req):
    """
    Run the prediction.
    """
    resp = {'request': req, 
     'prediction': []}
    ds_dir = app.config.get('WIND_DATASET_DIR', WindDataset.DEFAULT_DIRECTORY)
    try:
        if req['dataset'] == LATEST_DATASET_KEYWORD:
            tawhiri_ds = WindDataset.open_latest(persistent=True, directory=ds_dir)
        else:
            tawhiri_ds = WindDataset(datetime.fromtimestamp(req['dataset']), directory=ds_dir)
    except IOError:
        raise InvalidDatasetException('No matching dataset found.')
    except ValueError as e:
        raise InvalidDatasetException(*e.args)

    resp['request']['dataset'] = tawhiri_ds.ds_time.strftime('%Y-%m-%dT%H:00:00Z')
    if req['profile'] == PROFILE_STANDARD:
        stages = models.standard_profile(req['ascent_rate'], req['burst_altitude'], req['descent_rate'], tawhiri_ds, ruaumoko_ds())
    else:
        if req['profile'] == PROFILE_FLOAT:
            stages = models.float_profile(req['ascent_rate'], req['float_altitude'], req['stop_datetime'], tawhiri_ds)
        else:
            raise InternalException('No implementation for known profile.')
        try:
            result = solver.solve(req['launch_datetime'], req['launch_latitude'], req['launch_longitude'], req['launch_altitude'], stages)
        except Exception as e:
            raise PredictionException("Prediction did not complete: '%s'." % str(e))

        if req['profile'] == PROFILE_STANDARD:
            resp['prediction'] = _parse_stages(['ascent', 'descent'], result)
        else:
            if req['profile'] == PROFILE_FLOAT:
                resp['prediction'] = _parse_stages(['ascent', 'float'], result)
            else:
                raise InternalException('No implementation for known profile.')
    for key in resp['request']:
        if 'datetime' in key:
            resp['request'][key] = _timestamp_to_rfc3339(resp['request'][key])

    return resp


def _parse_stages(labels, data):
    """
    Parse the predictor output for a set of stages.
    """
    assert len(labels) == len(data)
    prediction = []
    for index, leg in enumerate(data):
        stage = {}
        stage['stage'] = labels[index]
        stage['trajectory'] = [{'latitude': lat, 'longitude': lon, 'altitude': alt, 'datetime': _timestamp_to_rfc3339(dt)} for dt, lat, lon, alt in leg]
        prediction.append(stage)

    return prediction


@app.route('/api/v{0}/'.format(API_VERSION), methods=['GET'])
def main():
    """
    Single API endpoint which accepts GET requests.
    """
    g.request_start_time = time.time()
    response = run_prediction(parse_request(request.args))
    g.request_complete_time = time.time()
    response['metadata'] = _format_request_metadata()
    return jsonify(response)


@app.errorhandler(APIException)
def handle_exception(error):
    """
    Return correct error message and HTTP status code for API exceptions.
    """
    response = {}
    response['error'] = {'type': type(error).__name__, 
     'description': str(error)}
    g.request_complete_time = time.time()
    response['metadata'] = _format_request_metadata()
    return (jsonify(response), error.status_code)


def _format_request_metadata():
    """
    Format the request metadata for inclusion in the response.
    """
    return {'start_datetime': _timestamp_to_rfc3339(g.request_start_time), 
     'complete_datetime': _timestamp_to_rfc3339(g.request_complete_time)}