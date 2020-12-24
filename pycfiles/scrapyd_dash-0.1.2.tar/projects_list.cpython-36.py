# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/projects_list.py
# Compiled at: 2019-07-24 03:10:14
# Size of source mod 2**32: 2006 bytes
from concurrent.futures import ThreadPoolExecutor
from ..models import ScrapydServer, ScrapydProject, ScrapydProjectVersion
from .versions_list import versions_list
import json, requests, asyncio

def projects_list(session, server):
    full_url = 'http://{}:{}/listprojects.json'.format(server.ip, server.port)
    timeout = 5
    try:
        with session.get(full_url, timeout=timeout) as (response):
            data = json.loads(response.text)
            for project in data.get('projects', []):
                proj = ScrapydProject.objects.update_or_create(server=server,
                  name=project)
                versions = versions_list(server, project)
                for ver in versions:
                    ScrapydProjectVersion.objects.create(version=ver,
                      project=proj)

    except Exception as e:
        print(e)


async def check_projects(servers):
    with ThreadPoolExecutor(max_workers=10) as (executor):
        with requests.Session() as (session):
            loop = asyncio.get_event_loop()
            tasks = [(loop.run_in_executor)(executor, projects_list, *(session, server)) for server in servers]
            for response in await (asyncio.gather)(*tasks):
                pass


def update_projects():
    servers = ScrapydServer.objects.filter(status='ok')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(check_projects(servers))
    loop.run_until_complete(future)