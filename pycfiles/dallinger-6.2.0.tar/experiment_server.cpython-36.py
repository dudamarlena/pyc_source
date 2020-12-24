# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/experiment_server/experiment_server.py
# Compiled at: 2020-04-24 19:15:49
# Size of source mod 2**32: 51597 bytes
""" This module provides the backend Flask server that serves an experiment. """
from datetime import datetime
import gevent
from json import dumps
from json import loads
import os, re
from flask import abort, Flask, render_template, request, Response, send_from_directory
from jinja2 import TemplateNotFound
from rq import Queue
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy.sql.expression import true
from psycopg2.extensions import TransactionRollbackError
from dallinger import db
from dallinger import experiment
from dallinger import models
from dallinger.config import get_config
from dallinger import recruiters
from dallinger.notifications import admin_notifier
from dallinger.notifications import MessengerError
from .replay import ReplayBackend
from .worker_events import worker_function
from .utils import crossdomain, nocache, ValidatesBrowser, error_page, error_response, success_response, ExperimentError
session = db.session
redis_conn = db.redis_conn
q = Queue(connection=redis_conn)
WAITING_ROOM_CHANNEL = 'quorum'
app = Flask('Experiment_Server')

@app.before_first_request
def _config():
    config = get_config()
    if not config.ready:
        config.load()
    return config


def Experiment(args):
    klass = experiment.load()
    return klass(args)


try:
    from dallinger_experiment.experiment import extra_routes
except ImportError:
    pass
else:
    app.register_blueprint(extra_routes)
app.register_blueprint(recruiters.mturk_routes)

@app.route('/')
def index():
    """Index route"""
    config = _config()
    html = '<html><head></head><body><h1>Dallinger Experiment in progress</h1><dl>'
    for item in sorted(config.as_dict().items()):
        html += ('<dt style="font-weight:bold;margin-top:15px;">{}</dt><dd>{}</dd>'.format)(*item)

    html += '</dl></body></html>'
    return html


@app.route('/robots.txt')
def static_robots_txt():
    """Serve robots.txt from static file."""
    return send_from_directory('static', 'robots.txt')


@app.route('/favicon.ico')
def static_favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')


@app.errorhandler(ExperimentError)
def handle_exp_error(exception):
    """Handle errors by sending an error page."""
    app.logger.error('%s (%s) %s', exception.value, exception.errornum, str(dict(request.args)))
    return error_page(error_type=(exception.value))


@app.teardown_request
def shutdown_session(_=None):
    """Rollback and close session at end of a request."""
    session.remove()
    db.logger.debug('Closing Dallinger DB session at flask request end')


@app.context_processor
def inject_experiment():
    """Inject experiment and enviroment variables into the template context."""
    exp = Experiment(session)
    return dict(experiment=exp, env=(os.environ))


@app.route('/error-page', methods=['POST', 'GET'])
def render_error():
    request_data = request.form.get('request_data')
    participant_id = request.form.get('participant_id')
    participant = None
    if participant_id:
        participant = models.Participant.query.get(participant_id)
    return error_page(participant=participant, request_data=request_data)


hit_error_template = 'Dear experimenter,\n\nThis is an automated email from Dallinger. You are receiving this email because\na recruited participant has been unable to complete the experiment due to\na bug.\n\nThe application id is: {app_id}\n\nThe information about the failed HIT is recorded in the database in the\nNotification table, with assignment_id {assignment_id}.\n\nTo see the logs, use the command "dallinger logs --app {app_id}"\nTo pause the app, use the command "dallinger hibernate --app {app_id}"\nTo destroy the app, use the command "dallinger destroy --app {app_id}"\n\n\nThe Dallinger dev. team.\n'

