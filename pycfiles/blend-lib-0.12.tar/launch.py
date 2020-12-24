# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: blend/cloudman/launch.py
# Compiled at: 2012-07-04 03:04:52
"""
Setup and launch a CloudMan instance.
"""
import logging, datetime
from httplib import HTTP
from urlparse import urlparse
import boto
from boto.ec2.regioninfo import RegionInfo
from boto.exception import EC2ResponseError
import blend

class Bunch(object):
    """
    A convenience class to allow dict keys to be representes as object fields.

    The end result is that this allows a dict to be to be represented the same
    as a database class, thus the two become interchangeable as a data source.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        """
        Return the contents of the dict in a printable representation
        """
        return str(self.__dict__)


class CloudManLaunch(object):

    def __init__(self, access_key, secret_key, cloud=None):
        """
        Define the environment in which this instance of CloudMan will be launched.

        Besides providing the credentials, optionally provide the ``cloud``
        object. This object must define the properties required to establish a
        `boto <https://github.com/boto/boto/>`_ connection to that cloud. See
        this method's implementation for an example of the required fields.
        Note that as long the as provided object defines the required fields,
        it can really by implemented as anything (e.g., a Bunch, a database
        object, a custom class). If no value for the ``cloud`` argument is
        provided, the default is to use the Amazon cloud.
        """
        self.access_key = access_key
        self.secret_key = secret_key
        if cloud is None:
            self.cloud = Bunch(id='1', name='Amazon', cloud_type='ec2', bucket_default='cloudman', region_name='us-east-1', region_endpoint='ec2.amazonaws.com', ec2_port='', ec2_conn_path='/', cidr_range='', is_secure=True, s3_host='s3.amazonaws.com', s3_port='', s3_conn_path='/')
        else:
            self.cloud = cloud
        self.ec2_conn = self.connect_ec2(self.access_key, self.secret_key, self.cloud)
        self.instance_id = None
        self.rs = None
        return

    def __repr__(self):
        return ('Cloud: {0}; acct ID: {1}').format(self.cloud.name, self.access_key)

    def launch(self, cluster_name, image_id, instance_type, password, kernel_id=None, ramdisk_id=None, key_name='cloudman_key_pair', security_groups=[
 'CloudMan'], placement='', **kwargs):
        """
        Check all the prerequisites (key pair and security groups) for
        launching a CloudMan instance, compose the user data based on the
        parameters specified in the arguments and the cloud properties as
        defined in the object's ``cloud`` field.

        For the current list of user data fields that can be provided via
        ``kwargs``, see `<http://wiki.g2.bx.psu.edu/CloudMan/UserData>`_

        Return a dict containing the properties and info with wich an instance
        was launched, namely: ``sg_names`` containing the names of the security
        groups, ``kp_name`` containing the name of the key pair, ``kp_material``
        containing the private portion of the key pair (*note* that this portion
        of the key is available and can be retrieved *only* at the time the key
        is created, which will happen only if no key with the name provided in
        the ``key_name`` argument exists), ``rs`` containing the
        `boto <https://github.com/boto/boto/>`_ ``ResultSet`` object,
        ``instance_id`` containing the ID of a started instance, and
        ``error`` containing an error message if there was one.
        """
        ret = {'sg_names': [], 'kp_name': '', 
           'kp_material': '', 
           'rs': '', 
           'instance_id': '', 
           'error': ''}
        for sg in security_groups:
            ret['sg_names'].append(self.create_cm_security_group(sg))

        (ret['kp_name'], ret['kp_material']) = self.create_key_pair(key_name)
        if placement == '':
            placement = self._find_placement(self.ec2_conn, instance_type, self.cloud.cloud_type)
        kwargs['access_key'] = self.access_key
        kwargs['secret_key'] = self.secret_key
        kwargs['cluster_name'] = cluster_name
        kwargs['password'] = password
        kwargs['cloud_name'] = self.cloud.name
        ud = self._compose_user_data(kwargs)
        try:
            rs = None
            rs = self.ec2_conn.run_instances(image_id=image_id, instance_type=instance_type, key_name=key_name, security_groups=security_groups, user_data=ud, kernel_id=kernel_id, ramdisk_id=ramdisk_id, placement=placement)
            ret['rs'] = rs
        except EC2ResponseError, e:
            err = 'Problem launching an instance: %s' % e
            blend.log.error(err)
            ret['error'] = err

        if rs:
            try:
                blend.log.info('Launched an instance with ID %s' % rs.instances[0].id)
                ret['instance_id'] = rs.instances[0].id
                ret['instance_ip'] = rs.instances[0].ip_address
                self.rs = rs
                self.instance_id = rs.instances[0].id
            except Exception, e:
                err = 'Problem with the launched instance object: %s' % e
                blend.log.error(err)
                ret['error'] = err

        else:
            err = 'Problem launching an instance?'
            blend.log.warning(err)
            ret['error'] = err
        return ret

    def create_cm_security_group(self, sg_name='CloudMan'):
        """ 
        Create a security group with all authorizations required to run CloudMan.
        If the group already exists, check its rules and add the missing ones.
        Return the name of the created security group.
        """
        cmsg = None
        sgs = self.ec2_conn.get_all_security_groups()
        for sg in sgs:
            if sg.name == sg_name:
                cmsg = sg
                blend.log.debug("Security group '%s' already exists; will add authorizations next." % sg_name)
                break

        if cmsg is None:
            blend.log.debug('Creating Security Group %s' % sg_name)
            cmsg = self.ec2_conn.create_security_group(sg_name, 'A security group for CloudMan')
        ports = (
         ('80', '80'),
         ('20', '21'),
         ('22', '22'),
         ('30000', '30100'),
         ('42284', '42284'))
        for port in ports:
            try:
                if not self.rule_exists(cmsg.rules, from_port=port[0], to_port=port[1]):
                    cmsg.authorize(ip_protocol='tcp', from_port=port[0], to_port=port[1], cidr_ip='0.0.0.0/0')
                else:
                    blend.log.debug('Rule (%s:%s) already exists in the SG' % (port[0], port[1]))
            except EC2ResponseError, e:
                blend.log.error('A problem with security group authorizations: %s' % e)

        g_rule_exists = False
        ci = self._get_cloud_info(self.cloud)
        cloud_type = ci['cloud_type']
        cidr_range = ci.get('cidr_range', '')
        if cloud_type == 'ec2':
            for rule in cmsg.rules:
                for grant in rule.grants:
                    if grant.name == cmsg.name:
                        g_rule_exists = True
                        blend.log.debug('Group rule already exists in the SG')

                if g_rule_exists:
                    break

        else:
            for rule in cmsg.rules:
                for grant in rule.grants:
                    if grant.cidr_ip == cidr_range:
                        g_rule_exists = True
                        blend.log.debug('Group rule already exists in the SG')
                    if g_rule_exists:
                        break

            if g_rule_exists is False:
                try:
                    if cloud_type == 'ec2':
                        cmsg.authorize(src_group=cmsg)
                    else:
                        cmsg.authorize(ip_protocol='tcp', from_port=1, to_port=65535, cidr_ip=cidr_range)
                except EC2ResponseError, e:
                    blend.log.error('A problem w/ security group authorization: %s' % e)

            blend.log.info("Done configuring '%s' security group" % cmsg.name)
            return cmsg.name

    def rule_exists--- This code section failed: ---

 L. 226         0  SETUP_LOOP          113  'to 116'
                3  LOAD_FAST             1  'rules'
                6  GET_ITER         
                7  FOR_ITER            105  'to 115'
               10  STORE_FAST            6  'rule'

 L. 227        13  LOAD_FAST             6  'rule'
               16  LOAD_ATTR             0  'ip_protocol'
               19  LOAD_FAST             4  'ip_protocol'
               22  COMPARE_OP            2  ==
               25  JUMP_IF_FALSE        83  'to 111'
               28  POP_TOP          
               29  LOAD_FAST             6  'rule'
               32  LOAD_ATTR             1  'from_port'
               35  LOAD_FAST             2  'from_port'
               38  COMPARE_OP            2  ==
               41  JUMP_IF_FALSE        67  'to 111'
               44  POP_TOP          

 L. 228        45  LOAD_FAST             6  'rule'
               48  LOAD_ATTR             2  'to_port'
               51  LOAD_FAST             3  'to_port'
               54  COMPARE_OP            2  ==
               57  JUMP_IF_FALSE        51  'to 111'
             60_0  THEN                     111
               60  POP_TOP          
               61  LOAD_FAST             5  'cidr_ip'
               64  BUILD_LIST_0          0 
               67  DUP_TOP          
               68  STORE_FAST            7  '_[1]'
               71  LOAD_FAST             6  'rule'
               74  LOAD_ATTR             3  'grants'
               77  GET_ITER         
               78  FOR_ITER             16  'to 97'
               81  STORE_FAST            8  'ip'
               84  LOAD_FAST             7  '_[1]'
               87  LOAD_FAST             8  'ip'
               90  LOAD_ATTR             4  'cidr_ip'
               93  LIST_APPEND      
               94  JUMP_BACK            78  'to 78'
               97  DELETE_FAST           7  '_[1]'
              100  COMPARE_OP            6  in
              103  JUMP_IF_FALSE         5  'to 111'
            106_0  THEN                     111
              106  POP_TOP          

 L. 229       107  LOAD_GLOBAL           5  'True'
              110  RETURN_END_IF    
              111  POP_TOP          
              112  JUMP_BACK             7  'to 7'
              115  POP_BLOCK        
            116_0  COME_FROM             0  '0'

 L. 230       116  LOAD_GLOBAL           6  'False'
              119  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 115

    def create_key_pair(self, key_name='cloudman_key_pair'):
        """ 
        Create a key pair with the provided ``key_name``.
        Return the name of the key or ``None`` if there was an error creating the key.
        """
        kp = None
        kps = self.ec2_conn.get_all_key_pairs()
        for akp in kps:
            if akp.name == key_name:
                blend.log.debug("Key pair '%s' already exists; not creating it again." % key_name)
                return (
                 akp.name, None)

        try:
            kp = self.ec2_conn.create_key_pair(key_name)
        except EC2ResponseError, e:
            blend.log.error("Problem creating key pair '%s': %s" % (key_name, e))
            return (None, None)

        blend.log.info("Created key pair '%s'" % kp.name)
        return (kp.name, kp.material)

    def get_status(self, instance_id=None, ec2_conn=None):
        """
        Check on the status of an instance. If ``instance_id`` is not provided,
        the ID obtained when launching *the most recent* instance is used. Note
        that this assumes the instance being checked on was launched using this
        class. Also note that the same class may be used to launch multiple instances
        but only the most recent ``instance_id`` is kept while any others will
        need to be explicitly specified.

        This method also allows the required ``ec2_conn`` connection object to be
        provided at invocation time. If the object is not provided, credentials
        defined for the class are used (ability to specify a custom ``ec2_conn``
        helps in case of stateless method invocations).

        Return a ``state`` dict with the current ``instance_state``, ``public_ip``,
        ``placement``, and ``error`` keys, which capture the current state (the
        values for those keys defualt to empty string if no data is available from
        the cloud).
        """
        if ec2_conn is None:
            ec2_conn = self.ec2_conn
        rs = None
        state = {'instance_state': '', 'public_ip': '', 
           'placement': '', 
           'error': ''}
        if instance_id is None:
            instance_id = self.instance_id
        if instance_id is None:
            err = 'Missing instance ID, cannot check the state.'
            blend.log.error(err)
            state['error'] = err
            return state
        else:
            try:
                rs = ec2_conn.get_all_instances([instance_id])
                if rs is not None:
                    inst_state = rs[0].instances[0].update()
                    public_ip = rs[0].instances[0].ip_address
                    if inst_state == 'running':
                        cm_url = ('http://{dns}/cloud').format(dns=public_ip)
                        if self._checkURL(cm_url) is True:
                            state['public_ip'] = public_ip
                            state['instance_state'] = inst_state
                            state['placement'] = rs[0].instances[0].placement
                        else:
                            state['instance_state'] = 'booting'
                    else:
                        state['instance_state'] = inst_state
            except Exception, e:
                err = "Problem updating instance '%s' state: %s" % (instance_id, e)
                blend.log.error(err)
                state['error'] = err

            return state

    def connect_ec2(self, a_key, s_key, cloud=None):
        """
        Create and return an EC2-compatible connection object for the given cloud.

        See ``_get_cloud_info`` method for more details on the requirements for
        the ``cloud`` parameter. If no value is provided, the class field is used.
        """
        if cloud is None:
            cloud = self.cloud
        ci = self._get_cloud_info(cloud)
        r = RegionInfo(name=ci['region_name'], endpoint=ci['region_endpoint'])
        ec2_conn = boto.connect_ec2(aws_access_key_id=a_key, aws_secret_access_key=s_key, api_version='2012-06-01' if ci['cloud_type'] == 'ec2' else None, is_secure=ci['is_secure'], region=r, port=ci['ec2_port'], path=ci['ec2_conn_path'])
        return ec2_conn

    def _compose_user_data(self, user_provided_data):
        """
        A convenience method used to compose and properly format the user data
        required when requiesting an instance.

        ``user_provided_data`` is the data provided by a user required to identify
        a cluster and user other user requirements.
        """
        form_data = {}
        excluded_fields = [
         'sg_name', 'image_id', 'instance_id', 'kp_name', 'cloud', 'cloud_type',
         'public_dns', 'cidr_range', 'kp_material', 'placement']
        for (key, value) in user_provided_data.iteritems():
            if key not in excluded_fields:
                form_data[key] = value

        udkeys = [
         'post_start_script_url', 'worker_post_start_script_url', 'bucket_default', 'share_string']
        for udkey in udkeys:
            if udkey in form_data and form_data[udkey] == '':
                del form_data[udkey]

        if 'bucket_default' not in form_data and self.cloud.bucket_default != '':
            form_data['bucket_default'] = self.cloud.bucket_default
        if 'freenxpass' not in form_data and 'password' in form_data:
            form_data['freenxpass'] = form_data['password']
        ud = ('\n').join([ '%s: %s' % (key, value) for (key, value) in form_data.iteritems() ])
        ci = self._get_cloud_info(self.cloud, as_str=True)
        return ud + '\n' + ci

    def _get_cloud_info(self, cloud, as_str=False):
        """
        Get connection information about a given cloud
        """
        ci = {}
        ci['cloud_type'] = cloud.cloud_type
        ci['region_name'] = cloud.region_name
        ci['region_endpoint'] = cloud.region_endpoint
        ci['is_secure'] = cloud.is_secure
        ci['ec2_port'] = cloud.ec2_port if cloud.ec2_port != '' else None
        ci['ec2_conn_path'] = cloud.ec2_conn_path
        if cloud.cidr_range != '':
            ci['cidr_range'] = cloud.cidr_range
        ci['s3_host'] = cloud.s3_host
        ci['s3_port'] = cloud.s3_port if cloud.s3_port != '' else None
        ci['s3_conn_path'] = cloud.s3_conn_path
        if as_str:
            ci = ('\n').join([ '%s: %s' % (key, value) for (key, value) in ci.iteritems() ])
        return ci

    def _find_placement(self, ec2_conn, instance_type, cloud_type, get_all=False):
        """
        Find an EC2 region zone that supports the requested instance type.

        By default, the method will return a single (first match) availability
        zone that matches the requirements. If want to get a list of all
        the zones that match the requirements, set ``get_all`` to ``True``.

        We do this by checking the spot prices in the potential availability zones
        for support before deciding on a region:
        http://blog.piefox.com/2011/07/ec2-availability-zones-and-instance.html

        Note that, currently, this only applies to AWS. For other clouds, all
        the available zones are returned.
        """
        zones = []
        if cloud_type == 'ec2':
            base = self.ec2_conn.region.name
            yesterday = datetime.datetime.now() - datetime.timedelta(1)
            for loc_choice in ['b', 'a', 'c', 'd']:
                cur_loc = ('{base}{ext}').format(base=base, ext=loc_choice)
                if len(self.ec2_conn.get_spot_price_history(instance_type=instance_type, end_time=yesterday.isoformat(), availability_zone=cur_loc)) > 0:
                    if get_all is True:
                        zones.append(cur_loc)
                    else:
                        return cur_loc

        for zone in self.ec2_conn.get_all_zones():
            if get_all is True:
                zones.append(zone.name)
            else:
                return zone.name

        if len(zones) == 0:
            blend.log.error(('Did not find availabilty zone in {0} for {1}').format(base, instance_type))
        return zones

    def _checkURL(self, url):
        """
        Check if the ``url`` is *alive* (i.e., remote server returns code 200(OK)
        or 401 (unauthorized)).
        """
        try:
            p = urlparse(url)
            h = HTTP(p[1])
            h.putrequest('HEAD', p[2])
            h.endheaders()
            r = h.getreply()
            if r[0] == 200 or r[0] == 401:
                return True
        except Exception:
            pass

        return False