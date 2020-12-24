# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/platforms/silverstripe.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 4340 bytes
import logging
from tfnz.location import Location
from tfnz.volume import Volume
from tfnz.components.postgresql import Postgresql
from tfnz.endpoint import WebEndpoint, Cluster

class SilverStripe:
    container_id = '7a4f9fbb6afc'

    def __init__(self, location: Location, volume: Volume, sql_volume: Volume, fqdn: str, *, image=None, log_callback=None):
        nodes = location.ranked_nodes()
        self.db = Postgresql((nodes[0]), sql_volume, log_callback=log_callback)
        first_server = nodes[0].spawn_container((SilverStripe.container_id if image is None else image), volumes=[
         (
          volume, '/site/public/assets')],
          sleep=True,
          stdout_callback=log_callback)
        first_server.create_ssh_server()
        dotenv = SilverStripe.environment_template % (fqdn, self.db.password, self.db.private_ip())
        first_server.put('/site/.env', dotenv.encode())
        self.webservers = [
         first_server]
        for node in nodes[1:]:
            server = node.spawn_container((SilverStripe.container_id), volumes=[
             (
              volume, '/site/public/assets')],
              sleep=True)
            self.webservers.append(server)

        fqdn_sed = "sed -i -e 's/--fqdn--/%s/g' /etc/nginx/conf.d/nginx.conf" % fqdn
        timezone_sed = "sed -i -e 's/;date.timezone =/date.timezone = %s/g' /etc/php7/php.ini" % 'UTC'
        pool_sed = "sed -i -e 's/pm.max_children = 5/pm.max_children = 16/g' /etc/php7/php-fpm.d/www.conf"
        for w in self.webservers:
            self.db.allow_connection_from(w)
            w.run_process('rm /etc/nginx/conf.d/default.conf /site/install*')
            w.run_process(fqdn_sed)
            w.run_process(timezone_sed)
            w.run_process(pool_sed)
            w.run_process('mkdir /run/nginx')
            w.spawn_process('nginx')
            w.spawn_process('php-fpm7')

        self.cluster = Cluster(containers=(self.webservers))
        location.endpoint_for(fqdn).publish(self.cluster, fqdn)
        self.db.wait_until_ready()
        WebEndpoint.wait_http_200(fqdn)
        logging.info('SilverStripe is up.')
        for w in self.webservers:
            w.spawn_process('tail -n 0 -f /var/log/nginx/access.log', data_callback=log_callback)
            w.spawn_process('tail -n 0 -f /var/log/nginx/error.log', data_callback=log_callback)

    environment_template = '\nSS_BASE_URL="http://%s"\nSS_DATABASE_CLASS="PostgreSQLDatabase"\nSS_DATABASE_NAME="SS_mysite"\nSS_DATABASE_PASSWORD="%s"\nSS_DATABASE_PORT="5432"\nSS_DATABASE_SERVER="%s"\nSS_DATABASE_USERNAME="postgres"\nSS_DEFAULT_ADMIN_USERNAME="admin"\nSS_DEFAULT_ADMIN_PASSWORD="password"\n'