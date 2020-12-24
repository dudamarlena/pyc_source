# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/elb/loadbalancer.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 16388 bytes
from boto.ec2.elb.healthcheck import HealthCheck
from boto.ec2.elb.listener import Listener
from boto.ec2.elb.listelement import ListElement
from boto.ec2.elb.policies import Policies, OtherPolicy
from boto.ec2.elb.securitygroup import SecurityGroup
from boto.ec2.instanceinfo import InstanceInfo
from boto.resultset import ResultSet
from boto.compat import six

class Backend(object):
    """Backend"""

    def __init__(self, connection=None):
        self.connection = connection
        self.instance_port = None
        self.policies = None

    def __repr__(self):
        return 'Backend(%r:%r)' % (self.instance_port, self.policies)

    def startElement(self, name, attrs, connection):
        if name == 'PolicyNames':
            self.policies = ResultSet([('member', OtherPolicy)])
            return self.policies

    def endElement(self, name, value, connection):
        if name == 'InstancePort':
            self.instance_port = int(value)


class LoadBalancerZones(object):
    """LoadBalancerZones"""

    def __init__(self, connection=None):
        self.connection = connection
        self.zones = ListElement()

    def startElement(self, name, attrs, connection):
        if name == 'AvailabilityZones':
            return self.zones

    def endElement(self, name, value, connection):
        pass