@app.route('/handle-error', methods=['POST'])
def handle_error():
    request_data = request.form.get('request_data')
    error_feedback = request.form.get('error_feedback')
    error_type = request.form.get('error_type')
    error_text = request.form.get('error_text')
    worker_id = request.form.get('worker_id')
    assignment_id = request.form.get('assignment_id')
    participant_id = request.form.get('participant_id')
    hit_id = request.form.get('hit_id')
    participant = None
    completed = False
    details = {'request_data': {}}
    if request_data:
        try:
            request_data = loads(request_data)
        except ValueError:
            request_data = {}

        details['request_data'] = request_data
        try:
            data = loads(request_data.get('data', 'null')) or request_data
        except ValueError:
            data = request_data

        if not participant_id:
            if 'participant_id' in data:
                participant_id = data['participant_id']
        if not worker_id and 'worker_id' in data:
            worker_id = data['worker_id']
        if not assignment_id:
            if 'assignment_id' in data:
                assignment_id = data['assignment_id']
        if not hit_id:
            if 'hit_id' in data:
                hit_id = data['hit_id']
    if participant_id:
        try:
            participant_id = int(participant_id)
        except (ValueError, TypeError):
            participant_id = None

    details['feedback'] = error_feedback
    details['error_type'] = error_type
    details['error_text'] = error_text
    if participant_id is None:
        if worker_id:
            participants = session.query(models.Participant).filter_by(worker_id=worker_id).all()
            if participants:
                participant = participants[0]
                if not assignment_id:
                    assignment_id = participant.assignment_id
    if participant_id is None:
        if assignment_id:
            participants = session.query(models.Participant).filter_by(worker_id=assignment_id).all()
            if participants:
                participant = participants[0]
                participant_id = participant.id
                if not worker_id:
                    worker_id = participant.worker_id
    if participant_id is not None:
        _worker_complete(participant_id)
        completed = True
    details['request_data'].update({'worker_id':worker_id, 
     'hit_id':hit_id,  'participant_id':participant_id})
    notif = models.Notification(assignment_id=(assignment_id or 'unknown'),
      event_type='ExperimentError',
      details=details)
    session.add(notif)
    session.commit()
    config = _config()
    message = {'subject':'Error during HIT.', 
     'body':hit_error_template.format(app_id=config.get('id', 'unknown'),
       assignment_id=assignment_id or 'unknown')}
    db.logger.debug('Reporting HIT error...')
    messenger = admin_notifier(config)
    try:
        (messenger.send)(**message)
    except MessengerError as ex:
        db.logger.exception(ex)

    return render_template('error-complete.html',
      completed=completed,
      contact_address=(config.get('contact_email_on_error')),
      hit_id=hit_id)


@app.route('/launch', methods=['POST'])
def launch():
    """Launch the experiment."""
    try:
        exp = Experiment(db.init_db(drop_all=False))
    except Exception as ex:
        return error_response(error_text=('Failed to load experiment in /launch: {}'.format(str(ex))),
          status=500,
          simple=True)

    try:
        exp.log('Launching experiment...', '-----')
    except IOError as ex:
        return error_response(error_text=('IOError writing to experiment log: {}'.format(str(ex))),
          status=500,
          simple=True)

    try:
        recruitment_details = exp.recruiter.open_recruitment(n=(exp.initial_recruitment_size))
        session.commit()
    except Exception as e:
        return error_response(error_text=('Failed to open recruitment, check experiment server log for details: {}'.format(str(e))),
          status=500,
          simple=True)

    for task in exp.background_tasks:
        try:
            gevent.spawn(task)
        except Exception:
            return error_response(error_text=('Failed to spawn task on launch: {}, '.format(task) + 'check experiment server log for details'),
              status=500,
              simple=True)

    if _config().get('replay', False):
        try:
            task = ReplayBackend(exp)
            gevent.spawn(task)
        except Exception:
            return error_response(error_text='Failed to launch replay task for experiment.check experiment server log for details',
              status=500,
              simple=True)

    if exp.channel is not None:
        try:
            from dallinger.experiment_server.sockets import chat_backend
            chat_backend.subscribe(exp, exp.channel)
        except Exception:
            return error_response(error_text=('Failed to subscribe to chat for channel on launch ' + '{}'.format(exp.channel) + ', check experiment server log for details'),
              status=500,
              simple=True)

    message = '\n'.join((
     'Initial recruitment list:\n{}'.format('\n'.join(recruitment_details['items'])),
     'Additional details:\n{}'.format(recruitment_details['message'])))
    return success_response(recruitment_msg=message)


def should_show_thanks_page_to(participant):
    """In the context of the /ad route, should the participant be shown
    the thanks.html page instead of ad.html?
    """
    if participant is None:
        return False
    else:
        status = participant.status
        marked_done = participant.end_time is not None
        ready_for_external_submission = status in ('overrecruited', 'working') and marked_done
        assignment_complete = status in ('submitted', 'approved')
        return assignment_complete or ready_for_external_submission


