# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/jobs_list.py
# Compiled at: 2019-07-03 02:36:58
# Size of source mod 2**32: 3347 bytes
from concurrent.futures import ThreadPoolExecutor
import requests, json, asyncio, datetime
from datetime import datetime
import time
from ..models import Task, ScrapydServer, ScrapydProject
from .projects_list import projects_list

def jobs_list(session, server, project):
    full_url = 'http://{}:{}/listjobs.json?project={}'.format(server.ip, server.port, project.name)
    timeout = 5
    jobs = []
    status = ['finished', 'pending', 'running']
    try:
        with session.get(full_url, timeout=timeout) as (response):
            data = json.loads(response.text)
            for s in status:
                jobs.append({'status':s, 
                 'jobs':data.get(s, []), 
                 'project':project, 
                 'server':server})

            save_jobs(jobs)
    except Exception as e:
        print(e)


def save_jobs(jobs):
    for job in jobs:
        for j in job['jobs']:
            start_time = j.get('start_time', datetime.now())
            end_time = j.get('end_time')
            start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            if j.get('end_time'):
                end_date = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
                runtime = end_date - start_date
            else:
                runtime = datetime.now() - start_date
            Task.objects.update_or_create(id=(j.get('id')),
              defaults={'name':j.get('name', 'default'), 
             'status':job.get('status'), 
             'server':job.get('server'), 
             'project':job.get('project'), 
             'spider':j.get('spider'), 
             'start_datetime':start_time, 
             'finished_datetime':end_time, 
             'deleted':False, 
             'runtime':str(runtime).split('.')[0]})


async def iterate_projects(server):
    projects = ScrapydProject.objects.filter(server=server)
    with ThreadPoolExecutor(max_workers=10) as (executor):
        with requests.Session() as (session):
            loop = asyncio.get_event_loop()
            tasks = [(loop.run_in_executor)(executor, jobs_list, *(session, server, project)) for project in projects]
            for response in await (asyncio.gather)(*tasks):
                pass


async def check_servers(servers):
    with ThreadPoolExecutor(max_workers=10) as (executor):
        loop = asyncio.get_event_loop()
        for server in servers:
            d = await iterate_projects(server)


def update_jobs():
    servers = ScrapydServer.objects.filter(status='ok')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(check_servers(servers))
    loop.run_until_complete(future)