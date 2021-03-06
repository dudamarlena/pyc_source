# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/apptool.py
# Compiled at: 2010-12-12 12:10:20
"""Console script to perform common tasks on configuring an application."""
from google.appengine.api.taskqueue.taskqueue_stub import _ParseQueueYaml
import google.appengine.api.croninfo, google.appengine.cron, getpass, logging, optparse, os, re, socket, subprocess, sys, tempfile, typhoonae, typhoonae.fcgiserver
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
DESCRIPTION = 'Console script to perform common tasks on configuring an application.'
USAGE = 'usage: %prog [options] <application root>'
DEFAULT_EXPIRATION = '30d'
NGINX_HEADER = '\nserver {\n    client_max_body_size 100m;\n    listen      %(http_port)s;\n    server_name %(app_domain)s.*;\n    %(add_server_params)s\n    access_log  %(var)s/log/httpd-access.log;\n    error_log   %(var)s/log/httpd-error.log;\n'
NGINX_ERROR_PAGES = '\nerror_page   500 502 503 504  /50x.html;\nlocation = /50x.html {\n    root "%(root)s";\n}\n'
NGINX_FOOTER = '\n}\n'
NGINX_STATIC_LOCATION = '\nlocation ~ ^/(%(path)s)/ {\n    root "%(root)s";%(rewrite)s\n    expires %(expires)s;\n}\n'
NGINX_REWRITE_LOCATION = '\nlocation ~* ^%(regex)s$ {\n    rewrite %(rewrite)s break;\n}\n'
NGINX_REGEX_LOCATION = '\nlocation ~* ^%(regex)s$ {\n    root "%(root)s";\n    rewrite %(rewrite)s break;\n    expires %(expires)s;\n}\n'
FCGI_PARAMS = '    set $stripped_http_host $http_host;\n    if ($http_host ~ ^(.*):([0-9]+)$) {\n      set $stripped_http_host $1;\n    }\n    fastcgi_param CONTENT_LENGTH $content_length;\n    fastcgi_param CONTENT_TYPE $content_type;\n    fastcgi_param PATH_INFO $fastcgi_script_name;\n    fastcgi_param QUERY_STRING $query_string;\n    fastcgi_param REMOTE_ADDR $remote_addr;\n    fastcgi_param REQUEST_METHOD $request_method;\n    fastcgi_param REQUEST_URI $request_uri;\n    fastcgi_param SERVER_NAME $stripped_http_host;\n    fastcgi_param SERVER_PORT $server_port;\n    fastcgi_param SERVER_PROTOCOL $server_protocol;\n    %(add_fcgi_params)s\n    fastcgi_pass_header Authorization;\n\n    # Increase the allowed size of the response.\n    fastcgi_buffer_size 128k;\n    fastcgi_buffers 4 256k;\n    fastcgi_busy_buffers_size 256k;\n    fastcgi_temp_file_write_size 256k;\n\n    fastcgi_intercept_errors off;'
NGINX_BASIC_AUTH_LOCATION = '\nlocation ~ ^/(%(path)s) {\n    auth_basic "%(app_id)s";\n    auth_basic_user_file %(passwd_file)s;\n    fastcgi_pass %(fcgi_host)s:%(fcgi_port)s;\n%(fcgi_params)s\n}\n'
NGINX_FCGI_CONFIG = '\nlocation ~ {\n    fastcgi_pass %(fcgi_host)s:%(fcgi_port)s;\n%(fcgi_params)s\n}\n'
NGINX_UPLOAD_CONFIG = '\nlocation ~* /%(upload_url)s {\n    # Pass altered request body to this location\n    upload_pass @%(app_version_domain)s;\n\n    # Store files to this directory\n    # The directory is hashed, subdirectories 0 1 2 3 4 5 6 7 8 9\n    # should exist\n    upload_store %(blobstore_path)s 1;\n\n    # Set permissions for uploaded files\n    upload_store_access user:rw group:rw;\n\n    # Set specified fields in request body\n    upload_set_form_field $upload_field_name.name "$upload_file_name";\n    upload_set_form_field $upload_field_name.content_type "$upload_content_type";\n    upload_set_form_field $upload_field_name.path "$upload_tmp_path";\n\n    # Inform backend about hash and size of a file\n    upload_aggregate_form_field "$upload_field_name.md5" "$upload_file_md5";\n    upload_aggregate_form_field "$upload_field_name.size" "$upload_file_size";\n\n    upload_pass_form_field ".*";\n\n    upload_cleanup 400 404 499 500-505;\n}\n\nlocation @%(app_version_domain)s {\n    fastcgi_pass %(fcgi_host)s:%(fcgi_port)s;\n%(fcgi_params)s\n}\n'
NGINX_DOWNLOAD_CONFIG = '\nlocation ~ ^/_ah/blobstore/%(app_id)s/(.*) {\n    root "%(blobstore_path)s";\n    rewrite ^/_ah/blobstore/%(app_id)s/(.*) /$1 break;\n    expires 5d;\n    internal;\n}\n'
NGINX_PUSH_PUBLISH_CONFIG = '\nlocation ~ ^/_ah/publish {\n    set $push_channel_id $arg_id;\n    push_publisher;\n    push_store_messages off;\n    push_message_timeout 2h;\n    push_max_message_buffer_length 10;\n}\n'
NGINX_PUSH_SUBSCRIBE_CONFIG = '\nlocation ~ ^/_ah/subscribe {\n    push_subscriber long-poll;\n    push_subscriber_concurrency broadcast;\n    set $push_channel_id $arg_id;\n    default_type text/plain;\n}\n'
SUPERVISOR_MONGODB_CONFIG = '\n[program:mongod]\ncommand = %(bin_dir)s/mongod --dbpath=%(var)s\nprocess_name = mongod\ndirectory = %(bin_dir)s\npriority = 10\nredirect_stderr = true\nstdout_logfile = %(var)s/log/mongod.log\nenvironment = %(environment)s\n'
SUPERVISOR_BDBDATASTORE_CONFIG = '\n[program:bdbdatastore]\ncommand = java -jar %(root)s/parts/bdbdatastore/bdbdatastore-0.2.2.jar %(var)s\nprocess_name = bdbdatastore\ndirectory = %(app_root)s\npriority = 10\nredirect_stderr = true\nstdout_logfile = %(var)s/log/bdbdatastore.log\n'
SUPERVISOR_APPSERVER_CONFIG = '\n[fcgi-program:%(app_id)s.%(version)s]\ncommand = %(bin_dir)s/appserver --server_name=%(server_name)s --http_port=%(http_port)s --auth_domain=%(auth_domain)s --datastore=%(datastore)s --xmpp_host=%(xmpp_host)s --server_software=%(server_software)s --blobstore_path=%(blobstore_path)s --upload_url=%(upload_url)s --smtp_host=%(smtp_host)s --smtp_port=%(smtp_port)s --smtp_user=%(smtp_user)s --smtp_password=%(smtp_password)s --email=%(email)s --password=%(password)s %(add_opts)s "%(app_root)s"\nsocket = tcp://%(fcgi_host)s:%(fcgi_port)s\nprocess_name = %%(program_name)s_%%(process_num)02d\nnumprocs = 2\npriority = 999\nredirect_stderr = true\nstdout_logfile = %(var)s/log/%(app_id)s.log\nstdout_logfile_maxbytes = 1MB\nstdout_logfile_backups = 10\nstderr_logfile = %(var)s/log/%(app_id)s-error.log\nstderr_logfile_maxbytes = 1MB\nenvironment = %(environment)s\nautorestart = True\n\n[eventlistener:%(app_id)s.%(version)s_monitor]\ncommand=%(bin_dir)s/memmon -g %(app_id)s=200MB\nevents=TICK_60\n'
SUPERVISOR_AMQP_CONFIG = '\n[program:%(app_id)s_taskworker]\ncommand = %(bin_dir)s/taskworker --amqp_host=%(amqp_host)s\nprocess_name = %(app_id)s_taskworker\ndirectory = %(root)s\npriority = 20\nredirect_stderr = true\nstdout_logfile = %(var)s/log/taskworker.log\nenvironment = %(environment)s\n\n[program:%(app_id)s_deferred_taskworker]\ncommand = %(bin_dir)s/deferred_taskworker --amqp_host=%(amqp_host)s\nprocess_name = %(app_id)s_deferred_taskworker\ndirectory = %(root)s\npriority = 20\nredirect_stderr = true\nstdout_logfile = %(var)s/log/deferred_taskworker.log\nenvironment = %(environment)s\n'
SUPERVISOR_CELERY_CONFIG = '\n[program:%(app_id)s_celeryworkers]\ncommand = %(bin_dir)s/celeryd\nprocess_name = %(app_id)s_celeryworkers\ndirectory = %(app_root)s\npriority = 20\nstdout_logfile = %(var)s/log/celery_workers.out.log\nstderr_logfile = %(var)s/log/celery_workers.err.log\nautostart=true\nautorestart=true\nstartsecs=10\nenvironment=APP_ROOT="%(app_root)s",TZ="UTC" %(environment)s\n\n; Need to wait for currently executing tasks to finish at shutdown.\n; Increase this if you have very long running tasks.\nstopwaitsecs = 30\n'
SUPERVISOR_XMPP_HTTP_DISPATCH_CONFIG = '\n[program:%(app_id)s_xmpp_http_dispatch]\ncommand = %(bin_dir)s/xmpp_http_dispatch --address=%(internal_address)s --jid=%(jid)s --password=%(password)s\nprocess_name = %(app_id)s_xmpp_http_dispatch\npriority = 999\nredirect_stderr = true\nstdout_logfile = %(var)s/log/xmpp_http_dispatch.log\nenvironment = %(environment)s\n'
SUPERVISOR_IMAP_HTTP_DISPATCH_CONFIG = '\n[program:%(app_id)s_imap_http_dispatch]\ncommand = %(bin_dir)s/imap_http_dispatch --address=%(internal_address)s --imap_host=%(imap_host)s --imap_port=%(imap_port)s %(imap_ssl_option_key)s  --imap_mailbox=%(imap_mailbox)s --imap_user=%(imap_user)s --imap_password=%(imap_password)s\nprocess_name = %(app_id)s_imap_http_dispatch\npriority = 999\nredirect_stderr = true\nstdout_logfile = %(var)s/log/imap_http_dispatch.log\nenvironment = %(environment)s\n'
SUPERVISOR_WEBSOCKET_CONFIG = '\n[program:websocket]\ncommand = %(bin_dir)s/websocket --internal_port=%(internal_port)s\nprocess_name = websocket\npriority = 999\nredirect_stderr = true\nstdout_logfile = %(var)s/log/websocket.log\nenvironment = %(environment)s\n'
EJABBERD_CONFIG = '\noverride_local.\n\noverride_acls.\n\n{loglevel, 4}.\n\n{hosts, ["%(xmpp_host)s"]}.\n\n{listen,\n [\n\n  {5222, ejabberd_c2s, [\n\n                        {access, c2s},\n                        {shaper, c2s_shaper},\n                        {max_stanza_size, 65536}\n                       ]},\n\n  {5269, ejabberd_s2s_in, [\n                           {shaper, s2s_shaper},\n                           {max_stanza_size, 131072}\n                          ]},\n\n  {5280, ejabberd_http, [\n                         captcha,\n                         http_bind,\n                         http_poll,\n                         web_admin\n                        ]}\n\n ]}.\n\n{auth_method, [external]}.\n\n{extauth_program, "%(bin_dir)s/ejabberdauth"}.\n\n{shaper, normal, {maxrate, 1000}}.\n\n{shaper, fast, {maxrate, 50000}}.\n\n{acl, local, {user_regexp, ""}}.\n\n{access, max_user_sessions, [{10, all}]}.\n\n{access, max_user_offline_messages, [{5000, admin}, {100, all}]}.\n\n{access, local, [{allow, local}]}.\n\n{access, c2s, [{deny, blocked},\n               {allow, all}]}.\n\n{access, c2s_shaper, [{none, admin},\n                      {normal, all}]}.\n\n{access, s2s_shaper, [{fast, all}]}.\n\n{access, announce, [{allow, admin}]}.\n\n{access, configure, [{allow, admin}]}.\n\n{access, muc_admin, [{allow, admin}]}.\n\n{access, muc, [{allow, all}]}.\n\n{access, pubsub_createnode, [{allow, all}]}.\n\n{access, register, [{allow, all}]}.\n\n{language, "en"}.\n\n{modules,\n [\n  {mod_adhoc,    []},\n  {mod_announce, [{access, announce}]},\n  {mod_caps,     []},\n  {mod_configure,[]},\n  {mod_disco,    []},\n  {mod_irc,      []},\n  {mod_http_bind, []},\n  {mod_last,     []},\n  {mod_muc,      [\n                  {access, muc},\n                  {access_create, muc},\n                  {access_persistent, muc},\n                  {access_admin, muc_admin}\n                 ]},\n  {mod_offline,  [{access_max_user_messages, max_user_offline_messages}]},\n  {mod_ping,     []},\n  {mod_privacy,  []},\n  {mod_private,  []},\n  {mod_pubsub,   [\n                  {access_createnode, pubsub_createnode},\n                  {pep_sendlast_offline, false},\n                  {last_item_cache, false},\n                  {plugins, ["flat", "hometree", "pep"]}\n                 ]},\n  {mod_register, [\n                  {welcome_message, {"Welcome!",\n                                     "Hi.\\nWelcome to this Jabber server."}},\n                  {access, register}\n                 ]},\n  {mod_roster,   []},\n  {mod_shared_roster,[]},\n  {mod_stats,    []},\n  {mod_time,     []},\n  {mod_vcard,    []},\n  {mod_version,  []}\n ]}.\n'
CELERY_CONFIG = '\nBROKER_HOST = "%(amqp_host)s"\nBROKER_PORT = 5672\nBROKER_USER = "guest"\nBROKER_PASSWORD = "guest"\nBROKER_VHOST = "/"\n\nCELERY_RESULT_BACKEND = "amqp"\nCELERY_IMPORTS = ("typhoonae.taskqueue.celery_tasks",%(celery_imports)s)\n\nCELERYD_LOG_FILE = "%(var)s/log/celeryd.log"\nCELERYD_LOG_LEVEL = "INFO"\nCELERYD_MAX_TASKS_PER_CHILD = 1000\nCELERYD_SOFT_TASK_TIME_LIMIT = %(soft_task_time_limit)s\nCELERYD_TASK_TIME_LIMIT = %(task_time_limit)s\n\nCELERY_QUEUES = %(celery_queues)s\nCELERY_DEFAULT_QUEUE = "default"\nCELERY_DEFAULT_EXCHANGE = "%(app_id)s"\nCELERY_DEFAULT_EXCHANGE_TYPE = "direct"\nCELERY_DEFAULT_ROUTING_KEY = "default"\n'

