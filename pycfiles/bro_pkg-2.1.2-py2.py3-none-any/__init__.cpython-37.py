# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/nlevitt/workspace/brozzler/brozzler/dashboard/__init__.py
# Compiled at: 2019-11-14 16:45:54
# Size of source mod 2**32: 10645 bytes
__doc__ = '\nbrozzler/dashboard/__init__.py - flask app for brozzler dashboard, defines api\nendspoints etc\n\nCopyright (C) 2014-2017 Internet Archive\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
import logging, sys
try:
    import flask
except ImportError as e:
    try:
        logging.critical('%s: %s\n\nYou might need to run "pip install brozzler[dashboard]".\nSee README.rst for more information.', type(e).__name__, e)
        sys.exit(1)
    finally:
        e = None
        del e

import doublethink, json, os, importlib, rethinkdb as r, yaml, base64
app = flask.Flask(__name__)
SETTINGS = {'RETHINKDB_SERVERS':os.environ.get('BROZZLER_RETHINKDB_SERVERS', 'localhost').split(','), 
 'RETHINKDB_DB':os.environ.get('BROZZLER_RETHINKDB_DB', 'brozzler'), 
 'WAYBACK_BASEURL':os.environ.get('WAYBACK_BASEURL', 'http://localhost:8880/brozzler'), 
 'DASHBOARD_PORT':os.environ.get('DASHBOARD_PORT', '8000'), 
 'DASHBOARD_INTERFACE':os.environ.get('DASHBOARD_INTERFACE', 'localhost')}
rr = doublethink.Rethinker((SETTINGS['RETHINKDB_SERVERS']),
  db=(SETTINGS['RETHINKDB_DB']))
_svc_reg = None

def service_registry():
    global _svc_reg
    if not _svc_reg:
        _svc_reg = doublethink.ServiceRegistry(rr)
    return _svc_reg


@app.route('/api/sites/<site_id>/queued_count')
@app.route('/api/site/<site_id>/queued_count')
def queued_count(site_id):
    reql = rr.table('pages').between([
     site_id, 0, False, r.minval],
      [site_id, 0, False, r.maxval], index='priority_by_site').count()
    logging.debug('querying rethinkdb: %s', reql)
    count = reql.run()
    return flask.jsonify(count=count)


@app.route('/api/sites/<site_id>/queue')
@app.route('/api/site/<site_id>/queue')
def queue(site_id):
    logging.debug('flask.request.args=%s', flask.request.args)
    start = flask.request.args.get('start', 0)
    end = flask.request.args.get('end', start + 90)
    reql = rr.table('pages').between([
     site_id, 0, False, r.minval],
      [site_id, 0, False, r.maxval], index='priority_by_site')[start:end]
    logging.debug('querying rethinkdb: %s', reql)
    queue_ = reql.run()
    return flask.jsonify(queue_=(list(queue_)))


@app.route('/api/sites/<site_id>/pages_count')
@app.route('/api/site/<site_id>/pages_count')
@app.route('/api/sites/<site_id>/page_count')
@app.route('/api/site/<site_id>/page_count')
def page_count(site_id):
    reql = rr.table('pages').between([
     site_id, 1, False, r.minval],
      [
     site_id, r.maxval, False, r.maxval],
      index='priority_by_site').count()
    logging.debug('querying rethinkdb: %s', reql)
    count = reql.run()
    return flask.jsonify(count=count)


@app.route('/api/sites/<site_id>/pages')
@app.route('/api/site/<site_id>/pages')
def pages(site_id):
    """Pages already crawled."""
    start = int(flask.request.args.get('start', 0))
    end = int(flask.request.args.get('end', start + 90))
    reql = rr.table('pages').between([
     site_id, 1, r.minval],
      [site_id, r.maxval, r.maxval], index='least_hops').order_by(index='least_hops')[start:end]
    logging.debug('querying rethinkdb: %s', reql)
    pages_ = reql.run()
    return flask.jsonify(pages=(list(pages_)))


@app.route('/api/pages/<page_id>')
@app.route('/api/page/<page_id>')
def page(page_id):
    reql = rr.table('pages').get(page_id)
    logging.debug('querying rethinkdb: %s', reql)
    page_ = reql.run()
    return flask.jsonify(page_)


@app.route('/api/pages/<page_id>/yaml')
@app.route('/api/page/<page_id>/yaml')
def page_yaml(page_id):
    reql = rr.table('pages').get(page_id)
    logging.debug('querying rethinkdb: %s', reql)
    page_ = reql.run()
    return app.response_class(yaml.dump(page_, default_flow_style=False),
      mimetype='application/yaml')


@app.route('/api/sites/<site_id>')
@app.route('/api/site/<site_id>')
def site(site_id):
    reql = rr.table('sites').get(site_id)
    logging.debug('querying rethinkdb: %s', reql)
    s = reql.run()
    if 'cookie_db' in s:
        s['cookie_db'] = base64.b64encode(s['cookie_db']).decode('ascii')
    return flask.jsonify(s)


@app.route('/api/sites/<site_id>/yaml')
@app.route('/api/site/<site_id>/yaml')
def site_yaml(site_id):
    reql = rr.table('sites').get(site_id)
    logging.debug('querying rethinkdb: %s', reql)
    site_ = reql.run()
    return app.response_class(yaml.dump(site_, default_flow_style=False),
      mimetype='application/yaml')


