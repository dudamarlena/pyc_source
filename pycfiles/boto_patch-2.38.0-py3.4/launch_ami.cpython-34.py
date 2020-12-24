# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/launch_ami.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 7585 bytes
import getopt, sys, imp, time, boto
usage_string = '\nSYNOPSIS\n    launch_ami.py -a ami_id [-b script_bucket] [-s script_name]\n                  [-m module] [-c class_name] [-r]\n                  [-g group] [-k key_name] [-n num_instances]\n                  [-w] [extra_data]\n    Where:\n        ami_id - the id of the AMI you wish to launch\n        module - The name of the Python module containing the class you\n                 want to run when the instance is started.  If you use this\n                 option the Python module must already be stored on the\n                 instance in a location that is on the Python path.\n        script_file - The name of a local Python module that you would like\n                      to have copied to S3 and then run on the instance\n                      when it is started.  The specified module must be\n                      import\'able (i.e. in your local Python path).  It\n                      will then be copied to the specified bucket in S3\n                      (see the -b option).  Once the new instance(s)\n                      start up the script will be copied from S3 and then\n                      run locally on the instance.\n        class_name - The name of the class to be instantiated within the\n                     module or script file specified.\n        script_bucket - the name of the bucket in which the script will be\n                        stored\n        group - the name of the security group the instance will run in\n        key_name - the name of the keypair to use when launching the AMI\n        num_instances - how many instances of the AMI to launch (default 1)\n        input_queue_name - Name of SQS to read input messages from\n        output_queue_name - Name of SQS to write output messages to\n        extra_data - additional name-value pairs that will be passed as\n                     userdata to the newly launched instance.  These should\n                     be of the form "name=value"\n        The -r option reloads the Python module to S3 without launching\n        another instance.  This can be useful during debugging to allow\n        you to test a new version of your script without shutting down\n        your instance and starting up another one.\n        The -w option tells the script to run synchronously, meaning to\n        wait until the instance is actually up and running.  It then prints\n        the IP address and internal and external DNS names before exiting.\n'

def usage():
    print(usage_string)
    sys.exit()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:b:c:g:hi:k:m:n:o:rs:w', [
         'ami', 'bucket', 'class', 'group', 'help',
         'inputqueue', 'keypair', 'module',
         'numinstances', 'outputqueue',
         'reload', 'script_name', 'wait'])
    except:
        usage()

    params = {'module_name': None,  'script_name': None,  'class_name': None, 
     'script_bucket': None, 
     'group': 'default', 
     'keypair': None, 
     'ami': None, 
     'num_instances': 1, 
     'input_queue_name': None, 
     'output_queue_name': None}
    reload = None
    wait = None
    for o, a in opts:
        if o in ('-a', '--ami'):
            params['ami'] = a
        if o in ('-b', '--bucket'):
            params['script_bucket'] = a
        if o in ('-c', '--class'):
            params['class_name'] = a
        if o in ('-g', '--group'):
            params['group'] = a
        if o in ('-h', '--help'):
            usage()
        if o in ('-i', '--inputqueue'):
            params['input_queue_name'] = a
        if o in ('-k', '--keypair'):
            params['keypair'] = a
        if o in ('-m', '--module'):
            params['module_name'] = a
        if o in ('-n', '--num_instances'):
            params['num_instances'] = int(a)
        if o in ('-o', '--outputqueue'):
            params['output_queue_name'] = a
        if o in ('-r', '--reload'):
            reload = True
        if o in ('-s', '--script'):
            params['script_name'] = a
        if o in ('-w', '--wait'):
            wait = True
            continue

    required = [
     'ami']
    for pname in required:
        if not params.get(pname, None):
            print('%s is required' % pname)
            usage()
            continue

    if params['script_name']:
        if reload:
            print('Reloading module %s to S3' % params['script_name'])
        else:
            print('Copying module %s to S3' % params['script_name'])
        l = imp.find_module(params['script_name'])
        c = boto.connect_s3()
        bucket = c.get_bucket(params['script_bucket'])
        key = bucket.new_key(params['script_name'] + '.py')
        key.set_contents_from_file(l[0])
        params['script_md5'] = key.md5
    l = []
    for k, v in params.items():
        if v:
            l.append('%s=%s' % (k, v))
            continue

    c = boto.connect_ec2()
    l.append('aws_access_key_id=%s' % c.aws_access_key_id)
    l.append('aws_secret_access_key=%s' % c.aws_secret_access_key)
    for kv in args:
        l.append(kv)

    s = '|'.join(l)
    if not reload:
        rs = c.get_all_images([params['ami']])
        img = rs[0]
        r = img.run(user_data=s, key_name=params['keypair'], security_groups=[
         params['group']], max_count=params.get('num_instances', 1))
        print('AMI: %s - %s (Started)' % (params['ami'], img.location))
        print('Reservation %s contains the following instances:' % r.id)
        for i in r.instances:
            print('\t%s' % i.id)

        if wait:
            running = False
            while not running:
                time.sleep(30)
                [i.update() for i in r.instances]
                status = [i.state for i in r.instances]
                print(status)
                if status.count('running') == len(r.instances):
                    running = True
                    continue

            for i in r.instances:
                print('Instance: %s' % i.ami_launch_index)
                print('Public DNS Name: %s' % i.public_dns_name)
                print('Private DNS Name: %s' % i.private_dns_name)


if __name__ == '__main__':
    main()