def make_blobstore_dirs(blobstore_path):
    """Makes Blobstore directories."""
    for i in range(10):
        p = os.path.join(blobstore_path, str(i))
        if not os.path.isdir(p):
            os.makedirs(p)


def write_nginx_conf(options, conf, app_root, default_version=True, internal=False, secure=False, mode='w'):
    """Writes nginx server configuration stub."""
    app_domain = ''
    add_fcgi_params = []
    add_server_params = ''
    app_id = conf.application
    blobstore_path = os.path.abspath(os.path.join(options.blobstore_path, app_id))
    fcgi_host = options.fcgi_host
    fcgi_port = options.fcgi_port
    html_error_pages_root = options.html_error_pages_root
    http_port = options.http_port
    server_name = options.server_name
    ssl_certificate = options.ssl_certificate
    ssl_certificate_key = options.ssl_certificate_key
    ssl_enabled = options.ssl_enabled
    upload_url = options.upload_url
    var = os.path.abspath(options.var)
    version = conf.version
    app_version_domain = app_id
    if not default_version:
        app_version_domain = '%s.latest.' % version + app_version_domain
    if options.multiple:
        app_domain = app_version_domain
    if secure:
        http_port = options.https_port
        add_server_params = ('\n    ').join((k + ' ' + v + ';' for (k, v) in [
         ('ssl', 'on'),
         (
          'ssl_certificate', ssl_certificate),
         (
          'ssl_certificate_key', ssl_certificate_key)]))
    if options.multiple:
        nginx_conf_path = os.path.join('etc', '%s-nginx.conf' % app_version_domain)
    else:
        nginx_conf_path = os.path.join('etc', 'default-nginx.conf')
    nginx_conf_path = os.path.abspath(nginx_conf_path)
    httpd_conf_stub = open(nginx_conf_path, mode)
    if not internal and not secure:
        httpd_conf_stub.write("# Automatically generated NGINX configuration file: don't edit!\n# Use apptool to modify.\n")
    elif internal:
        httpd_conf_stub.write('# Internal configuration.\n')
        (server_name, http_port) = options.internal_address.split(':')
        add_fcgi_params = ['fastcgi_param X-TyphoonAE-Secret "secret";']
        add_server_params = ''
    elif secure:
        httpd_conf_stub.write('# Secure configuration.\n')
    httpd_conf_stub.write(NGINX_HEADER % locals())
    urls_require_login = []
    for handler in conf.handlers:
        ltrunc_url = re.sub('^/', '', handler.url)
        if ltrunc_url and ssl_enabled and not internal and not secure and handler.secure == 'always':
            rewrite = '^/(%s)$ https://%s' % (ltrunc_url, server_name)
            if options.https_port != '443':
                rewrite += ':%s' % options.https_port
            rewrite += '/$1'
            httpd_conf_stub.write(NGINX_REWRITE_LOCATION % dict(regex='/(%s)' % ltrunc_url, rewrite=rewrite))
            continue
        if ltrunc_url and ssl_enabled and not internal and secure and handler.secure == 'never':
            rewrite = '^/(%s)$ http://%s' % (ltrunc_url, server_name)
            if options.http_port != '80':
                rewrite += ':%s' % options.http_port
            rewrite += '/$1'
            httpd_conf_stub.write(NGINX_REWRITE_LOCATION % dict(regex='/(%s)' % ltrunc_url, rewrite=rewrite))
            continue
        if handler.GetHandlerType() == 'static_dir':
            if ltrunc_url != handler.static_dir:
                rewrite = '^/(%s)/(.*)$ /%s/$2 break;' % (ltrunc_url,
                 handler.static_dir)
                rewrite = '\n    rewrite ' + rewrite
            else:
                rewrite = ''
            l = handler.static_dir.split('/')
            httpd_conf_stub.write(NGINX_STATIC_LOCATION % dict(expires=handler.expiration or conf.default_expiration or DEFAULT_EXPIRATION, path=ltrunc_url, rewrite=rewrite, root=app_root))
        if handler.GetHandlerType() == 'static_files':
            if handler.url == '/':
                url = '/(%s)' % handler.upload.split('/')[(-1)]
                files = handler.static_files.replace(handler.upload, '$1')
            else:
                url = handler.url
                files = handler.static_files.replace('\\', '$')
            rewrite = '^%s$ /%s' % (url, files)
            httpd_conf_stub.write(NGINX_REGEX_LOCATION % dict(expires=handler.expiration or conf.default_expiration or DEFAULT_EXPIRATION, regex=url, rewrite=rewrite, root=app_root))
        if handler.login in ('admin', 'required'):
            if ltrunc_url not in urls_require_login:
                urls_require_login.append(ltrunc_url)
        if not internal and secure:
            if handler.secure == 'always':
                logger.warn("secure parameter with value 'always' for %s ignored" % handler.url)
            elif handler.secure == 'never':
                logger.warn("secure parameter with value 'never' for %s ignored" % handler.url)

    if options.http_base_auth_enabled:
        login_url = options.login_url or '/_ah/login'
        urls_require_login.append(login_url[1:])
    if urls_require_login and options.http_base_auth_enabled and not internal:
        httpd_conf_stub.write(NGINX_BASIC_AUTH_LOCATION % dict(app_id=conf.application, fcgi_host=fcgi_host, fcgi_params=FCGI_PARAMS % {'add_fcgi_params': ('\n').join(add_fcgi_params)}, fcgi_port=fcgi_port, passwd_file=os.path.join(app_root, 'htpasswd'), path=('|').join(urls_require_login)))
    fcgi_params = FCGI_PARAMS % {'add_fcgi_params': ('\n').join(add_fcgi_params)}
    httpd_conf_stub.write(NGINX_UPLOAD_CONFIG % locals())
    httpd_conf_stub.write(NGINX_DOWNLOAD_CONFIG % locals())
    httpd_conf_stub.write(NGINX_PUSH_SUBSCRIBE_CONFIG % locals())
    if internal:
        httpd_conf_stub.write(NGINX_PUSH_PUBLISH_CONFIG % locals())
    httpd_conf_stub.write(NGINX_FCGI_CONFIG % locals())
    if html_error_pages_root:
        httpd_conf_stub.write(NGINX_ERROR_PAGES % {'root': html_error_pages_root})
    httpd_conf_stub.write(NGINX_FOOTER)
    httpd_conf_stub.close()
    return [
     nginx_conf_path]


