# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/orqal/web.py
# Compiled at: 2019-07-10 04:12:57
# Size of source mod 2**32: 16287 bytes
import collections, concurrent, datetime, inspect, json, logging, math, os, pymongo, shutil, sys, aiohttp_jinja2, docker, jinja2
from aiohttp import web
from aiohttp_swagger import setup_swagger
from bson import ObjectId
from bson.json_util import dumps
from mongolog.handlers import MongoHandler
from pymongo import MongoClient, DESCENDING
from orqal import conf
mongo = MongoClient((conf.mongourl), replicaSet=(conf.mongo_replicaset))
routes = web.RouteTableDef()
logging.basicConfig(level=(logging.DEBUG))
log = logging.getLogger('app')
log.addHandler(MongoHandler.to(db='orqal', collection='log'))

def in_cache(data):
    if 'use_cache' in data.keys():
        if data['use_cache']:
            r = mongo.orql.jobs.find_one({'app':data['app'],  'params':data['params'],  'input':data['input']})
            if r:
                return r['_id']


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def html_index(request):
    return {}


@routes.get('/doc')
@aiohttp_jinja2.template('doc.html')
async def html_doc(request):
    return {}


@routes.get('/jobs/{status}')
@routes.get('/jobs/{status}/{page}')
@aiohttp_jinja2.template('jobs.html')
async def html_jobs_status(request):
    status = mongostatus = request.match_info.get('status')
    if mongostatus == 'todo':
        mongostatus = None
    else:
        page = request.match_info.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
    nbpages = math.ceil(mongo.orqal.jobs.count({'current_status': mongostatus}) / conf.nb_disp_jobs)
    jobs = list(mongo.orqal.jobs.find({'current_status': mongostatus}).skip((page - 1) * conf.nb_disp_jobs).limit(conf.nb_disp_jobs).sort('ctime', DESCENDING))
    headers = ['_id', 'ctime', 'current_status', 'host', 'container_id', 'image', 'input', 'wd']
    logs = [[j.get(key, '') for key in headers] for j in jobs]
    return {'status':status,  'headers':headers,  'logs':logs,  'nbpages':nbpages,  'currentpage':page}


@routes.get('/logs/{process}')
@aiohttp_jinja2.template('logs.html')
async def html_logs(request):
    process = request.match_info.get('process')
    logs = list(mongo.orqal.log.find({'module': process}).sort([('time', pymongo.DESCENDING)]))
    headers = ['levelname', 'time', 'message']
    logs = [[j.get(key, '') for key in headers] for j in logs]
    return {'process':process,  'logs':logs}


@routes.get('/api/job/{id}', allow_head=False)
async def job_get(request):
    """
    ---
    summary:  Retrieve job informations
    parameters:
        - in: path
          name: id
          schema:
            type: hexstring
          required: true
          description: bson object ID of the job to get
    produces:
    - application/json
    responses:
        "200":
            description: a job in dictionary format
    """
    id = request.match_info.get('id')
    data = mongo.orqal.jobs.find_one({'_id': ObjectId(id)})
    if len(data) == 0:
        web.Response(status=404)
    else:
        data['_id'] = id
        return web.Response(body=(dumps(data)), content_type='application/json')


@routes.post('/api/job')
async def job_post(request):
    """
    ---
    summary:  Create a job
    parameters:
        - in: body
          name: data
          description: The job to create.
          schema:
            type: object
            required:
              - app
              - input
            properties:
              app:
                type: string
              input:
                type: string
              params:
                type: object
    produces:
    - text/plain
    responses:
        "200":
            description: a job identifier
    """
    data = await request.json()
    if data is None:
        web.Response(status=500)
    _id = in_cache(data)
    if not _id:
        del data['_id']
        data['ctime'] = datetime.datetime.now()
        log.debug('post job from %s for %s', request.transport.get_extra_info('peername'), data)
        _id = mongo.orqal.jobs.insert(data)
    return web.Response(text=(str(_id)))


@routes.get('/api/jobs/status', allow_head=False)
async def jobs_status(request):
    """
    ---
    summary:  Retrieve counters of job per status
    produces:
    - application/json
    responses:
        '200':
          description: a dictionary of status counter
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    description: The job status.
                  counter:
                    type: integer
                    description: The number of job in this job.
    """
    status_list = mongo.orqal.jobs.find().distinct('current_status')
    status = {s:mongo.orqal.jobs.find({'current_status': s}).count() for s in status_list}
    status['todo'] = status.pop(None) if None in status.keys() else 0
    return web.json_response(status, headers={'Access-Control-Allow-Origin': '*'})


