# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/virustotal2.py
# Compiled at: 2014-05-26 03:18:14
import base64, threading
from itertools import izip_longest
import os, urlparse, re, json, time, hashlib, requests

class VirusTotal2(object):
    _SCAN_ID_RE = re.compile('^[a-fA-F0-9]{64}-[0-9]{10}$')

    def __init__(self, api_key, limit_per_min=None):
        self.api_key = api_key
        self._urls_per_retrieve = 4
        self._hashes_per_retrieve = 4
        self._ips_per_retrieve = 1
        self._domains_per_retrieve = 1
        self._urls_per_scan = 4
        self._hashes_per_scan = 25
        self._files_per_scan = 1
        self.limits = []
        self.limit_lock = threading.Lock()
        if limit_per_min:
            self.limit_per_min = limit_per_min
        else:
            self.limit_per_min = 4

    def scan(self, thing, thing_type=None, raw=False, rescan=False):
        """
        Submit a file to or URL to VirusTotal for scanning.
        Returns a VirusTotal2Report object

        Keyword arguments:
         thing - a file name on the local system or a URL or list of URLs
         thing_type - Optional, a hint to the function as to what you are sending it
         raw - Optional, if True return the raw JSON output from VT

        Raises a TypeError if it gets something other than a file or URL/list of URLs
        Raises an TypeError if VirusTotal returns something we can't parse.
        """
        thing_id = self._whatisthing(thing)
        if thing_type is None:
            thing_type = thing_id
        data = {'apikey': self.api_key}
        if thing_type == 'url':
            endpoint = 'https://www.virustotal.com/vtapi/v2/url/scan'
            if isinstance(thing, list):
                data['url'] = ('\n').join(thing)
            else:
                data['url'] = thing
            self._limit_call_handler()
            result = requests.post(endpoint, data=data).text
        elif thing_type == 'file_name' or thing_type == 'base64':
            with open(thing, 'rb') as (f):
                if thing_type == 'base64':
                    content = base64.b64decode(f.read())
                else:
                    content = f.read()
            if rescan:
                endpoint = 'https://www.virustotal.com/vtapi/v2/file/rescan'
                data['resource'] = hashlib.sha256(content).hexdigest()
                self._limit_call_handler()
                result = requests.post(endpoint, data=data).text
            else:
                endpoint = 'https://www.virustotal.com/vtapi/v2/file/scan'
                self._limit_call_handler()
                result = requests.post(endpoint, data=data, files={'file': (os.path.basename(thing), content)}).text
        elif thing_type == 'hash':
            if rescan:
                endpoint = 'https://www.virustotal.com/vtapi/v2/file/rescan'
                if isinstance(thing, list):
                    data['resource'] = (', ').join(thing)
                else:
                    data['resource'] = thing
                self._limit_call_handler()
                result = requests.post(endpoint, data=data).text()
            else:
                raise TypeError('Hahses can only be re-scanned, please set rescan=True')
        else:
            raise TypeError("Unable to scan type '" + thing_type + '.')
        if raw:
            return result
        else:
            return self._generate_report(result, thing_id, thing)

    def retrieve(self, thing, thing_type=None, raw=False):
        """
        Retrieve a report from VirusTotal based on a hash, IP, domain, file or URL.  NOTE: URLs must include the scheme
         (e.g. http://)
        Returns a VirusTotal2Report object

        Keyword arguments:
         thing - a file name on the local system, a URL or list of URLs,
            an IP or list of IPs, a domain or list of domains, a hash or list of hashes
         thing_type - Optional, a hint to the function as to what you are sending it
         raw - Optional, if True return the raw JSON output from VT

        Raises a TypeError if it gets something other than a filename, URL, IP domain or hash
        Raises an TypeError if VirusTotal returns something we can't parse.
        """
        thing_id = self._whatisthing(thing)
        if thing_type is None:
            thing_type = thing_id
        data = {'apikey': self.api_key}
        if thing_type == 'url':
            endpoint = 'http://www.virustotal.com/vtapi/v2/url/report'
            if isinstance(thing, list):
                list_of_lists = self._grouped(thing, self._urls_per_retrieve)
                list_of_results = []
                for group in list_of_lists:
                    data['resource'] = ('\n').join([ url for url in group if url is not None ])
                    self._limit_call_handler()
                    try:
                        ret = json.loads(requests.post(endpoint, data=data).text)
                    except:
                        raise TypeError

                    if not isinstance(ret, list):
                        ret = [ret]
                    for item in ret:
                        list_of_results.append(item)

                result = json.dumps(list_of_results)
            else:
                data['resource'] = thing
                self._limit_call_handler()
                result = requests.post(endpoint, data=data).text
        elif thing_type == 'ip':
            endpoint = 'http://www.virustotal.com/vtapi/v2/ip-address/report'
            if not isinstance(thing, list):
                thing = [
                 thing]
            list_of_results = []
            for ip in thing:
                data['ip'] = ip
                self._limit_call_handler()
                try:
                    ret = json.loads(requests.get(endpoint, params=data).text)
                except:
                    raise TypeError

                list_of_results.append(ret)

            if len(list_of_results) == 1:
                list_of_results = list_of_results[0]
            result = json.dumps(list_of_results)
        elif thing_type == 'file_name' or thing_type == 'base64':
            endpoint = 'http://www.virustotal.com/vtapi/v2/file/report'
            hashes = []
            if not isinstance(thing, list):
                thing = [
                 thing]
            for f in thing:
                fh = open(f, 'rb')
                if thing_type == 'base64':
                    content = base64.b64decode(fh.read())
                else:
                    content = fh.read()
                hashval = hashlib.sha256(content).hexdigest()
                hashes.append(hashval)

            data['resource'] = (', ').join(hashes)
            self._limit_call_handler()
            result = requests.post(endpoint, data=data).text
        elif thing_type == 'domain':
            endpoint = 'http://www.virustotal.com/vtapi/v2/domain/report'
            if isinstance(thing, list):
                raise TypeError
            data['domain'] = thing
            self._limit_call_handler()
            result = requests.get(endpoint, params=data).text
        elif thing_type == 'hash':
            endpoint = 'http://www.virustotal.com/vtapi/v2/file/report'
            if isinstance(thing, list):
                data['resource'] = (', ').join(thing)
            else:
                data['resource'] = thing
            self._limit_call_handler()
            result = requests.post(endpoint, data=data).text
        elif thing_type == 'scanid':
            raise TypeError("Can't infer the proper endpoint when given scanIDs without a thing_type that is not scanID")
        else:
            raise TypeError("Unable to scan type '" + thing_type + '.')
        if raw:
            return result
        else:
            return self._generate_report(result, thing_id, thing)

    def _generate_report(self, result, thing_id, thing):
        """
        Generate a VirusTotal2Report object based on the passed JSON
        Returns a VirusTotal2Report object

        Keyword arguments:
         result - a JSON string to parse into a report.
         thing - the item we're reporting on
         thing_id - what kind of item thing is

        Raises an TypeError if report is something we can't parse.
        """
        report = []
        if isinstance(result, basestring):
            try:
                obj = json.loads(result)
                if isinstance(obj, dict):
                    report.append(VirusTotal2Report(obj, self, thing_id, thing))
                else:
                    for i, rep in enumerate(obj):
                        report.append(VirusTotal2Report(rep, self, thing_id, thing[i]))

            except:
                raise TypeError('VT String is unparsable: ' + str(result))

        else:
            raise TypeError('VT String (which is not a string?) is unparsable: ' + str(result))
        if len(report) > 1:
            return report
        return report[0]

    def _limit_call_handler(self):
        """
        Ensure we don't exceed the N requests a minute limit by leveraging a thread lock

        Keyword arguments:
            None
        """
        with self.limit_lock:
            if self.limit_per_min <= 0:
                return
            now = time.time()
            self.limits = [ l for l in self.limits if l > now ]
            self.limits.append(now + 60)
            if len(self.limits) >= self.limit_per_min:
                time.sleep(self.limits[0] - now)

    def _grouped(self, iterable, n):
        """
        take a list of items and return a list of groups of size n.  Fill any missing values at the end with None

        Keyword arguments:
            n - the size of the groups to return
        """
        return izip_longest(fillvalue=None, *([iter(iterable)] * n))

    def _whatisthing(self, thing):
        """
        Bucket the thing it gets passed into the list of items VT supports
        Returns a sting representation of the type of parameter passed in

        Keyword arguments:
            thing - a parameter to identify
        """
        if isinstance(thing, list):
            thing = thing[0]
        if isinstance(thing, basestring) and os.path.isfile(thing):
            if thing.endswith('.base64'):
                return 'base64'
            else:
                return 'file_name'

        if not isinstance(thing, basestring):
            return 'unknown'
        else:
            if all(i in '1234567890abcdef' for i in str(thing).lower()) and len(thing) in (32,
                                                                                           40,
                                                                                           64):
                return 'hash'
            if all(i in '1234567890.' for i in thing) and len(thing) <= 15:
                return 'ip'
            if '.' in thing and '/' not in thing:
                return 'domain'
            if self._SCAN_ID_RE.match(thing):
                return 'scanid'
            if urlparse.urlparse(thing).scheme:
                return 'url'
            return 'unknown'


