# -*- encoding:utf-8 -*-

import tensorflow as tf
import numpy as np
import cv2
import tensorflow.python.platform
import sqlite3
import base64
import numpy as np

image_size = 28
image_pixel = image_size*image_size*3

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_integer('max_step',200,'step')
flags.DEFINE_integer('batch_size',10,'batch size')
flags.DEFINE_float('learning_rate',1e-4,'rate')

IntList = list
sqlite3.register_converter("IntList", lambda s: [str(i) for i in s.split(';')])
layer_level = 0

def inference(images_placeholder,keep_prob,num_classes):

  def weight_variable(shape):
    initial = tf.truncated_normal(shape,stddev=0.1)
    global layer_level
    layer_level += 1
    return tf.Variable(initial,name="weight"+str(layer_level))

  def bias_variable(shape):
    initial = tf.constant(0.1,shape=shape)
    return tf.Variable(initial,name="bias"+str(layer_level))

  def conv2d(x,w):
    return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='SAME')

  def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

  x_image = tf.reshape(images_placeholder,[-1,image_size,image_size,3])

  w_conv1 = weight_variable([5,5,3,32])
  b_conv1 = bias_variable([32])
  h_conv1 = tf.nn.relu(conv2d(x_image,w_conv1)+b_conv1)

  h_pool1 = max_pool_2x2(h_conv1)

  w_conv2 = weight_variable([5,5,32,64])
  b_conv2 = bias_variable([64])
  h_conv2 = tf.nn.relu(conv2d(h_pool1,w_conv2)+b_conv2)

  h_pool2 = max_pool_2x2(h_conv2)

  w_fc1 = weight_variable([7*7*64,1024])
  b_fc1 = bias_variable([1024])
  h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
  h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,w_fc1)+b_fc1)
  h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

  w_fc2 = weight_variable([1024,num_classes])
  b_fc2 = bias_variable([num_classes])
 
  y = tf.nn.softmax(tf.matmul(h_fc1_drop,w_fc2)+b_fc2)
  return y

def loss(logits,labels):
  cross_entropy = -tf.reduce_sum(labels*tf.log(logits))
  return cross_entropy

def training(loss,learning_rate):
  train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)
  return train_step

def accuracy(logits,labels):
  correct_prediction = tf.equal(tf.argmax(logits,1),tf.argmax(labels,1))
  acc = tf.reduce_mean(tf.cast(correct_prediction,'float'))
  return acc

if __name__ == '__main__':

  train_image = []
  train_label = []
  con = sqlite3.connect('face_and_learn.db',detect_types = sqlite3.PARSE_DECLTYPES)
  con.row_factory = sqlite3.Row
  c = con.cursor()
  result = c.execute('select*from dataset')
  num_classes = len(c.fetchall())
  #tmp = np.zeros(num_classes)
  result = c.execute('select*from dataset')
  debug_image = []
  for train_data in result:
    imgDate = train_data['data']
    #print "image data :" + str(len(imgDate)) + " name :" + train_data['name']
    for Img in imgDate:
      #print len(Img)
      imgBase = base64.decodestring(Img)
      image = np.asarray(bytearray(imgBase), dtype="uint8")
      image = cv2.imdecode(image, cv2.IMREAD_COLOR)
      debug_image.append(image)
      image = cv2.resize(image,(28,28))
      train_image.append(image.flatten().astype(np.float32)/255.0)
      tmp = np.zeros(num_classes)
      tmp[int(train_data['label'])] = 1
      train_label.append(tmp)
  con.close()
  train_image = np.asarray(train_image)
  train_label = np.asarray(train_label)

  images_placeholder = tf.placeholder('float',shape=(None,image_pixel))
  labels_placeholder = tf.placeholder('float',shape=(None,num_classes))
  keep_prob = tf.placeholder('float')

  logits = inference(images_placeholder,keep_prob,num_classes)
  loss_value = loss(logits,labels_placeholder)
  train_op = training(loss_value,FLAGS.learning_rate)
  acc = accuracy(logits,labels_placeholder)
  
  sess = tf.Session()
  saver = tf.train.Saver()
  sess.run(tf.initialize_all_variables())

  for step in range(10):
    for i in range(len(train_image)/FLAGS.batch_size):
      batch = FLAGS.batch_size*i
      sess.run(train_op,feed_dict={
        images_placeholder:train_image[batch:batch+FLAGS.batch_size],
        labels_placeholder:train_label[batch:batch+FLAGS.batch_size],
        keep_prob:0.5
      })

    print sess.run(acc,feed_dict={
      images_placeholder:train_image,
      labels_placeholder:train_label,
      keep_prob:1.0
    })

  saver_path = saver.save(sess,'Solaris_model.ckpt')
