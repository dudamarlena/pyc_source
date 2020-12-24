# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tasks.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import absolute_import, unicode_literals
import json, pkg_resources
from celery.utils.log import get_task_logger
from celery.worker.control import Panel
from reviewbot.celery import celery
from rbtools.api.client import RBClient
from reviewbot.processing.review import Review
from reviewbot.repositories import repositories
from reviewbot.utils.filesystem import cleanup_tempfiles
COOKIE_FILE = b'reviewbot-cookies.txt'
AGENT = b'ReviewBot'
PENDING = b'pending'
DONE_SUCCESS = b'done-success'
DONE_FAILURE = b'done-failure'
ERROR = b'error'
logger = get_task_logger(__name__)

@celery.task(ignore_result=True)
def RunTool(server_url=b'', session=b'', username=b'', review_request_id=-1, diff_revision=-1, status_update_id=-1, review_settings={}, tool_options={}, repository_name=b'', base_commit_id=b'', *args, **kwargs):
    """Execute an automated review on a review request.

    Args:
        server_url (unicode):
            The URL of the Review Board server.

        session (unicode):
            The encoded session identifier.

        username (unicode):
            The name of the user who owns the ``session``.

        review_request_id (int):
            The ID of the review request being reviewed (ID for use in the
            API, which is the "display_id" field).

        diff_revision (int):
            The ID of the diff revision being reviewed.

        status_update_id (int):
            The ID of the status update for this invocation of the tool.

        review_settings (dict):
            Settings for how the review should be created.

        tool_options (dict):
            The tool-specific settings.

        repository_name (unicode):
            The name of the repository to clone to run the tool, if the tool
            requires full working directory access.

        base_commit_id (unicode):
            The ID of the commit that the patch should be applied to.

        args (tuple):
            Any additional positional arguments (perhaps used by a newer
            version of the Review Bot extension).

        kwargs (dict):
            Any additional keyword arguments (perhaps used by a newer version
            of the Review Bot extension).

    Returns:
        bool:
        Whether the task completed successfully.
    """
    try:
        routing_key = RunTool.request.delivery_info[b'routing_key']
        route_parts = routing_key.partition(b'.')
        tool_name = route_parts[0]
        log_detail = b'(server=%s, review_request_id=%s, diff_revision=%s)' % (
         server_url, review_request_id, diff_revision)
        logger.info(b'Running tool "%s" %s', tool_name, log_detail)
        try:
            logger.info(b'Initializing RB API %s', log_detail)
            api_client = RBClient(server_url, cookie_file=COOKIE_FILE, agent=AGENT, session=session)
            api_root = api_client.get_root()
        except Exception as e:
            logger.error(b'Could not contact Review Board server: %s %s', e, log_detail)
            return False

        logger.info(b'Loading requested tool "%s" %s', tool_name, log_detail)
        tools = [ entrypoint.load() for entrypoint in pkg_resources.iter_entry_points(group=b'reviewbot.tools', name=tool_name)
                ]
        if len(tools) == 0:
            logger.error(b'Tool "%s" not found %s', tool_name, log_detail)
            return False
        if len(tools) > 1:
            logger.error(b'Tool "%s" is ambiguous (found %s) %s', tool_name, (b', ').join(tool.name for tool in tools), log_detail)
            return False
        tool = tools[0]
        repository = None
        try:
            logger.info(b'Creating status update %s', log_detail)
            status_update = api_root.get_status_update(review_request_id=review_request_id, status_update_id=status_update_id)
        except Exception as e:
            logger.exception(b'Unable to create status update: %s %s', e, log_detail)
            return False

        if tool.working_directory_required:
            if not base_commit_id:
                logger.error(b'Working directory is required but the diffset has no base_commit_id %s', log_detail)
                status_update.update(state=ERROR, description=b'Diff does not include parent commit information.')
                return False
            try:
                repository = repositories[repository_name]
            except KeyError:
                logger.error(b'Unable to find configured repository "%s" %s', repository_name, log_detail)
                return False

        try:
            logger.info(b'Initializing review %s', log_detail)
            review = Review(api_root, review_request_id, diff_revision, review_settings)
            status_update.update(description=b'running...')
        except Exception as e:
            logger.exception(b'Failed to initialize review: %s %s', e, log_detail)
            status_update.update(state=ERROR, description=b'internal error.')
            return False

        try:
            logger.info(b'Initializing tool "%s %s" %s', tool.name, tool.version, log_detail)
            t = tool()
        except Exception as e:
            logger.exception(b'Error initializing tool "%s": %s %s', tool.name, e, log_detail)
            status_update.update(state=ERROR, description=b'internal error.')
            return False

        try:
            logger.info(b'Executing tool "%s" %s', tool.name, log_detail)
            t.execute(review, settings=tool_options, repository=repository, base_commit_id=base_commit_id)
            logger.info(b'Tool "%s" completed successfully %s', tool.name, log_detail)
        except Exception as e:
            logger.exception(b'Error executing tool "%s": %s %s', tool.name, e, log_detail)
            status_update.update(state=ERROR, description=b'internal error.')
            return False

        if t.output:
            file_attachments = api_root.get_user_file_attachments(username=username)
            attachment = file_attachments.upload_attachment(b'tool-output', t.output)
            status_update.update(url=attachment.absolute_url, url_text=b'Tool console output')
        try:
            if len(review.comments) == 0:
                status_update.update(state=DONE_SUCCESS, description=b'passed.')
            else:
                logger.info(b'Publishing review %s', log_detail)
                review_id = review.publish().id
                status_update.update(state=DONE_FAILURE, description=b'failed.', review_id=review_id)
        except Exception as e:
            logger.exception(b'Error when publishing review: %s %s', e, log_detail)
            status_update.update(state=ERROR, description=b'internal error.')
            return False

        logger.info(b'Review completed successfully %s', log_detail)
        return True
    finally:
        cleanup_tempfiles()

    return


