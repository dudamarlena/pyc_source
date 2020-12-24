# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/check_servers.py
# Compiled at: 2019-07-02 08:18:50
# Size of source mod 2**32: 1758 bytes
from ..models import ScrapydServer
from concurrent.futures import ThreadPoolExecutor
import json, requests, asyncio

def update_servers():
    """
    Gets server list from the database
    """
    servers = ScrapydServer.objects.all()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(check_servers(servers))
    loop.run_until_complete(future)


def check_server(session, server):
    url = 'http://{}:{}/daemonstatus.json'.format(server.ip, server.port)
    try:
        with session.get(url, timeout=2) as (response):
            data = response.json()
            server.node_name = data.get('node_name')
            server.status = data.get('status')
            server.pending_tasks = data.get('pending')
            server.running_tasks = data.get('running')
            server.finished_tasks = data.get('finished')
            server.save()
    except Exception as e:
        server.status = 'error'
        server.status_message = e
        server.save()


async def check_servers(servers):
    with ThreadPoolExecutor(max_workers=10) as (executor):
        with requests.Session() as (session):
            loop = asyncio.get_event_loop()
            tasks = [(loop.run_in_executor)(executor, check_server, *(session, server)) for server in servers]
            for response in await (asyncio.gather)(*tasks):
                pass