@routes.get('/api/job/{id}/download/{path}', allow_head=False)
async def download_job_file(request):
    """
    ---
    summary:  Download a job file
    description: job can produce file, this route enable to download it.
    parameters:
    - in: path
      name: id
      schema:
        type: hexstring
      required: true
      description: bson object ID of the job to get
    - in: path
      name: path
      schema:
        type: string
      required: true
      description: path of the file
    produces:
    - application/octet-stream
    responses:
        "200":
          description: return the file
    """
    id = request.match_info.get('id')
    path = request.match_info.get('path')
    filepath = os.path.join(conf.jobs_dir, id, path)
    return web.FileResponse(filepath)


@routes.post('/api/batch')
async def batch_post--- This code section failed: ---

 L. 231         0  BUILD_LIST_0          0 
                2  STORE_FAST               'jobs'

 L. 232         4  LOAD_GLOBAL              web
                6  LOAD_ATTR                StreamResponse
                8  LOAD_CONST               200
               10  LOAD_STR                 'OK'
               12  LOAD_STR                 'Content-Type'
               14  LOAD_STR                 'text/plain'
               16  BUILD_MAP_1           1 
               18  LOAD_CONST               ('status', 'reason', 'headers')
               20  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               22  STORE_FAST               'resp'

 L. 233        24  LOAD_FAST                'resp'
               26  LOAD_ATTR                prepare
               28  LOAD_FAST                'request'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  GET_AWAITABLE    
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  POP_TOP          

 L. 234        40  LOAD_CONST               b''
               42  STORE_FAST               'buffer'

 L. 235        44  SETUP_LOOP          232  'to 232'
               46  LOAD_FAST                'request'
               48  LOAD_ATTR                content
               50  LOAD_ATTR                iter_chunks
               52  CALL_FUNCTION_0       0  '0 positional arguments'
               54  GET_AITER        
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  SETUP_EXCEPT         78  'to 78'
               62  GET_ANEXT        
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'data'
               72  STORE_FAST               'complete'
               74  POP_BLOCK        
               76  JUMP_FORWARD         88  'to 88'
             78_0  COME_FROM_EXCEPT     60  '60'
               78  DUP_TOP          
               80  LOAD_GLOBAL              StopAsyncIteration
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_TRUE    220  'to 220'
               86  END_FINALLY      
             88_0  COME_FROM            76  '76'

 L. 236        88  LOAD_FAST                'buffer'
               90  LOAD_FAST                'data'
               92  BINARY_ADD       
               94  STORE_FAST               'buffer'

 L. 237        96  LOAD_FAST                'complete'
               98  POP_JUMP_IF_FALSE    60  'to 60'

 L. 238       100  LOAD_GLOBAL              json
              102  LOAD_ATTR                loads
              104  LOAD_FAST                'buffer'
              106  LOAD_ATTR                decode
              108  LOAD_STR                 'utf-8'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  STORE_FAST               'data'

 L. 239       116  LOAD_GLOBAL              in_cache
              118  LOAD_FAST                'data'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  STORE_FAST               '_id'

 L. 240       124  LOAD_FAST                '_id'
              126  POP_JUMP_IF_TRUE    162  'to 162'

 L. 241       128  LOAD_FAST                'data'
              130  LOAD_STR                 '_id'
              132  DELETE_SUBSCR    

 L. 242       134  LOAD_GLOBAL              datetime
              136  LOAD_ATTR                datetime
              138  LOAD_ATTR                now
              140  CALL_FUNCTION_0       0  '0 positional arguments'
              142  LOAD_FAST                'data'
              144  LOAD_STR                 'ctime'
              146  STORE_SUBSCR     

 L. 243       148  LOAD_GLOBAL              mongo
              150  LOAD_ATTR                orqal
              152  LOAD_ATTR                jobs
              154  LOAD_ATTR                insert
              156  LOAD_FAST                'data'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  STORE_FAST               '_id'
            162_0  COME_FROM           126  '126'

 L. 244       162  LOAD_FAST                'jobs'
              164  LOAD_ATTR                append
              166  LOAD_FAST                '_id'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  POP_TOP          

 L. 245       172  LOAD_FAST                'resp'
              174  LOAD_ATTR                write
              176  LOAD_FAST                '_id'
              178  LOAD_ATTR                binary
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  GET_AWAITABLE    
              184  LOAD_CONST               None
              186  YIELD_FROM       
              188  POP_TOP          

 L. 246       190  LOAD_GLOBAL              log
              192  LOAD_ATTR                debug
              194  LOAD_STR                 'batch %s %s %s'
              196  LOAD_FAST                '_id'
              198  LOAD_FAST                'data'
              200  LOAD_STR                 'input'
              202  BINARY_SUBSCR    
              204  LOAD_FAST                'data'
              206  LOAD_STR                 'app'
              208  BINARY_SUBSCR    
              210  CALL_FUNCTION_4       4  '4 positional arguments'
              212  POP_TOP          

 L. 247       214  LOAD_CONST               b''
              216  STORE_FAST               'buffer'
              218  JUMP_BACK            60  'to 60'
            220_0  COME_FROM            84  '84'
              220  POP_TOP          
              222  POP_TOP          
              224  POP_TOP          
              226  POP_EXCEPT       
              228  POP_TOP          
              230  POP_BLOCK        
            232_0  COME_FROM_LOOP       44  '44'

 L. 248       232  LOAD_FAST                'resp'
              234  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 84