def write_supervisor_conf(options, conf, app_root):
    """Writes supervisord configuration stub."""
    amqp_host = options.amqp_host
    app_id = conf.application
    auth_domain = options.auth_domain
    bin_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    blobstore_path = os.path.abspath(options.blobstore_path)
    current_version_id = options.current_version_id
    datastore = options.datastore.lower()
    develop_mode = options.develop_mode
    email = options.email
    environment = options.environment
    fcgi_host = options.fcgi_host
    fcgi_port = options.fcgi_port
    http_port = options.http_port
    imap_host = options.imap_host
    imap_port = options.imap_port
    imap_ssl_option_key = '--imap_ssl' if options.imap_ssl else ''
    imap_user = options.imap_user
    imap_password = options.imap_password
    imap_mailbox = options.imap_mailbox
    internal_address = options.internal_address
    internal_port = None
    password = options.password
    root = os.getcwd()
    server_software = options.server_software
    smtp_host = options.smtp_host
    smtp_port = options.smtp_port
    smtp_user = options.smtp_user
    smtp_password = options.smtp_password
    upload_url = options.upload_url
    var = os.path.abspath(options.var)
    version = conf.version
    websocket_disabled = options.websocket_disabled
    xmpp_host = options.xmpp_host
    if options.multiple:
        server_name = '%s.%s' % (app_id, options.server_name)
    else:
        server_name = options.server_name
    additional_options = []
    if current_version_id:
        additional_options.append(('current_version_id', current_version_id))
    if develop_mode:
        additional_options.append(('debug', None))
    if internal_address:
        additional_options.append(('internal_address', internal_address))
        (unused_host, internal_port) = internal_address.split(':')
    if options.login_url:
        additional_options.append(('login_url', options.login_url))
    if options.logout_url:
        additional_options.append(('logout_url', options.logout_url))
    if options.use_celery:
        additional_options.append(('use_celery', None))
    if datastore == 'mysql':
        if options.mysql_db:
            additional_options.append(('mysql_db', options.mysql_db))
        if options.mysql_host:
            additional_options.append(('mysql_host', options.mysql_host))
        if options.mysql_passwd:
            additional_options.append(('mysql_passwd', options.mysql_passwd))
        if options.mysql_user:
            additional_options.append(('mysql_user', options.mysql_user))
    add_opts = (' ').join([ '--%s' % opt for (opt, arg) in additional_options if arg is None ] + [ '--%s=%s' % (opt, arg) for (opt, arg) in additional_options if arg ])
    supervisor_conf_name = '%s.latest.%s-supervisor.conf' % (version, app_id)
    supervisor_conf_path = os.path.join(root, 'etc', supervisor_conf_name)
    supervisor_conf_stub = open(supervisor_conf_path, 'w')
    supervisor_conf_stub.write("# Automatically generated supervisor configuration file: don't edit!\n# Use apptool to modify.\n")
    if datastore == 'mongodb':
        supervisor_conf_stub.write(SUPERVISOR_MONGODB_CONFIG % locals())
    elif datastore == 'bdbdatastore':
        supervisor_conf_stub.write(SUPERVISOR_BDBDATASTORE_CONFIG % locals())
    elif datastore == 'mysql':
        pass
    elif datastore == 'remote':
        pass
    else:
        raise RuntimeError, 'unknown datastore'
    supervisor_conf_stub.write(SUPERVISOR_APPSERVER_CONFIG % locals())
    if options.use_celery:
        supervisor_conf_stub.write(SUPERVISOR_CELERY_CONFIG % locals())
    else:
        supervisor_conf_stub.write(SUPERVISOR_AMQP_CONFIG % locals())
    if not websocket_disabled:
        supervisor_conf_stub.write(SUPERVISOR_WEBSOCKET_CONFIG % locals())
    jid = conf.application + '@' + xmpp_host
    password = conf.application
    if conf.inbound_services is not None:
        for service in conf.inbound_services:
            if service == 'xmpp_message':
                supervisor_conf_stub.write(SUPERVISOR_XMPP_HTTP_DISPATCH_CONFIG % locals())
            elif service == 'mail':
                supervisor_conf_stub.write(SUPERVISOR_IMAP_HTTP_DISPATCH_CONFIG % locals())

    supervisor_conf_stub.close()
    return [
     supervisor_conf_path]