class LoadBalancer(object):
    """LoadBalancer"""

    def __init__(self, connection=None, name=None, endpoints=None):
        """
        :ivar boto.ec2.elb.ELBConnection connection: The connection this load
            balancer was instance was instantiated from.
        :ivar list listeners: A list of tuples in the form of
            ``(<Inbound port>, <Outbound port>, <Protocol>)``
        :ivar boto.ec2.elb.healthcheck.HealthCheck health_check: The health
            check policy for this load balancer.
        :ivar boto.ec2.elb.policies.Policies policies: Cookie stickiness and
            other policies.
        :ivar str name: The name of the Load Balancer.
        :ivar str dns_name: The external DNS name for the balancer.
        :ivar str created_time: A date+time string showing when the
            load balancer was created.
        :ivar list instances: A list of :py:class:`boto.ec2.instanceinfo.InstanceInfo`
            instances, representing the EC2 instances this load balancer is
            distributing requests to.
        :ivar list availability_zones: The availability zones this balancer
            covers.
        :ivar str canonical_hosted_zone_name: Current CNAME for the balancer.
        :ivar str canonical_hosted_zone_name_id: The Route 53 hosted zone
            ID of this balancer. Needed when creating an Alias record in a
            Route 53 hosted zone.
        :ivar boto.ec2.elb.securitygroup.SecurityGroup source_security_group:
            The security group that you can use as part of your inbound rules
            for your load balancer back-end instances to disallow traffic
            from sources other than your load balancer.
        :ivar list subnets: A list of subnets this balancer is on.
        :ivar list security_groups: A list of additional security groups that
            have been applied.
        :ivar str vpc_id: The ID of the VPC that this ELB resides within.
        :ivar list backends: A list of :py:class:`boto.ec2.elb.loadbalancer.Backend
            back-end server descriptions.
        """
        self.connection = connection
        self.name = name
        self.listeners = None
        self.health_check = None
        self.policies = None
        self.dns_name = None
        self.created_time = None
        self.instances = None
        self.availability_zones = ListElement()
        self.canonical_hosted_zone_name = None
        self.canonical_hosted_zone_name_id = None
        self.source_security_group = None
        self.subnets = ListElement()
        self.security_groups = ListElement()
        self.vpc_id = None
        self.scheme = None
        self.backends = None
        self._attributes = None

    def __repr__(self):
        return 'LoadBalancer:%s' % self.name

    def startElement(self, name, attrs, connection):
        if name == 'HealthCheck':
            self.health_check = HealthCheck(self)
            return self.health_check
        if name == 'ListenerDescriptions':
            self.listeners = ResultSet([('member', Listener)])
            return self.listeners
        if name == 'AvailabilityZones':
            return self.availability_zones
        if name == 'Instances':
            self.instances = ResultSet([('member', InstanceInfo)])
            return self.instances
        if name == 'Policies':
            self.policies = Policies(self)
            return self.policies
        if name == 'SourceSecurityGroup':
            self.source_security_group = SecurityGroup()
            return self.source_security_group
        if name == 'Subnets':
            return self.subnets
        if name == 'SecurityGroups':
            return self.security_groups
        if name == 'VPCId':
            pass
        else:
            if name == 'BackendServerDescriptions':
                self.backends = ResultSet([('member', Backend)])
                return self.backends
            else:
                return

    def endElement(self, name, value, connection):
        if name == 'LoadBalancerName':
            self.name = value
        else:
            if name == 'DNSName':
                self.dns_name = value
            else:
                if name == 'CreatedTime':
                    self.created_time = value
                else:
                    if name == 'InstanceId':
                        self.instances.append(value)
                    else:
                        if name == 'CanonicalHostedZoneName':
                            self.canonical_hosted_zone_name = value
                        else:
                            if name == 'CanonicalHostedZoneNameID':
                                self.canonical_hosted_zone_name_id = value
                            else:
                                if name == 'VPCId':
                                    self.vpc_id = value
                                else:
                                    if name == 'Scheme':
                                        self.scheme = value
                                    else:
                                        setattr(self, name, value)

    def enable_zones(self, zones):
        """
        Enable availability zones to this Access Point.
        All zones must be in the same region as the Access Point.

        :type zones: string or List of strings
        :param zones: The name of the zone(s) to add.

        """
        if isinstance(zones, six.string_types):
            zones = [
             zones]
        new_zones = self.connection.enable_availability_zones(self.name, zones)
        self.availability_zones = new_zones

    def disable_zones(self, zones):
        """
        Disable availability zones from this Access Point.

        :type zones: string or List of strings
        :param zones: The name of the zone(s) to add.

        """
        if isinstance(zones, six.string_types):
            zones = [
             zones]
        new_zones = self.connection.disable_availability_zones(self.name, zones)
        self.availability_zones = new_zones

    def get_attributes(self, force=False):
        """
        Gets the LbAttributes.  The Attributes will be cached.

        :type force: bool
        :param force: Ignore cache value and reload.

        :rtype: boto.ec2.elb.attributes.LbAttributes
        :return: The LbAttribues object
        """
        if not self._attributes or force:
            self._attributes = self.connection.get_all_lb_attributes(self.name)
        return self._attributes

    def is_cross_zone_load_balancing(self, force=False):
        """
        Identifies if the ELB is current configured to do CrossZone Balancing.

        :type force: bool
        :param force: Ignore cache value and reload.

        :rtype: bool
        :return: True if balancing is enabled, False if not.
        """
        return self.get_attributes(force).cross_zone_load_balancing.enabled

    def enable_cross_zone_load_balancing(self):
        """
        Turns on CrossZone Load Balancing for this ELB.

        :rtype: bool
        :return: True if successful, False if not.
        """
        success = self.connection.modify_lb_attribute(self.name, 'crossZoneLoadBalancing', True)
        if success and self._attributes:
            self._attributes.cross_zone_load_balancing.enabled = True
        return success

    def disable_cross_zone_load_balancing(self):
        """
        Turns off CrossZone Load Balancing for this ELB.

        :rtype: bool
        :return: True if successful, False if not.
        """
        success = self.connection.modify_lb_attribute(self.name, 'crossZoneLoadBalancing', False)
        if success and self._attributes:
            self._attributes.cross_zone_load_balancing.enabled = False
        return success

    def register_instances(self, instances):
        """
        Adds instances to this load balancer. All instances must be in the same
        region as the load balancer. Adding endpoints that are already
        registered with the load balancer has no effect.

        :param list instances: List of instance IDs (strings) that you'd like
            to add to this load balancer.

        """
        if isinstance(instances, six.string_types):
            instances = [
             instances]
        new_instances = self.connection.register_instances(self.name, instances)
        self.instances = new_instances

    def deregister_instances(self, instances):
        """
        Remove instances from this load balancer. Removing instances that are
        not registered with the load balancer has no effect.

        :param list instances: List of instance IDs (strings) that you'd like
            to remove from this load balancer.

        """
        if isinstance(instances, six.string_types):
            instances = [
             instances]
        new_instances = self.connection.deregister_instances(self.name, instances)
        self.instances = new_instances

    def delete(self):
        """
        Delete this load balancer.
        """
        return self.connection.delete_load_balancer(self.name)

    def configure_health_check(self, health_check):
        """
        Configures the health check behavior for the instances behind this
        load balancer. See :ref:`elb-configuring-a-health-check` for a
        walkthrough.

        :param boto.ec2.elb.healthcheck.HealthCheck health_check: A
            HealthCheck instance that tells the load balancer how to check
            its instances for health.
        """
        return self.connection.configure_health_check(self.name, health_check)

    def get_instance_health(self, instances=None):
        """
        Returns a list of :py:class:`boto.ec2.elb.instancestate.InstanceState`
        objects, which show the health of the instances attached to this
        load balancer.

        :rtype: list
        :returns: A list of
            :py:class:`InstanceState <boto.ec2.elb.instancestate.InstanceState>`
            instances, representing the instances
            attached to this load balancer.
        """
        return self.connection.describe_instance_health(self.name, instances)

    def create_listeners(self, listeners):
        return self.connection.create_load_balancer_listeners(self.name, listeners)

    def create_listener(self, inPort, outPort=None, proto='tcp'):
        if outPort is None:
            outPort = inPort
        return self.create_listeners([(inPort, outPort, proto)])

    def delete_listeners(self, listeners):
        return self.connection.delete_load_balancer_listeners(self.name, listeners)

    def delete_listener(self, inPort):
        return self.delete_listeners([inPort])

    def delete_policy(self, policy_name):
        """
        Deletes a policy from the LoadBalancer. The specified policy must not
        be enabled for any listeners.
        """
        return self.connection.delete_lb_policy(self.name, policy_name)

    def set_policies_of_listener(self, lb_port, policies):
        return self.connection.set_lb_policies_of_listener(self.name, lb_port, policies)

    def set_policies_of_backend_server(self, instance_port, policies):
        return self.connection.set_lb_policies_of_backend_server(self.name, instance_port, policies)

    def create_cookie_stickiness_policy(self, cookie_expiration_period, policy_name):
        return self.connection.create_lb_cookie_stickiness_policy(cookie_expiration_period, self.name, policy_name)

    def create_app_cookie_stickiness_policy(self, name, policy_name):
        return self.connection.create_app_cookie_stickiness_policy(name, self.name, policy_name)

    def set_listener_SSL_certificate(self, lb_port, ssl_certificate_id):
        return self.connection.set_lb_listener_SSL_certificate(self.name, lb_port, ssl_certificate_id)

    def create_lb_policy(self, policy_name, policy_type, policy_attribute):
        return self.connection.create_lb_policy(self.name, policy_name, policy_type, policy_attribute)

    def attach_subnets(self, subnets):
        """
        Attaches load balancer to one or more subnets.
        Attaching subnets that are already registered with the
        Load Balancer has no effect.

        :type subnets: string or List of strings
        :param subnets: The name of the subnet(s) to add.

        """
        if isinstance(subnets, six.string_types):
            subnets = [
             subnets]
        new_subnets = self.connection.attach_lb_to_subnets(self.name, subnets)
        self.subnets = new_subnets

    def detach_subnets(self, subnets):
        """
        Detaches load balancer from one or more subnets.

        :type subnets: string or List of strings
        :param subnets: The name of the subnet(s) to detach.

        """
        if isinstance(subnets, six.string_types):
            subnets = [
             subnets]
        new_subnets = self.connection.detach_lb_from_subnets(self.name, subnets)
        self.subnets = new_subnets

    def apply_security_groups(self, security_groups):
        """
        Associates one or more security groups with the load balancer.
        The provided security groups will override any currently applied
        security groups.

        :type security_groups: string or List of strings
        :param security_groups: The name of the security group(s) to add.

        """
        if isinstance(security_groups, six.string_types):
            security_groups = [
             security_groups]
        new_sgs = self.connection.apply_security_groups_to_lb(self.name, security_groups)
        self.security_groups = new_sgs