@app.route('/ad', methods=['GET'])
@nocache
def advertisement():
    """
    This is the url we give for the ad for our 'external question'.  The ad has
    to display two different things: This page will be called from within
    mechanical turk, with url arguments hitId, assignmentId, and workerId.
    If the worker has not yet accepted the hit:
        These arguments will have null values, we should just show an ad for
        the experiment.
    If the worker has accepted the hit:
        These arguments will have appropriate values and we should enter the
        person in the database and provide a link to the experiment popup.
    """
    if not ('hitId' in request.args and 'assignmentId' in request.args):
        raise ExperimentError('hit_assign_worker_id_not_set_in_mturk')
    else:
        config = _config()
        browser = ValidatesBrowser(config)
        if not browser.is_supported(request.user_agent.string):
            raise ExperimentError('browser_type_not_allowed')
        hit_id = request.args['hitId']
        assignment_id = request.args['assignmentId']
        app_id = config.get('id', 'unknown')
        mode = config.get('mode')
        debug_mode = mode == 'debug'
        worker_id = request.args.get('workerId')
        participant = None
        if worker_id is not None:
            already_participated = bool(models.Participant.query.filter(models.Participant.assignment_id != assignment_id).filter(models.Participant.worker_id == worker_id).count())
            if already_participated:
                if not debug_mode:
                    raise ExperimentError('already_did_exp_hit')
            try:
                participant = models.Participant.query.filter(models.Participant.hit_id == hit_id).filter(models.Participant.assignment_id == assignment_id).filter(models.Participant.worker_id == worker_id).one()
            except exc.SQLAlchemyError:
                pass

        recruiter_name = request.args.get('recruiter')
        if recruiter_name:
            recruiter = recruiters.by_name(recruiter_name)
        else:
            recruiter = recruiters.from_config(config)
        recruiter_name = recruiter.nickname
    if should_show_thanks_page_to(participant):
        return render_template('thanks.html',
          hitid=hit_id,
          assignmentid=assignment_id,
          workerid=worker_id,
          external_submit_url=(recruiter.external_submission_url),
          mode=(config.get('mode')),
          app_id=app_id)
    else:
        if participant:
            if participant.status == 'working':
                raise ExperimentError('already_started_exp_mturk')
        return render_template('ad.html',
          recruiter=recruiter_name,
          hitid=hit_id,
          assignmentid=assignment_id,
          workerid=worker_id,
          mode=(config.get('mode')),
          app_id=app_id)


@app.route('/summary', methods=['GET'])
def summary():
    """Summarize the participants' status codes."""
    exp = Experiment(session)
    state = {'status':'success', 
     'summary':exp.log_summary(), 
     'completed':exp.is_complete()}
    unfilled_nets = models.Network.query.filter(models.Network.full != true()).with_entities(models.Network.id, models.Network.max_size).all()
    working = models.Participant.query.filter_by(status='working').with_entities(func.count(models.Participant.id)).scalar()
    state['unfilled_networks'] = len(unfilled_nets)
    nodes_remaining = 0
    required_nodes = 0
    if state['unfilled_networks'] == 0:
        if working == 0:
            if state['completed'] is None:
                state['completed'] = True
    else:
        for net in unfilled_nets:
            node_count = models.Node.query.filter_by(network_id=(net.id), failed=False).with_entities(func.count(models.Node.id)).scalar()
            net_size = net.max_size
            required_nodes += net_size
            nodes_remaining += net_size - node_count

    state['nodes_remaining'] = nodes_remaining
    state['required_nodes'] = required_nodes
    if state['completed'] is None:
        state['completed'] = False
    nonfailed_count = models.Participant.query.filter((models.Participant.status == 'working') | (models.Participant.status == 'overrecruited') | (models.Participant.status == 'submitted') | (models.Participant.status == 'approved')).count()
    exp = Experiment(session)
    overrecruited = exp.is_overrecruited(nonfailed_count)
    if exp.quorum:
        quorum = {'q':exp.quorum, 
         'n':nonfailed_count,  'overrecruited':overrecruited}
        db.queue_message(WAITING_ROOM_CHANNEL, dumps(quorum))
    return Response((dumps(state)), status=200, mimetype='application/json')


@app.route('/experiment_property/<prop>', methods=['GET'])
@app.route('/experiment/<prop>', methods=['GET'])
def experiment_property(prop):
    """Get a property of the experiment by name."""
    exp = Experiment(session)
    try:
        value = exp.public_properties[prop]
    except KeyError:
        abort(404)

    return success_response(**{prop: value})


@app.route('/<page>', methods=['GET'])
def get_page(page):
    """Return the requested page."""
    try:
        return render_template(page + '.html')
    except TemplateNotFound:
        abort(404)


@app.route('/<directory>/<page>', methods=['GET'])
def get_page_from_directory(directory, page):
    """Get a page from a given directory."""
    return render_template(directory + '/' + page + '.html')


@app.route('/consent')
def consent():
    """Return the consent form. Here for backwards-compatibility with 2.x."""
    config = _config()
    return render_template('consent.html',
      hit_id=(request.args['hit_id']),
      assignment_id=(request.args['assignment_id']),
      worker_id=(request.args['worker_id']),
      mode=(config.get('mode')))


