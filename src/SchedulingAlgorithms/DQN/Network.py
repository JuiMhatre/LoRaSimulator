import tensorflow as tf
import numpy as np

class Network(object):
    """Q-function approximator."""

    def __init__(self,
                 input_size,
                 output_size,
                 hidden_size=[50, 50],
                 weights_initializer=tf.initializers.glorot_uniform(),
                 bias_initializer=tf.initializers.zeros(),
                 optimizer=tf.optimizers.Adam,
                 **optimizer_kwargs):
        """Initialize weights and hyperparameters."""
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size

        np.random.seed(41)

        self.initialize_weights(weights_initializer, bias_initializer)
        self.optimizer = optimizer(**optimizer_kwargs)

    def initialize_weights(self, weights_initializer, bias_initializer):
        """Initialize and store weights."""
        wshapes = [
            [self.input_size, self.hidden_size[0]],
            [self.hidden_size[0], self.hidden_size[1]],
            [self.hidden_size[1], self.output_size]
        ]

        bshapes = [
            [1, self.hidden_size[0]],
            [1, self.hidden_size[1]],
            [1, self.output_size]
        ]

        self.weights = [init_weights(s, weights_initializer) for s in wshapes]
        self.biases = [init_weights(s, bias_initializer) for s in bshapes]

        self.trainable_variables = self.weights + self.biases

    def model(self, inputs):
        """Given a state vector, return the Q values of actions."""
        h1 = dense(inputs, self.weights[0], self.biases[0], tf.nn.relu)
        h2 = dense(h1, self.weights[1], self.biases[1], tf.nn.relu)

        out = dense(h2, self.weights[2], self.biases[2])

        return out

    def train_step(self, inputs, targets, actions_one_hot):
        """Update weights."""
        with tf.GradientTape() as tape:
            qvalues = tf.squeeze(self.model(inputs))
            preds = tf.reduce_sum(qvalues * actions_one_hot, axis=1)
            loss = tf.losses.mean_squared_error(targets, preds)

        grads = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

def dense(x, weights, bias, activation=tf.identity, **activation_kwargs):
    """Dense layer."""
    z = tf.matmul(x, weights) + bias
    return activation(z, **activation_kwargs)


def init_weights(shape, initializer):
    """Initialize weights for tensorflow layer."""
    weights = tf.Variable(
        initializer(shape),
        trainable=True,
        dtype=tf.float32
    )

    return weights