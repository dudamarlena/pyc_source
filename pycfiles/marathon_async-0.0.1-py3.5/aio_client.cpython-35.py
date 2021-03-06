# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marathon_async/aio_client.py
# Compiled at: 2017-10-29 16:51:33
# Size of source mod 2**32: 32144 bytes
import itertools, time
try:
    import json
except ImportError:
    import simplejson as json

import aiohttp
from aiohttp import client
import marathon
from marathon.models import MarathonApp, MarathonDeployment, MarathonGroup, MarathonInfo, MarathonTask, MarathonEndpoint, MarathonQueueItem
from marathon.exceptions import InternalServerError, NotFoundError, MarathonError
from .exceptions import MarathonAioHttpError
from marathon.util import MarathonJsonEncoder, MarathonMinimalJsonEncoder

class MarathonAsyncClient(object):
    __doc__ = 'Client interface for the Marathon REST API.'

    def __init__(self, servers, username=None, password=None, timeout=10, session=None, auth_token=None, verify=True, sse_session=None):
        """Create a MarathonClient instance.

        If multiple servers are specified, each will be tried in succession until a non-"Connection Error"-type
        response is received. Servers are expected to have the same username and password.

        :param servers: One or a priority-ordered list of Marathon URLs (e.g., 'http://host:8080' or
        ['http://host1:8080','http://host2:8080'])
        :type servers: str or list[str]
        :param str username: Basic auth username
        :param str password: Basic auth password
        :param requests.session session: requests.session for reusing the connections
        :param int timeout: Timeout (in seconds) for requests to Marathon
        :param str auth_token: Token-based auth token, used with DCOS + Oauth
        :param bool verify: Enable SSL certificate verification
        :param requests.session sse_session: requests.session for event stream connections, which by default enables tcp keepalive
        """
        self.verify = verify
        if session is None:
            self.session = client.ClientSession(raise_for_status=self.verify)
        else:
            self.session = session
        if sse_session is None:
            self.sse_session = client.ClientSession(raise_for_status=self.verify)
        else:
            self.sse_session = sse_session
        self.servers = servers if isinstance(servers, list) else [servers]
        self.auth = (username, password) if username and password else None
        self.timeout = timeout
        self.auth_token = auth_token
        if self.auth and self.auth_token:
            raise ValueError("Can't specify both auth token and username/password. Must select one type of authentication.")

    def __repr__(self):
        return 'Connection:%s' % self.servers

    @staticmethod
    async def _parse_response(response, clazz, is_list=False, resource_name=None):
        """Parse a Marathon response into an object or list of objects."""
        target = await response.json()
        target = target[resource_name] if resource_name else target
        if is_list:
            return [clazz.from_json(resource) for resource in target]
        else:
            return clazz.from_json(target)

    async def _do_request(self, method, path, params=None, data=None):
        """Query Marathon server."""
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        if self.auth_token:
            headers['Authorization'] = 'token={}'.format(self.auth_token)
        response = None
        servers = list(self.servers)
        while servers and response is None:
            server = servers.pop(0)
            url = ''.join([server.rstrip('/'), path])
            try:
                response = await self.session.request(method, url, params=params, data=data, headers=headers, auth=self.auth, timeout=self.timeout)
                marathon.log.info('Got response from %s', server)
            except aiohttp.ClientConnectionError as e:
                marathon.log.error('Error while calling %s: %s', url, str(e))

        if response is None:
            raise MarathonError('No remaining Marathon servers to try')
        if response.status >= 500:
            response_text = await response.text()
            marathon.log.error('Got HTTP {code}: {body}'.format(code=response.status, body=response_text))
            raise InternalServerError(response)
        else:
            if response.status >= 400:
                response_text = await response.text()
                marathon.log.error('Got HTTP {code}: {body}'.format(code=response.status, body=response_text))
                if response.status == 404:
                    raise NotFoundError(response)
                else:
                    content = await response.json() if response.content_type == 'application/json' else None
                    raise MarathonAioHttpError(response, content)
            else:
                if response.status >= 300:
                    response_text = await response.text()
                    marathon.log.warn('Got HTTP {code}: {body}'.format(code=response.status, body=response_text))
                else:
                    response_text = await response.text()
                    marathon.log.debug('Got HTTP {code}: {body}'.format(code=response.status, body=response_text))
        return response

    async def _do_sse_request(self, path, params=None):
        """Query Marathon server for events."""
        for server in list(self.servers):
            url = ''.join([server.rstrip('/'), path])
            try:
                response = await self.sse_session.get(url, params=params, headers={'Accept': 'text/event-stream'}, auth=self.auth)
            except Exception as e:
                marathon.log.error('Error while calling %s: %s', url, e)
            else:
                if response.ok:
                    return response.iter_lines()

        raise MarathonError('No remaining Marathon servers to try')

    async def list_endpoints(self):
        """List the current endpoints for all applications

        :returns: list of endpoints
        :rtype: list[`MarathonEndpoint`]
        """
        return MarathonEndpoint.from_tasks(self.list_tasks())

    async def create_app(self, app_id, app):
        """Create and start an app.

        :param str app_id: application ID
        :param :class:`marathon_async.models.app.MarathonApp` app: the application to create

        :returns: the created app (on success)
        :rtype: :class:`marathon_async.models.app.MarathonApp` or False
        """
        app.id = app_id
        data = app.to_json()
        response = await self._do_request('POST', '/v2/apps', data=data)
        if response.status == 201:
            return await self._parse_response(response, MarathonApp)
        else:
            return False

    def list_apps(self, cmd=None, embed_tasks=False, embed_counts=False, embed_deployments=False,
                  embed_readiness=False, embed_last_task_failure=False,
                  embed_failures=False, embed_task_stats=False,
                  app_id=None, label=None, **kwargs) -> list:
        """List all apps.

        :param str cmd: if passed, only show apps with a matching `cmd`
        :param bool embed_tasks: embed tasks in result
        :param bool embed_counts: embed all task counts
        :param bool embed_deployments: embed all deployment identifier
        :param bool embed_readiness: embed all readiness check results
        :param bool embed_last_task_failure: embeds the last task failure
        :param bool embed_failures: shorthand for embed_last_task_failure
        :param bool embed_task_stats: embed task stats in result
        :param str app_id: if passed, only show apps with an 'id' that matches or contains this value
        :param str label: if passed, only show apps with the selected labels
        :param kwargs: arbitrary search filters

        :returns: list of applications
        :rtype: list[:class:`marathon_async.models.app.MarathonApp`]
        """
        params = {}
        if cmd:
            params['cmd'] = cmd
        if app_id:
            params['id'] = app_id
        if label:
            params['label'] = label
        embed_params = {'app.tasks': embed_tasks, 
         'app.counts': embed_counts, 
         'app.deployments': embed_deployments, 
         'app.readiness': embed_readiness, 
         'app.lastTaskFailure': embed_last_task_failure, 
         'app.failures': embed_failures, 
         'app.taskStats': embed_task_stats}
        filtered_embed_params = [k for k, v in embed_params.items() if v]
        if filtered_embed_params:
            params['embed'] = filtered_embed_params
        response = await self._do_request('GET', '/v2/apps', params=params)
        apps = await self._parse_response(response, MarathonApp, is_list=True, resource_name='apps')
        for k, v in kwargs.items():
            apps = [o for o in apps if getattr(o, k) == v]

        return apps

    async def get_app(self, app_id, embed_tasks=False, embed_counts=False, embed_deployments=False, embed_readiness=False, embed_last_task_failure=False, embed_failures=False, embed_task_stats=False):
        """Get a single app.

        :param str app_id: application ID
        :param bool embed_tasks: embed tasks in result
        :param bool embed_counts: embed all task counts
        :param bool embed_deployments: embed all deployment identifier
        :param bool embed_readiness: embed all readiness check results
        :param bool embed_last_task_failure: embeds the last task failure
        :param bool embed_failures: shorthand for embed_last_task_failure
        :param bool embed_task_stats: embed task stats in result

        :returns: application
        :rtype: :class:`marathon_async.models.app.MarathonApp`
        """
        params = {}
        embed_params = {'app.tasks': embed_tasks, 
         'app.counts': embed_counts, 
         'app.deployments': embed_deployments, 
         'app.readiness': embed_readiness, 
         'app.lastTaskFailure': embed_last_task_failure, 
         'app.failures': embed_failures, 
         'app.taskStats': embed_task_stats}
        filtered_embed_params = [k for k, v in embed_params.items() if v]
        if filtered_embed_params:
            params['embed'] = filtered_embed_params
        response = await self._do_request('GET', '/v2/apps/{app_id}'.format(app_id=app_id), params=params)
        return await self._parse_response(response, MarathonApp, resource_name='app')

    async def restart_app(self, app_id, force=False):
        """
        Restarts given application by app_id
        :param str app_id: application ID
        :param bool force: apply even if a deployment is in progress
        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        params = {'force': force}
        response = await self._do_request('POST', '/v2/apps/{app_id}/restart'.format(app_id=app_id), params=params)
        return await response.json()

    async def update_app(self, app_id, app, force=False, minimal=True):
        """Update an app.

        Applies writable settings in `app` to `app_id`
        Note: this method can not be used to rename apps.

        :param str app_id: target application ID
        :param app: application settings
        :type app: :class:`marathon_async.models.app.MarathonApp`
        :param bool force: apply even if a deployment is in progress
        :param bool minimal: ignore nulls and empty collections

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        app.version = None
        params = {'force': force}
        data = app.to_json(minimal=minimal)
        response = await self._do_request('PUT', '/v2/apps/{app_id}'.format(app_id=app_id), params=params, data=data)
        return await response.json()

    async def update_apps(self, apps, force=False, minimal=True):
        """Update multiple apps.

        Applies writable settings in elements of apps either by upgrading existing ones or creating new ones

        :param apps: sequence of application settings
        :param bool force: apply even if a deployment is in progress
        :param bool minimal: ignore nulls and empty collections

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        json_repr_apps = []
        for app in apps:
            app.version = None
            json_repr_apps.append(app.json_repr(minimal=minimal))

        params = {'force': force}
        encoder = MarathonMinimalJsonEncoder if minimal else MarathonJsonEncoder
        data = json.dumps(json_repr_apps, cls=encoder, sort_keys=True)
        response = await self._do_request('PUT', '/v2/apps', params=params, data=data)
        return await response.json()

    async def rollback_app(self, app_id, version, force=False):
        """Roll an app back to a previous version.

        :param str app_id: application ID
        :param str version: application version
        :param bool force: apply even if a deployment is in progress

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        params = {'force': force}
        data = json.dumps({'version': version})
        response = await self._do_request('PUT', '/v2/apps/{app_id}'.format(app_id=app_id), params=params, data=data)
        return await response.json()

    async def delete_app(self, app_id, force=False):
        """Stop and destroy an app.

        :param str app_id: application ID
        :param bool force: apply even if a deployment is in progress

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        params = {'force': force}
        response = await self._do_request('DELETE', '/v2/apps/{app_id}'.format(app_id=app_id), params=params)
        return await response.json()

    async def scale_app(self, app_id, instances=None, delta=None, force=False):
        """Scale an app.

        Scale an app to a target number of instances (with `instances`), or scale the number of
        instances up or down by some delta (`delta`). If the resulting number of instances would be negative,
        desired instances will be set to zero.

        If both `instances` and `delta` are passed, use `instances`.

        :param str app_id: application ID
        :param int instances: [optional] the number of instances to scale to
        :param int delta: [optional] the number of instances to scale up or down by
        :param bool force: apply even if a deployment is in progress

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        if instances is None and delta is None:
            marathon.log.error('instances or delta must be passed')
            return
            try:
                app = self.get_app(app_id)
            except NotFoundError:
                marathon.log.error('App "{app}" not found'.format(app=app_id))
                return

            desired = instances if instances is not None else app.instances + delta
            return self.update_app(app.id, MarathonApp(instances=desired), force=force)

    async def create_group(self, group):
        """Create and start a group.

        :param :class:`marathon_async.models.group.MarathonGroup` group: the group to create

        :returns: success
        :rtype: dict containing the version ID
        """
        data = group.to_json()
        response = await self._do_request('POST', '/v2/groups', data=data)
        return await response.json()

    def list_groups(self, **kwargs) -> list:
        """List all groups.

        :param kwargs: arbitrary search filters

        :returns: list of groups
        :rtype: list[:class:`marathon_async.models.group.MarathonGroup`]
        """
        response = await self._do_request('GET', '/v2/groups')
        groups = await self._parse_response(response, MarathonGroup, is_list=True, resource_name='groups')
        for k, v in kwargs.items():
            groups = [o for o in groups if getattr(o, k) == v]

        return groups

    async def get_group(self, group_id):
        """Get a single group.

        :param str group_id: group ID

        :returns: group
        :rtype: :class:`marathon_async.models.group.MarathonGroup`
        """
        response = await self._do_request('GET', '/v2/groups/{group_id}'.format(group_id=group_id))
        return await self._parse_response(response, MarathonGroup)

    async def update_group(self, group_id, group, force=False, minimal=True):
        """Update a group.

        Applies writable settings in `group` to `group_id`
        Note: this method can not be used to rename groups.

        :param str group_id: target group ID
        :param group: group settings
        :type group: :class:`marathon_async.models.group.MarathonGroup`
        :param bool force: apply even if a deployment is in progress
        :param bool minimal: ignore nulls and empty collections

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        group.version = None
        params = {'force': force}
        data = group.to_json(minimal=minimal)
        response = await self._do_request('PUT', '/v2/groups/{group_id}'.format(group_id=group_id), data=data, params=params)
        return await response.json()

    async def rollback_group(self, group_id, version, force=False):
        """Roll a group back to a previous version.

        :param str group_id: group ID
        :param str version: group version
        :param bool force: apply even if a deployment is in progress

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        params = {'force': force}
        response = await self._do_request('PUT', '/v2/groups/{group_id}/versions/{version}'.format(group_id=group_id, version=version), params=params)
        return await response.json()

    def delete_group(self, group_id, force=False) -> dict:
        """Stop and destroy a group.

        :param str group_id: group ID
        :param bool force: apply even if a deployment is in progress

        :returns: a dict containing the deleted version
        :rtype: dict
        """
        params = {'force': str(force)}
        response = await self._do_request('DELETE', '/v2/groups/{group_id}'.format(group_id=group_id), params=params)
        return await response.json()

    async def scale_group(self, group_id, scale_by):
        """Scale a group by a factor.

        :param str group_id: group ID
        :param int scale_by: factor to scale by

        :returns: a dict containing the deployment id and version
        :rtype: dict
        """
        params = {'scaleBy': scale_by}
        response = await self._do_request('PUT', '/v2/groups/{group_id}'.format(group_id=group_id), params=params)
        return await response.json()

    async def list_tasks(self, app_id=None, **kwargs):
        """List running tasks, optionally filtered by app_id.

        :param str app_id: if passed, only show tasks for this application
        :param kwargs: arbitrary search filters

        :returns: list of tasks
        :rtype: list[:class:`marathon_async.models.task.MarathonTask`]
        """
        response = await self._do_request('GET', '/v2/apps/%s/tasks' % app_id if app_id else '/v2/tasks')
        tasks = await self._parse_response(response, MarathonTask, is_list=True, resource_name='tasks')
        [setattr(t, 'app_id', app_id) for t in tasks if app_id and t.app_id is None]
        for k, v in kwargs.items():
            tasks = [o for o in tasks if getattr(o, k) == v]

        return tasks

    async def kill_given_tasks(self, task_ids, scale=False, force=None):
        """Kill a list of given tasks.

        :param list[str] task_ids: tasks to kill
        :param bool scale: if true, scale down the app by the number of tasks killed
        :param bool force: if true, ignore any current running deployments

        :return: True on success
        :rtype: bool
        """
        params = {'scale': scale}
        if force is not None:
            params['force'] = force
        data = json.dumps({'ids': task_ids})
        response = await self._do_request('POST', '/v2/tasks/delete', params=params, data=data)
        return response == 200

    async def kill_tasks(self, app_id, scale=False, wipe=False, host=None, batch_size=0, batch_delay=0):
        """Kill all tasks belonging to app.

        :param str app_id: application ID
        :param bool scale: if true, scale down the app by the number of tasks killed
        :param str host: if provided, only terminate tasks on this Mesos slave
        :param int batch_size: if non-zero, terminate tasks in groups of this size
        :param int batch_delay: time (in seconds) to wait in between batched kills. If zero, automatically determine

        :returns: list of killed tasks
        :rtype: list[:class:`marathon_async.models.task.MarathonTask`]
        """

        def batch(iterable, size):
            sourceiter = iter(iterable)
            while True:
                batchiter = itertools.islice(sourceiter, size)
                yield itertools.chain([next(batchiter)], batchiter)

        if batch_size == 0:
            params = {'scale': scale, 'wipe': wipe}
            if host:
                params['host'] = host
            response = await self._do_request('DELETE', '/v2/apps/{app_id}/tasks'.format(app_id=app_id), params)
            if 'tasks' in response.json():
                return await self._parse_response(response, MarathonTask, is_list=True, resource_name='tasks')
            else:
                return await response.json()
        else:
            tasks = self.list_tasks(app_id, host=host) if host else self.list_tasks(app_id)
            for tbatch in batch(tasks, batch_size):
                killed_tasks = [self.kill_task(app_id, t.id, scale=scale, wipe=wipe) for t in tbatch]
                killed_task_ids = set(t.id for t in killed_tasks)
                running_task_ids = killed_task_ids
                while killed_task_ids.intersection(running_task_ids):
                    time.sleep(1)
                    running_task_ids = set(t.id for t in self.get_app(app_id).tasks)

                if batch_delay == 0:
                    desired_instances = self.get_app(app_id).instances
                    running_instances = 0
                    while running_instances < desired_instances:
                        time.sleep(1)
                        running_instances = sum(t.started_at is None for t in self.get_app(app_id).tasks)

                else:
                    time.sleep(batch_delay)

            return tasks

    async def kill_task(self, app_id, task_id, scale=False, wipe=False):
        """Kill a task.

        :param str app_id: application ID
        :param str task_id: the task to kill
        :param bool scale: if true, scale down the app by one if the task exists

        :returns: the killed task
        :rtype: :class:`marathon_async.models.task.MarathonTask`
        """
        params = {'scale': scale, 'wipe': wipe}
        response = await self._do_request('DELETE', '/v2/apps/{app_id}/tasks/{task_id}'.format(app_id=app_id, task_id=task_id), params)
        if 'task' in response.json():
            return await self._parse_response(response, MarathonTask, is_list=False, resource_name='task')
        else:
            return await response.json()

    async def list_versions(self, app_id):
        """List the versions of an app.

        :param str app_id: application ID

        :returns: list of versions
        :rtype: list[str]
        """
        response = await self._do_request('GET', '/v2/apps/{app_id}/versions'.format(app_id=app_id))
        json_data = await response.json()
        return [version for version in json_data['versions']]

    async def get_version(self, app_id, version):
        """Get the configuration of an app at a specific version.

        :param str app_id: application ID
        :param str version: application version

        :return: application configuration
        :rtype: :class:`marathon_async.models.app.MarathonApp`
        """
        response = await self._do_request('GET', '/v2/apps/{app_id}/versions/{version}'.format(app_id=app_id, version=version))
        return MarathonApp.from_json(await response.json())

    async def list_event_subscriptions(self):
        """List the event subscriber callback URLs.

        :returns: list of callback URLs
        :rtype: list[str]
        """
        response = await self._do_request('GET', '/v2/eventSubscriptions')
        json_data = await response.json()
        return [url for url in json_data['callbackUrls']]

    async def create_event_subscription(self, url):
        """Register a callback URL as an event subscriber.

        :param str url: callback URL

        :returns: the created event subscription
        :rtype: dict
        """
        params = {'callbackUrl': url}
        response = await self._do_request('POST', '/v2/eventSubscriptions', params)
        return await response.json()

    async def delete_event_subscription(self, url):
        """Deregister a callback URL as an event subscriber.

        :param str url: callback URL

        :returns: the deleted event subscription
        :rtype: dict
        """
        params = {'callbackUrl': url}
        response = await self._do_request('DELETE', '/v2/eventSubscriptions', params)
        return await response.json()

    async def list_deployments(self):
        """List all running deployments.

        :returns: list of deployments
        :rtype: list[:class:`marathon_async.models.deployment.MarathonDeployment`]
        """
        response = await self._do_request('GET', '/v2/deployments')
        return await self._parse_response(response, MarathonDeployment, is_list=True)

    async def list_queue(self, embed_last_unused_offers=False):
        """List all the tasks queued up or waiting to be scheduled.

        :returns: list of queue items
        :rtype: list[:class:`marathon_async.models.queue.MarathonQueueItem`]
        """
        if embed_last_unused_offers:
            params = {'embed': 'lastUnusedOffers'}
        else:
            params = {}
        response = await self._do_request('GET', '/v2/queue', params=params)
        return await self._parse_response(response, MarathonQueueItem, is_list=True, resource_name='queue')

    async def delete_deployment(self, deployment_id, force=False):
        """Cancel a deployment.

        :param str deployment_id: deployment id
        :param bool force: if true, don't create a rollback deployment to restore the previous configuration

        :returns: a dict containing the deployment id and version (empty dict if force=True)
        :rtype: dict
        """
        if force:
            params = {'force': True}
            self._do_request('DELETE', '/v2/deployments/{deployment}'.format(deployment=deployment_id), params=params)
            return {}
        else:
            response = await self._do_request('DELETE', '/v2/deployments/{deployment}'.format(deployment=deployment_id))
            return await response.json()

    async def get_info(self):
        """Get server configuration information.

        :returns: server config info
        :rtype: :class:`marathon_async.models.info.MarathonInfo`
        """
        response = await self._do_request('GET', '/v2/info')
        return await self._parse_response(response, MarathonInfo)

    async def get_leader(self):
        """Get the current marathon_async leader.

        :returns: leader endpoint
        :rtype: dict
        """
        response = await self._do_request('GET', '/v2/leader')
        return await response.json()

    async def delete_leader(self):
        """Causes the current leader to abdicate, triggers a new election.

        :returns: message saying leader abdicated
        :rtype: dict
        """
        response = await self._do_request('DELETE', '/v2/leader')
        return await response.json()

    async def ping(self):
        """Ping the Marathon server.

        :returns: the text response
        :rtype: str
        """
        response = await self._do_request('GET', '/ping')
        return response.text.encode('utf-8')

    async def get_metrics(self):
        """Get server metrics

        :returns: metrics dict
        :rtype: dict
        """
        response = await self._do_request('GET', '/metrics')
        return await response.json()

    async def event_stream(self, raw=False, event_types=None):
        """Polls event bus using /v2/events

        :param bool raw: if true, yield raw event text, else yield MarathonEvent object
        :param event_types: a list of event types to consume
        :type event_types: list[type] or list[str]
        :returns: iterator with events
        :rtype: iterator
        """
        raise NotImplementedError()