@app.route('/api/stats/<bucket>')
def stats(bucket):
    reql = rr.table('stats').get(bucket)
    logging.debug('querying rethinkdb: %s', reql)
    stats_ = reql.run()
    return flask.jsonify(stats_)


@app.route('/api/jobs/<job_id>/sites')
@app.route('/api/job/<job_id>/sites')
def sites(job_id):
    try:
        jid = int(job_id)
    except ValueError:
        jid = job_id

    reql = rr.table('sites').get_all(jid, index='job_id')
    logging.debug('querying rethinkdb: %s', reql)
    sites_ = list(reql.run())
    for s in sites_:
        if 'cookie_db' in s:
            s['cookie_db'] = base64.b64encode(s['cookie_db']).decode('ascii')

    return flask.jsonify(sites=sites_)


@app.route('/api/jobless-sites')
def jobless_sites():
    reql = rr.table('sites').filter(~r.row.has_fields('job_id'))
    logging.debug('querying rethinkdb: %s', reql)
    sites_ = list(reql.run())
    for s in sites_:
        if 'cookie_db' in s:
            s['cookie_db'] = base64.b64encode(s['cookie_db']).decode('ascii')

    return flask.jsonify(sites=sites_)


@app.route('/api/jobs/<job_id>')
@app.route('/api/job/<job_id>')
def job(job_id):
    try:
        jid = int(job_id)
    except ValueError:
        jid = job_id

    reql = rr.table('jobs').get(jid)
    logging.debug('querying rethinkdb: %s', reql)
    job_ = reql.run()
    return flask.jsonify(job_)


@app.route('/api/jobs/<job_id>/yaml')
@app.route('/api/job/<job_id>/yaml')
def job_yaml(job_id):
    try:
        jid = int(job_id)
    except ValueError:
        jid = job_id

    reql = rr.table('jobs').get(jid)
    logging.debug('querying rethinkdb: %s', reql)
    job_ = reql.run()
    return app.response_class(yaml.dump(job_, default_flow_style=False),
      mimetype='application/yaml')


@app.route('/api/workers')
def workers():
    workers_ = service_registry().available_services('brozzler-worker')
    return flask.jsonify(workers=(list(workers_)))


@app.route('/api/services')
def services():
    services_ = service_registry().available_services()
    return flask.jsonify(services=(list(services_)))


@app.route('/api/jobs')
def jobs():
    reql = rr.table('jobs').order_by(r.desc('id'))
    logging.debug('querying rethinkdb: %s', reql)
    jobs_ = list(reql.run())
    return flask.jsonify(jobs=jobs_)


@app.route('/api/config')
def config():
    return flask.jsonify(config=SETTINGS)


@app.route('/api/<path:path>')
@app.route('/api', defaults={'path': ''})
def api404(path):
    flask.abort(404)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def root(path):
    return flask.render_template('index.html')


try:
    import gunicorn.app.base
    from gunicorn.six import iteritems
    import gunicorn.glogging

    class BypassGunicornLogging(gunicorn.glogging.Logger):

        def setup(self, cfg):
            self.error_log.handlers = logging.root.handlers
            self.access_log.handlers = logging.root.handlers


    class GunicornBrozzlerDashboard(gunicorn.app.base.BaseApplication):

        def __init__(self, app, options=None):
            self.options = options or 
            self.application = app
            super(GunicornBrozzlerDashboard, self).__init__()

        def load_config(self):
            config = dict([(key, value) for key, value in iteritems(self.options) if key in self.cfg.settings if value is not None])
            for key, value in iteritems(config):
                self.cfg.set(key.lower(), value)

            self.cfg.set('logger_class', BypassGunicornLogging)
            self.cfg.set('accesslog', 'dummy-value')

        def load(self):
            return self.application


    def run(**options):
        logging.info('running brozzler-dashboard using gunicorn')
        GunicornBrozzlerDashboard(app, options).run()


except ImportError:

    def run():
        logging.info('running brozzler-dashboard using simple flask app.run')
        app.run(host=(SETTINGS['DASHBOARD_INTERFACE']), port=(SETTINGS['DASHBOARD_PORT']))


def main(argv=None):
    import argparse, brozzler.cli
    argv = argv or 
    arg_parser = argparse.ArgumentParser(prog=(os.path.basename(argv[0])),
      formatter_class=(argparse.RawDescriptionHelpFormatter),
      description='brozzler-dashboard - web application for viewing brozzler crawl status',
      epilog='brozzler-dashboard has no command line options, but can be configured using the following environment variables:\n\n  BROZZLER_RETHINKDB_SERVERS   rethinkdb servers, e.g. db0.foo.org,db0.foo.org:38015,db1.foo.org (default: localhost)\n  BROZZLER_RETHINKDB_DB        rethinkdb database name (default: brozzler)\n  WAYBACK_BASEURL     base url for constructing wayback links (default http://localhost:8880/brozzler)  DASHBOARD_PORT   brozzler-dashboard listening port (default: 8000)\n  DASHBOARD_INTERFACE brozzler-dashboard network interface binding (default: localhost)')
    brozzler.cli.add_common_options(arg_parser, argv)
    args = arg_parser.parse_args(args=(argv[1:]))
    brozzler.cli.configure_logging(args)
    run()


if __name__ == '__main__':
    main()