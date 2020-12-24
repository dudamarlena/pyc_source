# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/Actors/MCTSPlayer.py
# Compiled at: 2016-08-02 10:00:55
# Size of source mod 2**32: 10274 bytes
__doc__ = '\nThe Monte Carlo Tree Search player is a generic player, and can be used in games\nof incomplete information and with chance events.\n\nIt is based on the Monte Carlo Tree Search algorithm.\n'
import random, time, math
from ..GameBase import Actor

class TreeNode(object):
    """TreeNode"""

    def __init__(self, utility=None, simulations=0, parent=None, children=None):
        self.parent = parent
        self.simulations = simulations
        if not children:
            self.children = {}
        else:
            self.children = children
        if not utility:
            self.utility = []
        else:
            self.utility = utility

    def is_leaf():
        """True if this node is a leaf of the tree.

        Parameters
        ----------

        Returns
        -------
        is_leaf: Bool
            True if node is a leaf, False if node is not a leaf"""
        return len(self.children) == 0


class MCTSPlayer(Actor):
    """MCTSPlayer"""

    def __init__(self, exploration_exploitation=1.4, simulation_count=10000, simulation_time=90, verbose=False, verboseverbose=False):
        self.verbose = verbose
        self.verboseverbose = verboseverbose
        self.exploration_exploitation = exploration_exploitation
        self.simulation_count = simulation_count
        self.simulation_time = simulation_time

    def get_action(self, state):
        """Return the best action according to MCTS algorithm

        Parameters
        ----------
        state: State
            The state in which the actor must perform an action

        Returns
        -------
        action: Action
            Best action according to MCTS algorithm"""
        if len(state.get_legal_actions(self)) == 1:
            return state.get_legal_actions(self)[0]
        n_players = len(state.get_players())
        root = TreeNode(utility=[0 for player in range(n_players)], simulations=0)
        start_time = time.time()
        simulations = 0
        while True:
            out_of_simulations = simulations >= self.simulation_count
            out_of_time = time.time() - start_time >= self.simulation_time
            if out_of_simulations or out_of_time:
                break
            random_state = state.get_random(self)
            selected_node, selected_state, action = self.selection_phase(root, random_state)
            expanded_node, expanded_state = self.expansion_phase(selected_node, selected_state, action)
            utility = self.simulation_phase(expanded_state)
            self.backpropagation_phase(expanded_node, utility)
            simulations += 1

        most_simulations, action_with_most_simulations = (-1, None)
        for action, tree_node in root.children.items():
            if tree_node.simulations > most_simulations:
                most_simulations = tree_node.simulations
                action_with_most_simulations = action
                continue

        if self.verbose:
            print('[MCTS] Total number of simulations: {} in {} seconds'.format(str(simulations), time.time() - start_time))
            print('[MCTS] Possible action, average utility, simulations')
            for action, child in root.children.items():
                print('[MCTS] {}, {}, {}'.format(str(action), str(['{0:0.2f}'.format(u / child.simulations) for u in child.utility]), str(child.simulations)))

        return action_with_most_simulations

    def selection_phase(self, root_node, root_state):
        """The selection phase of the MCTS algorithm.

        This phase will analyse the constructed MCTS tree,
        use UCT to traverse down the tree, until a root node is reached.

        Parameters
        ----------
        root_node: TreeNode
            The root tree node from where to start selection phase
        root_state: State
            The State corresponding to the root_node

        Returns
        -------
        selected_node: TreeNode
            The node in the MCTS tree that needs to be expanded
        selected_state: State
            The State corresponding to selected_node
        action: Action
            The action by which the selected node should be expanded with"""
        players = root_state.get_players()
        current_node = root_node
        current_state = root_state
        current_action = None
        while 1:
            current_actor = current_state.get_actor()
            legal_actions = current_state.get_legal_actions(current_actor)
            for legal_action in legal_actions:
                children_str = [str(child) for child in current_node.children.keys()]
                if str(legal_action) not in children_str:
                    current_action = legal_action
                    return (
                     current_node, current_state, current_action)

            is_random_state = current_actor not in players
            if is_random_state:
                current_action = random.choice(legal_actions)
            else:
                current_player_index = players.index(current_actor)
                ntotal = current_node.simulations
                best_uct, best_action = -float('inf'), None
                for action, child_state in current_node.children.items():
                    ni = child_state.simulations
                    win_percentage = child_state.utility[current_player_index] / ni
                    confidence = math.sqrt(math.log(ntotal) / ni)
                    uct = win_percentage + self.exploration_exploitation * confidence
                    if uct > best_uct:
                        best_uct = uct
                        best_action = action
                        continue

                current_action = best_action
            current_node = current_node.children[current_action]
            current_state = current_action.execute(current_state)
            if current_state.is_final():
                return (
                 current_node, current_state, current_action)

    def expansion_phase(self, selected_node, selected_state, action):
        """The expansion phase of the MCTS algorithm.

        This expansion will add a node to the constructed MCTS tree,

        Parameters
        ----------
        selected_node: TreeNode
            The node which needs to be expanded
        selected_state: State
            The State corresponding to the selected_node
        action: Action
            The action by which the selected node needs to be expanded

        Returns
        -------
        expanded_node: TreeNode
            The new node added to the constructed MCTS tree
        expanded_state: State
            The State corresponding to expanded_node"""
        expanded_node = TreeNode(parent=selected_node, utility=[0 for _ in selected_state.get_players()])
        selected_node.children[action] = expanded_node
        expanded_state = action.execute(selected_state)
        return (
         expanded_node, expanded_state)

    def simulation_phase(self, expanded_state):
        """The simulation phase of the MCTS algorithm.

        This phase will simulate a random playout from a given state

        Parameters
        ----------
        expanded_state: State
            The state from where to start the random playout

        Returns
        -------
        utility: List
            The utility vector of the final state"""
        state = expanded_state
        while not state.is_final():
            actor = state.get_actor()
            actions = state.get_legal_actions(actor)
            action = random.choice(actions)
            if self.verboseverbose:
                print('[MCTS][simulation]: {}'.format(str(action)))
            state = action.execute(state)
            if self.verboseverbose:
                print(state.str(actor))
                continue

        return [state.get_utility(player) for player in state.get_players()]

    def backpropagation_phase(self, expanded_node, utility):
        """The backpropagation phase of the MCTS algorithm.

        This phase will update the constructed MCTS tree based on the
        utility vector from the simulation

        Parameters
        ----------
        expanded_node: TreeNode
            The node from where to start backpropagation
        utility: List<float>
            The utility vector from the simulation phase

        Returns
        -------"""
        node = expanded_node
        while node:
            node.simulations += 1
            node.utility = [old + new for old, new in zip(node.utility, utility)]
            node = node.parent

    def __str__(self):
        return 'MCTSPlayer'