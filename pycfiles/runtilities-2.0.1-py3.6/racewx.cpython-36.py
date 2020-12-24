# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\racewx.py
# Compiled at: 2020-02-26 14:50:54
# Size of source mod 2**32: 10631 bytes
"""
racewx - determine weather for race day
===================================================
"""
import argparse, urllib.request, urllib.parse, urllib.error, json, csv, time, math, os.path, pytz, httplib2, gpxpy, gpxpy.geo
from running.running import version
from running import *
from loutilities import timeu
from loutilities import apikey
_ak = apikey.ApiKey('Lou King', 'running')
try:
    _FORECASTIOKEY = _ak.getkey('forecastio')
except apikey.unknownKey:
    print("'forecastio' key needs to be configured using apikey")
    raise

WXPERIOD = 300
HTTPTIMEOUT = 5
HTTPTZ = httplib2.Http(timeout=HTTPTIMEOUT)
HTTPWX = httplib2.Http(timeout=HTTPTIMEOUT, disable_ssl_certificate_validation=True)
DPa = 17.271
DPb = 237.7
HIc = [
 None, -42.379, 2.04901523, 10.14333127, -0.22475541, -0.00683783, -0.05481717, 0.00122874, 0.00085282, -1.99e-06]

def dewpoint(temp, humidity):
    """
    approximate dewpoint from temp and relative humidity
    from http://www.meteo-blog.net/2012-05/dewpoint-calculation-script-in-python/
    
    :param temp: temperature (fahrenheit)
    :param humidity: relative humidity (1-100)
    :rtype: dewpoint (fahrenheit)
    """
    tempC = celsius(temp)
    Td = DPb * gamma(tempC, humidity) / (DPa - gamma(tempC, humidity))
    return fahrenheit(Td)


def gamma(tempC, humidity):
    """
    gamma function for dewpoint calculation
    from http://www.meteo-blog.net/2012-05/dewpoint-calculation-script-in-python/
    
    :param tempC: temperature (celcius)
    :param humidity: relative humidity (1-100)
    """
    g = DPa * tempC / (DPb + tempC) + math.log(humidity / 100.0)
    return g


def windchill(temp, windspeed):
    """
    wind chill calculation
    from http://en.wikipedia.org/wiki/Wind_chill#North_American_and_UK_wind_chill_index
    
    :param temp: temperature (fahrenheit)
    :param windspeed: wind speed (mph)
    :rtype: windchill (fahrenheit) or None if temp > 50 or windspeed < 3 mph
    """
    if temp <= 50:
        if windspeed >= 3.0:
            return 35.74 + 0.6215 * temp - 35.75 * windspeed ** 0.16 + 0.4275 * temp * windspeed ** 0.16
    return


def heatindex(temp, humidity):
    """
    heat index calculation
    from http://en.wikipedia.org/wiki/Heat_index#Formula
    
    :param temp: temperature (fahrenheit)
    :param humidity: relative humidity (0-100)
    :rtype: heat index (fahrenheit) or None if temp < 80 or humidity < 40
    """
    if temp >= 80:
        if humidity >= 40:
            return HIc[1] + HIc[2] * temp + HIc[3] * humidity + HIc[4] * temp * humidity + HIc[5] * temp ** 2 + HIc[6] * humidity ** 2 + HIc[7] * temp ** 2 * humidity + HIc[8] * temp * humidity ** 2 + HIc[9] * temp ** 2 * humidity ** 2
    return


def celsius(temp):
    """
    convert Fahrenheit temp to Celcius
    
    :param temp: temperature in Fahrenheit
    :rtype: temperature in Celcius
    """
    return (temp - 32) / 1.8


def fahrenheit(temp):
    """
    convert Celcius temp to Fahrenheit
    
    :param temp: temperature in Celcius
    :rtype: temperature in Fahrenheit
    """
    return temp * 1.8 + 32


