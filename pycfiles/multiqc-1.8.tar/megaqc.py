# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/utils/megaqc.py
# Compiled at: 2019-11-20 10:26:38
""" MultiQC code to export data to MegaQC / flat JSON files """
from __future__ import print_function
import gzip, io, json, os, requests
from multiqc import config
log = config.logger

class MQCJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if callable(obj):
            try:
                return obj(1)
            except:
                return

        return json.JSONEncoder.default(self, obj)


def multiqc_dump_json(report):
    exported_data = dict()
    export_vars = {'report': [
                'data_sources',
                'general_stats_data',
                'general_stats_headers',
                'multiqc_command',
                'plot_data',
                'saved_raw_data'], 
       'config': [
                'analysis_dir',
                'creation_date',
                'git_hash',
                'intro_text',
                'report_comment',
                'report_header_info',
                'script_path',
                'short_version',
                'subtitle',
                'title',
                'version']}
    for s in export_vars:
        for k in export_vars[s]:
            try:
                if s == 'config':
                    d = {('{}_{}').format(s, k): getattr(config, k)}
                elif s == 'report':
                    d = {('{}_{}').format(s, k): getattr(report, k)}
                json.dumps(d, cls=MQCJSONEncoder, ensure_ascii=False)
                exported_data.update(d)
            except (TypeError, KeyError, AttributeError):
                log.warn(("Couldn't export data key '{}.{}'").format(s, k))

        exported_data['config_analysis_dir_abs'] = list()
        for d in exported_data.get('config_analysis_dir', []):
            try:
                exported_data['config_analysis_dir_abs'].append(os.path.abspath(d))
            except:
                pass

    return exported_data


def multiqc_api_post(exported_data):
    headers = {'Content-Type': 'application/json', 'content-encoding': 'gzip'}
    if config.megaqc_access_token is not None:
        headers['access_token'] = config.megaqc_access_token
    post_data = json.dumps({'data': exported_data}, cls=MQCJSONEncoder, ensure_ascii=False, indent=2)
    post_data = post_data.encode('utf-8', 'ignore')
    sio_obj = io.BytesIO()
    gzfh = gzip.GzipFile(fileobj=sio_obj, mode='w')
    gzfh.write(post_data)
    gzfh.close()
    request_body = sio_obj.getvalue()
    log.debug('Sending data to MegaQC')
    log.debug(('MegaQC URL: {}').format(config.megaqc_url))
    try:
        r = requests.post(config.megaqc_url, headers=headers, data=request_body, timeout=config.megaqc_timeout)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
        log.error(('Timed out when sending data: {}').format(e))
    except requests.exceptions.ConnectionError:
        log.error(("Couldn't connect to MegaQC URL {}").format(config.megaqc_url))
    except Exception as e:
        log.error(('Error sending data: {}').format(e))
    else:
        try:
            api_r = json.loads(r.text)
        except Exception as e:
            log.error(('Error: JSON response could not be parsed (status code: {})').format(r.status_code))
            return

    if r.status_code == 200:
        if api_r['success']:
            log.info(('{}').format(api_r['message']))
        else:
            log.error(('Error - {}').format(api_r['message']))
    elif r.status_code == 403:
        if config.megaqc_access_token is not None:
            log.error('Error 403: Authentication error, megaqc_access_token not recognised')
        else:
            log.error('Error 403: Authentication error, megaqc_access_token is required')
    else:
        log.debug(('MegaQC API status code was {}').format(r.status_code))
        log.error(('Error - {}').format(api_r.get('message', 'Unknown problem')))
    return