def request_parameter(parameter, parameter_type=None, default=None, optional=False):
    """Get a parameter from a request.

    parameter is the name of the parameter you are looking for
    parameter_type is the type the parameter should have
    default is the value the parameter takes if it has not been passed

    If the parameter is not found and no default is specified,
    or if the parameter is found but is of the wrong type
    then a Response object is returned
    """
    exp = Experiment(session)
    try:
        value = request.values[parameter]
    except KeyError:
        if default is not None:
            return default
        else:
            if optional:
                return
            msg = '{} {} request, {} not specified'.format(request.url, request.method, parameter)
            return error_response(error_type=msg)

    if parameter_type is None:
        return value
    else:
        if parameter_type == 'int':
            try:
                value = int(value)
                return value
            except ValueError:
                msg = '{} {} request, non-numeric {}: {}'.format(request.url, request.method, parameter, value)
                return error_response(error_type=msg)

        else:
            if parameter_type == 'known_class':
                try:
                    value = exp.known_classes[value]
                    return value
                except KeyError:
                    msg = '{} {} request, unknown_class: {} for parameter {}'.format(request.url, request.method, value, parameter)
                    return error_response(error_type=msg)

            else:
                if parameter_type == 'bool':
                    if value in ('True', 'False'):
                        return value == 'True'
                    else:
                        msg = '{} {} request, non-boolean {}: {}'.format(request.url, request.method, parameter, value)
                        return error_response(error_type=msg)
                else:
                    msg = '/{} {} request, unknown parameter type: {} for parameter {}'.format(request.url, request.method, parameter_type, parameter)
                    return error_response(error_type=msg)


def assign_properties(thing):
    """Assign properties to an object.

    When creating something via a post request (e.g. a node), you can pass the
    properties of the object in the request. This function gets those values
    from the request and fills in the relevant columns of the table.
    """
    details = request_parameter(parameter='details', optional=True)
    if details:
        setattr(thing, 'details', loads(details))
    for p in range(5):
        property_name = 'property' + str(p + 1)
        property = request_parameter(parameter=property_name, optional=True)
        if property:
            setattr(thing, property_name, property)

    session.commit()


@app.route('/participant/<worker_id>/<hit_id>/<assignment_id>/<mode>', methods=['POST'])
@db.serialized
def create_participant(worker_id, hit_id, assignment_id, mode):
    """Create a participant.

    This route is hit early on. Any nodes the participant creates will be
    defined in reference to the participant object. You must specify the
    worker_id, hit_id, assignment_id, and mode in the url.
    """
    try:
        session.connection().execute('LOCK TABLE participant IN EXCLUSIVE MODE NOWAIT')
    except exc.OperationalError as e:
        e.orig = TransactionRollbackError()
        raise e

    missing = [p for p in (worker_id, hit_id, assignment_id) if p == 'undefined']
    if missing:
        msg = "/participant POST: required values were 'undefined'"
        return error_response(error_type=msg, status=403)
    else:
        fingerprint_hash = request.args.get('fingerprint_hash')
        try:
            fingerprint_found = models.Participant.query.filter_by(fingerprint_hash=fingerprint_hash).one_or_none()
        except MultipleResultsFound:
            fingerprint_found = True

        if fingerprint_hash:
            if fingerprint_found:
                db.logger.warning('Same browser fingerprint detected.')
                if mode == 'live':
                    return error_response(error_type='/participant POST: Same participant dectected.',
                      status=403)
        already_participated = models.Participant.query.filter_by(worker_id=worker_id).one_or_none()
        if already_participated:
            db.logger.warning('Worker has already participated.')
            return error_response(error_type='/participant POST: worker has already participated.',
              status=403)
        duplicate = models.Participant.query.filter_by(assignment_id=assignment_id,
          status='working').one_or_none()
        if duplicate:
            msg = '\n            AWS has reused assignment_id while existing participant is\n            working. Replacing older participant {}.\n        '
            app.logger.warning(msg.format(duplicate.id))
            q.enqueue(worker_function, 'AssignmentReassigned', None, duplicate.id)
        nonfailed_count = models.Participant.query.filter((models.Participant.status == 'working') | (models.Participant.status == 'overrecruited') | (models.Participant.status == 'submitted') | (models.Participant.status == 'approved')).count() + 1
        recruiter_name = request.args.get('recruiter', 'undefined')
        if not recruiter_name or recruiter_name == 'undefined':
            recruiter = recruiters.from_config(_config())
            if recruiter:
                recruiter_name = recruiter.nickname
        participant = models.Participant(recruiter_id=recruiter_name,
          worker_id=worker_id,
          assignment_id=assignment_id,
          hit_id=hit_id,
          mode=mode,
          fingerprint_hash=fingerprint_hash)
        exp = Experiment(session)
        overrecruited = exp.is_overrecruited(nonfailed_count)
        if overrecruited:
            participant.status = 'overrecruited'
        session.add(participant)
        session.flush()
        result = {'participant': participant.__json__()}
        if exp.quorum:
            quorum = {'q':exp.quorum, 
             'n':nonfailed_count,  'overrecruited':overrecruited}
            db.queue_message(WAITING_ROOM_CHANNEL, dumps(quorum))
            result['quorum'] = quorum
        return success_response(**result)


