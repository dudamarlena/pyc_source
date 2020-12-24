# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/player.py
# Compiled at: 2016-06-22 17:23:26
"""
对mplayer及其他播放器(TODO)的控制

    player = MPlayer()

方法:
    player.start(url)
    player.pause()
    player.quit()
    player.loop()
    player.set_volume(50)
    player.time_pos
    player.is_alive

queue自定义get_song方法, 从中取出url, 进行播放(暂时, 以后可以抽象)
    player.start_queue(queue)

如果需要更新,更换播放列表直接重复上面命令即可
    player.start_queue(queue)
"""
import subprocess, logging, signal, fcntl, time, abc, os
from threading import Thread, Event
logger = logging.getLogger('doubanfm.player')

class NotPlayingError(Exception):
    """对播放器操作但播放器未在运行"""
    pass


class PlayerUnavailableError(Exception):
    """该播放器在该系统上不存在"""
    pass


class Player(object):
    """所有播放器的抽象类"""
    __metaclass__ = abc.ABCMeta
    _player_command = ''
    _default_args = []
    _null_file = open(os.devnull, 'w')

    @abc.abstractmethod
    def __init__(self, default_volume=50):
        u"""初始化

        子类需要先判断该播放器是否可用（不可用则抛出异常），再调用该方法
        event: 传入的一个 Event ，用于通知播放完成
        default_volume: 默认音量
        """
        self.sub_proc = None
        self._args = [self._player_command] + self._default_args
        self._exit_event = Event()
        self._volume = default_volume
        return

    def __repr__(self):
        if self.is_alive:
            status = ('PID {0}').format(self.sub_proc.pid)
        else:
            status = 'not running'
        return ('<{0} ({1})>').format(self.__class__.__name__, status)

    def _run_player(self, extra_cmd):
        u"""
        运行播放器（若当前已有正在运行的，强制推出）

        extra_cmd: 额外的参数 (list)
        """
        if self.is_alive:
            self.quit()
        args = self._args + extra_cmd
        logger.debug('Exec: ' + (' ').join(args))
        self.sub_proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self._null_file, preexec_fn=os.setsid)
        flags = fcntl.fcntl(self.sub_proc.stdout, fcntl.F_GETFL)
        flags |= os.O_NONBLOCK
        fcntl.fcntl(self.sub_proc.stdout, fcntl.F_SETFL, flags)
        Thread(target=self._watchdog).start()

    def _watchdog(self):
        u"""
        监控正在运行的播放器（独立线程）

        播放器退出后将会设置 _exit_event
        """
        if not self.is_alive:
            logger.debug('Player has already terminated.')
            self._exit_event.set()
            return
        logger.debug('Watching %s[%d]', self._player_command, self.sub_proc.pid)
        returncode = self.sub_proc.wait()
        logger.debug('%s[%d] exit with code %d', self._player_command, self.sub_proc.pid, returncode)
        self._exit_event.set()

    @property
    def is_alive(self):
        u"""判断播放器是否正在运行"""
        if self.sub_proc is None:
            return False
        else:
            return self.sub_proc.poll() is None

    def quit(self):
        u"""退出播放器

        子类应当覆盖这个方法（但不强制），先尝试 gracefully exit ，再调用 super().quit()
        """
        if not self.is_alive:
            return
        self.sub_proc.terminate()

    @abc.abstractmethod
    def start(self, url):
        u"""开始播放

        url: 歌曲地址
        """
        pass

    @abc.abstractmethod
    def pause(self):
        u"""暂停播放"""
        pass

    @abc.abstractmethod
    def set_volume(self, volume):
        u"""设置音量

        volume: 音量 (int)"""
        self._volume = volume

    @abc.abstractproperty
    def time_pos(self):
        u"""获取当前播放时间

        返回播放时间的秒数 (int)"""
        pass


class MPlayer(Player):
    _player_command = 'mplayer'
    _default_args = [
     '-slave',
     '-nolirc',
     '-quiet',
     '-softvol',
     '-cache', '1024',
     '-cache-min', '0.1']

    def __init__(self, *args):
        super(MPlayer, self).__init__(*args)
        self._exit_queue_event = False
        self._loop = False
        self._pause = False
        self._time = 0

    def _watchdog_queue(self):
        self._exit_queue_event = True
        while self._exit_queue_event:
            if self._loop:
                self.start(self.queue.get_playingsong()['url'])
            else:
                self.start(self.queue.get_song()['url'])
            self.sub_proc.wait()

    def start_queue(self, queue, volume=None):
        self.queue = queue
        self._volume = volume if volume else self._volume
        if not self._exit_queue_event:
            Thread(target=self._watchdog_queue).start()
        else:
            try:
                self.sub_proc.terminate()
            except OSError:
                logger.info('wrong with start_queue')

    def loop(self):
        self._loop = False if self._loop else True

    def next(self):
        self.start_queue(self.queue, self._volume)

    def start(self, url):
        self._run_player(['-volume', str(self._volume), url])

    def pause(self):
        u"""
        pasue状态下如果取时间会使歌曲继续, 这里加了一个_pause状态
        """
        self._pause = False if self._pause else True
        self._send_command('pause')

    def quit(self):
        self._exit_queue_event = False
        if not self.is_alive:
            return
        try:
            os.killpg(os.getpgid(self.sub_proc.pid), signal.SIGKILL)
        except OSError:
            pass

    @property
    def time_pos(self):
        try:
            if self._pause:
                return self._time
            else:
                songtime = self._send_command('get_time_pos', 'ANS_TIME_POSITION')
                if songtime:
                    self._time = int(round(float(songtime)))
                    return self._time
                return 0

        except NotPlayingError:
            return 0

    def set_volume(self, volume):
        self._volume = volume
        self._send_command('volume %d 1' % volume)
        super(MPlayer, self).set_volume(volume)

    def _send_command(self, cmd, expect=None):
        """Send a command to MPlayer.

        cmd: the command string
        expect: expect the output starts with a certain string
        The result, if any, is returned as a string.
        """
        if not self.is_alive:
            raise NotPlayingError()
        logger.debug('Send command to mplayer: ' + cmd)
        cmd = cmd + '\n'
        try:
            self.sub_proc.stdin.write(cmd)
        except (TypeError, UnicodeEncodeError):
            self.sub_proc.stdin.write(cmd.encode('utf-8', 'ignore'))

        time.sleep(0.1)
        if not expect:
            return
        else:
            while True:
                try:
                    output = self.sub_proc.stdout.readline().rstrip()
                except IOError:
                    return

                split_output = output.split('=')
                if len(split_output) == 2 and split_output[0].strip() == expect:
                    value = split_output[1]
                    return value.strip()

            return