# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/ponyexpress/gearman_interface.py
# Compiled at: 2011-02-06 15:08:18
from core import PonyExpress
import gearman, json
config = None

class JSONDataEncoder(gearman.DataEncoder):

    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)


class PonyExpressClient(PonyExpress, gearman.GearmanClient):
    """
        Gearman interface
        """
    data_encoder = JSONDataEncoder

    def to_gearman(self, gearman_servers=None, **kwargs):
        """
                gearman_servers:
                        An array of one or more gearman servers. Defaults to ['localhost:4730']
                        All other keyword arguments are passed to GearmanClient.submit_job()

                Example to create a job that runs in the background:
                >>> to_gearman(background=True, wait_until_complete=False)

                More about submitting gearman jobs:
                        http://packages.python.org/gearman/client.html#submitting-jobs
                """
        gearman_client = gearman.GearmanClient(gearman_servers or ['localhost:4730'])
        params = self.to_json()
        job = gearman_client.submit_job('ponyexpress', self.to_json(), **kwargs)
        if not kwargs.get('background') and not kwargs.get('wait_until_complete'):
            status = lambda job: job.result if job.complete else None
            rs = status(job)
            print str(rs)
            return json.loads(rs)
        else:
            return {'result': True, 'id': None}
            return

    @classmethod
    def from_gearman(cls, x, job):
        """
                Handles a job from gearman 
                """
        try:
            pony = PonyExpress.from_json(job.data)
            rs = pony.send(config=config)
            print str(rs)
            return json.dumps(rs)
        except Exception, e:
            return json.dumps(dict(result=False, id=None, error=str(e)))

        return

    @classmethod
    def start_gearman(cls, gearman_servers):
        """
                Connect to gearmand and fire up a worker
                """
        gearman_worker = gearman.GearmanWorker(gearman_servers or ['localhost:4730'])
        gearman_worker.register_task('ponyexpress', cls.from_gearman)
        gearman_worker.work()
        return True