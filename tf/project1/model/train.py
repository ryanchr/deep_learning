# python

import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import os as os
import skimage as skimage

from skimage import data  

#matplotlib.use('Agg')

config=tf.ConfigProto(log_device_placement=True)
config=tf.ConfigProto(allow_soft_placement=True)


def load_data(data_dir):
    dirs = [ d for d in os.listdir(data_dir)
             if os.path.isdir(os.path.join(data_dir, d))]
    labels = []
    images = []
    for d in dirs:
        label_dir = os.path.join(data_dir, d)
        file_names = [ os.path.join(label_dir, f)
                       for f in os.listdir(label_dir)
                       if f.endswith(".ppm") ]
        for f in file_names:
            images.append(skimage.data.imread(f))
            labels.append(int(d))
    return images, labels

ROOT_PATH = "../data/"
train_data_dir = os.path.join(ROOT_PATH, "Training")
test_data_dir = os.path.join(ROOT_PATH, "Testing")

images, labels = load_data(train_data_dir)

##histgram
'''
plt.hist(labels, 62)
plt.show()
plt.savefig('hist1.png')
'''

##visualize some images
traffic_signs = [300,2250,3650,4000]

'''
for i in range(len(traffic_signs)):
    plt.subplot(1,4,i+1)
    plt.axis('off')
    plt.imshow(images[traffic_signs[i]])
    plt.subplots_adjust(wspace=0.5)
'''

##plt.show()

#reshape the images

'''
for i in range(len(traffic_signs)):
    plt.subplot(1, 4, i+1)
    plt.axis('off')
    plt.imshow(images[traffic_signs[i]])
    plt.subplots_adjust(wspace=0.5)
    plt.show()
    print("shape: {0}, min: {1}, max: {2}".format(images[traffic_signs[i]].shape, images[traffic_signs[i]].min(), images[traffic_signs[i]].max()))
'''

## image transform
from skimage import transform

images28 = [transform.resize(image, (28,28)) for image in images]

'''
for i in range(len(traffic_signs)):
    plt.subplot(1, 4, i+1)
    plt.axis('off')
    plt.imshow(images[traffic_signs[i]])
    plt.subplots_adjust(wspace=0.5)
    plt.show()
    print("shape: {0}, min: {1}, max: {2}".format(images28[traffic_signs[i]].shape, images28[traffic_signs[i]].min(), images28[traffic_signs[i]].max()))
'''

## convert rgb to gray
from skimage.color import rgb2gray
import numpy as np

images28 = np.array(images28)
images28 = rgb2gray(images28)

# check gray images
'''
plt.subplot(1,1,1)
plt.axis('off')
plt.imshow(images28[traffic_signs[0]], cmap="gray")
plt.subplots_adjust(wspace=0.5)
plt.show()
'''

## implement the neural network
x = tf.placeholder(dtype = tf.float32, shape = [None,28,28])
y = tf.placeholder(dtype = tf.int32, shape = [None])

# Flatten the input data
images_flat = tf.contrib.layers.flatten(x)

# Fully connected layer
logits = tf.contrib.layers.fully_connected(images_flat, 62, tf.nn.relu)

# Define a loss function
loss =tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = y, logits = logits))

train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

#convert logits to label indexex
correct_pred = tf.argmax(logits, 1)

#define an accuracy metric
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

#check the code
'''
print("images_flat: ", images_flat)
print("logits: ", logits)
print("loss: ", loss)
print("predicated_labels: ", correct_pred)
'''

# train the network
tf.set_random_seed(1234)
sess = tf.Session()
sess.run(tf.global_variables_initializer())

for i in range(201):
    print('EPOCH', i)
    _, accuracy_val = sess.run([train_op, accuracy], feed_dict={x: images28, y: labels})
    if i % 10 == 0:
        print("Loss: ", loss)
    print('Done with epoch')


# Test the neural network
'''
import random

# pick 10 random images
sample_idx = random.sample(range(len(images28)), 10)
sample_images = [images28[i] for i in sample_idx]
sample_labels = [labels[i] for i in sample_idx]

# Run the "correct_pred" operation
predicted = sess.run([correct_pred], feed_dict={x:sample_images})[0]

print(sample_labels)
print(predicted)

# display the predictions and the ground truth
fig = plt.figure(figsize=(10,10))
for i in range(len(sample_images)):
    truth = sample_labels[i]
    prediction = predicted[i]
    plt.subplot(5,2,1+i)
    plt.axis('off')
    color='green' if truth == prediction else 'red'
    plt.text(40, 10, "Truth:  {0}\nPrediction: {1}".format(truth, prediction), fontsize=12, color=color)
    plt.imshow(sample_images[i], cmap="gray")

plt.show()
'''


### test all the test data

test_images, test_labels = load_data(test_data_dir)

print "test_images sizeL ", len(test_images)

test_images28 = [transform.resize(image, (28,28)) for image in test_images]

test_images28 = rgb2gray(np.array(test_images28))

predicted = sess.run([correct_pred], feed_dict={x: test_images28})[0]

print "size of predicted:", len(predicted)
print predicted[:50]

test_labels = [x for x in test_labels]

match_count = sum([int(y==y_) for y, y_ in zip(test_labels, predicted)])

print "match_count:", match_count

accuracy = match_count*1.0 / len(test_labels)

print("Accuracy: {:.3f}".format(accuracy))
print test_labels[:50]


# Exit the session
sess.close()


