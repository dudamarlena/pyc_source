# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jackrecorder/recorder.py
# Compiled at: 2020-02-11 10:53:44
# Size of source mod 2**32: 8538 bytes
import jack, numpy as np, queue, soundfile as sf, sys, threading

def print_error(*args):
    print(*args, **{'file': sys.stderr})


def xrun(delay):
    print_error("An xrun occured, increase JACK's period size?")


def shutdown(status, reason):
    print_error('JACK shutdown!')
    print_error('status:', status)
    print_error('reason:', reason)
    event.set()


def recorder(ctrl_q, clientname, buffersize, n_tapes, manual, verbose):

    def stop_callback(msg=''):
        if msg:
            print_error(msg)
        for port in client.outports:
            port.get_array().fill(0)

        event.set()
        raise jack.CallbackExit

    def process(frames):
        if frames != blocksize:
            stop_callback('blocksize must not be changed, I quit!')
        monitor.get_buffer()[:] = input_line.get_buffer()
        for t, q in zip(tapes, play_q):
            try:
                pos_r, data_r = q.get_nowait()
            except queue.Empty:
                stop_callback('Buffer is empty: increase buffersize?')
            except TypeError:
                rec_q.put(None, timeout=timeout)
                stop_callback()

            t.get_array()[:] = data_r

        rec_q.put((pos_r + blocksize * buffersize, input_line.get_array()), timeout=timeout)

    def coordinator():
        pos_r = -1
        next_pos_r = 0
        selected = -1
        cmd = 'STOP'
        while 1:
            try:
                cmd = ctrl_q.get_nowait()
            except queue.Empty:
                pass

            if cmd is None:
                if verbose:
                    print('Coordinator incites the workers to kill JACK')
                for i in range(n_tapes):
                    sync_q[i].put(None, timeout=timeout)

                if verbose:
                    print('Wait for JACK to die')
                while rec_q.get() is not None:
                    pass

                if verbose:
                    print('Jack died')
                break
            else:
                selected = -1
                speed = 1
                pos_r = next_pos_r
                if cmd == 'STOP':
                    next_pos_r = 0
                    pos_r = -1
                else:
                    if cmd == 'PAUSE':
                        pos_r = -1
            if cmd[:3] == 'REC':
                selected = int(cmd[3:])
            else:
                if cmd[:3] == 'RWD':
                    speed = -float(cmd[3:])
                else:
                    if cmd[:3] == 'FWD':
                        speed = float(cmd[3:])
                    else:
                        try:
                            pos_w, data_w = rec_q.get_nowait()
                        except queue.Empty:
                            if verbose:
                                print('Jack → Coordinator empty')
                            pos_w = -1

                        for i in range(n_tapes):
                            if i == selected:
                                sync_q[i].put((speed, pos_r, pos_w, data_w), timeout=timeout)
                            else:
                                sync_q[i].put((speed, pos_r, -1, None), timeout=timeout)

                        if cmd == 'PLAY' or cmd[:3] == 'REC':
                            next_pos_r = pos_r + blocksize
            if cmd[:3] == 'RWD':
                next_pos_r = max(0, pos_r + int(speed * blocksize))
                if next_pos_r == 0:
                    cmd = 'STOP'
                elif cmd[:3] == 'FWD':
                    next_pos_r = pos_r + int(speed * blocksize)

    def worker(index, filename):
        with sf.SoundFile(filename, 'r+') as (f):
            while 1:
                try:
                    speed, pos_r, pos_w, data_w = sync_q[index].get()
                except queue.Empty:
                    if verbose:
                        print('sync_q: Coordinator → Worker', index, 'empty')
                    continue
                except TypeError:
                    break

                if pos_r < f.frames and pos_r >= 0 and pos_w < 0:
                    f.seek(pos_r)
                    direct = speed < 0
                    speed = abs(speed)
                    length = int(speed * blocksize)
                    data_r = f.read(length)
                    speed = len(data_r) / blocksize
                    sample = [int(i * speed) for i in range(blocksize)]
                    data_r = data_r[sample]
                    data_r = np.concatenate((data_r, silence[:blocksize - data_r.shape[0]]))
                    if direct:
                        data_r = data_r[::-1]
                    play_q[index].put((pos_r, data_r), timeout=timeout)
                else:
                    play_q[index].put((pos_r, silence), timeout=timeout)
                if pos_w >= 0:
                    f.seek(pos_w)
                    f.write(data_w)

            if verbose:
                print('Worker', index, 'stabbed JACK, ouch!')
            play_q[index].put(None, timeout=timeout)

    client = jack.Client(clientname)
    blocksize = client.blocksize
    samplerate = client.samplerate
    timeout = blocksize * buffersize / samplerate
    if verbose:
        print('blocksize', blocksize)
    if verbose:
        print('samplerate', samplerate)
    if verbose:
        print('buffersize', buffersize)
    if verbose:
        print('timeout', timeout)
    silence = np.zeros(blocksize)
    noise = np.random.rand(blocksize)
    client.set_shutdown_callback(shutdown)
    client.set_xrun_callback(xrun)
    client.set_process_callback(process)
    event = threading.Event()
    input_line = client.inports.register('input')
    monitor = client.outports.register('monitor')
    tapes = []
    for i in range(n_tapes):
        tapes.append(client.outports.register('output_' + str(i + 1)))

    sync_q = []
    for i in range(n_tapes):
        sync_q.append(queue.Queue(maxsize=buffersize))

    play_q = []
    for i in range(n_tapes):
        play_q.append(queue.Queue(maxsize=buffersize))

    rec_q = queue.Queue(maxsize=buffersize)
    for i in range(n_tapes):
        filename = str(i + 1) + '.wav'
        try:
            sf.SoundFile(filename, 'r')
        except:
            fp = sf.SoundFile(filename, 'w+', samplerate=samplerate, channels=1, format='WAV', subtype='FLOAT')
            fp.close()

    coordinator = threading.Thread(target=coordinator)
    workers = []
    for i in range(n_tapes):
        filename = str(i + 1) + '.wav'
        workers.append(threading.Thread(target=worker, args=(i, filename)))

    for _ in range(buffersize):
        rec_q.put((-1, silence))
        for i in range(n_tapes):
            play_q[i].put((-1, silence))

    client.activate()
    if not manual:
        client.connect('system:capture_1', clientname + ':input')
        for pan in ('1', '2'):
            client.connect(clientname + ':monitor', 'system:playback_' + pan)
            for i in range(n_tapes):
                client.connect(clientname + ':output_' + str(i + 1), 'system:playback_' + pan)

    coordinator.start()
    for i in range(n_tapes):
        workers[i].start()

    coordinator.join()
    for i in range(n_tapes):
        workers[i].join()

    client.deactivate()
    client.close()


class Recorder:

    def __init__(self, clientname, buffersize, n_tapes, manual, verbose):
        self.ctrl_q = queue.Queue(maxsize=buffersize)
        self.main = threading.Thread(target=recorder, args=(self.ctrl_q, clientname, buffersize, n_tapes, manual, verbose))

    def __enter__(self):
        self.main.start()
        return self

    def __exit__(self, *args):
        self.ctrl_q.put(None)
        self.main.join()

    def play(self):
        self.ctrl_q.put('PLAY')

    def stop(self):
        self.ctrl_q.put('STOP')

    def pause(self):
        self.ctrl_q.put('PAUSE')

    def record(self, tape):
        self.ctrl_q.put('REC' + tape)

    def forward(self, speed):
        self.ctrl_q.put('FWD' + speed)

    def backward(self, speed):
        ctrl_q.put('RWD' + speed)