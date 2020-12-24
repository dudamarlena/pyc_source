# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/tasks_list.py
# Compiled at: 2019-07-31 09:37:14
# Size of source mod 2**32: 3566 bytes
from concurrent.futures import ThreadPoolExecutor
import requests, json, asyncio, datetime
from datetime import datetime
import time
from ..models import Task, ScrapydServer, ScrapydProject
from .projects_list import projects_list

def tasks_list(session, server, project):
    full_url = 'http://{}:{}/listjobs.json?project={}'.format(server.ip, server.port, project.name)
    timeout = 5
    tasks = []
    status = ['finished', 'pending', 'running']
    try:
        with session.get(full_url, timeout=timeout) as (response):
            data = json.loads(response.text)
            for s in status:
                tasks.append({'status':s, 
                 'tasks':data.get(s, []), 
                 'project':project, 
                 'server':server})

            save_tasks(tasks)
    except Exception as e:
        print(e)


def save_tasks(tasks):
    for task in tasks:
        for j in task['tasks']:
            start_time = j.get('start_time', datetime.now())
            end_time = j.get('end_time')
            start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            if j.get('end_time'):
                end_date = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
                runtime = end_date - start_date
            else:
                runtime = datetime.now() - start_date
            log_href = 'http://{}:{}/logs/{}/{}/{}.json'.format(task.get('server').ip, task.get('server').port, task.get('project').name, j.get('spider'), j.get('id'))
            Task.objects.update_or_create(id=(j.get('id')),
              defaults={'status':task.get('status'), 
             'server':task.get('server'), 
             'project':task.get('project'), 
             'spider':j.get('spider'), 
             'start_datetime':start_time, 
             'finished_datetime':end_time, 
             'runtime':str(runtime).split('.')[0], 
             'log_href':log_href})


async def iterate_projects(server):
    projects = ScrapydProject.objects.filter(server=server)
    with ThreadPoolExecutor(max_workers=10) as (executor):
        with requests.Session() as (session):
            loop = asyncio.get_event_loop()
            tasks = [(loop.run_in_executor)(executor, tasks_list, *(session, server, project)) for project in projects]
            for response in await (asyncio.gather)(*tasks):
                pass


async def check_servers(servers):
    with ThreadPoolExecutor(max_workers=10) as (executor):
        loop = asyncio.get_event_loop()
        for server in servers:
            d = await iterate_projects(server)


def update_tasks():
    servers = ScrapydServer.objects.filter(status='ok')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(check_servers(servers))
    loop.run_until_complete(future)