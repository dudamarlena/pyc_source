# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_octavia.py
# Compiled at: 2020-03-25 13:10:41
import doctest, insights.parsers.octavia as octavia_module
from insights.parsers.octavia import OctaviaConf, VALID_KEYS
from insights.tests import context_wrap
CONF_FILE = '\n[DEFAULT]\n# Print debugging output (set logging level to DEBUG instead of default WARNING level).\ndebug = False\n\n# Plugin options are hot_plug_plugin (Hot-pluggable controller plugin)\noctavia_plugins = hot_plug_plugin\n\n# Hostname to be used by the host machine for services running on it.\n# The default value is the hostname of the host machine.\nhost = some_hostname.some_domain.com\n\n# AMQP Transport URL\n# For Single Host, specify one full transport URL:\n#   transport_url = rabbit://<user>:<pass>@127.0.0.1:5672/<vhost>\n# For HA, specify queue nodes in cluster, comma delimited:\n#   transport_url = rabbit://<user>:<pass>@server01,<user>:<pass>@server02/<vhost>\ntransport_url =\n\n# How long in seconds to wait for octavia worker to exit before killing them.\ngraceful_shutdown_timeout = 60\n\nlog_file = some_file\nlog_dir = some_dir\npolicy_file = some_policy_file\n\n[api_settings]\nbind_host = 127.0.0.1\nbind_port = 9876\n\n# How should authentication be handled (keystone, noauth)\nauth_strategy = keystone\n\nallow_pagination = True\nallow_sorting = True\npagination_max_limit = 1000\n# Base URI for the API for use in pagination links.\n# This will be autodetected from the request if not overridden here.\n# Example:\n#   api_base_uri = http://localhost:9876\napi_base_uri = http://localhost:9876\n\n# Enable/disable ability for users to create TLS Terminated listeners\nallow_tls_terminated_listeners = True\n\n# Enable/disable ability for users to create PING type Health Monitors\nallow_ping_health_monitors = True\n\n# Dictionary of enabled provider driver names and descriptions\n# A comma separated list of dictionaries of the enabled provider driver names\n# and descriptions.\nenabled_provider_drivers = amphora:The Octavia Amphora driver.,octavia: \\\n                           Deprecated alias of the Octavia Amphora driver.\n\n# Default provider driver\ndefault_provider_driver = amphora\n\n# The minimum health monitor delay interval for UDP-CONNECT Health Monitor type\nudp_connect_min_interval_health_monitor = 3\n\n[database]\n# This line MUST be changed to actually run the plugin.\n# Example:\n# connection = mysql+pymysql://root:pass@127.0.0.1:3306/octavia\n# Replace 127.0.0.1 above with the IP address of the database used by the\n# main octavia server. (Leave it as is if the database runs on this host.)\n\nconnection = mysql+pymysql://\n\n# NOTE: In deployment the [database] section and its connection attribute may\n# be set in the corresponding core plugin \'.ini\' file. However, it is suggested\n# to put the [database] section and its connection attribute in this\n# configuration file.\n\n[health_manager]\nbind_ip = 127.0.0.1\nbind_port = 5555\n# controller_ip_port_list example: 127.0.0.1:5555, 127.0.0.1:5555\ncontroller_ip_port_list = 127.0.0.1:5555, 127.0.0.1:5555\nfailover_threads = 10\n# status_update_threads will default to the number of processors on the host.\n# This setting is deprecated and if you specify health_update_threads and\n# stats_update_threads, they override this parameter.\nstatus_update_threads = 10\n# health_update_threads will default to the number of processors on the host\nhealth_update_threads = 10\n# stats_update_threads will default to the number of processors on the host\nstats_update_threads = 10\nheartbeat_interval = 10\n# Symmetric encrpytion key\nheartbeat_key =\nheartbeat_timeout = 60\nhealth_check_interval = 3\nsock_rlimit = 0\n\n# Health/StatsUpdate options are\n#                           *_db\n#                           *_logger\nhealth_update_driver = health_db\nstats_update_driver = stats_db\n\n[keystone_authtoken]\n# This group of config options are imported from keystone middleware. Thus the\n# option names should match the names declared in the middleware.\n# The www_authenticate_uri is the public endpoint and is returned in headers on a 401\n# www_authenticate_uri = https://localhost:5000/v3\n# The auth_url is the admin endpoint actually used for validating tokens\nauth_url = https://localhost:5000/v3\nusername = octavia\npassword = password\nproject_name = service\n\n# Domain names must be set, these are *not* default but work for most clouds\n# project_domain_name = Default\nuser_domain_name = Default\n\ninsecure = False\ncafile =\n\n[certificates]\n# Certificate Generator options are local_cert_generator\ncert_generator = local_cert_generator\n\n# For local certificate signing:\nca_certificate = /etc/ssl/certs/ssl-cert-snakeoil.pem\nca_private_key = /etc/ssl/private/ssl-cert-snakeoil.key\nca_private_key_passphrase =\nserver_certs_key_passphrase = do-not-use-this-key\nsigning_digest = sha256\ncert_validity_time = 2592000  # 30 days = 30d * 24h * 60m * 60s = 2592000s\nstorage_path = /var/lib/octavia/certificates/\n\n# For the TLS management\n# Certificate Manager options are local_cert_manager\n#                                 barbican_cert_manager\n#                                 castellan_cert_manager\ncert_manager = barbican_cert_manager\n# For Barbican authentication (if using any Barbican based cert class)\nbarbican_auth = barbican_acl_auth\n#\n# Region in Identity service catalog to use for communication with the Barbican service.\nregion_name = some_region\n#\n# Endpoint type to use for communication with the Barbican service.\nendpoint_type = publicURL\n\n[networking]\n# The maximum attempts to retry an action with the networking service.\nmax_retries = 15\n# Seconds to wait before retrying an action with the networking service.\nretry_interval = 1\n# The maximum time to wait, in seconds, for a port to detach from an amphora\nport_detach_timeout = 300\n# Allow/disallow specific network object types when creating VIPs.\nallow_vip_network_id = True\nallow_vip_subnet_id = True\nallow_vip_port_id = True\n# List of network_ids that are valid for VIP creation.\n# If this field empty, no validation is performed.\nvalid_vip_networks =\n# List of reserved IP addresses that cannot be used for member addresses\n# The default is the nova metadata service address\nreserved_ips = [\'169.254.169.254\']\n\n[haproxy_amphora]\nbase_path = /var/lib/octavia\nbase_cert_dir = /var/lib/octavia/certs\n# Absolute path to a custom HAProxy template file\nhaproxy_template = /some/path\nconnection_logging = True\nconnection_max_retries = 120\nconnection_retry_interval = 5\nbuild_rate_limit = -1\nbuild_active_retries = 120\nbuild_retry_interval = 5\n\n# Maximum number of entries that can fit in the stick table.\n# The size supports "k", "m", "g" suffixes.\nhaproxy_stick_size = 10k\n\n# REST Driver specific\nbind_host = 0.0.0.0\nbind_port = 9443\n#\n# This setting is only needed with IPv6 link-local addresses (fe80::/64) are\n# used for communication between Octavia and its Amphora, if IPv4 or other IPv6\n# addresses are used it can be ignored.\nlb_network_interface = o-hm0\n#\nhaproxy_cmd = /usr/sbin/haproxy\nrespawn_count = 2\nrespawn_interval = 2\nclient_cert = /etc/octavia/certs/client.pem\nserver_ca = /etc/octavia/certs/server_ca.pem\n#\n# This setting is deprecated. It is now automatically discovered.\nuse_upstart = True\n#\nrest_request_conn_timeout = 10\nrest_request_read_timeout = 60\n#\n# These "active" timeouts are used once the amphora should already\n# be fully up and active. These values are lower than the other values to\n# facilitate "fail fast" scenarios like failovers\nactive_connection_max_retries = 15\nactive_connection_rety_interval = 2\n\n# The user flow log format for HAProxy.\n# {{ project_id }} and {{ lb_id }} will be automatically substituted by the\n# controller when configuring HAProxy if they are present in the string.\nuser_log_format = \'{{ project_id }} {{ lb_id }} %f %ci %cp %t %{+Q}r %ST %B %U %[ssl_c_verify] %{+Q}[ssl_c_s_dn] %b %s %Tt %tsc\'\n\n[controller_worker]\nworkers = 1\namp_active_retries = 30\namp_active_wait_sec = 10\n# Glance parameters to extract image ID to use for amphora. Only one of\n# parameters is needed. Using tags is the recommended way to refer to images.\namp_image_id =\namp_image_tag =\n# Optional owner ID used to restrict glance images to one owner ID.\n# This is a recommended security setting.\namp_image_owner_id =\n# Nova parameters to use when booting amphora\namp_flavor_id =\n# Upload the ssh key as the service_auth user described elsewhere in this config.\n# Leaving this variable blank will install no ssh key on the amphora.\namp_ssh_key_name =\n\namp_ssh_access_allowed = True\n\n# Networks to attach to the Amphorae examples:\n#  - One primary network\n#  - - amp_boot_network_list = 22222222-3333-4444-5555-666666666666\n#  - Multiple networks\n#  - - amp_boot_network_list = 11111111-2222-33333-4444-555555555555, 22222222-3333-4444-5555-666666666666\n#  - All networks defined in the list will be attached to each amphora\namp_boot_network_list =\n\namp_secgroup_list =\nclient_ca = /etc/octavia/certs/ca_01.pem\n\n# Amphora driver options are amphora_noop_driver,\n#                            amphora_haproxy_rest_driver\n#\namphora_driver = amphora_noop_driver\n#\n# Compute driver options are compute_noop_driver\n#                            compute_nova_driver\n#\ncompute_driver = compute_noop_driver\n#\n# Network driver options are network_noop_driver\n#                            allowed_address_pairs_driver\n#\nnetwork_driver = network_noop_driver\n# Volume driver options are volume_noop_driver\n#                           volume_cinder_driver\n#\nvolume_driver = volume_noop_driver\n#\n# Distributor driver options are distributor_noop_driver\n#                                single_VIP_amphora\n#\ndistributor_driver = distributor_noop_driver\n#\n# Load balancer topology options are SINGLE, ACTIVE_STANDBY\nloadbalancer_topology = SINGLE\nuser_data_config_drive = False\n\n[task_flow]\n# TaskFlow engine options are:\n#   - serial:   Runs all tasks on a single thread.\n#   - parallel: Schedules tasks onto different threads to allow\n#               for running non-dependent tasks simultaneously\n#\nengine = parallel\nmax_workers = 5\n#\n# This setting prevents the controller worker from reverting taskflow flows.\n# This will leave resources in an inconsistent state and should only be used\n# for debugging purposes.\ndisable_revert = False\n\n[oslo_messaging]\n# Queue Consumer Thread Pool Size\nrpc_thread_pool_size = 2\n\n# Topic (i.e. Queue) Name\ntopic = octavia_prov\n\n[oslo_middleware]\n# HTTPProxyToWSGI middleware enabled\nenable_proxy_headers_parsing = False\n\n[house_keeping]\n# Interval in seconds to initiate spare amphora checks\nspare_check_interval = 30\nspare_amphora_pool_size = 0\n\n# Cleanup interval for Deleted amphora\ncleanup_interval = 30\n# Amphora expiry age in seconds. Default is 1 week\namphora_expiry_age = 604800\n\n# Load balancer expiry age in seconds. Default is 1 week\nload_balancer_expiry_age = 604800\n\n[amphora_agent]\nagent_server_ca = /etc/octavia/certs/client_ca.pem\nagent_server_cert = /etc/octavia/certs/server.pem\n\n# Defaults for agent_server_network_dir when not specified here are:\n# Ubuntu: /etc/netns/amphora-haproxy/network/interfaces.d/\n# Centos/fedora/rhel: /etc/netns/amphora-haproxy/sysconfig/network-scripts/\n#\nagent_server_network_dir =\n\nagent_server_network_file =\nagent_request_read_timeout = 180\n\n# Minimum TLS protocol, eg: TLS, TLSv1.1, TLSv1.2, TLSv1.3 (if available)\nagent_tls_protocol = TLSv1.2\n\n# Amphora default UDP driver is keepalived_lvs\n#\namphora_udp_driver = keepalived_lvs\n\n##### Log offloading\n#\n# Note: The admin and tenant logs can point to the same endpoints.\n#\n# List of log server ip and port pairs for Administrative logs.\n# Additional hosts are backup to the primary server. If none are\n# specified, remote logging is disabled.\n# Example 192.0.2.1:10514, 2001:db8:1::10:10514\'\n#\nadmin_log_targets =\n#\n# List of log server ip and port pairs for tenant traffic logs.\n# Additional hosts are backup to the primary server. If none are\n# specified, remote logging is disabled.\n# Example 192.0.2.1:10514, 2001:db8:2::15:10514\'\n#\ntenant_log_targets =\n\n# Sets the syslog LOG_LOCAL[0-7] facility number for amphora log offloading.\n# user_log_facility will receive the traffic flow logs.\n# administrative_log_facility will receive the amphora processes logs.\n# Note: Some processes only support LOG_LOCAL, so we are restricted to the\n#       LOG_LOCAL facilities.\n#\nuser_log_facility = 0\nadministrative_log_facility = 1\n\n# The log forwarding protocol to use. One of TCP or UDP.\nlog_protocol = UDP\n\n# The maximum attempts to retry connecting to the logging host.\nlog_retry_count = 5\n\n# The time, in seconds, to wait between retries connecting to the logging host.\nlog_retry_interval = 2\n\n# The queue size (messages) to buffer log messages.\nlog_queue_size = 10000\n\n# Controller local path to a custom logging configuration template.\n# Currently this is an rsyslog configuration file template.\nlogging_template_override =\n\n# When True, the amphora will forward all of the system logs (except tenant\n# traffice logs) to the admin log target(s). When False, only amphora specific\n# admin logs will be forwarded.\nforward_all_logs = False\n\n# When True, no logs will be written to the amphora filesystem. When False,\n# log files will be written to the local filesystem.\ndisable_local_log_storage = False\n\n[keepalived_vrrp]\n# Amphora Role/Priority advertisement interval in seconds\nvrrp_advert_int = 1\n\n# Service health check interval and success/fail count\nvrrp_check_interval = 5\nvrrp_fail_count = 2\nvrrp_success_count = 2\n\n# Amphora MASTER gratuitous ARP refresh settings\nvrrp_garp_refresh_interval = 5\nvrrp_garp_refresh_count = 2\n\n[service_auth]\nmemcached_servers =\ncafile = /opt/stack/data/ca-bundle.pem\nproject_domain_name = Default\nproject_name = admin\nuser_domain_name = Default\npassword = password\nusername = admin\nauth_type = password\nauth_url = http://localhost:5555/\n\n[nova]\n# The name of the nova service in the keystone catalog\nservice_name =\n# Custom nova endpoint if override is necessary\nendpoint =\n\n# Region in Identity service catalog to use for communication with the\n# OpenStack services.\nregion_name =\n\n# Endpoint type in Identity service catalog to use for communication with\n# the OpenStack services.\nendpoint_type = publicURL\n\n# CA certificates file to verify neutron connections when TLS is enabled\nca_certificates_file =\n\n# Disable certificate validation on SSL connections\ninsecure = False\n\n# If non-zero, generate a random name of the length provided for each amphora,\n# in the format "a[A-Z0-9]*".\n# Otherwise, the default name format will be used: "amphora-{UUID}".\nrandom_amphora_name_length = 0\n#\n# Availability zone to use for creating Amphorae\navailability_zone =\n\n# Enable anti-affinity in nova\nenable_anti_affinity = False\n# Set the anti-affinity policy to what is suitable.\n# Nova supports: anti-affinity and soft-anti-affinity\nanti_affinity_policy = anti-affinity\n\n[cinder]\n# The name of the cinder service in the keystone catalog\nservice_name =\n# Custom cinder endpoint if override is necessary\nendpoint =\n\n# Region in Identity service catalog to use for communication with the\n# OpenStack services.\nregion_name =\n\n# Endpoint type in Identity service catalog to use for communication with\n# the OpenStack services.\nendpoint_type = publicURL\n\n# Availability zone to use for creating Volume\navailability_zone =\n\n# CA certificates file to verify cinder connections when TLS is enabled\ninsecure = False\nca_certificates_file =\n\n# Size of root volume in GB for Amphora Instance when use Cinder\n# In some storage backends such as ScaleIO, the size of volume is multiple of 8\nvolume_size = 16\n\n# Volume type to be used for Amphora Instance root disk\n# If not specified, default_volume_type from cinder.conf will be used\nvolume_type =\n\n# Interval time to wait until volume becomes available\nvolume_create_retry_interval = 5\n\n# Timeout to wait for volume creation success\nvolume_create_timeout = 300\n\n# Maximum number of retries to create volume\nvolume_create_max_retries = 5\n\n[glance]\n# The name of the glance service in the keystone catalog\nservice_name =\n# Custom glance endpoint if override is necessary\nendpoint =\n\n# Region in Identity service catalog to use for communication with the\n# OpenStack services.\nregion_name =\n\n# Endpoint type in Identity service catalog to use for communication with\n# the OpenStack services.\nendpoint_type = publicURL\n\n# CA certificates file to verify neutron connections when TLS is enabled\ninsecure = False\nca_certificates_file =\n\n[neutron]\n# The name of the neutron service in the keystone catalog\nservice_name =\n# Custom neutron endpoint if override is necessary\nendpoint =\n\n# Region in Identity service catalog to use for communication with the\n# OpenStack services.\nregion_name =\n\n# Endpoint type in Identity service catalog to use for communication with\n# the OpenStack services.\nendpoint_type = publicURL\n\n# CA certificates file to verify neutron connections when TLS is enabled\ninsecure = False\nca_certificates_file =\n\n[quotas]\ndefault_load_balancer_quota = -1\ndefault_listener_quota = -1\ndefault_member_quota = -1\ndefault_pool_quota = -1\ndefault_health_monitor_quota = -1\n\n[audit]\n# Enable auditing of API requests.\nenabled = False\n\n# Path to audit map file for octavia-api service. Used only\n# when API audit is enabled.\naudit_map_file = /etc/octavia/octavia_api_audit_map.conf\n\n# Comma separated list of REST API HTTP methods to be\n# ignored during audit. For example: auditing will not be done\n# on any GET or POST requests if this is set to "GET,POST". It\n# is used only when API audit is enabled.\nignore_req_list =\n\n[audit_middleware_notifications]\n# Note: This section comes from openstack/keystonemiddleware\n# It is included here for documentation convenience and may be out of date\n\n# Indicate whether to use oslo_messaging as the notifier. If set to False,\n# the local logger will be used as the notifier. If set to True, the\n# oslo_messaging package must also be present. Otherwise, the local will be\n# used instead.\nuse_oslo_messaging = True\n\n# The Driver to handle sending notifications. Possible values are messaging,\n# messagingv2, routing, log, test, noop. If not specified, then value from\n# oslo_messaging_notifications conf section is used.\ndriver =\n\n# List of AMQP topics used for OpenStack notifications. If not specified,\n# then value from oslo_messaging_notifications conf section is used.\ntopics =\n\n# A URL representing messaging driver to use for notification. If not\n# specified, we fall back to the same configuration used for RPC.\ntransport_url =\n\n[driver_agent]\nstatus_socket_path = /var/run/octavia/status.sock\nstats_socket_path = /var/run/octavia/stats.sock\nget_socket_path = /var/run/octavia/get.sock\n\n# Maximum time to wait for a status message before checking for shutdown\nstatus_request_timeout = 5\n\n# Maximum number of status processes per driver-agent\nstatus_max_processes = 50\n\n# Maximum time to wait for a stats message before checking for shutdown\nstats_request_timeout = 5\n\n# Maximum number of stats processes per driver-agent\nstats_max_processes = 50\n\n# Percentage of max_processes (both status and stats) in use to start\n# logging warning messages about an overloaded driver-agent.\nmax_process_warning_percent = .75\n\n# How long in seconds to wait for provider agents to exit before killing them.\nprovider_agent_shutdown_timeout = 60\n\n# List of enabled provider agents.\nenabled_provider_agents =\n'
DEFAULT_OPTIONS = set([
 'debug', 'octavia_plugins', 'graceful_shutdown_timeout',
 'log_file', 'log_dir', 'policy_file'])