@routes.get('/api/batch/{id}')
async def batch_get(request):
    """
    ---
    summary:  Retrieve job per batch identifier
    parameters:
    - in: path
      name: id
      schema:
        type: string
      required: true
      description: a batch identifier

    produces:
    - application/json
    responses:
        "200":
          description: response a jobs identifier array
    """
    batch_id = request.match_info.get('id')
    data = mongo.orqal.batch.find_one({'_id': batch_id})
    if data:
        return web.Response(body=(dumps(data)), content_type='application/json')
    else:
        return web.Response(body='Not found', status=404)


@routes.get('/api/stream/http://{host}/{id}')
async def stream_get(request):
    """
    ---
    summary:  Retrieve log stream from container id
    parameters:
    - in: path
      name: host
      schema:
        type: string
      required: true
      description: a host ip
    - in: path
      name: id
      schema:
        type: string
      required: true
      description: a container identifier

    produces:
    - text/plain
    responses:
        "200":
          description: stream from container logs
    """
    host = request.match_info.get('host')
    id = request.match_info.get('id')
    client = docker.DockerClient(base_url=host, version=(conf.docker_api_version))
    if id not in [c.id for c in client.containers.list()]:
        return web.Response(status=404)
    else:
        container = client.containers.get(id)
        resp = web.StreamResponse(status=200, reason='OK',
          headers={'Content-Type': 'text/plain'})
        await resp.prepare(request)
        for log in container.attach(stdout=True, stderr=True, logs=True, stream=True):
            await resp.write(log)

        await resp.write_eof()
        return resp


@routes.get('/api/load', allow_head=False)
async def load(request):
    """
    ---
    summary:  Retrieve load of cluster nodes
    produces:
    - application/json
    responses:
        '200':
          description: a dictionary of status counter
          content:
            application/json:
              schema:
                type: object
                properties:
                  host:
                    type: string
                    description: The host node.
                  metrics:
                    type: object
                    description: mem, cpu, images, ...
                    properties:
                      mem:
                        type: number
                        description: memory load scheduled between 0 and 1
                      cpu:
                        type: number
                        description: cpu load scheduled between 0 and 1
                      images:
                        type: object
                        properties:
                          image_name:
                            type: integer
                            description: number of container currently running
    """

    def load_metrics():
        for h in conf.docker_hosts:
            cpu_used = 0
            mem_used = 0
            images = []
            client = docker.DockerClient(base_url=h, version=(conf.docker_api_version))
            mem_total = client.info()['MemTotal']
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as (executor):
                images.extend([''.join(c.attrs['Config']['Image']) for c in client.containers.list()])
                future_to_stats = {executor.submit((c.stats), stream=False):c for c in client.containers.list()}
                for future in concurrent.futures.as_completed(future_to_stats):
                    try:
                        stat = future.result()
                        cpu_delta = stat['cpu_stats']['cpu_usage']['total_usage'] - stat['precpu_stats']['cpu_usage']['total_usage']
                        sys_delta = stat['cpu_stats']['system_cpu_usage'] - stat['precpu_stats']['system_cpu_usage']
                        if cpu_delta > 0:
                            if sys_delta > 0:
                                cpu_used += cpu_delta / sys_delta * 100.0
                        mem_used += stat['memory_stats']['usage']
                    except Exception as exc:
                        log.error(exc)

            yield {h: {'mem':mem_used / mem_total * 100.0,  'cpu':cpu_used, 
                 'images':collections.Counter(images)}}

    return web.json_response(list(load_metrics()))


