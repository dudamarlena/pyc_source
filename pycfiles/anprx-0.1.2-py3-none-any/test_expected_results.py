# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jfurr/anouman/anouman/templates/test_expected_results.py
# Compiled at: 2013-09-29 11:07:37
shell_commands_expected = "\n#This section defines commands specified by Anouman\n\nNGINX=/etc/init.d/nginx\nDOMAINNAME=example.com\n\nfunction site {\n        if [ $1 == 'status' ];\n        then\n                sudo $NGINX status\n                sudo status $DOMAINNAME\n        fi\n\n        if [ $1 == 'stop' ];\n        then\n                sudo $NGINX stop\n                sudo stop $DOMAINNAME\n        fi\n\n        if [ $1 == 'start' ];\n        then\n                sudo $NGINX start\n                sudo start $DOMAINNAME\n        fi\n\n        if [ $1 == 'reload' ];\n        then\n                sudo nginx -s reload\n        fi\n}"