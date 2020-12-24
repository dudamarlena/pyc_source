# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/reportingplugins/elasticsearchreporter.py
# Compiled at: 2018-12-19 07:29:10
# Size of source mod 2**32: 4022 bytes
import datetime, os, json, fastr
from fastr.helpers.classproperty import classproperty
from fastr.plugins.reportingplugin import ReportingPlugin
from fastr.execution.job import JobState, Job
from elasticsearch import Elasticsearch

class ElasticsearchReporter(ReportingPlugin):

    def __init__(self):
        super().__init__()

    def activate(self):
        """
        Activate the reporting plugin
        """
        super().activate()
        if fastr.config.elasticsearch_host == '':
            fastr.log.info('No valid elasticsearchsearch host given, elasticsearch Reporting will be disabled!')
            self.elasticsearch_uri = None
            return
        fastr.log.info('')
        self.elasticsearch_uri = fastr.config.elasticsearch_host
        self.elasticsearch_index = fastr.config.elasticsearch_index
        fastr.log.info('ES Logging to {} at index {}'.format(self.elasticsearch_uri, self.elasticsearch_index))
        es = Elasticsearch([self.elasticsearch_uri])
        es.indices.create(index=self.elasticsearch_index, ignore=400)

    @classproperty
    def configuration_fields(cls):
        return {'elasticsearch_host': (str, '', 'The elasticsearch host to report to'), 
         'elasticsearch_index': (str, 'fastr', 'The elasticsearch index to store data in'), 
         'elasticsearch_debug': (bool, False, 'Setup elasticsearch debug mode to send stdout stderr on job succes')}

    def elasticsearch_update_status(self, job):
        es = Elasticsearch([self.elasticsearch_uri])
        es.indices.create(index=self.elasticsearch_index, ignore=400)
        node = job.node
        job_data = {'timestamp': datetime.datetime.utcnow().isoformat(), 
         'network_id': node.parent.long_id, 
         'network_version': str(node.parent.network_version), 
         'network_tmpurl': node.parent.tmpurl, 
         'run_id': node.parent.id, 
         'node': str(node), 
         'node_id': node.id, 
         'node_global_id': node.global_id, 
         'tool_name': node.tool.ns_id, 
         'tool_version': str(node.tool.command['version']), 
         'sample_index': list(job.sample_index), 
         'sample_id': list(job.sample_id), 
         'errors': str(job.errors), 
         'status': str(job.status)}
        if os.path.exists(job.extrainfofile):
            with open(job.extrainfofile) as (extra_info_file):
                extra_info = json.load(extra_info_file)
                process = extra_info.get('process')
                job_data['process'] = process
        es.index(index=self.elasticsearch_index, doc_type='fastr-job', body=job_data)

    def job_updated(self, job: Job):
        if self.elasticsearch_uri:
            self.elasticsearch_update_status(job)