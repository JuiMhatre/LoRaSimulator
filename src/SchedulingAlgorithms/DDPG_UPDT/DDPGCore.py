import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from tensorflow.keras.layers import Lambda
import numpy as np
from SchedulingAlgorithms.DDPG_UPDT import parameters
from keras import backend as BK
import Utils as utils
import torch
from tensorflow.keras.layers import concatenate
class DDPGCore:
    def __init__(self, a_dim, s_dim, a_bound):
        self.memory = np.zeros((parameters.MEMORY_CAPACITY, int(s_dim * 2 + a_dim + 1)), dtype=np.float32)
        self.pointer = 0
        self.sess = tf.Session()

        self.a_dim, self.s_dim, self.a_bound = a_dim, s_dim, a_bound,
        self.S = tf.placeholder(tf.float32, [None, s_dim], 's')  
        self.S_ = tf.placeholder(tf.float32, [None, s_dim], 's_')
        self.R = tf.placeholder(tf.float32, [None, 1], 'r')

        with tf.variable_scope('Actor'):
            self.a = self._build_a(self.S, scope='eval', trainable=True)
            a_ = self._build_a(self.S_, scope='target', trainable=False)
        with tf.variable_scope('Critic'):
            # assign self.a = a in memory when calculating q for td_error,
            # otherwise the self.a is from Actor when updating Actor
            q = self._build_c(self.S, self.a, scope='eval', trainable=True)
            q_ = self._build_c(self.S_, a_, scope='target', trainable=False)

        self.ae_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Actor/eval')
        self.at_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Actor/target')
        self.ce_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Critic/eval')
        self.ct_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Critic/target')

        # target net replacement
        self.soft_replace = [tf.assign(t, (1 - parameters.TAU) * t + parameters.TAU * e)
                             for t, e in zip(self.at_params + self.ct_params, self.ae_params + self.ce_params)]

        q_target = self.R + parameters.GAMMA * q_
        # in the feed_dic for the td_error, the self.a should change to actions in memory
        td_error = tf.losses.mean_squared_error(labels=q_target, predictions=q)
        self.ctrain = tf.train.AdamOptimizer(parameters.LR_C).minimize(td_error, var_list=self.ce_params)

        a_loss = - tf.reduce_mean(q)  # maximize the q
        # self.atrain = tf.train.AdamOptimizer(parameters.LR_A).minimize(loss=CustomLossFunction(), var_list=self.ae_params)
        self.atrain = tf.train.AdamOptimizer(parameters.LR_A).minimize(a_loss, var_list=self.ae_params)

        self.sess.run(tf.global_variables_initializer())

    def rmse(self,ytrue, ypred):
        return BK.sqrt(BK.mean(BK.square(ypred-ytrue)))
    
    def choose_action(self, s):
        temp = self.sess.run(self.a, {self.S: s[np.newaxis, :]})
        return temp[0]

    def learn(self):
        self.sess.run(self.soft_replace)

        indices = np.random.choice(parameters.MEMORY_CAPACITY, size=parameters.BATCH_SIZE)
        bt = self.memory[indices, :]
        bs = bt[:, :self.s_dim]
        ba = bt[:, self.s_dim: self.s_dim + self.a_dim]
        br = bt[:, -self.s_dim - 1: -self.s_dim]
        bs_ = bt[:, -self.s_dim:]

        self.sess.run(self.atrain, {self.S: bs})
        self.sess.run(self.ctrain, {self.S: bs, self.a: ba, self.R: br, self.S_: bs_})

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, a, [r], s_))
        index = self.pointer % parameters.MEMORY_CAPACITY  # replace the old memory with new memory
        self.memory[index, :] = transition
        self.pointer += 1

    def _build_a(self, s, scope, trainable):
        with tf.variable_scope(scope):
            net = tf.layers.Dense(400, activation=tf.nn.relu6, name='l1', trainable=trainable)(s)
            net = tf.layers.Dense(300, activation=tf.nn.relu6, name='l2', trainable=trainable)(net)
            net = tf.layers.Dense(10, activation=tf.nn.relu, name='l3', trainable=trainable)(net)
            # a = tf.layers.Dense(self.a_dim, activation=tf.nn.tanh, name='a', trainable=trainable)(net)
            # a= tf.layers.Dense(self.a_dim, activation=self.clipactions,dynamic=True,trainable = trainable)(net)
            tx =tf.layers.Dense(self.a_dim/5, activation=mapping_to_target_range_TX)(net)
            cf =tf.layers.Dense(self.a_dim/5, activation=mapping_to_target_range_CF)(net)
            cr =tf.layers.Dense(self.a_dim/5, activation=mapping_to_target_range_CR)(net)    
            sf =tf.layers.Dense(self.a_dim/5, activation=mapping_to_target_range_SF)(net) 
            bw =tf.layers.Dense(self.a_dim/5, activation=mapping_to_target_range_BW)(net) 
            a= concatenate([tx, cf, cr,sf,bw])
            return tf.multiply(a, self.a_bound[1], name='scaled_a')
    
    def _build_c(self, s, a, scope, trainable):
        with tf.variable_scope(scope):
            n_l1 = 400
            w1_s = tf.get_variable('w1_s', [self.s_dim, n_l1], trainable=trainable)
            w1_a = tf.get_variable('w1_a', [self.a_dim, n_l1], trainable=trainable)
            b1 = tf.get_variable('b1', [1, n_l1], trainable=trainable)
            net = tf.nn.relu6(tf.matmul(s, w1_s) + tf.matmul(a, w1_a) + b1)
            net = tf.layers.Dense(300, activation=tf.nn.relu6, name='l2', trainable=trainable)(net)
            net = tf.layers.Dense( 10, activation=tf.nn.relu, name='l3', trainable=trainable)(net)
            return tf.layers.Dense(1, trainable=trainable)(net)  # Q(s,a)
    
def mapping_to_target_range_TX( x, target_min=0, target_max=14 ) :
    x02 = BK.tanh(x) + 1 # x in range(0,2)
    scale = ( target_max-target_min )/2.
    return  x02 * scale + target_min
def mapping_to_target_range_CF( x, target_min=0, target_max=71 ) :
    x02 = BK.tanh(x) + 1 # x in range(0,2)
    scale = ( target_max-target_min )/2.
    return  x02 * scale + target_min   
def mapping_to_target_range_CR( x, target_min=0, target_max=4 ) :
    x02 = BK.tanh(x) + 1 # x in range(0,2)
    scale = ( target_max-target_min )/2.
    return  x02 * scale + target_min    
def mapping_to_target_range_SF( x, target_min=0, target_max=5 ) :
    x02 = BK.tanh(x) + 1 # x in range(0,2)
    scale = ( target_max-target_min )/2.
    return  x02 * scale + target_min  
def mapping_to_target_range_BW( x, target_min=0, target_max=1 ) :
    x02 = BK.tanh(x) + 1 # x in range(0,2)
    scale = ( target_max-target_min )/2.
    return  x02 * scale + target_min 