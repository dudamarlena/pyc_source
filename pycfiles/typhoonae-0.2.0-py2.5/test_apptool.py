# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/tests/test_apptool.py
# Compiled at: 2010-12-12 12:11:16
"""Unit tests for the apptool console script."""
import os, re, shutil, sys, tempfile, typhoonae, typhoonae.apptool, unittest

class ApptoolTestCase(unittest.TestCase):
    """Tests apptoll functions."""

    def setUp(self):
        """Loads the sample application."""
        self.app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sample'))
        self.curr_dir = os.getcwd()
        os.chdir(os.path.abspath(self.app_root))
        sys.path.insert(0, os.getcwd())
        self.conf = typhoonae.getAppConfig()
        assert self.conf.application == 'sample'

        class OptionsMock:
            amqp_host = 'localhost'
            auth_domain = 'example.com'
            blobstore_path = '/tmp/blobstore'
            current_version_id = None
            datastore = 'mongodb'
            develop_mode = False
            fcgi_host = 'localhost'
            fcgi_port = 8081
            email = 'test@example.com'
            environment = ''
            html_error_pages_root = '/tmp/html'
            http_base_auth_enabled = False
            http_port = 8080
            imap_host = 'localhost'
            imap_port = 143
            imap_ssl = False
            imap_user = ''
            imap_password = ''
            imap_mailbox = 'INBOX'
            internal_address = 'localhost:8770'
            login_url = None
            logout_url = None
            multiple = False
            password = ''
            server_name = 'host.local'
            server_software = 'TyphoonAE'
            set_crontab = False
            smtp_host = 'localhost'
            smtp_port = 25
            smtp_user = ''
            smtp_password = ''
            ssl_enabled = False
            ssl_certificate = None
            ssl_certificate_key = None
            upload_url = 'upload/'
            use_celery = False
            var = '/tmp/var'
            websocket_disabled = False
            xmpp_host = 'localhost'

        self.options = OptionsMock()

    def tearDown(self):
        """Clean up the test environment."""
        try:
            shutil.rmtree(os.path.join(os.getcwd(), 'etc'))
        except OSError:
            pass

        os.chdir(self.curr_dir)

    def testScheduledTasksConfig(self):
        """Tests the configuration for scheduled tasks."""
        typhoonae.apptool.read_crontab(self.options)
        tab = typhoonae.apptool.write_crontab(self.options, self.app_root)
        self.assertEqual([
         (
          '*/1', '*', '*', '*', '*',
          os.path.join(os.getcwd(), 'bin', 'runtask') + ' http://localhost:8770/a',
          ' # Test A (every 1 minutes)', 'Test A (every 1 minutes)')], tab)

    def testNGINXConfig(self):
        """Writes a NGINX configuration file."""
        os.mkdir(os.path.join(os.getcwd(), 'etc'))
        paths = typhoonae.apptool.write_nginx_conf(self.options, self.conf, self.app_root)
        try:
            f = open(paths[0], 'r')
            config = f.read()
            self.assertTrue('location ~* ^/(.*\\.(gif|jpg|png))$ {\n    root "%(app_root)s";\n    rewrite ^/(.*\\.(gif|jpg|png))$ /static/$1 break;\n    expires 5h;\n}' % {'app_root': os.getcwd()} in config)
            self.assertTrue('location ~* ^/favicon.ico$ {\n    root "%(app_root)s";\n    rewrite ^/favicon.ico$ /static/favicon.ico break;\n    expires 30d;\n}' % {'app_root': os.getcwd()} in config)
            self.assertTrue('location ~ ^/(static)/ {\n    root "%(app_root)s";\n    expires 30d;\n}' % {'app_root': os.getcwd()} in config)
            self.assertTrue('location ~ ^/(foo)/ {\n    root "%(app_root)s";\n    rewrite ^/(foo)/(.*)$ /bar/$2 break;\n    expires 30d;\n}' % {'app_root': os.getcwd()} in config)
            self.assertTrue('location ~ ^/(images)/ {\n    root "%(app_root)s";\n    rewrite ^/(images)/(.*)$ /static/images/$2 break;\n    expires 30d;\n}' % {'app_root': os.getcwd()} in config)
            self.assertTrue('location ~* ^/(index.html)$ {\n    root "%(app_root)s";\n    rewrite ^/(index.html)$ /$1 break;\n    expires 30d;\n}' % {'app_root': os.getcwd()} in config)
            self.assertTrue('location ~* /upload/ {\n    # Pass altered request body to this location\n    upload_pass @sample;\n\n    # Store files to this directory\n    # The directory is hashed, subdirectories 0 1 2 3 4 5 6 7 8 9\n    # should exist\n    upload_store /tmp/blobstore/sample 1;\n\n    # Set permissions for uploaded files\n    upload_store_access user:rw group:rw;\n\n    # Set specified fields in request body\n    upload_set_form_field $upload_field_name.name "$upload_file_name";\n    upload_set_form_field $upload_field_name.content_type "$upload_content_type";\n    upload_set_form_field $upload_field_name.path "$upload_tmp_path";\n\n    # Inform backend about hash and size of a file\n    upload_aggregate_form_field "$upload_field_name.md5" "$upload_file_md5";\n    upload_aggregate_form_field "$upload_field_name.size" "$upload_file_size";\n\n    upload_pass_form_field ".*";\n\n    upload_cleanup 400 404 499 500-505;\n}\n\nlocation @sample {\n    fastcgi_pass localhost:8081;\n    set $stripped_http_host $http_host;\n    if ($http_host ~ ^(.*):([0-9]+)$) {\n      set $stripped_http_host $1;\n    }\n    fastcgi_param CONTENT_LENGTH $content_length;\n    fastcgi_param CONTENT_TYPE $content_type;\n    fastcgi_param PATH_INFO $fastcgi_script_name;\n    fastcgi_param QUERY_STRING $query_string;\n    fastcgi_param REMOTE_ADDR $remote_addr;\n    fastcgi_param REQUEST_METHOD $request_method;\n    fastcgi_param REQUEST_URI $request_uri;\n    fastcgi_param SERVER_NAME $stripped_http_host;\n    fastcgi_param SERVER_PORT $server_port;\n    fastcgi_param SERVER_PROTOCOL $server_protocol;\n    \n    fastcgi_pass_header Authorization;\n\n    # Increase the allowed size of the response.\n    fastcgi_buffer_size 128k;\n    fastcgi_buffers 4 256k;\n    fastcgi_busy_buffers_size 256k;\n    fastcgi_temp_file_write_size 256k;\n\n    fastcgi_intercept_errors off;\n}\n\nlocation ~ ^/_ah/blobstore/sample/(.*) {\n    root "/tmp/blobstore/sample";\n    rewrite ^/_ah/blobstore/sample/(.*) /$1 break;\n    expires 5d;\n    internal;\n}\n\nlocation ~ ^/_ah/subscribe {\n    push_subscriber long-poll;\n    push_subscriber_concurrency broadcast;\n    set $push_channel_id $arg_id;\n    default_type text/plain;\n}\n\nlocation ~ {\n    fastcgi_pass localhost:8081;\n    set $stripped_http_host $http_host;\n    if ($http_host ~ ^(.*):([0-9]+)$) {\n      set $stripped_http_host $1;\n    }\n    fastcgi_param CONTENT_LENGTH $content_length;\n    fastcgi_param CONTENT_TYPE $content_type;\n    fastcgi_param PATH_INFO $fastcgi_script_name;\n    fastcgi_param QUERY_STRING $query_string;\n    fastcgi_param REMOTE_ADDR $remote_addr;\n    fastcgi_param REQUEST_METHOD $request_method;\n    fastcgi_param REQUEST_URI $request_uri;\n    fastcgi_param SERVER_NAME $stripped_http_host;\n    fastcgi_param SERVER_PORT $server_port;\n    fastcgi_param SERVER_PROTOCOL $server_protocol;\n    \n    fastcgi_pass_header Authorization;\n\n    # Increase the allowed size of the response.\n    fastcgi_buffer_size 128k;\n    fastcgi_buffers 4 256k;\n    fastcgi_busy_buffers_size 256k;\n    fastcgi_temp_file_write_size 256k;\n\n    fastcgi_intercept_errors off;\n}\n\nerror_page   500 502 503 504  /50x.html;\nlocation = /50x.html {\n    root "/tmp/html";\n}\n\n}\n' % {'app_root': os.getcwd()} in config)
            f.close()
        except Exception, e:
            print config
            raise e

    def testSupervisorConfig(self):
        """Writes a supervisord configuration file."""
        os.mkdir(os.path.join(os.getcwd(), 'etc'))
        paths = typhoonae.apptool.write_supervisor_conf(self.options, self.conf, self.app_root)