@Panel.register
def update_tools_list(panel, payload):
    """Update the list of installed tools.

    This will detect the installed analysis tool plugins
    and inform Review Board of them.

    Args:
        panel (celery.worker.control.Panel):
            The worker control panel.

        payload (dict):
            The payload as assembled by the extension.

    Returns:
        bool:
        Whether the task completed successfully.
    """
    logger.info(b'Request to refresh installed tools from "%s"', payload[b'url'])
    logger.info(b'Iterating Tools')
    tools = []
    for ep in pkg_resources.iter_entry_points(group=b'reviewbot.tools'):
        entry_point = ep.name
        tool_class = ep.load()
        tool = tool_class()
        logger.info(b'Tool: %s' % entry_point)
        if tool.check_dependencies():
            tools.append({b'name': tool_class.name, 
               b'entry_point': entry_point, 
               b'version': tool_class.version, 
               b'description': tool_class.description, 
               b'tool_options': json.dumps(tool_class.options), 
               b'timeout': tool_class.timeout, 
               b'working_directory_required': tool_class.working_directory_required})
        else:
            logger.warning(b'%s dependency check failed.', ep.name)

    logger.info(b'Done iterating Tools')
    hostname = panel.hostname
    try:
        api_client = RBClient(payload[b'url'], cookie_file=COOKIE_FILE, agent=AGENT, session=payload[b'session'])
        api_root = api_client.get_root()
    except Exception as e:
        logger.exception(b'Could not reach RB server: %s', e)
        return {b'status': b'error', 
           b'error': b'Could not reach Review Board server: %s' % e}

    try:
        api_tools = _get_extension_resource(api_root).get_tools()
        api_tools.create(hostname=hostname, tools=json.dumps(tools))
    except Exception as e:
        logger.exception(b'Problem POSTing tools: %s', e)
        return {b'status': b'error', 
           b'error': b'Problem uploading tools: %s' % e}

    return {b'status': b'ok', 
       b'tools': tools}


def _get_extension_resource(api_root):
    """Return the Review Bot extension resource.

    Args:
        api_root (rbtools.api.resource.Resource):
            The server API root.

    Returns:
        rbtools.api.resource.Resource:
        The extension's API resource.
    """
    return api_root.get_extension(extension_name=b'reviewbotext.extension.ReviewBotExtension')