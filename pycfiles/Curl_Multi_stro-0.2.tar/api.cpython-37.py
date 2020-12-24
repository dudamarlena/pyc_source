# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\curl_modifier\api.py
# Compiled at: 2019-07-06 08:54:03
# Size of source mod 2**32: 1599 bytes


def execute_uncurled_request(uncurled_request):
    import requests
    exec(uncurled_request)


def execute_repeated_request(curl_request, n, parallel=True):
    import uncurl, multiprocessing
    uncurled_request = uncurl.parse(curl_request)
    core_count = multiprocessing.cpu_count()
    if not parallel or core_count is 1:
        print('Serial job initiated')
        for request in range(n):
            execute_uncurled_request(uncurled_request)

    print('Parallel job initiated')
    p = multiprocessing.Pool(core_count)
    requests = [uncurled_request] * n
    job = p.map(execute_uncurled_request, requests)
    p.close()
    p.join()
    print('Job finished, {} requests completed'.format(len(job)))


def replace_curl_substring(curl_request, substring, replacement):
    replaced_curl = curl_request.replace(substring, replacement)
    return replaced_curl


def execute_requests_with_file_substrings(curl_request, substring, full_path_to_file):
    import uncurl
    converted_request = uncurl.parse(curl_request)
    file = open(full_path_to_file)
    line_count = 0
    print('Job initiated')
    for line in file:
        sanitised_line = line.strip('\n').replace("'", '"')
        uncurled_request = replace_curl_substring(converted_request, substring, sanitised_line)
        execute_uncurled_request(uncurled_request)
        print('Request with vector {} which replaced substring {} successful'.format(sanitised_line, substring))
        line_count += 1

    print('Job finished, {} requests completed'.format(line_count))