def gettzid(lat, lon):
    """
    get time zone name based on lat, lon
    uses google maps api
    
    :param lat: latitude in decimal degrees
    :param lon: longitude in decimal degrees
    """
    params = {'location':'{lat},{lon}'.format(lat=lat, lon=lon), 
     'timestamp':0, 
     'sensor':'true'}
    body = urllib.parse.urlencode(params)
    url = 'https://maps.googleapis.com/maps/api/timezone/json?{body}'.format(body=body)
    resp, jsoncontent = HTTPTZ.request(url)
    if resp.status != 200:
        raise accessError('URL response status = {0}'.format(resp.status))
    content = json.loads(jsoncontent)
    if content['status'] != 'OK':
        raise accessError('URL content status = {0}'.format(content['status']))
    return content['timeZoneId']


def getwx(lat, lon, etime):
    """
    get weather from forecast.io for specified latitude, longitude, time
    
    :param lat: latitude
    :param long: longitude
    :param etime: time in unix format (that is, seconds since midnight GMT on 1 Jan 1970)
    :rtype: weather dict for that location, time, e.g., {u'temperature': 46.59, u'precipType': u'rain', u'humidity': 0.62, u'cloudCover': 0.53, u'summary': u'Mostly Cloudy', u'pressure': 1014.87, u'windSpeed': 8.63, u'visibility': 10, u'time': 1366036200, u'windBearing': 326, u'icon': u'partly-cloudy-day'}
    """
    url = 'http://api.forecast.io/forecast/{apikey}/{lat},{lon},{time}'.format(apikey=_FORECASTIOKEY, lat=lat, lon=lon, time=etime)
    resp, jsoncontent = HTTPWX.request(url)
    if resp.status != 200:
        raise accessError('URL response status = {0}'.format(resp.status))
    content = json.loads(jsoncontent)
    return content['currently']


def main():
    parser = argparse.ArgumentParser(version=('{0} {1}'.format('running', version.__version__)))
    parser.add_argument('gpxfile', help='gpx formatted file')
    parser.add_argument('racestarttime', help="time of race start in '%%Y-%%m-%%dT%%H:%%M' format")
    parser.add_argument('-o', '--output', help='name of output file (default %(default)s)', default='racewx.csv')
    args = parser.parse_args()
    gpxfile = args.gpxfile
    racestarttime = args.racestarttime
    timrace = timeu.asctime('%Y-%m-%dT%H:%M')
    racestartdt = timrace.asc2dt(racestarttime)
    output = args.output
    _GPX = open(gpxfile, 'r')
    gpx = gpxpy.parse(_GPX)
    wxdata = []
    lasttime = None
    exectime = int(round(time.time()))
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                pepoch = timeu.dt2epoch(point.time)
                if not lasttime or pepoch - lasttime >= WXPERIOD:
                    plon = point.longitude
                    plat = point.latitude
                    if not lasttime:
                        starttime = pepoch
                        tzid = gettzid(plat, plon)
                        tz = pytz.timezone(tzid)
                        racestartlocdt = tz.normalize(tz.localize(racestartdt))
                        racestartepoch = timeu.dt2epoch(racestartlocdt)
                        shift = racestartepoch - starttime
                    targtime = timeu.dt2epoch(point.time) + shift
                    wx = getwx(plat, plon, targtime)
                    wx['lat'] = plat
                    wx['lon'] = plon
                    wx['dewpoint'] = dewpoint(wx['temperature'], wx['humidity'] * 100)
                    wx['windchill'] = windchill(wx['temperature'], wx['windSpeed'])
                    wx['heatindex'] = heatindex(wx['temperature'], wx['humidity'] * 100)
                    wxdata.append(wx)
                    lasttime = pepoch

    if not os.path.exists(output):
        writeheader = True
        _WX = open(output, 'w', newline='')
    else:
        writeheader = False
        _WX = open(output, 'a', newline='')
    heading = ['exectime', 'time', 'lat', 'lon', 'temperature', 'humidity', 'dewpoint', 'windchill', 'heatindex', 'precipType', 'precipProbability', 'precipIntensity', 'windSpeed', 'windBearing', 'cloudCover', 'summary', 'pressure', 'visibility']
    WX = csv.DictWriter(_WX, heading, extrasaction='ignore')
    if writeheader:
        WX.writeheader()
    for wx in wxdata:
        wx['exectime'] = exectime
        WX.writerow(wx)

    _WX.close()


if __name__ == '__main__':
    main()