# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/platforms/mezzanine.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 5989 bytes
import logging, shortuuid
from secrets import token_urlsafe
from tfnz.location import Location
from tfnz.volume import Volume
from tfnz.components.postgresql import Postgresql
from tfnz.endpoint import WebEndpoint, Cluster

class Mezzanine:
    container_id = 'cc06f4404bda'

    def __init__(self, location: Location, volume: Volume, sql_volume: Volume, fqdn: str, app_name: str, image, *, log_callback=None, superuser=None, debug=False):
        nodes = location.ranked_nodes()
        manage = 'python3 /%s/manage.py ' % app_name
        self.db = Postgresql(nodes[0], sql_volume)
        first_server = nodes[0].spawn_container((Mezzanine.container_id if image is None else image), volumes=[
         (
          volume, '/%s/static/media/uploads/' % app_name)])
        localsettings = Mezzanine.localsettings_template % (
         self.db.password, self.db.private_ip(), str(debug), token_urlsafe(32), token_urlsafe(32))
        first_server.put('/%s/%s/local_settings.py' % (app_name, app_name), localsettings.encode())
        self.db.allow_connection_from(first_server)
        if self.db.ensure_database('mezzanine'):
            first_server.run_process((manage + 'createdb --noinput --nodata'), data_callback=log_callback)
            if superuser is not None:
                first_server.run_process((manage + 'createsuperuser --noinput --username %s --email %s' % (
                 superuser[0], superuser[1])),
                  data_callback=log_callback)
        self.webservers = [first_server]
        for node in nodes[1:]:
            server = node.spawn_container((Mezzanine.container_id if image is None else image), volumes=[
             (
              volume, '/%s/static/media/uploads/' % app_name)])
            server.put('/%s/%s/local_settings.py' % (app_name, app_name), localsettings.encode())
            self.webservers.append(server)

        for w in self.webservers:
            self.db.allow_connection_from(w)
            w.run_process('rm /etc/nginx/conf.d/default.conf')
            w.run_process('mkdir /run/nginx')
            w.put('/etc/nginx/conf.d/nginx.conf', (Mezzanine.nginx_template % (fqdn, '/%s/' % app_name)).encode())
            w.run_process(manage + 'collectstatic --noinput')
            w.spawn_process(('cd %s ; gunicorn -b unix:/tmp/gunicorn.sock --workers=8 %s.wsgi' % (
             app_name, app_name)),
              stderr_callback=log_callback)
            w.run_process('nginx')

        self.cluster = Cluster(containers=(self.webservers))
        location.endpoint_for(fqdn).publish(self.cluster, fqdn)
        WebEndpoint.wait_http_200(fqdn)
        logging.info('Mezzanine is up.')

    def change_password(self, username, password):
        """change the username and password of the given user"""
        w = self.webservers[0]
        py = Mezzanine.chpass_template % (password, shortuuid.uuid(), username, self.db.private_ip())
        w.put('update_password.py', py.encode())
        w.run_process('python3 update_password.py')
        w.run_process('rm update_password.py')

    localsettings_template = '\nDATABASES = {\n    "default": {\n        "ENGINE": "django.db.backends.postgresql_psycopg2",\n        "NAME": "mezzanine",\n        "USER": "postgres",\n        "PASSWORD": "%s",\n        "HOST": "%s",\n        "PORT": "5432"\n    }\n}\n\nALLOWED_HOSTS = ["*"]\n\nDEBUG = %s\n\nSECRET_KEY = "%s"\nNEVERCACHE_KEY = "%s"\n'
    nginx_template = '\nupstream gunicorn {\n    server unix:/tmp/gunicorn.sock fail_timeout=0;\n}    \n\nserver {\n    listen 80;\n    server_name %s;\n    charset utf-8;\n\n    location /static/ {\n        root %s;\n    }\n\n    location / {\n        proxy_pass http://gunicorn;\n    }\n}\n'
    chpass_template = '\nfrom django.contrib.auth.hashers import PBKDF2PasswordHasher\nimport psycopg2\n\nhash = PBKDF2PasswordHasher().encode(\'%s\', \'%s\')\nsql = "UPDATE auth_user SET password=\'" + hash + "\' WHERE username=\'%s\'"\n\nconn = psycopg2.connect("dbname=mezzanine user=postgres host=%s")\ncur = conn.cursor()\ncur.execute(sql)\nconn.commit()\ncur.close()\nconn.close()\n'