@app.route('/participant/<participant_id>', methods=['GET'])
def get_participant(participant_id):
    """Get the participant with the given id."""
    try:
        ppt = models.Participant.query.filter_by(id=participant_id).one()
    except NoResultFound:
        return error_response(error_type='/participant GET: no participant found',
          status=403)
    else:
        return success_response(participant=(ppt.__json__()))


@app.route('/network/<network_id>', methods=['GET'])
def get_network(network_id):
    """Get the network with the given id."""
    try:
        net = models.Network.query.filter_by(id=network_id).one()
    except NoResultFound:
        return error_response(error_type='/network GET: no network found', status=403)
    else:
        return success_response(network=(net.__json__()))


@app.route('/question/<participant_id>', methods=['POST'])
def create_question(participant_id):
    """Send a POST request to the question table.

    Questions store information at the participant level, not the node
    level.
    You should pass the question (string) number (int) and response
    (string) as arguments.
    """
    try:
        ppt = models.Participant.query.filter_by(id=participant_id).one()
    except NoResultFound:
        return error_response(error_type='/question POST no participant found',
          status=403)
    else:
        question = request_parameter(parameter='question')
        response = request_parameter(parameter='response')
        number = request_parameter(parameter='number', parameter_type='int')
        for x in [question, response, number]:
            if isinstance(x, Response):
                return x

        rejection = ppt.recruiter.rejects_questionnaire_from(ppt)
        if rejection:
            return error_response(error_type=('/question POST, status = {}, reason: {}'.format(ppt.status, rejection)),
              participant=ppt)
        config = get_config()
        question_max_length = config.get('question_max_length', 1000)
        if len(question) > question_max_length or len(response) > question_max_length:
            return error_response(error_type='/question POST length too long', status=400)
        try:
            models.Question(participant=ppt,
              question=question,
              response=response,
              number=number)
            session.commit()
        except Exception:
            return error_response(error_type='/question POST server error', status=403)
        else:
            return success_response()


@app.route('/node/<int:node_id>/neighbors', methods=['GET'])
def node_neighbors(node_id):
    """Send a GET request to the node table.

    This calls the neighbours method of the node
    making the request and returns a list of descriptions of
    the nodes (even if there is only one).
    Required arguments: participant_id, node_id
    Optional arguments: type, connection

    After getting the neighbours it also calls
    exp.node_get_request()
    """
    exp = Experiment(session)
    node_type = request_parameter(parameter='node_type',
      parameter_type='known_class',
      default=(models.Node))
    connection = request_parameter(parameter='connection', default='to')
    failed = request_parameter(parameter='failed', parameter_type='bool', optional=True)
    for x in [node_type, connection]:
        if type(x) == Response:
            return x

    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/node/neighbors, node does not exist',
          error_text=('/node/{0}/neighbors, node {0} does not exist'.format(node_id)))
    if failed is not None:
        try:
            node.neighbors(type=node_type, direction=connection, failed=failed)
        except Exception as e:
            return error_response(error_type='node.neighbors', error_text=(str(e)))

    else:
        nodes = node.neighbors(type=node_type, direction=connection)
        try:
            exp.node_get_request(node=node, nodes=nodes)
            session.commit()
        except Exception:
            return error_response(error_type='exp.node_get_request')

        return success_response(nodes=[n.__json__() for n in nodes])


@app.route('/node/<participant_id>', methods=['POST'])
@db.serialized
def create_node(participant_id):
    """Send a POST request to the node table.

    This makes a new node for the participant, it calls:
        1. exp.get_network_for_participant
        2. exp.create_node
        3. exp.add_node_to_network
        4. exp.node_post_request
    """
    exp = Experiment(session)
    try:
        participant = models.Participant.query.filter_by(id=participant_id).one()
    except NoResultFound:
        return error_response(error_type='/node POST no participant found', status=403)
    else:
        if participant.status != 'working':
            error_type = '/node POST, status = {}'.format(participant.status)
            return error_response(error_type=error_type, participant=participant)
        else:
            network = exp.get_network_for_participant(participant=participant)
            if network is None:
                return Response((dumps({'status': 'error'})), status=403)
            node = exp.create_node(participant=participant, network=network)
            assign_properties(node)
            exp.add_node_to_network(node=node, network=network)
            exp.node_post_request(participant=participant, node=node)
            return success_response(node=(node.__json__()))


@app.route('/node/<int:node_id>/vectors', methods=['GET'])
def node_vectors(node_id):
    """Get the vectors of a node.

    You must specify the node id in the url.
    You can pass direction (incoming/outgoing/all) and failed
    (True/False/all).
    """
    exp = Experiment(session)
    direction = request_parameter(parameter='direction', default='all')
    failed = request_parameter(parameter='failed', parameter_type='bool', default=False)
    for x in [direction, failed]:
        if type(x) == Response:
            return x

    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/node/vectors, node does not exist')
    try:
        vectors = node.vectors(direction=direction, failed=failed)
        exp.vector_get_request(node=node, vectors=vectors)
        session.commit()
    except Exception:
        return error_response(error_type='/node/vectors GET server error',
          status=403,
          participant=(node.participant))
    else:
        return success_response(vectors=[v.__json__() for v in vectors])


