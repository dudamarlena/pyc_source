# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/artillery.py
# Compiled at: 2018-01-02 10:57:42
import sys, os, glob, json, jmespath, subprocess, random, datetime

class ArtilleryDriver:

    def __init__(self, test_name, target, config_path, assertions, test_results):
        self.test_name = test_name
        self.target = target
        self.config_path = config_path
        self.test_assertions = assertions
        self.test_results = test_results
        self.artillery_aggregates = {}

    def run(self):
        results_path = self.get_results_path()
        artillery_cmd = 'artillery run %s -k -t %s -o %s' % (self.config_path, self.target, results_path)
        print ('artillery command:\n{0}').format(artillery_cmd)
        artillery_cmd_array = artillery_cmd.split(' ')
        last_line = ''
        process = subprocess.Popen(artillery_cmd_array, stdout=subprocess.PIPE)
        for c in iter(lambda : process.stdout.read(1), ''):
            sys.stdout.write(c)

        results_dict = load_dictionary(results_path)
        if self.test_name in self.artillery_aggregates:
            print 'name collision: %s is already included in test results' % self.test_name
            self.test_name = '%s-%s' % (self.test_name, random.randint(1, 10))
            print 'saving results as %s' % self.test_name
        self.artillery_aggregates[self.test_name] = {}
        if 'aggregate' in results_dict:
            self.artillery_aggregates[self.test_name] = results_dict['aggregate']
        self.test_results.append_results_file(results_path)
        self.assert_results()

    def assert_results(self):
        if 'p95_sec' in self.test_assertions:
            value_ms = self.get_p95()
            if value_ms:
                value_sec = value_ms / 1000
                threshold_sec = self.test_assertions['p95_sec']
                threshold_ms = 1000 * threshold_sec
                self.assert_threshold(value_ms, threshold_ms, 'p95 latency exceeded threshold\n' + 'measured: %s, threshold: %s' % (value_sec, threshold_sec))
            else:
                msg = 'p95 latency is null, so test deemed a failure. \n' + 'increase test duration?'
                self.test_results.failing_test(self.test_name, msg)
        if 'median_sec' in self.test_assertions:
            value_ms = self.get_median()
            value_sec = value_ms / 1000
            threshold_sec = self.test_assertions['median_sec']
            threshold_ms = 1000 * threshold_sec
            self.assert_threshold(value_ms, threshold_ms, 'median latency exceeded threshold\n' + 'measured: %s, threshold: %s' % (value_sec, threshold_sec))

    def assert_threshold(self, value_ms, threshold_ms, failure_msg):
        if value_ms > threshold_ms:
            self.test_results.failing_test(self.test_name, failure_msg)
        else:
            self.test_results.passing_test(self.test_name)

    def create_config_file(self):
        configs_path = os.path.join('/tmp', '%s.json' % self.test_name)
        write_dictionary(self.test_description, configs_path)
        return configs_path

    def get_results_path(self):
        timestamp = ('{:%Y-%m-%d.%H:%M:%S}').format(datetime.datetime.now())
        results_path = os.path.join('/tmp/artillery', '%s.%s' % (self.test_name, timestamp))
        if not os.path.exists('/tmp/artillery'):
            os.makedirs('/tmp/artillery')
        return results_path

    def load_results(self):
        results_file_search_str = 'results/%s.%s.*' % (test_name, env)
        all_results = filter(os.path.isfile, glob.glob(results_file_search_str))
        all_results.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        self.most_recent_results = {}
        if len(all_results) >= 1:
            self.most_recent_results = load_dictionary(all_results[0])

    def get_p95(self):
        return jmespath.search('latency.p95', self.artillery_aggregates[self.test_name])

    def get_median(self):
        return jmespath.search('latency.median', self.artillery_aggregates[self.test_name])

    def get_errors(self):
        return jmespath.search('errors', self.artillery_aggregates[self.test_name])

    def get_bad_http_status_counts(self):
        return get_bad_http_status_counts(self.artillery_aggregates[self.test_name])


def get_bad_http_status_counts(results_dict):
    codes = jmespath.search('codes', results_dict)
    bad_status_count = 0
    if codes:
        for code in codes:
            if code not in ('200', '201'):
                bad_status_count += codes[code]

    return bad_status_count


def load_dictionary(file_path):
    dictionary = {}
    if os.path.exists(file_path):
        with open(file_path) as (file_path_fp):
            file_contents = file_path_fp.read()
            dictionary = json.loads(file_contents)
    return dictionary


def write_dictionary(dict, file_w_path):
    dict_str = json.dumps(dict, indent=2)
    file_path = os.path.dirname(file_w_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)
    with open(file_w_path, 'w') as (file_path_fp):
        file_path_fp.write(dict_str)


def delete_results():
    files = filter(os.path.isfile, glob.glob('/results/*'))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    if len(files) >= 1:
        for file in files:
            os.remove(file)


def rebase():
    test_results_prefixes = get_test_prefixes()
    for prefix in test_results_prefixes:
        search_pattern = 'results/%s.*' % prefix
        files = filter(os.path.isfile, glob.glob(search_pattern))
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        if len(files) >= 1:
            file = files[0]
            results = load_dictionary(file)
            filename = os.path.basename(files[0])
            destination = os.path.join('baselines', filename)
            print 'saving aggregates from: %s to: %s' % (files[0], destination)
            with open(destination, 'w') as (outfile):
                json.dump({'aggregate': results['aggregate']}, outfile, indent=2)


def get_test_prefixes():
    test_results_prefixes = set()
    files = filter(os.path.isfile, glob.glob('./results/*'))
    for file_path in files:
        file = os.path.basename(file_path)
        file_name_parts = file.split('.')
        if len(file_name_parts) > 2:
            test_results_prefixes.add('%s.%s' % (file_name_parts[0], file_name_parts[1]))

    return test_results_prefixes