# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/baseline.py
# Compiled at: 2015-09-30 11:20:13
import csv, logging, os
from random import shuffle
import time, urlparse
from centinel.experiment import Experiment
from centinel.primitives import dnslib
from centinel.primitives import tls
import centinel.primitives.http as http, centinel.primitives.traceroute as traceroute

class BaselineExperiment(Experiment):
    name = 'baseline'
    input_files = [
     'country.csv', 'world.csv']

    def __init__(self, input_files):
        self.input_files = input_files
        self.results = []
        if self.params is not None:
            if 'traceroute_methods' in self.params:
                self.traceroute_methods = self.params['traceroute_methods']
        if os.geteuid() != 0:
            logging.info('Centinel is not running as root, traceroute will be limited to UDP.')
            if self.traceroute_methods:
                self.traceroute_methods = [
                 'udp']
        return

    def run(self):
        for input_file in self.input_files.items():
            logging.info('Testing input file %s...' % input_file[0])
            self.results.append(self.run_file(input_file))

    def run_file(self, input_file):
        file_name, file_contents = input_file
        result = {'file_name': file_name}
        run_start_time = time.time()
        http_results = {}
        http_inputs = []
        tls_results = {}
        tls_inputs = []
        dns_results = {}
        dns_inputs = []
        traceroute_results = {}
        traceroute_inputs = []
        url_metadata_results = {}
        file_metadata = {}
        file_comments = []
        index_row = None
        comments = ''
        csvreader = csv.reader(file_contents, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[0][0] == '#':
                row = row[0][1:].strip()
                if len(row.split(':')) > 1:
                    key, value = row.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    file_metadata[key] = value
                else:
                    file_comments.append(row)
                continue
            if row[0].strip().lower() == 'url':
                index_row = row
                continue
            url = row[0].strip()
            if url is None:
                continue
            meta = row[1:]
            http_ssl = False
            ssl_port = 443
            http_path = '/'
            try:
                urlparse_object = urlparse.urlparse(url)
                http_netloc = urlparse_object.netloc
                if http_netloc == '':
                    urlparse_object = urlparse.urlparse('//%s' % url)
                    http_netloc = urlparse_object.netloc
                domain_name = http_netloc.split(':')[0]
                http_path = urlparse_object.path
                if http_path == '':
                    http_path = '/'
                if urlparse_object.scheme == 'https':
                    http_ssl = True
                    if len(http_netloc.split(':')) == 2:
                        ssl_port = http_netloc.split(':')[1]
            except Exception as exp:
                logging.exception('%s: failed to parse URL: %s' % (url, exp))
                http_netloc = url
                http_ssl = False
                ssl_port = 443
                http_path = '/'
                domain_name = url

            http_inputs.append({'host': http_netloc, 'path': http_path, 
               'ssl': http_ssl, 
               'url': url})
            if http_ssl:
                tls_inputs.append('%s:%s' % (domain_name, ssl_port))
            dns_inputs.append(domain_name)
            traceroute_inputs.append(domain_name)
            url_metadata_results[url] = meta

        shuffle(http_inputs)
        start = time.time()
        logging.info('Running HTTP GET requests...')
        result['http'] = http.get_requests_batch(http_inputs)
        elapsed = time.time() - start
        logging.info('HTTP GET requests took %d seconds for %d URLs.' % (
         elapsed,
         len(http_inputs)))
        shuffle(tls_inputs)
        start = time.time()
        logging.info('Running TLS certificate requests...')
        result['tls'] = tls.get_fingerprint_batch(tls_inputs)
        elapsed = time.time() - start
        logging.info('TLS certificate requests took %d seconds for %d domains.' % (
         elapsed,
         len(tls_inputs)))
        shuffle(dns_inputs)
        start = time.time()
        logging.info('Running DNS requests...')
        result['dns'] = dnslib.lookup_domains(dns_inputs)
        elapsed = time.time() - start
        logging.info('DNS requests took %d seconds for %d domains.' % (
         elapsed,
         len(dns_inputs)))
        for method in self.traceroute_methods:
            shuffle(traceroute_inputs)
            start = time.time()
            logging.info('Running %s traceroutes...' % method.upper())
            result['traceroute.%s' % method] = traceroute.traceroute_batch(traceroute_inputs, method)
            elapsed = time.time() - start
            logging.info('Traceroutes took %d seconds for %d domains.' % (
             elapsed, len(traceroute_inputs)))

        if index_row is not None:
            indexed_url_metadata = {}
            for url, meta in url_metadata_results.items():
                try:
                    indexed_meta = {}
                    for i in range(1, len(index_row)):
                        indexed_meta[index_row[i]] = meta[(i - 1)]

                    indexed_url_metadata[url] = indexed_meta
                except:
                    indexed_url_metadata[url] = indexed_meta
                    continue

            url_metadata_results = indexed_url_metadata
        result['url_metadata'] = url_metadata_results
        result['file_metadata'] = file_metadata
        result['file_comments'] = file_comments
        run_finish_time = time.time()
        elapsed = run_finish_time - run_start_time
        result['total_time'] = elapsed
        logging.info('Testing took a total of %d seconds.' % elapsed)
        return result