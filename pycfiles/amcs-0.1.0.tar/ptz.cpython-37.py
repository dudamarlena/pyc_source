# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/ptz.py
# Compiled at: 2020-01-12 12:29:08
# Size of source mod 2**32: 12033 bytes


class Ptz(object):

    @property
    def ptz_config(self):
        ret = self.command('configManager.cgi?action=getConfig&name=Ptz')
        return ret.content.decode('utf-8')

    @property
    def ptz_auto_movement(self):
        ret = self.command('configManager.cgi?action=getConfig&name=PtzAutoMovement')
        return ret.content.decode('utf-8')

    def ptz_presets_list(self, channel=0):
        ret = self.command('ptz.cgi?action=getPresets&channel={0}'.format(channel))
        return ret.content.decode('utf-8')

    @property
    def ptz_presets_count(self, channel=0):
        ret = self.ptz_presets_list()
        return ret.count('Name=')

    def ptz_status(self, channel=0):
        ret = self.command('ptz.cgi?action=getStatus&channel={0}'.format(channel))
        return ret.content.decode('utf-8')

    def ptz_tour_routines_list(self, channel=0):
        ret = self.command('configManager.cgi?action=getTours&channel={0}'.format(channel))
        return ret.content.decode('utf-8')

    def ptz_control_command(self, channel=0, action=None, code=None, arg1=None, arg2=None, arg3=None):
        if action is None:
            if code is None:
                if arg1 is None:
                    if arg2 is None:
                        if arg3 is None:
                            raise RuntimeError('code, arg1, arg2, arg3 is required!')
        ret = self.command('ptz.cgi?action={0}&channel={1}&code={2}&arg1={3}&arg2={4}&arg3={5}'.format(action, channel, code, arg1, arg2, arg3))
        return ret.content.decode('utf-8')

    def zoom_in(self, action=None, channel=0):
        """
        Params:
            action              - start or stop
            channel             - channel number

        The magic of zoom in 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=ZoomTele&arg1=0&arg2=0&arg3=0'.format(action, channel))
        return ret.content.decode('utf-8')

    def zoom_out(self, action=None, channel=0):
        """
        Params:
            action              - start or stop
            channel             - channel number

        The magic of zoom out 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=ZoomWide&arg1=0&arg2=0&arg3=0'.format(action, channel))
        return ret.content.decode('utf-8')

    def move_left(self, action=None, channel=0, vertical_speed=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            vertical_speed      - range 1-8

        The magic of move left 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=Left&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def move_right(self, action=None, channel=0, vertical_speed=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            vertical_speed      - range 1-8

        The magic of move right 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=Right&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def move_up(self, action=None, channel=0, vertical_speed=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            vertical_speed      - range 1-8

        The magic of move up 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=Up&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def move_down(self, action=None, channel=0, vertical_speed=1):
        """
        The magic of move down 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=Down&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def focus_near(self, action=None, channel=0):
        """
        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=FocusNear&arg1=0&arg2=0&arg3=0'.format(action, channel))
        return ret.content.decode('utf-8')

    def focus_far(self, action=None, channel=0):
        """
        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=FocusFar&arg1=0&arg2=0&arg3=0'.format(action, channel))
        return ret.content.decode('utf-8')

    def iris_large(self, action=None, channel=0):
        """
        Aperture larger

        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=IrisLarge&arg1=0&arg2=0&arg3=0'.format(action, channel))
        return ret.content.decode('utf-8')

    def iris_small(self, action=None, channel=0):
        """
        Aperture smaller

        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=IrisSmall&arg1=0&arg2=0&arg3=0'.format(action, channel))
        return ret.content.decode('utf-8')

    def go_to_preset(self, action=None, channel=0, preset_point_number=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            preset_point_number - preset point number
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=GotoPreset&arg1=0&arg2={2}&arg3=0'.format(action, channel, preset_point_number))
        return ret.content.decode('utf-8')

    def set_preset(self, action='start', channel=0, preset_point_number=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            preset_point_number - preset point number
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=SetPreset&arg1=0&arg2={2}&arg3=0'.format(action, channel, preset_point_number))
        return ret.content.decode('utf-8')

    def tour(self, action='start', channel=0, start=True, tour_path_number=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            start               - True (StartTour) or False (StopTour)
            tour_path_number    - tour path number
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code={2}Tour&arg1={3}&arg2=0&arg3=0&arg4=0'.format(action, channel, 'Start' if start else 'Stop', tour_path_number))
        return ret.content.decode('utf-8')

    def move_left_up(self, action=None, channel=0, vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=LeftUp&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def move_left_down(self, action=None, channel=0, vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=LeftDown&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def move_right_up(self, action=None, channel=0, vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=RightUp&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def move_right_down(self, action=None, channel=0, vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        ret = self.command('ptz.cgi?action={0}&channel={1}&code=RightDown&arg1=0&arg2={2}&arg3=0'.format(action, channel, vertical_speed))
        return ret.content.decode('utf-8')

    def move_directly--- This code section failed: ---

 L. 330         0  LOAD_FAST                'startpoint_x'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_TRUE     32  'to 32'
                8  LOAD_FAST                'startpoint_y'
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_TRUE     32  'to 32'

 L. 331        16  LOAD_FAST                'endpoint_x'
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  LOAD_FAST                'endpoint_y'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    40  'to 40'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            14  '14'
             32_2  COME_FROM             6  '6'

 L. 332        32  LOAD_GLOBAL              RuntimeError
               34  LOAD_STR                 'Required args, start_point_x, start_point_yend_point_x and end_point_y not speficied'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  ''
             40_0  COME_FROM            30  '30'

 L. 335        40  LOAD_FAST                'self'
               42  LOAD_METHOD              command

 L. 336        44  LOAD_STR                 'ptzBase.cgi?action=moveDirectly&channel={0}&startPoint[0]={1}&startPoint[1]={2}&endPoint[0]={3}&endPoint[1]={4}'
               46  LOAD_METHOD              format

 L. 338        48  LOAD_FAST                'channel'
               50  LOAD_FAST                'startpoint_x'
               52  LOAD_FAST                'startpoint_y'
               54  LOAD_FAST                'endpoint_x'
               56  LOAD_FAST                'endpoint_y'
               58  CALL_METHOD_5         5  ''
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'ret'

 L. 340        64  LOAD_FAST                'ret'
               66  LOAD_ATTR                content
               68  LOAD_METHOD              decode
               70  LOAD_STR                 'utf-8'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 40_0