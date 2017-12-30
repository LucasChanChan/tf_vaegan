import tensorflow as tf
from .tf_utils import variable_decorator

class ModuleBase(object):
  def __init__(self, learning_rate, dtype):
    self.optimizer = None
    self.learning_rate = learning_rate
    self.dtype = dtype

  def __call__(self, x, training, reuse=True):
    return self.net(x, training, reuse)

  def net(self, x, training, reuse):
    raise NotImplemented

class EncoderBase(ModuleBase):
  def __init__(self, latent_size, learning_rate, dtype=tf.float32):
    ModuleBase.__init__(self, learning_rate, dtype)
    self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
    self.latent_size = latent_size
    self.scope_name = 'enc'

  def __call__(self, x, training, reuse=True):
    with tf.variable_scope(self.scope_name, reuse=reuse):
      hidden = self.net(x, training, reuse)
      mu = tf.layers.dense(hidden, self.latent_size, name='mu')
      log_sigm_sq = tf.layers.dense(hidden, self.latent_size, name='log_sigm_sq')
      sigma = tf.sqrt(tf.exp(log_sigm_sq), name='sigma')
      eps = tf.random_normal(shape=tf.shape(sigma), name='epsilon')
      z = mu + sigma * eps
    return z, mu, sigma


class DecoderBase(ModuleBase):
  def __init__(self, learning_rate, dtype=tf.float32):
    ModuleBase.__init__(self, learning_rate, dtype)
    self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
    self.scope_name = 'dec'


class DiscriminatorBase(ModuleBase):
  def __init__(self, learning_rate, dtype=tf.float32):
    ModuleBase.__init__(self, learning_rate, dtype)
    self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
    self.scope_name = 'dis'