def test_full_conf():
    filtered_content = []
    for line in CONF_FILE.strip().splitlines():
        if any([ f in line for f in VALID_KEYS ]):
            filtered_content.append(line)

    octavia_conf = OctaviaConf(context_wrap(('\n').join(filtered_content)))
    assert octavia_conf is not None
    assert set(octavia_conf.defaults().keys()) == DEFAULT_OPTIONS
    assert octavia_conf.defaults()['debug'] == 'False'
    assert octavia_conf.defaults()['octavia_plugins'] == 'hot_plug_plugin'
    assert 'api_settings' in octavia_conf
    assert set(octavia_conf.items('api_settings').keys()) == set([
     'bind_host', 'bind_port', 'auth_strategy', 'allow_pagination', 'allow_sorting',
     'pagination_max_limit', 'api_base_uri', 'allow_tls_terminated_listeners',
     'allow_ping_health_monitors', 'enabled_provider_drivers', 'default_provider_driver',
     'udp_connect_min_interval_health_monitor']) | DEFAULT_OPTIONS
    assert 'database' in octavia_conf
    assert set(octavia_conf.items('database').keys()) == DEFAULT_OPTIONS
    assert 'health_manager' in octavia_conf
    assert set(octavia_conf.items('health_manager').keys()) == set([
     'bind_ip', 'bind_port', 'controller_ip_port_list', 'failover_threads',
     'status_update_threads', 'health_update_threads', 'stats_update_threads',
     'heartbeat_interval', 'heartbeat_timeout', 'health_check_interval',
     'sock_rlimit', 'health_update_driver', 'stats_update_driver']) | DEFAULT_OPTIONS
    assert 'keystone_authtoken' in octavia_conf
    assert set(octavia_conf.items('keystone_authtoken').keys()) == set(['insecure', 'cafile']) | DEFAULT_OPTIONS
    assert 'certificates' in octavia_conf
    assert set(octavia_conf.items('certificates').keys()) == set([
     'cert_generator', 'signing_digest', 'cert_validity_time', 'storage_path',
     'cert_manager', 'region_name', 'endpoint_type']) | DEFAULT_OPTIONS
    assert 'networking' in octavia_conf
    assert set(octavia_conf.items('networking').keys()) == set([
     'max_retries', 'retry_interval', 'port_detach_timeout', 'allow_vip_network_id',
     'allow_vip_subnet_id', 'allow_vip_port_id', 'reserved_ips']) | DEFAULT_OPTIONS
    assert 'haproxy_amphora' in octavia_conf
    assert set(octavia_conf.items('haproxy_amphora').keys()) == set([
     'base_path',
     'base_cert_dir',
     'haproxy_template',
     'connection_logging',
     'connection_max_retries',
     'connection_retry_interval',
     'build_rate_limit',
     'build_active_retries',
     'build_retry_interval',
     'haproxy_stick_size',
     'bind_host',
     'bind_port',
     'lb_network_interface',
     'haproxy_cmd',
     'respawn_count',
     'respawn_interval',
     'client_cert',
     'server_ca',
     'use_upstart',
     'rest_request_conn_timeout',
     'rest_request_read_timeout',
     'active_connection_max_retries',
     'active_connection_rety_interval',
     'user_log_format']) | DEFAULT_OPTIONS
    assert 'controller_worker' in octavia_conf
    assert set(octavia_conf.items('controller_worker').keys()) == set([
     'workers',
     'amp_active_retries',
     'amp_active_wait_sec',
     'amp_image_id',
     'amp_image_tag',
     'amp_image_owner_id',
     'amp_flavor_id',
     'amp_boot_network_list',
     'amp_secgroup_list',
     'amp_ssh_access_allowed',
     'client_ca',
     'amphora_driver',
     'compute_driver',
     'network_driver',
     'volume_driver',
     'distributor_driver',
     'loadbalancer_topology',
     'user_data_config_drive']) | DEFAULT_OPTIONS
    assert 'task_flow' in octavia_conf
    assert set(octavia_conf.items('task_flow').keys()) == set([
     'engine',
     'max_workers',
     'disable_revert']) | DEFAULT_OPTIONS
    assert 'oslo_messaging' in octavia_conf
    assert set(octavia_conf.items('oslo_messaging').keys()) == set([
     'rpc_thread_pool_size',
     'topic']) | DEFAULT_OPTIONS
    assert 'oslo_middleware' in octavia_conf
    assert set(octavia_conf.items('oslo_middleware').keys()) == set([
     'enable_proxy_headers_parsing']) | DEFAULT_OPTIONS
    assert 'house_keeping' in octavia_conf
    assert set(octavia_conf.items('house_keeping').keys()) == set([
     'spare_check_interval',
     'spare_amphora_pool_size',
     'cleanup_interval',
     'amphora_expiry_age',
     'load_balancer_expiry_age']) | DEFAULT_OPTIONS
    assert 'amphora_agent' in octavia_conf
    assert set(octavia_conf.items('amphora_agent').keys()) == set([
     'agent_server_ca',
     'agent_server_cert',
     'agent_server_network_dir',
     'agent_server_network_file',
     'agent_request_read_timeout',
     'agent_tls_protocol',
     'amphora_udp_driver',
     'admin_log_targets',
     'tenant_log_targets',
     'user_log_facility',
     'administrative_log_facility',
     'log_protocol',
     'log_retry_count',
     'log_retry_interval',
     'log_queue_size',
     'logging_template_override',
     'forward_all_logs',
     'disable_local_log_storage']) | DEFAULT_OPTIONS
    assert 'keepalived_vrrp' in octavia_conf
    assert set(octavia_conf.items('keepalived_vrrp').keys()) == set([
     'vrrp_advert_int',
     'vrrp_check_interval',
     'vrrp_fail_count',
     'vrrp_success_count',
     'vrrp_garp_refresh_interval',
     'vrrp_garp_refresh_count']) | DEFAULT_OPTIONS
    assert 'service_auth' in octavia_conf
    assert set(octavia_conf.items('service_auth').keys()) == set([
     'memcached_servers',
     'cafile',
     'auth_type']) | DEFAULT_OPTIONS
    assert 'nova' in octavia_conf
    assert set(octavia_conf.items('nova').keys()) == set([
     'service_name',
     'region_name',
     'endpoint_type',
     'ca_certificates_file',
     'insecure',
     'random_amphora_name_length',
     'availability_zone',
     'enable_anti_affinity',
     'anti_affinity_policy']) | DEFAULT_OPTIONS
    assert 'cinder' in octavia_conf
    assert set(octavia_conf.items('cinder').keys()) == set([
     'service_name',
     'region_name',
     'endpoint_type',
     'availability_zone',
     'insecure',
     'ca_certificates_file',
     'volume_size',
     'volume_type',
     'volume_create_retry_interval',
     'volume_create_timeout',
     'volume_create_max_retries']) | DEFAULT_OPTIONS
    assert 'glance' in octavia_conf
    assert set(octavia_conf.items('glance').keys()) == set([
     'service_name',
     'region_name',
     'endpoint_type',
     'insecure',
     'ca_certificates_file']) | DEFAULT_OPTIONS
    assert 'neutron' in octavia_conf
    assert set(octavia_conf.items('neutron').keys()) == set([
     'service_name',
     'region_name',
     'endpoint_type',
     'insecure',
     'ca_certificates_file']) | DEFAULT_OPTIONS
    assert 'quotas' in octavia_conf
    assert set(octavia_conf.items('quotas').keys()) == set([
     'default_load_balancer_quota',
     'default_listener_quota',
     'default_member_quota',
     'default_pool_quota',
     'default_health_monitor_quota']) | DEFAULT_OPTIONS
    assert 'audit' in octavia_conf
    assert set(octavia_conf.items('audit').keys()) == set([
     'enabled',
     'audit_map_file',
     'ignore_req_list']) | DEFAULT_OPTIONS
    assert 'audit_middleware_notifications' in octavia_conf
    assert set(octavia_conf.items('audit_middleware_notifications').keys()) == set([
     'use_oslo_messaging',
     'driver',
     'topics']) | DEFAULT_OPTIONS
    assert 'driver_agent' in octavia_conf
    assert set(octavia_conf.items('driver_agent').keys()) == set([
     'status_socket_path',
     'stats_socket_path',
     'get_socket_path',
     'status_request_timeout',
     'status_max_processes',
     'stats_request_timeout',
     'stats_max_processes',
     'max_process_warning_percent',
     'provider_agent_shutdown_timeout',
     'enabled_provider_agents']) | DEFAULT_OPTIONS
    return


def test_doc_examples():
    env = {'octavia_conf': OctaviaConf(context_wrap(CONF_FILE))}
    failed, total = doctest.testmod(octavia_module, globs=env)
    assert failed == 0