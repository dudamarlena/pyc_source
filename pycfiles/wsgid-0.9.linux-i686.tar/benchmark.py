# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/wsgid/benchmark.py
# Compiled at: 2009-03-17 01:36:40
import os, sys, subprocess, time
all = [
 'twistedweb']
try:
    os.mkdir('bench_out')
except OSError:
    pass

processes = []
results = []
sys.stderr.write('performing benchmark for %s\n' % all)
for rps in ['1', '100', '1000']:
    sys.stderr.write('c=%4s' % rps)
    for sname in all:
        sys.stderr.write(' %s:' % sname)
        daemon = subprocess.Popen([
         'wsgid', '-T', '-O', sname, '-p', 'benchmark.pid', '-N'], stdout=open(os.path.join('bench_out', 'benchout.txt'), 'a'), stderr=open(os.path.join('bench_out', 'benchout.txt'), 'a'))
        processes.append(daemon.pid)
        time.sleep(1)
        tester = subprocess.Popen([
         'ab', '-n', '1000', '-c', rps,
         'http://localhost:9090/'], stdout=subprocess.PIPE, stderr=open(os.path.join('bench_out', 'benchout.txt'), 'a'))
        (output, a) = tester.communicate()
        stopper = subprocess.Popen(['wsgid', '-s', sname, '-p', 'benchmark.pid'], stdout=open(os.path.join('bench_out', 'benchout.txt'), 'a'), stderr=open(os.path.join('bench_out', 'benchout.txt'), 'a'))
        stopper.communicate()
        daemon.communicate()
        sys.stderr.write('(%s,%s,%s)' % (
         daemon.returncode,
         tester.returncode,
         stopper.returncode))
        pid = daemon.pid
        try:
            os.kill(pid, 15)
        except OSError:
            pass

        try:
            os.kill(pid, 9)
        except OSError:
            pass

        for line in output.splitlines():
            if 'Requests per second' in line:
                results.append((
                 float(line.strip().split(':', 1)[(-1)].strip().split()[0]),
                 sname,
                 rps))

    sys.stderr.write('\n')
    sys.stderr.flush()

sys.stderr.write('Finished. Results:\n')
sys.stderr.flush()
for pid in processes:
    try:
        os.kill(pid, 15)
        time.sleep(1)
    except OSError:
        pass

    try:
        os.kill(pid, 9)
    except OSError:
        pass

print '%8s\t%18s\t%8s' % ('--------', '------------------', '--------')
print '%8s\t%18s\t%8s' % ('Req/s', 'Server', 'c')
print '%8s\t%18s\t%8s' % ('--------', '------------------', '--------')
for res in reversed(sorted(results)):
    print '%8s\t%18s\t%8s' % res