@routes.get('/api/clean/{action}', allow_head=False)
async def clean(request):
    """
    ---
    summary:  Drop all jobs in db and all containers in the cluster
    parameters:
    - in: path
      name: action
      schema:
        type: string
      required: true
      description: action all: remove all jobs + containers / scheduled: remove job execpt exited + containers
    """

    def containers_to_kill(client):
        for c in client.containers.list():
            if conf.protected_containers and c.name in conf.protected_containers:
                continue
            else:
                yield c

    def kill_and_remove(c):
        c.kill()
        c.remove()

    action = request.match_info.get('action')
    if action == 'all':
        mongo.orqal.jobs.delete_many({})
        return web.Response(text='all jobs purged', status=200)
    else:
        if action == 'scheduled':
            mongo.orqal.jobs.delete_many({'current_status': {'$ne': 'exited'}})
            return web.Response(text='all jobs scheduled purged', status=200)
        if action == 'old':
            resp = web.StreamResponse(status=200, reason='OK', headers={'Content-Type': 'text/plain'})
            await resp.prepare(request)
            for d in os.listdir(conf.jobs_dir):
                if not mongo.orqal.jobs.find_one({'_id': d}):
                    log.debug('delete dir %s', d)
                    shutil.rmtree(os.path.join(conf.jobs_dir, d))
                    await resp.write(bytes('%s\n' % d, 'utf8'))

            return resp
        if action == 'containers':
            for h in conf.docker_hosts:
                client = docker.DockerClient(base_url=h, version=(conf.docker_api_version))
                with concurrent.futures.ThreadPoolExecutor(max_workers=50) as (executor):
                    future_to_stats = {executor.submit(kill_and_remove, c):c for c in containers_to_kill(client)}
                    for future in concurrent.futures.as_completed(future_to_stats):
                        try:
                            future.result()
                        except Exception as exc:
                            log.error(exc)

                return web.Response(text='containers removed', status=200)

        else:
            return web.Response(text='action in path needed', status=500)


@routes.get('/api/status', allow_head=False)
async def status(request):
    """
    ---
    summary:  Global status description
    produces:
    - application/json
    """
    import wrapper

    def containers():
        for d in dockers.values():
            yield {d['docker'].info()['Name']: [(c.id, c.image.tags[0], c.status) for c in d['docker'].containers.list()]}

    dockers = {h:{'docker':docker.DockerClient(base_url=h, version=conf.docker_api_version),  'api':docker.APIClient(base_url=h, version=conf.docker_api_version)} for h in conf.docker_hosts}
    status_list = mongo.db.jobs.find().distinct('current_status')
    status = {s:mongo.db.jobs.find({'current_status': s}).count() for s in status_list}
    s = {'_id':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  '_doc':__doc__, 
     'status':status, 
     '_services':[name for name, obj in inspect.getmembers(sys.modules['wrapper']) if inspect.isclass(obj)],  'hosts':conf.docker_hosts, 
     'nodes':{ip:{'info':d['docker'].info(),  'containers':[d['api'].inspect_container(c) for c in d['api'].containers()]} for ip, d in dockers.items()}, 
     'containers':[c for c in containers()]}
    return web.json_response(s)


app = web.Application()
current_dir = os.path.dirname(os.path.abspath(__file__))
aiohttp_jinja2.setup(app, loader=(jinja2.FileSystemLoader(os.path.join(current_dir, 'templates'))))
for d in ('assets', 'images', 'vendors'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app.router.add_static(('/' + d), path=(os.path.join(current_dir, 'static', d)), name=d)

app.add_routes(routes)
setup_swagger(app, description='Scalable cluster management and job scheduling system for large and small Docker clusters',
  title='orqal',
  api_version='1.0',
  contact=(conf.contact))

def main():
    web.run_app(app, port=5001)


if __name__ == '__main__':
    main()