class VirusTotal2Report(object):

    def __init__(self, obj, parent, thing_id, query):
        super(VirusTotal2Report, self).__init__()
        self.scan = parent
        self._json = obj
        self.type = thing_id
        self.query = query
        self.update()

    def __repr__(self):
        return '<VirusTotal2 report %s (%s)>' % (
         self.id,
         self.status)

    def __iter__(self):
        if self.type == 'ip':
            for resolution in self.resolutions.iteritems():
                yield resolution

        elif self.type == 'domain':
            for resolution in self.resolutions.iteritems():
                yield resolution

        elif self.type == 'url':
            for scanner, report in self.scans.iteritems():
                yield (
                 scanner, report['result'])

        else:
            for antivirus, report in self.scans.iteritems():
                yield (
                 (
                  antivirus, report['version'], report['update']),
                 report['result'])

    def __getattr__(self, attr):
        item = {'id': 'resource', 
           'status': 'verbose_msg'}.get(attr, attr)
        try:
            return self._json[item]
        except KeyError:
            raise AttributeError(attr)

    def update(self):
        """
        Re-query the Virustotal API for new results on the current object.  If the current object is listed as
        not in VirusTotal (can be the case with IPs or domains), this function does nothing.

        Keyword arguments:
            none

        Raises:
            TypeError if we don't get JSON back from VT
        """
        if self.response_code == 0:
            return
        if self.type in ('ip', 'domain'):
            data = self.scan.retrieve(self.query, raw=True)
        else:
            if self.type == 'file_name' or self.type == 'base64':
                data = self.scan.retrieve(self.scan_id, thing_type='hash', raw=True)
            else:
                data = self.scan.retrieve(self.scan_id, thing_type=self.type, raw=True)
            try:
                self._json = json.loads(data)
            except:
                raise TypeError

    def rescan(self):
        """
        Requests a rescan of the current file.  This API only works for reports that have been generated from files or
          hashes.

        Keyword arguments:
            none

        Raises:
            TypeError if we don't get JSON back from VT
        """
        if self.type in ('file_name', 'hash'):
            data = self.scan.retrieve(self.scan_id, thing_type='hash', raw=True, rescan=True)
        else:
            raise TypeError('cannot rescan type ' + self.type)
        try:
            self._json = json.loads(data)
        except:
            raise TypeError

    def wait(self):
        """
        Wait until the Virustotal API is done scanning the current object.  If the current object is listed as not in
        VirusTotal (can be the case with IPs or domains), or we already have results this function returns immediately.

        Keyword arguments:
            none

        Raises:
            TypeError if we don't get JSON back from VT (it would pass through from the update() function)
        """
        interval = 60
        self.update()
        while self.response_code not in (1, 0):
            time.sleep(interval)
            self.update()