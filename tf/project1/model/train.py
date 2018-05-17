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

for i in range(len(traffic_signs)):
    plt.subplot(1, 4, i+1)
    plt.axis('off')
    plt.imshow(images[traffic_signs[i]])
    plt.subplots_adjust(wspace=0.5)
    plt.show()
    print("shape: {0}, min: {1}, max: {2}".format(images[traffic_signs[i]].shape, images[traffic_signs[i]].min(), images[traffic_signs[i]].max()))



