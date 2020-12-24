# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/rpc/controller.py
# Compiled at: 2018-11-30 15:05:10
# Size of source mod 2**32: 6862 bytes
import logging
from mercury.common.asyncio.endpoints import StaticEndpointController, async_endpoint
from mercury.common.exceptions import EndpointError, MercuryUserError
from mercury.common.mongo import serialize_object_id
from mercury.rpc.jobs import Job, tasks
log = logging.getLogger(__name__)

class RPCController(StaticEndpointController):

    def __init__(self, inventory_client, jobs_collection, tasks_collection):
        super(RPCController, self).__init__()
        self.inventory_client = inventory_client
        self.jobs_collection = jobs_collection
        self.tasks_collection = tasks_collection

    @staticmethod
    def prepare_for_serialization(obj):
        """Converts object_id to a string and a datetime object to ctime format
        :param obj: probably a task or a job document
        :return: the object reference
        """
        serialize_object_id(obj)
        if obj.get('ttl_time_completed'):
            obj['ttl_time_completed'] = obj['ttl_time_completed'].ctime()
        return obj

    @async_endpoint('get_job')
    async def get_job(self, job_id, projection=None):
        """Gets a job from the job_collection. Jobs expire quickly.

        :param job_id: The Id of the job to get
        :param projection: A mongodb projection. https://goo.gl/kB2g26
        :return: A job object
        """
        job = await self.jobs_collection.find_one({'job_id': job_id}, projection=projection)
        if not job:
            return
        return self.prepare_for_serialization(job)

    @async_endpoint('get_job_status')
    async def get_job_status--- This code section failed: ---

 L.  56         0  LOAD_STR                 'ERROR'
                2  LOAD_STR                 'TIMEOUT'
                4  LOAD_STR                 'EXCEPTION'
                6  BUILD_LIST_3          3 
                8  STORE_FAST               'error_states'

 L.  57        10  LOAD_FAST                'self'
               12  LOAD_ATTR                jobs_collection
               14  LOAD_METHOD              find_one
               16  LOAD_STR                 'job_id'
               18  LOAD_FAST                'job_id'
               20  BUILD_MAP_1           1 
               22  CALL_METHOD_1         1  '1 positional argument'
               24  GET_AWAITABLE    
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  STORE_FAST               'job'

 L.  58        32  LOAD_FAST                'job'
               34  POP_JUMP_IF_TRUE     40  'to 40'

 L.  59        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L.  61        40  LOAD_FAST                'self'
               42  LOAD_ATTR                tasks_collection
               44  LOAD_METHOD              find

 L.  62        46  LOAD_STR                 'job_id'
               48  LOAD_FAST                'job_id'
               50  BUILD_MAP_1           1 
               52  LOAD_CONST               1
               54  LOAD_CONST               1
               56  LOAD_CONST               0
               58  LOAD_CONST               ('task_id', 'status', '_id')
               60  BUILD_CONST_KEY_MAP_3     3 
               62  CALL_METHOD_2         2  '2 positional arguments'
               64  STORE_FAST               'tasks'

 L.  64        66  LOAD_CONST               False
               68  LOAD_FAST                'job'
               70  LOAD_STR                 'has_failures'
               72  STORE_SUBSCR     

 L.  65        74  BUILD_LIST_0          0 
               76  LOAD_FAST                'job'
               78  LOAD_STR                 'tasks'
               80  STORE_SUBSCR     

 L.  67        82  SETUP_LOOP          164  'to 164'
               84  LOAD_FAST                'tasks'
               86  GET_AITER        
             88_0  COME_FROM           140  '140'
               88  SETUP_EXCEPT        102  'to 102'
               90  GET_ANEXT        
               92  LOAD_CONST               None
               94  YIELD_FROM       
               96  STORE_FAST               'task'
               98  POP_BLOCK        
              100  JUMP_FORWARD        112  'to 112'
            102_0  COME_FROM_EXCEPT     88  '88'
              102  DUP_TOP          
              104  LOAD_GLOBAL              StopAsyncIteration
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_TRUE    152  'to 152'
              110  END_FINALLY      
            112_0  COME_FROM           100  '100'

 L.  68       112  LOAD_FAST                'job'
              114  LOAD_STR                 'tasks'
              116  BINARY_SUBSCR    
              118  LOAD_METHOD              append
              120  LOAD_GLOBAL              serialize_object_id
              122  LOAD_FAST                'task'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  POP_TOP          

 L.  69       130  LOAD_FAST                'task'
              132  LOAD_STR                 'status'
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'error_states'
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE    88  'to 88'

 L.  70       142  LOAD_CONST               True
              144  LOAD_FAST                'job'
              146  LOAD_STR                 'has_failures'
              148  STORE_SUBSCR     
              150  JUMP_BACK            88  'to 88'
            152_0  COME_FROM           108  '108'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          
              158  POP_EXCEPT       
              160  POP_TOP          
              162  POP_BLOCK        
            164_0  COME_FROM_LOOP       82  '82'

 L.  72       164  LOAD_FAST                'self'
              166  LOAD_METHOD              prepare_for_serialization
              168  LOAD_FAST                'job'
              170  CALL_METHOD_1         1  '1 positional argument'
              172  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 88_0

    @async_endpoint('get_job_tasks')
    async def get_job_tasks(self, job_id, projection=None):
        """Get tasks belonging to a job

        :param job_id: The id of a job (UUID)
        :param projection: A mongodb projection. https://goo.gl/kB2g26
        :return: dictionary containing top level keys count and jobs
        """
        c = self.tasks_collection.find({'job_id': job_id}, projection=projection)
        count = await c.count()
        tasks = []
        async for task in c:
            tasks.append(self.prepare_for_serialization(task))

        return {'count':count,  'tasks':tasks}

    @async_endpoint('get_task')
    async def get_task(self, task_id):
        """Get a single task

        :param task_id: The id of the task (UUID)
        :return: The task object (dict)
        """
        task = await self.tasks_collection.find_one({'task_id': task_id})
        if not task:
            return
        return self.prepare_for_serialization(task)

    @async_endpoint('get_active_tasks_by_mercury_id')
    async def get_active_tasks_by_mercury_id(self, mercury_id):
        """Gets all active tasks associated with specified mercury id

        :param mercury_id:
        :return: dictionary containing tasks list and count
        """
        c = self.tasks_collection.find({'mercury_id':mercury_id,  'time_completed':None})
        count = await c.count()
        tasks = []
        async for task in c:
            tasks.append(self.prepare_for_serialization(task))

        return {'count':count,  'tasks':tasks}

    @async_endpoint('get_jobs')
    async def get_jobs(self, projection=None):
        """Get active jobs. The jobs collection is made ephemeral via a ttl key;
        this collection should not grow very large

        :param projection: A mongodb projection. https://goo.gl/kB2g26
        :return: dictionary containing top level keys count and jobs
        """
        projection = projection or {'instruction': 0}
        c = self.jobs_collection.find({}, projection=projection).sort'time_created'1
        count = await c.count()
        jobs = []
        async for job in c:
            jobs.append(self.prepare_for_serialization(job))

        return {'count':count, 
         'jobs':jobs}

    @async_endpoint('create_job')
    async def create_job(self, query, instruction):
        """Create a job

        :param query: Query representing targets of the instruction
        :param instruction: An instruction or preprocessor directive. See the
        full documentation regarding instruction syntax at
        http://jr0d.github.io/mercury_api
        :raises EndpointException: Raised after catching a MercuryUserError as
        to conform to dispatch semantics
        :return: The job_id or None
        """
        query.update({'active': {'$ne': None}})
        active_targets = await self.inventory_client.query(query,
          projection={'active':1,  'origin':1}, limit=0, sort_direction=1)
        total_targets = active_targets['message']['total']
        targets = active_targets['message']['items']
        log.debug(f"Found {total_targets} for query {query}")
        if not total_targets:
            return
        try:
            job = Job(instruction, targets, self.jobs_collection, self.tasks_collection)
        except MercuryUserError as mue:
            try:
                raise EndpointError(str(mue), 'create_job')
            finally:
                mue = None
                del mue

        await job.insert()
        job.enqueue_tasks()
        return {'job_id':str(job.job_id), 
         'targets':total_targets}

    @async_endpoint('update_task')
    async def update_task(self, update_data):
        self.validate_required['task_id']update_data
        return await tasks.update_taskupdate_dataself.tasks_collection

    @async_endpoint('complete_task')
    async def complete_task(self, return_data):
        self.validate_required['task_id',
         'job_id',
         'status',
         'message']return_data
        return await tasks.complete_task(return_data, self.jobs_collection, self.tasks_collection)