def write_ejabberd_conf(options):
    """Writes ejabberd configuration file."""
    bin_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    xmpp_host = options.xmpp_host
    ejabberd_conf_path = os.path.abspath(options.ejabberd)
    ejabberd_conf = open(ejabberd_conf_path, 'w')
    ejabberd_conf.write(EJABBERD_CONFIG % locals())
    ejabberd_conf.close()
    return [
     ejabberd_conf_path]


def write_celery_conf(options, conf, app_root):
    """Writes celery configuration file."""
    amqp_host = options.amqp_host
    if options.celery_imports:
        celery_imports_list = options.celery_imports.split(',')
        celery_imports = (',').join(('"%s"' % i for i in celery_imports_list))
    else:
        celery_imports = ''
    task_time_limit = int(options.task_time_limit)
    if task_time_limit:
        soft_task_time_limit = task_time_limit - 1
    else:
        task_time_limit = 'None'
        soft_task_time_limit = 'None'
    var = options.var
    queue_info = _ParseQueueYaml(None, app_root)
    if queue_info and queue_info.queue:
        queues = [ entry.name for entry in queue_info.queue ]
    else:
        queues = [
         'default']
    celery_queues = '{\n    %s\n}' % (',\n    ').join(('"%s": { "binding_key": "%s" }' % (q, q) for q in queues))
    app_id = conf.application
    celery_conf = open(options.celery, 'w')
    celery_conf.write(CELERY_CONFIG % locals())
    celery_conf.close()
    return [
     options.celery]