@app.route('/node/<int:node_id>/connect/<int:other_node_id>', methods=['POST'])
def connect(node_id, other_node_id):
    """Connect to another node.

    The ids of both nodes must be speficied in the url.
    You can also pass direction (to/from/both) as an argument.
    """
    exp = Experiment(session)
    direction = request_parameter(parameter='direction', default='to')
    if type(direction == Response):
        return direction
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/node/connect, node does not exist')
    other_node = models.Node.query.get(other_node_id)
    if other_node is None:
        return error_response(error_type='/node/connect, other node does not exist',
          participant=(node.participant))
    try:
        vectors = node.connect(whom=other_node, direction=direction)
        for v in vectors:
            assign_properties(v)

        exp.vector_post_request(node=node, vectors=vectors)
        session.commit()
    except Exception:
        return error_response(error_type='/vector POST server error',
          status=403,
          participant=(node.participant))
    else:
        return success_response(vectors=[v.__json__() for v in vectors])


@app.route('/info/<int:node_id>/<int:info_id>', methods=['GET'])
def get_info(node_id, info_id):
    """Get a specific info.

    Both the node and info id must be specified in the url.
    """
    exp = Experiment(session)
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/info, node does not exist')
    info = models.Info.query.get(info_id)
    if info is None:
        return error_response(error_type='/info GET, info does not exist',
          participant=(node.participant))
    if info.origin_id != node.id:
        if info.id not in [t.info_id for t in node.transmissions(direction='incoming', status='received')]:
            return error_response(error_type='/info GET, forbidden info',
              status=403,
              participant=(node.participant))
    try:
        exp.info_get_request(node=node, infos=info)
        session.commit()
    except Exception:
        return error_response(error_type='/info GET server error',
          status=403,
          participant=(node.participant))
    else:
        return success_response(info=(info.__json__()))


@app.route('/node/<int:node_id>/infos', methods=['GET'])
def node_infos(node_id):
    """Get all the infos of a node.

    The node id must be specified in the url.
    You can also pass info_type.
    """
    exp = Experiment(session)
    info_type = request_parameter(parameter='info_type',
      parameter_type='known_class',
      default=(models.Info))
    if type(info_type) == Response:
        return info_type
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/node/infos, node does not exist')
    try:
        infos = node.infos(type=info_type)
        exp.info_get_request(node=node, infos=infos)
        session.commit()
    except Exception:
        return error_response(error_type='/node/infos GET server error',
          status=403,
          participant=(node.participant))
    else:
        return success_response(infos=[i.__json__() for i in infos])


@app.route('/node/<int:node_id>/received_infos', methods=['GET'])
def node_received_infos(node_id):
    """Get all the infos a node has been sent and has received.

    You must specify the node id in the url.
    You can also pass the info type.
    """
    exp = Experiment(session)
    info_type = request_parameter(parameter='info_type',
      parameter_type='known_class',
      default=(models.Info))
    if type(info_type) == Response:
        return info_type
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type=('/node/infos, node {} does not exist'.format(node_id)))
    infos = node.received_infos(type=info_type)
    try:
        exp.info_get_request(node=node, infos=infos)
        session.commit()
    except Exception:
        return error_response(error_type='info_get_request error',
          status=403,
          participant=(node.participant))
    else:
        return success_response(infos=[i.__json__() for i in infos])


@app.route('/tracking_event/<int:node_id>', methods=['POST'])
@crossdomain(origin='*')
def tracking_event_post(node_id):
    """Enqueue a TrackingEvent worker for the specified Node.
    """
    details = request_parameter(parameter='details', optional=True)
    if details:
        details = loads(details)
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/info POST, node does not exist')
    else:
        db.logger.debug('rq: Queueing %s with for node: %s for worker_function', 'TrackingEvent', node_id)
        q.enqueue(worker_function,
          'TrackingEvent', None, None, node_id=node_id, details=details)
        return success_response(details=details)


@app.route('/info/<int:node_id>', methods=['POST'])
@crossdomain(origin='*')
def info_post(node_id):
    """Create an info.

    The node id must be specified in the url.

    You must pass contents as an argument.
    info_type is an additional optional argument.
    If info_type is a custom subclass of Info it must be
    added to the known_classes of the experiment class.
    """
    contents = request_parameter(parameter='contents')
    info_type = request_parameter(parameter='info_type',
      parameter_type='known_class',
      default=(models.Info))
    failed = request_parameter(parameter='failed', parameter_type='bool', default=False)
    for x in [contents, info_type]:
        if type(x) == Response:
            return x

    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/info POST, node does not exist')
    exp = Experiment(session)
    try:
        additional_params = {}
        if failed:
            additional_params['failed'] = failed
        info = info_type(origin=node, contents=contents, **additional_params)
        assign_properties(info)
        exp.info_post_request(node=node, info=info)
        session.commit()
    except Exception:
        return error_response(error_type='/info POST server error',
          status=403,
          participant=(node.participant))
    else:
        return success_response(info=(info.__json__()))


