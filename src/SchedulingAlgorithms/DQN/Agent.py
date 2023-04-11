import numpy as np
import tensorflow as tf
import Network
import Memory
class Agent(object):
    """Deep Q-learning agent."""

    def __init__(self,
                 state_space_size,
                 action_space_size,
                 target_update_freq=1000,
                 discount=0.99,
                 batch_size=32,
                 max_explore=1,
                 min_explore=0.05,
                 anneal_rate=(1 / 100000),
                 replay_memory_size=100000,
                 replay_start_size=10000):
        """Set parameters, initialize network."""
        self.action_space_size = action_space_size

        self.online_network = Network(state_space_size, action_space_size)
        self.target_network = Network(state_space_size, action_space_size)

        self.update_target_network()

        # training parameters
        self.target_update_freq = target_update_freq
        self.discount = discount
        self.batch_size = batch_size

        # policy during learning
        self.max_explore = max_explore + (anneal_rate * replay_start_size)
        self.min_explore = min_explore
        self.anneal_rate = anneal_rate
        self.steps = 0

        # replay memory
        self.memory = Memory(replay_memory_size)
        self.replay_start_size = replay_start_size
        self.experience_replay = Memory(replay_memory_size)

    def handle_episode_start(self):
        self.last_state, self.last_action = None, None

    def step(self, observation, training=True):
        """Observe state and rewards, select action.
        It is assumed that `observation` will be an object with
        a `state` vector and a `reward` float or integer. The reward
        corresponds to the action taken in the previous step.
        """
        last_state, last_action = self.last_state, self.last_action
        last_reward = observation.reward
        state = observation.state

        action = self.policy(state, training)

        if training:
            self.steps += 1

            if last_state:
                experience = {
                    "state": last_state,
                    "action": last_action,
                    "reward": last_reward,
                    "next_state": state
                }

                self.memory.add(experience)

            if self.steps > self.replay_start_size:
                self.train_network()

                if self.steps % self.target_update_freq == 0:
                    self.update_target_network()

        self.last_state = state
        self.last_action = action

        return action

    def policy(self, state, training):
        """Epsilon-greedy policy for training, greedy policy otherwise."""
        explore_prob = self.max_explore - (self.steps * self.anneal_rate)
        explore = max(explore_prob, self.min_explore) > np.random.rand()

        if training and explore:
            action = np.random.randint(self.action_space_size)
        else:
            inputs = np.expand_dims(state, 0)
            qvalues = self.online_network.model(inputs)
            action = np.squeeze(np.argmax(qvalues, axis=-1))

        return action

    def update_target_network(self):
        """Update target network weights with current online network values."""
        variables = self.online_network.trainable_variables
        variables_copy = [tf.Variable(v) for v in variables]
        self.target_network.trainable_variables = variables_copy

    def train_network(self):
        """Update online network weights."""
        batch = self.memory.sample(self.batch_size)
        inputs = np.array([b["state"] for b in batch])
        actions = np.array([b["action"] for b in batch])
        rewards = np.array([b["reward"] for b in batch])
        next_inputs = np.array([b["next_state"] for b in batch])

        actions_one_hot = np.eye(self.action_space_size)[actions]

        next_qvalues = np.squeeze(self.target_network.model(next_inputs))
        targets = rewards + self.discount * np.amax(next_qvalues, axis=-1)

        self.online_network.train_step(inputs, targets, actions_one_hot)