def print_error(msg):
    """Prints an error message to the standard error stream."""
    sys.stderr.write('%s: %s\n' % (os.path.basename(sys.argv[0]), msg))


CRONTAB_ROW = re.compile('^\\s*([^@#\\s]+)\\s+([^@#\\s]+)\\s+([^@#\\s]+)\\s+([^@#\\s]+)\\s+([^@#\\s]+)\\s+([^#\\n]*)(\\s+#\\s*([^\\n]*)|$)')
EVERY_DAY_SET = set([0, 1, 2, 3, 4, 5, 6])
EVERY_MONTH_SET = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

def read_crontab(options):
    """Reads the user's crontab.

    Args:
        options: Dictionary of command line options.

    Returns crontab entries.
    """
    result = list()
    p = subprocess.Popen([
     'crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    for entry in stdout.split('\n'):
        m = re.match(CRONTAB_ROW, entry)
        if m:
            result.append(m.groups())

    return result


class CrontabRow(object):
    """Represents one crontab row."""

    def __init__(self):
        """Initialize crontab row instance."""
        self.minute = '*'
        self.hour = '*'
        self.dom = '*'
        self.month = '*'
        self.dow = '*'
        self.command = ''
        self.description = None
        return

    def __repr__(self):
        return '%s %s %s %s %s %s # %s' % (
         self.minute, self.hour, self.dom, self.month, self.dow,
         self.command, self.description)


def write_crontab(options, app_root):
    """Writes crontab entries."""
    cron_path = os.path.join(app_root, 'cron.yaml')
    if not os.path.isfile(cron_path):
        return
    cron_file = open(cron_path, 'r')
    try:
        try:
            cron_info = google.appengine.api.croninfo.LoadSingleCron(cron_file)
        except Exception, err_obj:
            print_error(str(err_obj))
            return

    finally:
        cron_file.close()

    tab = read_crontab(options)
    if not cron_info.cron:
        return tab
    for entry in cron_info.cron:
        parser = google.appengine.cron.groc.CreateParser(entry.schedule)
        parser.timespec()
        row = CrontabRow()
        if parser.time_string:
            (m, h) = parser.time_string.split(':')
            if len(m) == 2 and m[0] == '0':
                m = m[1:]
            if len(h) == 2 and h[0] == '0':
                h = h[1:]
            row.minute = m
            row.hour = h
        if parser.period_string:
            if parser.period_string == 'hours':
                row.minute = '0'
                row.hour = '*/%i' % parser.interval_mins
            elif parser.period_string == 'minutes':
                row.minute = '*/%i' % parser.interval_mins
        if parser.month_set and parser.month_set != EVERY_MONTH_SET:
            row.month = (',').join(map(str, parser.month_set))
        if parser.weekday_set and parser.weekday_set != EVERY_DAY_SET:
            row.dow = (',').join(map(str, parser.weekday_set))
        row.command = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'runtask')
        (server_name, http_port) = options.internal_address.split(':')
        row.command += ' http://%s:%s%s' % (server_name, http_port, entry.url)
        row.description = '%s (%s)' % (entry.description, entry.schedule)
        tab.append(re.match(CRONTAB_ROW, str(row)).groups())

    if options.set_crontab:
        (_, path) = tempfile.mkstemp()
        try:
            tmp = open(path, 'w')
            tmp.write(('\n').join([ (' ').join(r) for r in tab ]) + '\n')
            tmp.close()
            subprocess.call(['crontab', path])
        finally:
            if os.path.isfile(path):
                os.remove(path)

    return tab


def setdir(path):
    """Returns the path if present."""
    if os.path.isdir(path):
        return path
    raise RuntimeError('Directory not found: "%s"' % path)


def main():
    """Runs the apptool console script."""
    op = optparse.OptionParser(description=DESCRIPTION, usage=USAGE)
    op.add_option('--auth_domain', dest='auth_domain', metavar='DOMAIN', help='use this value for the AUTH_DOMAIN environment variable', default='localhost')
    op.add_option('--amqp_host', dest='amqp_host', metavar='ADDR', help='use this AMQP host', default='localhost')
    op.add_option('--blobstore_path', dest='blobstore_path', metavar='PATH', help='path to use for storing Blobstore file stub data', default=os.path.join('var', 'blobstore'))
    op.add_option('--celery', dest='celery', metavar='FILE', help='write celery configuration to this file', default=os.path.join('etc', 'celeryconfig.py'))
    op.add_option('--celery_imports', dest='celery_imports', metavar='LIST', help='sequence of modules to import when the celery daemon starts')
    op.add_option('--crontab', dest='set_crontab', action='store_true', help='set crontab if cron.yaml exists', default=False)
    op.add_option('--current_version_id', dest='current_version_id', metavar='STRING', help='the current version id', default=None)
    op.add_option('--datastore', dest='datastore', metavar='NAME', help='use this Datastore backend (%s)' % ('/').join(sorted(typhoonae.SUPPORTED_DATASTORES)), default='mongodb')
    op.add_option('--develop', dest='develop_mode', action='store_true', help='configure application for development', default=False)
    op.add_option('--disable_websocket', dest='websocket_disabled', action='store_true', help='disable the Web Socket Service backend', default=False)
    op.add_option('--ejabberd', dest='ejabberd', metavar='FILE', help='write ejabberd configuration to this file', default=os.path.join('etc', 'ejabberd.cfg'))
    op.add_option('--email', dest='email', metavar='EMAIL', help='the username to use', default='')
    op.add_option('--environment', dest='environment', metavar='STRING', help='specify additional environment variables', default='')
    op.add_option('--enable_ssl', dest='ssl_enabled', action='store_true', help='enable SSL support', default=False)
    op.add_option('--fcgi_host', dest='fcgi_host', metavar='HOST', help='use this FastCGI host', default='localhost')
    op.add_option('--fcgi_port', dest='fcgi_port', metavar='PORT', help='use this port of the FastCGI host', default=8081)
    op.add_option('--html_error_pages_root', dest='html_error_pages_root', metavar='PATH', help='set root for HTML error pages', default=None)
    op.add_option('--http_base_auth', dest='http_base_auth_enabled', action='store_true', help='enable HTTP base authentication', default=False)
    op.add_option('--http_port', dest='http_port', metavar='PORT', help='port for the HTTP server to listen on', default=8080)
    op.add_option('--https_port', dest='https_port', metavar='PORT', help='use this port for HTTPS', default=8443)
    op.add_option('--imap_host', dest='imap_host', metavar='ADDR', help='use this IMAP host', default='localhost')
    op.add_option('--imap_port', dest='imap_port', metavar='PORT', help='use this IMAP port', type='int', default=143)
    op.add_option('--imap_ssl', dest='imap_ssl', metavar='IMAPSSL', action='store_true', help='connect to IMAP server via SSL', default=False)
    op.add_option('--imap_user', dest='imap_user', metavar='STRING', help='use this IMAP user', default='')
    op.add_option('--imap_password', dest='imap_password', metavar='STRING', help='user this IMAP password', default='')
    op.add_option('--imap_mailbox', dest='imap_mailbox', metavar='STRING', help='use this IMAP mailbox', default='INBOX')
    op.add_option('--internal_address', dest='internal_address', metavar='HOST:PORT', help='the internal application host and port', default='localhost:8770')
    op.add_option('--login_url', dest='login_url', metavar='URL', help='login URL', default=None)
    op.add_option('--logout_url', dest='logout_url', metavar='URL', help='logout URL', default=None)
    op.add_option('--multiple', dest='multiple', action='store_true', help='configure multiple applications', default=False)
    op.add_option('--mysql_db', dest='mysql_db', metavar='STRING', help='connect to the given MySQL database', default='typhoonae')
    op.add_option('--mysql_host', dest='mysql_host', metavar='ADDR', help='connect to this MySQL database server', default='127.0.0.1')
    op.add_option('--mysql_passwd', dest='mysql_passwd', metavar='PASSWORD', help='use this password to connect to the MySQL database server', default='')
    op.add_option('--mysql_user', dest='mysql_user', metavar='USER', help='use this user to connect to the MySQL database server', default='root')
    op.add_option('--password', dest='password', metavar='PASSWORD', help='the password to use', default='')
    op.add_option('--server_name', dest='server_name', metavar='STRING', help='use this server name', default='localhost')
    op.add_option('--server_software', dest='server_software', metavar='STRING', help='use this server software identifier', default=typhoonae.fcgiserver.SERVER_SOFTWARE)
    op.add_option('--smtp_host', dest='smtp_host', metavar='ADDR', help='use this SMTP host', default='localhost')
    op.add_option('--smtp_port', dest='smtp_port', metavar='PORT', help='use this SMTP port', default=25)
    op.add_option('--smtp_user', dest='smtp_user', metavar='STRING', help='use this SMTP user', default='')
    op.add_option('--smtp_password', dest='smtp_password', metavar='STRING', help='use this SMTP password', default='')
    op.add_option('--ssl_certificate', dest='ssl_certificate', metavar='PATH', help='use this SSL certificate file')
    op.add_option('--ssl_certificate_key', dest='ssl_certificate_key', metavar='PATH', help='use this SSL certificate key file')
    op.add_option('--task_time_limit', dest='task_time_limit', metavar='SECONDS', help="Task Queue's task hard time limit in seconds. By default unlimited.", default=0)
    op.add_option('--upload_url', dest='upload_url', metavar='URI', help="use this upload URL for the Blobstore configuration (no leading '/')", default='upload/')
    op.add_option('--use_celery', dest='use_celery', action='store_true', help='use Celery as Task Queue backend', default=False)
    op.add_option('--var', dest='var', metavar='PATH', help='use this directory for platform independent data', default=setdir(os.path.abspath(os.path.join('.', 'var'))))
    op.add_option('--verbose', dest='verbose', action='store_true', help='set verbosity mode to display all warnings', default=False)
    op.add_option('--xmpp_host', dest='xmpp_host', metavar='ADDR', help='use this XMPP host', default=socket.getfqdn())
    (options, args) = op.parse_args()
    if sys.argv[(-1)].startswith('-') or sys.argv[(-1)] == sys.argv[0]:
        op.print_usage()
        sys.exit(2)
    if options.ssl_enabled and (options.ssl_certificate is None or options.ssl_certificate_key is None):
        logger.error('must specify --ssl_certificate and --ssl_certificate_key')
        sys.exit(3)
    app_root = sys.argv[(-1)]
    if not os.path.isabs(app_root):
        app_root = os.path.normpath(os.path.join(os.getcwd(), app_root))
    if options.datastore == 'remote':
        if not options.email:
            options.email = raw_input('Email: ')
        if not options.password:
            options.password = getpass.getpass('Password: ')
    if options.verbose:
        logger.setLevel(logging.WARNING)
    conf = typhoonae.getAppConfig(app_root)

    def write_httpd_conf(default_version=False):
        f = write_nginx_conf
        f(options, conf, app_root, default_version)
        if options.ssl_enabled:
            f(options, conf, app_root, default_version, secure=True, mode='a')
        f(options, conf, app_root, default_version, internal=True, mode='a')

    write_httpd_conf()
    if options.multiple:
        write_httpd_conf(True)
    make_blobstore_dirs(os.path.abspath(os.path.join(options.blobstore_path, conf.application)))
    write_supervisor_conf(options, conf, app_root)
    write_ejabberd_conf(options)
    if options.use_celery:
        write_celery_conf(options, conf, app_root)
    write_crontab(options, app_root)
    return