@app.route('/node/<int:node_id>/transmissions', methods=['GET'])
def node_transmissions(node_id):
    """Get all the transmissions of a node.

    The node id must be specified in the url.
    You can also pass direction (to/from/all) or status (all/pending/received)
    as arguments.
    """
    exp = Experiment(session)
    direction = request_parameter(parameter='direction', default='incoming')
    status = request_parameter(parameter='status', default='all')
    for x in [direction, status]:
        if type(x) == Response:
            return x

    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/node/transmissions, node does not exist')
    transmissions = node.transmissions(direction=direction, status=status)
    try:
        if direction in ('incoming', 'all'):
            if status in ('pending', 'all'):
                node.receive()
                session.commit()
        exp.transmission_get_request(node=node, transmissions=transmissions)
        session.commit()
    except Exception:
        return error_response(error_type='/node/transmissions GET server error',
          status=403,
          participant=(node.participant))
    else:
        return success_response(transmissions=[t.__json__() for t in transmissions])


@app.route('/node/<int:node_id>/transmit', methods=['POST'])
def node_transmit(node_id):
    """Transmit to another node.

    The sender's node id must be specified in the url.

    As with node.transmit() the key parameters are what and to_whom. However,
    the values these accept are more limited than for the back end due to the
    necessity of serialization.

    If what and to_whom are not specified they will default to None.
    Alternatively you can pass an int (e.g. '5') or a class name (e.g. 'Info' or
    'Agent'). Passing an int will get that info/node, passing a class name will
    pass the class. Note that if the class you are specifying is a custom class
    it will need to be added to the dictionary of known_classes in your
    experiment code.

    You may also pass the values property1, property2, property3, property4,
    property5 and details. If passed this will fill in the relevant values of
    the transmissions created with the values you specified.

    For example, to transmit all infos of type Meme to the node with id 10:
    dallinger.post(
        "/node/" + my_node_id + "/transmit",
        {what: "Meme",
         to_whom: 10}
    );
    """
    exp = Experiment(session)
    what = request_parameter(parameter='what', optional=True)
    to_whom = request_parameter(parameter='to_whom', optional=True)
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type='/node/transmit, node does not exist')
    if what is not None:
        try:
            what = int(what)
            what = models.Info.query.get(what)
            if what is None:
                return error_response(error_type='/node/transmit POST, info does not exist',
                  participant=(node.participant))
        except Exception:
            try:
                what = exp.known_classes[what]
            except KeyError:
                msg = '/node/transmit POST, {} not in experiment.known_classes'
                return error_response(error_type=(msg.format(what)),
                  participant=(node.participant))

    if to_whom is not None:
        try:
            to_whom = int(to_whom)
            to_whom = models.Node.query.get(to_whom)
            if to_whom is None:
                return error_response(error_type='/node/transmit POST, recipient Node does not exist',
                  participant=(node.participant))
        except Exception:
            try:
                to_whom = exp.known_classes[to_whom]
            except KeyError:
                msg = '/node/transmit POST, {} not in experiment.known_classes'
                return error_response(error_type=(msg.format(to_whom)),
                  participant=(node.participant))

    try:
        transmissions = node.transmit(what=what, to_whom=to_whom)
        for t in transmissions:
            assign_properties(t)

        session.commit()
        exp.transmission_post_request(node=node, transmissions=transmissions)
        session.commit()
    except Exception:
        return error_response(error_type='/node/transmit POST, server error',
          participant=(node.participant))
    else:
        return success_response(transmissions=[t.__json__() for t in transmissions])


@app.route('/node/<int:node_id>/transformations', methods=['GET'])
def transformation_get(node_id):
    """Get all the transformations of a node.

    The node id must be specified in the url.

    You can also pass transformation_type.
    """
    exp = Experiment(session)
    transformation_type = request_parameter(parameter='transformation_type',
      parameter_type='known_class',
      default=(models.Transformation))
    if type(transformation_type) == Response:
        return transformation_type
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type=('/node/transformations, node {} does not exist'.format(node_id)))
    transformations = node.transformations(type=transformation_type)
    try:
        exp.transformation_get_request(node=node, transformations=transformations)
        session.commit()
    except Exception:
        return error_response(error_type='/node/transformations GET failed',
          participant=(node.participant))
    else:
        return success_response(transformations=[t.__json__() for t in transformations])


