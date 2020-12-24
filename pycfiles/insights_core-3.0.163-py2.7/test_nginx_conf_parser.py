# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_nginx_conf_parser.py
# Compiled at: 2019-11-14 13:57:46
from insights.combiners.nginx_conf import _NginxConf
from insights.tests import context_wrap
NGINXCONF = ('\nuser       root;\nworker_processes  5;\nerror_log  logs/error.log;\npid        logs/nginx.pid;\nworker_rlimit_nofile 8192;\n\nevents {\n  worker_connections  4096;\n}\n\nmail {\n  server_name mail.example.com;\n  auth_http  localhost:9000/cgi-bin/auth;\n  server {\n    listen   143;\n    protocol imap;\n  }\n}\n\nhttp {\n  include    conf/mime.types;\n  include    /etc/nginx/proxy.conf;\n  include    /etc/nginx/fastcgi.conf;\n  index    index.html index.htm index.php;\n  log_format  main  \'$remote_addr - $remote_user [$time_local] "$request" \'\n                      \'$status $body_bytes_sent "$http_referer" \'\n                      \'"$http_user_agent" "$http_x_forwarded_for"\';\n\n  default_type application/octet-stream;\n  access_log   logs/access.log  main;\n  sendfile     on;\n  tcp_nopush   on;\n  server_names_hash_bucket_size 128;\n\n  server { # php/fastcgi\n    listen       80;\n    server_name  domain1.com www.domain1.com;\n    access_log   logs/domain1.access.log  main;\n    root         html;\n\n    location ~ \\.php$ {\n      fastcgi_pass   127.0.0.1:1025;\n    }\n  }\n\n  server { # simple reverse-proxy\n    listen       80;\n    server_name  domain2.com www.domain2.com;\n    access_log   logs/domain2.access.log  main;\n\n    location ~ ^/(images|javascript|js|css|flash|media|static)/  {\n      root    /var/www/virtual/big.server.com/htdocs;\n      expires 30d;\n    }\n\n    location / {\n      proxy_pass   http://127.0.0.1:8080;\n    }\n  }\n\n  map $http_upgrade $connection_upgrade {\n    default upgrade;\n    \'\' close;\n  }\n\n  upstream websocket {\n    server 10.66.208.205:8010;\n  }\n\n  upstream big_server_com {\n    server 127.0.0.3:8000 weight=5;\n    server 127.0.0.3:8001 weight=5;\n    server 192.168.0.1:8000;\n    server 192.168.0.1:8001;\n  }\n\n  server { # simple load balancing\n    listen          80;\n    server_name     big.server.com;\n    access_log      logs/big.server.access.log main;\n\n    location / {\n      proxy_pass      http://big_server_com;\n      location /inner/ {\n         proxy_pass http://u2;\n         limit_except GET {\n             allow 192.168.2.0/32;\n         }\n      }\n    }\n  }\n}\n').strip()

def test_nginx_conf_parser():
    nginxconf = _NginxConf(context_wrap(NGINXCONF))
    assert nginxconf['user'][(-1)].value == 'root'
    assert nginxconf['events'][(-1)]['worker_connections'][(-1)].value == 4096
    assert nginxconf['mail'][(-1)]['server'][0]['listen'][(-1)].value == 143
    assert nginxconf['http'][(-1)]['access_log'][(-1)].value == 'logs/access.log main'
    assert nginxconf['http'][(-1)]['server'][0]['location'][0]['fastcgi_pass'][(-1)].value == '127.0.0.1:1025'
    assert nginxconf['http'][(-1)]['server'][1]['location'][(-1)].value == '/'
    assert nginxconf['http'][(-1)]['upstream'][1].value == 'big_server_com'
    assert nginxconf['http'][(-1)]['include'][0].value == 'conf/mime.types'
    assert nginxconf['http'][(-1)]['upstream'][1]['server'][0].value == '127.0.0.3:8000 weight=5'
    assert nginxconf['http'][(-1)]['log_format'][(-1)].value == 'main $remote_addr - $remote_user [$time_local] "$request"  $status $body_bytes_sent "$http_referer"  "$http_user_agent" "$http_x_forwarded_for"'
    assert nginxconf['http'][(-1)]['server'][2]['location'][0]['location'][0]['limit_except'][(-1)]['allow'][(-1)].value == '192.168.2.0/32'
    assert nginxconf['http']['server']['location']['location']['limit_except']['allow'][(-1)].value == '192.168.2.0/32'
    assert nginxconf['http']['server'][0]['location'][(-1)].value == '~ \\.php$'
    assert nginxconf['http']['server'][1]['location'][0].value == '~ ^/(images|javascript|js|css|flash|media|static)/'
    assert nginxconf['http']['server'][1]['location'][(-1)].value == '/'
    assert nginxconf['http']['server'][(-1)] == nginxconf['http']['server'][2]