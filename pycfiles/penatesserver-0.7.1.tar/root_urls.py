# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/root_urls.py
# Compiled at: 2015-12-29 03:04:14
from __future__ import unicode_literals
from django.conf.urls import include, url
from rest_framework import routers
from penatesserver.glpi.views import xmlrpc, register_service
from penatesserver.models import name_pattern
from penatesserver.pki.views import get_host_certificate, get_ca_certificate, get_admin_certificate, get_service_certificate, get_crl, get_user_certificate, get_email_certificate, get_signature_certificate, get_encipherment_certificate
from penatesserver.views import GroupDetail, GroupList, UserDetail, UserList, get_host_keytab, get_info, set_dhcp, get_dhcpd_conf, get_dns_conf, set_mount_point, set_ssh_pub, set_service, set_extra_service, get_service_keytab, change_own_password, get_user_mobileconfig, index
__author__ = b'flanker'
router = routers.DefaultRouter()
service_pattern = b'(?P<scheme>\\w+)/(?P<hostname>[a-zA-Z0-9\\.\\-_]+)/(?P<port>\\d+)/'
app_name = b'penatesserver'
urls = [
 url(b'^index$', index, name=b'index'),
 url(b'^', include(router.urls)),
 url(b'^no-auth/get_host_keytab/(?P<hostname>[a-zA-Z0-9\\.\\-_]+)$', get_host_keytab, name=b'get_host_keytab'),
 url(b'^auth/get_info/$', get_info, name=b'get_info'),
 url(b'^auth/set_dhcp/(?P<mac_address>([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})/$', set_dhcp, name=b'set_dhcp'),
 url(b'^auth/conf/dhcpd.conf$', get_dhcpd_conf, name=b'get_dhcpd_conf'),
 url(b'^auth/conf/dns.conf$', get_dns_conf, name=b'get_dns_conf'),
 url(b'^auth/set_mount_point/$', set_mount_point, name=b'set_mount_point'),
 url(b'^auth/set_ssh_pub/$', set_ssh_pub, name=b'set_ssh_pub'),
 url(b'^auth/set_service/%s$' % service_pattern, set_service, name=b'set_service'),
 url(b'^auth/set_extra_service/(?P<hostname>[a-zA-Z0-9\\.\\-_]+)$', set_extra_service, name=b'set_extra_service'),
 url(b'^auth/get_service_keytab/%s$' % service_pattern, get_service_keytab, name=b'get_service_keytab'),
 url(b'^auth/user/$', UserList.as_view(), name=b'user_list'),
 url(b'^auth/user/(?P<name>%s)$' % name_pattern, UserDetail.as_view(), name=b'user_detail'),
 url(b'^auth/group/$', GroupList.as_view(), name=b'group_list'),
 url(b'^auth/group/(?P<name>%s)$' % name_pattern, GroupDetail.as_view(), name=b'group_detail'),
 url(b'^auth/change_password/$', change_own_password, name=b'change_own_password'),
 url(b'^auth/get_host_certificate/$', get_host_certificate, name=b'get_host_certificate'),
 url(b'^auth/get_admin_certificate/$', get_admin_certificate, name=b'get_admin_certificate'),
 url(b'^auth/get_service_certificate/%s$' % service_pattern, get_service_certificate, name=b'get_service_certificate'),
 url(b'^auth/glpi/register_service/(?P<check_command>.*)$', register_service, name=b'register_service'),
 url(b'^no-auth/(?P<kind>ca|users|hosts|services).pem$', get_ca_certificate, name=b'get_ca_certificate'),
 url(b'^no-auth/crl.pem$', get_crl, name=b'get_crl'),
 url(b'^no-auth/glpi/rpc$', xmlrpc, name=b'xmlrpc'),
 url(b'^auth/get_user_certificate/$', get_user_certificate, name=b'get_user_certificate'),
 url(b'^auth/get_email_certificate/$', get_email_certificate, name=b'get_email_certificate'),
 url(b'^auth/get_signature_certificate/$', get_signature_certificate, name=b'get_signature_certificate'),
 url(b'^auth/get_encipherment_certificate/$', get_encipherment_certificate, name=b'get_encipherment_certificate'),
 url(b'^auth/get_mobileconfig/profile.mobileconfig$', get_user_mobileconfig, name=b'get_user_mobileconfig'),
 url(b'^auth/api/', include(b'rest_framework.urls', namespace=b'rest_framework'))]