@app.route('/transformation/<int:node_id>/<int:info_in_id>/<int:info_out_id>',
  methods=['POST'])
def transformation_post(node_id, info_in_id, info_out_id):
    """Transform an info.

    The ids of the node, info in and info out must all be in the url.
    You can also pass transformation_type.
    """
    exp = Experiment(session)
    transformation_type = request_parameter(parameter='transformation_type',
      parameter_type='known_class',
      default=(models.Transformation))
    if type(transformation_type) == Response:
        return transformation_type
    node = models.Node.query.get(node_id)
    if node is None:
        return error_response(error_type=('/transformation POST, node {} does not exist'.format(node_id)))
    info_in = models.Info.query.get(info_in_id)
    if info_in is None:
        return error_response(error_type=('/transformation POST, info_in {} does not exist'.format(info_in_id)),
          participant=(node.participant))
    info_out = models.Info.query.get(info_out_id)
    if info_out is None:
        return error_response(error_type=('/transformation POST, info_out {} does not exist'.format(info_out_id)),
          participant=(node.participant))
    try:
        transformation = transformation_type(info_in=info_in, info_out=info_out)
        assign_properties(transformation)
        session.commit()
        exp.transformation_post_request(node=node, transformation=transformation)
        session.commit()
    except Exception:
        return error_response(error_type='/transformation POST failed',
          participant=(node.participant))
    else:
        return success_response(transformation=(transformation.__json__()))


@app.route('/notifications', methods=['POST', 'GET'])
@crossdomain(origin='*')
def api_notifications():
    """Receive MTurk REST notifications."""
    event_type = request.values['Event.1.EventType']
    assignment_id = request.values.get('Event.1.AssignmentId')
    participant_id = request.values.get('participant_id')
    db.logger.debug('rq: Queueing %s with id: %s for worker_function', event_type, assignment_id)
    q.enqueue(worker_function, event_type, assignment_id, participant_id)
    db.logger.debug('rq: Submitted Queue Length: %d (%s)', len(q), ', '.join(q.job_ids))
    return success_response()


def check_for_duplicate_assignments(participant):
    """Check that the assignment_id of the participant is unique.

    If it isnt the older participants will be failed.
    """
    participants = models.Participant.query.filter_by(assignment_id=(participant.assignment_id)).all()
    duplicates = [p for p in participants if p.id != participant.id if p.status == 'working']
    for d in duplicates:
        q.enqueue(worker_function, 'AssignmentAbandoned', None, d.id)


@app.route('/worker_complete', methods=['GET'])
@db.scoped_session_decorator
def worker_complete():
    """Complete worker."""
    participant_id = request.args.get('participant_id')
    if not participant_id:
        return error_response(error_type='bad request',
          error_text='participantId parameter is required')
    try:
        _worker_complete(participant_id)
    except KeyError:
        return error_response(error_type=('ParticipantId not found: {}'.format(participant_id)))
    else:
        return success_response(status='success')


def _worker_complete(participant_id):
    participants = models.Participant.query.filter_by(id=participant_id).all()
    if not participants:
        raise KeyError()
    participant = participants[0]
    participant.end_time = datetime.now()
    session.add(participant)
    session.commit()
    participant.recruiter.notify_completed(participant)
    event_type = participant.recruiter.submitted_event()
    if event_type is None:
        return
    worker_function(event_type=event_type,
      assignment_id=(participant.assignment_id),
      participant_id=participant_id)


@app.route('/worker_failed', methods=['GET'])
@db.scoped_session_decorator
def worker_failed():
    """Fail worker. Used by bots only for now."""
    participant_id = request.args.get('participant_id')
    if not participant_id:
        return error_response(error_type='bad request',
          error_text='participantId parameter is required')
    try:
        _worker_failed(participant_id)
    except KeyError:
        return error_response(error_type=('ParticipantId not found: {}'.format(participant_id)))
    else:
        return success_response(field='status',
          data='success',
          request_type='worker failed')


def _worker_failed(participant_id):
    participants = models.Participant.query.filter_by(id=participant_id).all()
    if not participants:
        raise KeyError()
    participant = participants[0]
    participant.end_time = datetime.now()
    session.add(participant)
    session.commit()
    if participant.recruiter_id == 'bots' or participant.recruiter_id.startswith('bots:'):
        worker_function(assignment_id=(participant.assignment_id),
          participant_id=(participant.id),
          event_type='BotAssignmentRejected')


def insert_mode(page_html, mode):
    """Insert mode."""
    match_found = False
    matches = re.finditer('workerId={{ workerid }}', page_html)
    match = None
    for match in matches:
        match_found = True

    if match_found:
        new_html = page_html[:match.end()] + '&mode=' + mode + page_html[match.end():]
        return new_html
    raise ExperimentError('insert_mode_failed')