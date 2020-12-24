# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dreegdl/utils.py
# Compiled at: 2020-03-04 18:14:20
# Size of source mod 2**32: 6169 bytes
import io, fcntl, os, select, sys, numpy as np, subprocess, base64
from glob import glob
from tqdm import tqdm_notebook as tqdmn
from IPython.display import HTML, display, Image
import IPython.utils as ipio
from datetime import datetime

class Utils:

    def list2arr(*argv):
        out = np.empty((len(argv)), dtype=(np.object))
        for i in range(len(argv)):
            out[i] = argv[i]

        return out

    def run_cmd(cmd, ret=False, cb_err=None, cb_out=None):
        out = ''
        proc = subprocess.Popen(cmd, stdin=(subprocess.PIPE), stderr=(subprocess.PIPE), stdout=(subprocess.PIPE),
          universal_newlines=True,
          shell=True)
        while proc.poll() == None:
            fcntl.fcntl(proc.stderr.fileno(), fcntl.F_SETFL, fcntl.fcntl(proc.stderr.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
            fcntl.fcntl(proc.stdout.fileno(), fcntl.F_SETFL, fcntl.fcntl(proc.stdout.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
            while proc.poll() == None:
                readx_err = select.select([proc.stderr.fileno()], [], [], 0.1)[0]
                if readx_err:
                    chunk = proc.stderr.read().strip()
                    if chunk:
                        if cb_err:
                            cb_err(chunk)
                        else:
                            if ret:
                                with ipio.capture_output() as (capt):
                                    print(('\r' + chunk), end='', flush=False)
                                    sys.stdout.flush()
                                out += capt.stdout.strip()
                            else:
                                print(('\r' + chunk), end='', flush=False)
                                sys.stdout.flush()
                else:
                    readx_out = select.select([proc.stdout.fileno()], [], [], 0.1)[0]
                    if readx_out:
                        chunk = proc.stdout.read().strip()
                        if chunk:
                            if cb_out:
                                cb_out(chunk)
                            else:
                                if ret:
                                    with ipio.capture_output() as (capt):
                                        print(chunk)
                                    out += capt.stdout.strip()
                                else:
                                    print(chunk)
                    else:
                        break

        return_code = proc.wait()
        chunk = proc.stdout.read().strip()
        if chunk:
            if cb_out:
                cb_out(chunk)
            else:
                if ret:
                    with ipio.capture_output() as (capt):
                        print(chunk)
                    out += capt.stdout.strip()
                else:
                    print(chunk)
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)
        if ret:
            return out

    def unzip(src, dest, options=''):
        count = 0
        try:
            count = int(Utils.run_cmd(['unzip -Z1 {} | wc -l'.format(src)], ret=True))
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        if count:
            out = tqdmn(range(count))
            lastupdate = datetime.now().timestamp()
            updates = 0

            def red_out(l):
                nonlocal updates
                keyword = [
                 'inflating:', 'extracting:']
                if any([k in l for k in keyword]):
                    founds = len([x for x in l.split('\n') if any([x.strip()[0:len(k)] == k for k in keyword])])
                    updates += max(1, founds)
                    if datetime.now().timestamp() - lastupdate > 1 or founds >= out.total - out.n:
                        out.update(max(1, updates))
                        updates = 0
                elif 'warning:' in l or 'error:' in l:
                    print(l)

            Utils.run_cmd(['unzip {} -o {} -d {}'.format(options, src, dest)], cb_err=red_out, cb_out=red_out)

    def zip(src, dest, options=''):
        count = len(glob(src))
        if count:
            out = tqdmn(range(count))
            lastupdate = datetime.now().timestamp()
            updates = 0

            def red_out(l):
                nonlocal updates
                keyword = 'adding:'
                if keyword in l:
                    founds = len([x for x in l.split('\n') if x.strip()[0:len(keyword)] == keyword])
                    updates += max(1, founds)
                    if datetime.now().timestamp() - lastupdate > 1 or founds >= out.total - out.n:
                        out.update(max(1, updates))
                        updates = 0
                elif 'warning:' in l or 'error:' in l:
                    print(l)

            Utils.run_cmd(['zip {} {} {}'.format(options, dest, src)], cb_err=red_out, cb_out=red_out)

    def highlight_corrects(c):
        s = ['']
        for x in c[1:]:
            s.append('background-color: yellowgreen; color: white;' if x == c.iloc[0] else '')

        return s

    def summary_print(currModel):
        ms = []
        currModel.summary(positions=[
         0.5, 0.75, 1.0, 0],
          line_length=200,
          print_fn=(lambda x: len(x.split('    ')) >= 3 and ms.append([a.strip() for a in list(filter(None, x.split('    ')))][0:3]) or False))
        ms = list(zip(*ms))
        len_dash = max([max([len(a) for a in x]) for x in ms])
        len_dash = len_dash + len_dash % 2
        delim_h = '\n' + '-' * (len_dash * (len(ms[0]) + 1)) + '\n'
        print('Total Params: {:n}\n'.format(sum([int(x) for x in ms[(-1)][1:]])) + delim_h + (delim_h.join(['{}'] * len(ms)).format)(*[(' '.join(['{:^' + str(len_dash) + '}'] * len(x)).format)(*x) for x in ms]) + delim_h)

    def fig_to_html(fig):
        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return HTML('<img src="data:image/png;base64, {}">'.format(base64.b64encode(img.getvalue()).decode('utf-8')))

    def crop_N_epochs(x, limit):
        return np.array([y[:limit] for y in x])

    def pad_N_epochs(x, limit):
        out = []
        for y in x:
            if len(y) < limit:
                tmp = np.concatenate([y, y[-(limit - len(y)):]])
                out.append(tmp)
            else:
                out.append(y[:limit])

        return np.array(out)