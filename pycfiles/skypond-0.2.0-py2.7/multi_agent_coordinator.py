# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/base/multi_agent_coordinator.py
# Compiled at: 2019-05-07 01:08:19
from __future__ import absolute_import
import gym
from ..four_keys.four_keys_shared_state import FourKeysSharedState
from ..four_keys.four_keys_environment import FourKeysEnvironment
from .agent_http_proxy import AgentHTTPProxy
from .base_agent import Agent
from distutils.dir_util import copy_tree
import shutil, errno, docker, hashlib, time

class MultiAgentCoordinator(gym.Env):

    def __init__(self, game_type='four_keys', seed=None, gym_compatibility=True):
        self.game_type = game_type
        self.shared_state = None
        self.total_agents = 0
        self.agents = {}
        self.environments = {}
        self.successfully_loaded_media = []
        self.current_turn_agent_id = 0
        self.last_seed = seed
        self.image = 'upkoi/skypond-host:one'
        self.restrict_network = True
        self.image_network_whitelist = '172.17.0.1/8'
        self.debug_messages = False
        self.before_reset = None
        self.on_reset = None
        self.shuffle_starting_points = True
        self.gym_compatibility = gym_compatibility
        self.shared_state_initialization = dict()
        self.custom_reward = None
        self.agent_hash_salt = 'cw1tbfrGqImDeGZn3ZjHtz5bvAnyx1fDGhJJyw02Iq5wf39GqrCKdd97RLD7TYf'
        self.action_space = None
        self.observation_space = None
        self.start_new_game()
        if self.gym_compatibility:
            self.add_agent(None)
        return

    def debug(self, message):
        if self.debug_messages:
            print '[SKYPOND][Debug] ' + message

    def get_agent_verification_code(self, agent):
        description = agent.describe()
        name = description['username']
        result = hashlib.md5((self.agent_hash_salt + name).encode())
        return result.hexdigest()

    def get_agent_meta(self, agent_number):
        if agent_number + 1 > len(self.agents):
            raise Exception('Invalid agent number specified')
        return self.environments[agent_number].status

    def step(self, action):
        if not self.gym_compatibility:
            raise Exception('Not configured for gym compatibility - use process_turn() instead')
        primary_env = self.environments[0]
        primary_env.step(action)
        if self.total_agents > 0:
            for i in range(1, self.total_agents):
                env = self.environments[i]
                agent = self.agents[i]
                observation = None
                if not agent.blind:
                    observation, _, _, _ = env.observe()
                action = agent.react(observation)
                env.step(action)

        return primary_env.observe()

    def seed(self, seed=None):
        self.shared_state.seed(seed)

    def reset(self):
        if self.before_reset:
            self.before_reset(self)
        self.start_new_game()
        self.add_agent(None)
        if self.on_reset:
            self.on_reset(self)
        if self.gym_compatibility:
            self.environments[0].reset(reset_shared_state=False)
        return self.environments[0].generate_current_observation()

    def render(self, clear=True, label=''):
        self.environments[0].render(clear=clear, label=label)

    def start_new_game(self):
        self.shared_state = None
        self.total_agents = 0
        self.agents = {}
        self.environments = {}
        self.successfully_loaded_media = []
        if self.game_type == 'four_keys':
            self.shared_state = FourKeysSharedState(seed=self.last_seed, **self.shared_state_initialization)
        if self.shared_state is None:
            raise Exception('Unable to find target game')
        if self.shuffle_starting_points:
            self.shared_state.shuffle_starting_points()
        self.action_space = self.shared_state.action_space
        self.observation_space = self.shared_state.observation_space
        return self.shared_state.global_base_state

    def agent_exists_by_name(self, agent):
        new_agent_description = agent.describe()
        for existing_agent in self.agents.values():
            description = existing_agent.describe()
            if description['username'] == new_agent_description['username']:
                return True

        return False

    def copy_tree(src, dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                raise

    def add_isolated_agent(self, source_path, staging_path='/var/skypond/', reuse_loaded_instance=False, verification_callback=None):
        if source_path in self.successfully_loaded_media:
            return False
        else:
            name = 'skypond-host-' + str(self.total_agents)
            exposed_port = 5000 + self.total_agents
            client = docker.from_env()
            agent_staging_directory = staging_path + str(self.total_agents)
            if reuse_loaded_instance:
                try:
                    existing_instance = client.containers.get(name)
                    if existing_instance:
                        agent = AgentHTTPProxy('http://localhost:' + str(exposed_port))
                        self.add_agent(agent)
                        self.successfully_loaded_media.append(source_path)
                        return
                except:
                    None

            shutil.rmtree(agent_staging_directory, ignore_errors=True)
            copy_tree(source_path, agent_staging_directory)
            token = ''
            try:
                token_path = os.path.join(source_path, 'qualification.dat')
                if os.path.isfile(token_path):
                    with open(token_path, 'r') as (file):
                        token = file.read()
            except:
                None

            try:
                existing_instance = client.containers.get(name)
                if existing_instance:
                    self.debug('Existing Instance Found, Stopping...')
                    existing_instance.stop()
                    existing_instance.remove(force=True)
            except:
                None

            self.debug('Starting Container...')
            volumes_config = {}
            volumes_config[agent_staging_directory] = {'bind': '/mnt/agent', 'mode': 'ro'}
            capabilities = None
            if self.restrict_network:
                capabilities = 'NET_ADMIN'
            client.containers.run(self.image, name=name, cap_add=capabilities, environment=['ALLOWED_CIDR=' + self.image_network_whitelist], detach=True, mem_limit='256m', ports={'5000/tcp': exposed_port}, volumes=volumes_config)
            self.debug('Letting Docker Instance Warm Up...')
            time.sleep(3)
            self.debug('Starting Proxy Agent...')
            agent = AgentHTTPProxy('http://localhost:' + str(exposed_port))
            if verification_callback is not None:
                verification_result = verification_callback(agent, self, token)
                if not verification_result:
                    self.debug('Verification callback provided and verification failed. Not adding agent.')
                    return
            self.debug('Adding...')
            self.add_agent(agent)
            self.successfully_loaded_media.append(source_path)
            return agent

    def saved_env_with_name(self, name):
        for env_index in self.environments:
            if self.environments[env_index].status['name'] == name:
                return True

        return False

    def add_agent(self, agent):
        if agent is not None:
            agent_details = agent.describe()
        else:
            agent_details = None
        if self.game_type == 'four_keys':
            env = FourKeysEnvironment(self.shared_state, self.total_agents, details=agent_details)
            if not self.gym_compatibility:
                env.max_steps = 999999999999
        if self.total_agents >= 8:
            raise Exception('At maximum number of agents')
        if self.custom_reward is not None:
            env.custom_reward = self.custom_reward
        if not (self.total_agents == 0 and self.gym_compatibility):
            if not isinstance(agent, Agent):
                raise Exception('Agent must derive from skypond agent type')
            if agent in self.agents.values():
                raise Exception('Specific agent instance already added')
            if self.saved_env_with_name(env.status['name']):
                for i in range(8):
                    suffix = ' [%i]' % i + 1
                    name = env.status['name'] + suffix
                    if not self.saved_env_with_name(name):
                        env.status['name'] = name
                        break

            self.agents[self.total_agents] = agent
        self.environments[self.total_agents] = env
        self.total_agents += 1
        return

    def process_turn(self, visualize=False, build_status_response=False, visualization_label='', visualize_agent=0):
        if self.gym_compatibility:
            raise Exception('Configured for gym compatibility - use step() instead')
        env = self.environments[self.current_turn_agent_id]
        agent = self.agents[self.current_turn_agent_id]
        if not self.shared_state.any_agent_won:
            observation, _, _, _ = env.observe()
            action = 0
            try:
                action = agent.react(observation)
            except:
                self.debug('Failed to Get Reaction From Player %i:' % self.current_turn_agent_id)
                if self.debug_messages:
                    raise

            env.step(action)
            should_visualize = visualize and (visualize_agent is None or visualize_agent == self.current_turn_agent_id)
            if should_visualize:
                env.render(label=visualization_label)
        if self.current_turn_agent_id >= self.total_agents - 1:
            self.current_turn_agent_id = 0
        else:
            self.current_turn_agent_id += 1
        if build_status_response:
            return self.shared_state.get_status()
        else:
            return