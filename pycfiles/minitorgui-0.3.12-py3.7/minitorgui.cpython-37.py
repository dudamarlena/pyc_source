# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorgui/minitorgui/minitorgui.py
# Compiled at: 2020-03-06 15:30:18
# Size of source mod 2**32: 29159 bytes
"""
Main code for minitorgui.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import os, inspect, logging.config, threading, tkinter as tk
from tkinter.filedialog import askopenfilename
from dataclasses import dataclass
from time import sleep
from minitorcorelib import Configuration, StateManager, Heartbeat, start_application, BootstrapAgent, PortGenerator, TransferAgentFactory, MachineFactory, TunnelFactory
from minitorcorelib.minitorcorelibexceptions import InvalidConfigurationFile
from minitorgui.frames import InnerWindow, SubCommandWindow
from minitorgui.lib import setup_link, ConnectionVisualizer
from minitorgui.minitorguiexceptions import SetupFailed
from minitorgui.shapes import ClientShape, MachineShape, TunnelShape, AgentShape, AnimateConnection
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-12-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
LOGGER_BASENAME = 'minitorgui'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOCAL_HEARTBEAT_PORT = 11600
LOCAL_PROXY_PORT = 8080
LOCAL_TRANSFER_PORT = 11700
LOCAL_COMMAND_PORT = 11800
LOCAL_PROXYCHAINS_BINARY_FILE = '/usr/bin/proxychains4'
LOCAL_PROXYCHAINS_CONFIG_FILE = '/tmp/proxychains.conf'
MACHINE_DEPLOY_PATH = '/tmp/'
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
GENERIC_SCREEN_WIDTH = 1920

@dataclass
class CollectionShapes:
    __doc__ = 'Creates a data structure that enforces the order of specific objects.\n\n    This data structure enforces that each type of shape gets its\n    rightful position in the structure. The object is only used by\n    the ShapeGenerator, to improve readability of the code.\n    '
    client: ClientShape
    machine: MachineShape
    tunnel: TunnelShape
    agent: AgentShape


class LoggerMixin:
    __doc__ = 'Contains a logger method for use by other classes.'

    def __init__(self):
        """Initialize the LoggerMixin object."""
        logger_basename = 'minitorgui'
        self._logger = logging.getLogger(f"{logger_basename}.{self.__class__.__name__}")


class LoggingHandler(logging.Handler):
    __doc__ = 'A handler for sending logging events to LoggingWindow.\n\n    Handlers send the log records (created by loggers) to the appropriate destination.\n    In this case, it invokes the insert_log_line() of LoggingWindow and passes the\n    filtered message (for log level INFO) to be rendered on screen in the GUI.\n    '

    def __init__(self, main_window):
        super().__init__(level=(logging.INFO))
        self.logger = main_window.inner_window.log_window

    def emit(self, record):
        msg = self.format(record)
        self.logger.insert_log_line(msg)


def determine_scale(screen_width):
    """Sets the width of the application screen depending on type of screen."""
    if screen_width <= GENERIC_SCREEN_WIDTH:
        scale = 1
    else:
        scale = 2
    return scale


class MainWindow(tk.Tk, LoggerMixin):
    __doc__ = 'Represents mostly the main window of an application.'

    def __init__(self, *args, **kwargs):
        """______________."""
        (tk.Tk.__init__)(self, *args, **kwargs)
        LoggerMixin.__init__(self)
        self.scale = 0
        self._set_title_icon()
        self._set_size_window()
        self._create_menu()
        self._bind_to_event()
        self.path_config_file = None
        self.inner_window = InnerWindow(self, self.scale)
        self.inner_window.pack(side='top', fill='both', expand=True)
        self.inner_window.config(highlightthickness=2)
        self.set_scrollregion(init=True)
        self.should_terminate_minitor = False
        self.is_busy = False
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.configuration = None
        self.shape_generator = None

    def _determine_script_path(self):
        running_script = inspect.getframeinfo(inspect.currentframe()).filename
        running_script_dir = os.path.dirname(os.path.abspath(running_script))
        return running_script_dir

    def _set_title_icon(self):
        self.title('minitor')
        path_file = os.path.join(self._determine_script_path(), 'icon', 'application_icon_tunnel.png')
        img = tk.PhotoImage(file=path_file)
        self.iconphoto(True, img)

    def _set_size_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.scale = determine_scale(screen_width)
        win_width = WINDOW_WIDTH * self.scale
        win_height = WINDOW_HEIGHT * self.scale
        start_x = screen_width / 2 - win_width / 2
        start_y = screen_height / 2 - win_height / 2
        self.geometry('%dx%d+%d+%d' % (win_width, win_height, start_x, start_y))
        self.resizable(True, True)
        print('screen size is: %s x %s' % (screen_width, screen_height))
        print('window size: %s x %s' % (win_width, win_height))

    def _create_menu(self):
        self.option_add('*tearOff', False)
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar)
        run_menu = tk.Menu(menubar)
        quit_menu = tk.Menu(menubar)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=(self._config_file_dialog))
        file_menu.entryconfig('Open', accelerator='Ctrl+O')
        file_menu.add_command(label='Open Recent', command=(self._retrieve_recently_opened))
        file_menu.entryconfig('Open Recent', accelerator='Ctrl+T')
        menubar.add_cascade(label='Execution', menu=run_menu)
        run_menu.add_command(label='Run minitor', command=(self.run_minitor))
        run_menu.entryconfig('Run minitor', accelerator='Ctrl+R')
        run_menu.add_command(label='Stop minitor', command=(self.stop_minitor))
        run_menu.entryconfig('Stop minitor', accelerator='Ctrl+C')
        menubar.add_cascade(label='Quit', menu=quit_menu)
        quit_menu.add_command(label='Quit', command=(self.close_window))
        quit_menu.entryconfig('Quit', accelerator='Ctrl+Q')

    def _bind_to_event(self):
        self.bind('<Control-o>', lambda e: self._config_file_dialog())
        self.bind('<Control-t>', lambda e: self._retrieve_recently_opened())
        self.bind('<Control-r>', lambda e: self.run_minitor())
        self.bind('<Control-c>', lambda e: self.stop_minitor())
        self.bind('<Control-q>', lambda e: self.close_window())

    def set_scrollregion(self, init=False):
        """Sets a scroll region that encompasses all the shapes."""
        self.inner_window.canvas_window.canvas.update_idletasks()
        w_height = self.inner_window.canvas_window.canvas.winfo_height()
        w_width = self.inner_window.canvas_window.canvas.winfo_width()
        if init:
            self.inner_window.canvas_window.canvas.config(scrollregion=(0, 0, w_width, w_height))
        else:
            _, _, x_axis_2, _ = self.inner_window.canvas_window.canvas.bbox('all')
            if x_axis_2 <= w_width:
                self.inner_window.canvas_window.canvas.config(scrollregion=(0, 0, w_width, w_height))
            else:
                self.inner_window.canvas_window.canvas.config(scrollregion=(0, 0, x_axis_2 + 100, w_height))

    def _retrieve_recently_opened(self):
        if self.is_busy:
            return
        path_file_recent = os.path.join(self._determine_script_path(), 'settings', 'recently_opened_config_file')
        try:
            with open(path_file_recent) as (file):
                self.path_config_file = file.read().rstrip()
        except FileNotFoundError:
            return
        else:
            config_thread = threading.Thread(target=show_config_graphics, args=(self,))
            config_thread.start()

    def _write_to_recently_opened(self, path_config_file):
        path_file_recent = os.path.join(self._determine_script_path(), 'settings', 'recently_opened_config_file')
        with open(path_file_recent, 'w') as (file):
            file.write(path_config_file)

    def _config_file_dialog(self):
        if self.is_busy:
            return
        self.inner_window.canvas_window.canvas.delete('all')
        file_types = [('minitor config file', '*.json')]
        self.path_config_file = askopenfilename(filetypes=file_types)
        if self.path_config_file:
            config_thread = threading.Thread(target=show_config_graphics, args=(self,))
            config_thread.start()
            self._write_to_recently_opened(self.path_config_file)

    def run_minitor(self):
        """_________________."""
        if self.is_busy:
            return
        run_thread = threading.Thread(target=business_logic, args=(self,))
        run_thread.start()

    def stop_minitor(self):
        """Sets the should_terminate var to True.

        When the program, or rather, the business logic, is in
        FOR or TOR mode, it will run indefinitely. When the user
        hits ctrl + c, the window widget will capture the event,
        and sets the should_terminate to True. The business
        logic, polling this var, will break the loop, and
        dismantles the tunnel.

        Note: in COMMAND mode, the KeyboardInterrupt is passed
        from the widget to the logic, so no need for a
        polling mechanism.

        Note: in FILE mode, no need for KeyboardInterrupts.
        Once the files are transferred, the tunnel will be
        automatically dismantled.
        """
        self.should_terminate_minitor = True

    def close_window(self):
        """Closes the window when the business logic says so."""
        if not self.is_busy:
            self.should_terminate_minitor = True
            self.destroy()
        else:
            self._logger.info('*** window cannot be closed during setup and operation of tunnel ***')


class CommandWindow(tk.Toplevel):
    __doc__ = 'Represents a Toplevel widget, e.g. to have user input and show output.'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.scale = 0
        self.title('Interface')
        self._bind_to_event()
        self._is_return_pressed = False
        self._terminate = False
        self.protocol('WM_DELETE_WINDOW', self._terminate_window)
        self.sub_command_window = SubCommandWindow(self)
        self._set_size()

    def _bind_to_event(self):
        self.bind('<Return>', lambda e: self._return_pressed())
        self.bind('<Control-c>', lambda e: self._terminate_window())

    def _set_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.scale = determine_scale(screen_width)
        win_width = WINDOW_WIDTH * self.scale
        win_height = WINDOW_HEIGHT * self.scale
        start_x = screen_width / 2 - win_width / 2
        start_y = screen_height / 2 - win_height / 2
        self.geometry('%dx%d+%d+%d' % (win_width, win_height, start_x, start_y))
        self.resizable(True, True)

    def _return_pressed(self):
        self._is_return_pressed = True

    def _terminate_window(self):
        self._terminate = True

    def get_input(self):
        """Captures the input of the user and returns it."""
        while not self._is_return_pressed:
            if self._terminate:
                self.destroy()
                raise KeyboardInterrupt
            sleep(0.1)

        text = self.sub_command_window.command_entry.entry.get()
        self.sub_command_window.command_entry.entry.delete(0, 'end')
        self._is_return_pressed = False
        return text

    def show_response(self, line):
        """Shows the output sent by the Agent."""
        self.sub_command_window.command_response.text.insert('end', line + '\n')
        self.sub_command_window.command_response.text.see('end')


class ShapeGenerator(LoggerMixin):
    __doc__ = 'Gives out a new set of ports that setup_link() requires.'

    def __init__(self, main_window, configuration):
        super().__init__()
        self.main_window = main_window
        self.main_window.inner_window.canvas_window.canvas.delete('all')
        self.scale = main_window.scale
        self.iteration = 0
        self.quit = False
        self.shape_client = None
        self.shape_machines = []
        self.shape_tunnels = []
        self.shape_agents = []
        self._create_shapes(configuration)

    def _create_shapes(self, config_file):
        """Create all shapes and render only base shapes.

        The number of shapes are based on the total amount of Machines.
        All components (eg. Client, Machine, Agent, and Tunnel) are rendered, but hidden.
        The rendered instances can appear be invoking the show() method.

        Returns:
            A list containing shapes. Each type of shape has its own position:
            • element 0: client - the client is given an unique position on the X-axis
            • element 1: [machines] - each machine is given an unique position on the X-axis
            • element 2: [tunnels] - each tunnels is given its from and to destination
            • element 3: [agents] - each agent is a 'child' of the machine

        """
        start_y_pos = 60 * self.scale
        start_x_pos = 70 * self.scale
        amount_machines = len(config_file.proxies) + 1
        self.shape_client = ClientShape(self.main_window, start_x_pos, start_y_pos)
        self.shape_client.render()
        for i in range(amount_machines):
            start_x_pos += 220 * self.scale
            machine = MachineShape(self.main_window, start_x_pos, start_y_pos)
            machine.render()
            self.shape_machines.append(machine)
            if i == 0:
                tunnel = TunnelShape(self.main_window, self.shape_client, self.shape_machines[i])
                tunnel.render()
            else:
                tunnel = TunnelShape(self.main_window, self.shape_machines[(i - 1)], self.shape_machines[i])
                tunnel.render()
            self.shape_tunnels.append(tunnel)
            agent = AgentShape(self.main_window, self.shape_client, self.shape_machines[i])
            agent.render()
            self.shape_agents.append(agent)

    def show_landscape(self):
        """Shows the shapes of Client and Machine(s).

        Modifying the scroll region only works after the items
        have been changed ("configured") from hidden to normal.

        Note: A shape of Tunnel will be drawn when a Tunnel object
        is opened, this will not happen in this class.

        """
        sleep(0.5)
        self.shape_client.show()
        for machine in self.shape_machines:
            machine.show()
            sleep(0.25)

        self.main_window.set_scrollregion()

    def get_set_of_shapes(self):
        """Returns a set of shapes (other than client).

        The set contains with every invocation:
        - one (new) Machine
        - one (new) Tunnel
        - one (new) Agent

        Returns:
            A list that contains shapes.

        """
        shape_set = CollectionShapes(self.shape_client, self.shape_machines[self.iteration], self.shape_tunnels[self.iteration], self.shape_agents[self.iteration])
        self.iteration += 1
        return shape_set


def check_availability_linux_binaries():
    """Returns False or True depending on the availability of programs."""
    return True


def parse_config_file(config_file_path):
    """Parses the configuration file to a (dictionary) object."""
    try:
        configuration = Configuration(config_file_path)
    except InvalidConfigurationFile:
        return
    else:
        if configuration.mode == 'FILE':
            LOGGER.info('mode FILE enabled')
        else:
            if configuration.mode == 'COMMAND':
                LOGGER.info('mode COMMAND enabled')
            else:
                if configuration.mode == 'FOR':
                    LOGGER.info('mode FOR enabled')
                else:
                    if configuration.mode == 'TOR':
                        LOGGER.info('mode TOR enabled')
        return configuration


def get_configuration_file(main_window):
    """Retrieves the path from main window, parses the config file, and returns config object."""
    if not main_window.path_config_file:
        return
    else:
        configuration = parse_config_file(main_window.path_config_file)
        main_window.path_config_file = configuration or None
        return
    return configuration


def show_config_graphics(main_window):
    """Creates shapes and shows the landscape based on the config object in main window"""
    main_window.configuration = get_configuration_file(main_window)
    if not main_window.configuration:
        return
    main_window.shape_generator = ShapeGenerator(main_window, main_window.configuration)
    main_window.shape_generator.show_landscape()


def business_logic(main_window):
    """Executes the business logic.

    To be executed in a separate thread, to avoid interference
    with the widgets.
    """
    configuration = main_window.configuration
    if not configuration:
        return
    if not check_availability_linux_binaries():
        LOGGER.error('required packages not available. quitting.')
        main_window.after(200, main_window.destroy)
        return
    shape_generator = main_window.shape_generator
    shape_generator.shape_client.setup_ok()
    port_generator = PortGenerator()
    try:
        try:
            main_window.is_busy = True
            with StateManager() as (state):
                LOGGER.info('opening Tunnels and starting Machines...')
                for proxy in configuration.proxies:
                    ports = port_generator.get_next_port_ranges()
                    shapes = shape_generator.get_set_of_shapes()
                    transfer_agent = TransferAgentFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), ip_address_i=(proxy['ip_in']),
                      identity_file=(proxy['identity_file']),
                      machine_deploy_path=MACHINE_DEPLOY_PATH,
                      local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
                      local_proxychains_binary_path=LOCAL_PROXYCHAINS_BINARY_FILE)
                    tunnel = TunnelFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), local_agent_port=(ports['local_agent_port']),
                      count_connection=(ports['count_connection']),
                      ip_address_i=(proxy['ip_in']),
                      identity_file=(proxy['identity_file']),
                      local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
                      mode=None)
                    bootstrap_agent = BootstrapAgent(tunnel=tunnel, deploy_path=MACHINE_DEPLOY_PATH)
                    machine = MachineFactory(tunnel=tunnel, hostname=(proxy['hostname']),
                      ip_address_e=(proxy['ip_out']))
                    setup_link(state, transfer_agent, tunnel, bootstrap_agent, machine, shapes.machine, shapes.tunnel, shapes.agent)

                ports = port_generator.get_next_port_ranges()
                shapes = shape_generator.get_set_of_shapes()
                transfer_agent = TransferAgentFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), ip_address_i=(configuration.destination['ip_in']),
                  identity_file=(configuration.destination['identity_file']),
                  machine_deploy_path=MACHINE_DEPLOY_PATH,
                  local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
                  local_proxychains_binary_path=LOCAL_PROXYCHAINS_BINARY_FILE)
                tunnel = TunnelFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), local_agent_port=(ports['local_agent_port']),
                  count_connection=(ports['count_connection']),
                  ip_address_i=(configuration.destination['ip_in']),
                  identity_file=(configuration.destination['identity_file']),
                  local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
                  mode=(configuration.mode),
                  local_heartbeat_port=LOCAL_HEARTBEAT_PORT,
                  local_browser_port=LOCAL_PROXY_PORT,
                  local_transfer_port=LOCAL_TRANSFER_PORT,
                  local_command_port=LOCAL_COMMAND_PORT,
                  local_forward_connections=(configuration.forwarders_string))
                bootstrap_agent = BootstrapAgent(tunnel=tunnel, deploy_path=MACHINE_DEPLOY_PATH)
                machine = MachineFactory(tunnel=tunnel, hostname=(configuration.destination['hostname']),
                  mode=(configuration.mode),
                  ip_address_e=(configuration.destination['ip_out']),
                  transfer_port=LOCAL_TRANSFER_PORT,
                  command_port=LOCAL_COMMAND_PORT)
                setup_link(state, transfer_agent, tunnel, bootstrap_agent, machine, shapes.machine, shapes.tunnel, shapes.agent)
                if configuration.mode == 'FOR':
                    LOGGER.info('connections on local ports %s will be forwarded', configuration.forwarders_ports)
                else:
                    if configuration.mode == 'TOR':
                        LOGGER.info('local port %s will be listening for web traffic', LOCAL_PROXY_PORT)
                    else:
                        if configuration.mode == 'COMMAND':
                            shell_machine = machine
                        else:
                            if configuration.mode == 'FILE':
                                file_machine = machine
                with Heartbeat(LOCAL_HEARTBEAT_PORT) as (heartbeat):
                    LOGGER.info('encrypted tunnel established')
                    animate_connection = AnimateConnection(main_window, shapes.client, shapes.machine)
                    conn_visualizer = ConnectionVisualizer(animate_connection, heartbeat)
                    threading.Thread(target=(conn_visualizer.start)).start()
                    if configuration.application:
                        LOGGER.info('starting application...')
                        process = start_application(binary_name=(configuration.application['binary_name']), binary_location=(configuration.application['binary_location']))
                        while not main_window.should_terminate_minitor:
                            sleep(0.1)

                        process.terminate()
                    else:
                        if configuration.mode == 'COMMAND':
                            command_window = CommandWindow()
                            while True:
                                command = command_window.get_input()
                                response_raw = shell_machine.exec_command(command)
                                response_str = response_raw.decode('utf-8')
                                response_line = response_str.split('\n')
                                for line in response_line:
                                    command_window.show_response('>    %s' % line)

                        else:
                            if configuration.mode == 'FILE':
                                sleep(0.75)
                                file_machine.transfer(metadata_files=(configuration.files))
                            else:
                                while not main_window.should_terminate_minitor:
                                    sleep(0.1)

        except SetupFailed as msg:
            try:
                LOGGER.error(msg)
                raise SystemExit(1)
            finally:
                msg = None
                del msg

    finally:
        shapes.client.dim()
        sleep(3)
        main_window.after(200, main_window.destroy)


def main():
    """Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    main_window = MainWindow()
    logging_win_handler = LoggingHandler(main_window)
    logger = logging.getLogger()
    logger.addHandler(logging_win_handler)
    logger.setLevel(logging.DEBUG)
    main_window.mainloop()