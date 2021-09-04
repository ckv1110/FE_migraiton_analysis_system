##IMPORTING_MODULES##
import tensorflow as tf
config = tf.compat.v1.ConfigProto(gpu_options=tf.compat.v1.GPUOptions(allow_growth=True))
sess = tf.compat.v1.Session(config=config)
import os
import numpy as np
from tqdm import tqdm
from skimage.io import imread, imshow
from skimage.transform import resize
from PIL import Image
from numpy import asarray
import cv2
from skimage.color import rgb2gray
import random
import matplotlib.pyplot as plt
import datetime

#END_OF_IMPORT##
# config = tf.config
# config.gpu_options.allow_growth = True
# session = tf.Session(config=config)


##INITIALIZE_GPU_AND_SET_GPU_MEM_LIMIT
# physical_devices = tf.config.list_physical_devices('GPU')
# try:
#   tf.config.experimental.set_memory_growth(physical_devices[0], True)
# except:
#   # Invalid device or cannot modify virtual devices once initialized.
#   pass
#try:
    #tf.config.experimental.set_virtual_device_configuration(physical_devices[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)]) ##Limit your GPU memory usage
#except RuntimeError as e:
    #print(e)

seed = 42
np.random.seed = seed

##WHAT_IS_YOUR_TRIAL_AND_DATE?
date_time = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
trial = "1_scratch_v2"

#DIMENSIONS_OF_IMAGE##
img_width = 512
img_height = 512
img_channels = 3

#TRAINING_AND_VAL_DIRECTORIES
training_path = 'train/'
test_path = 'test/'

#GETS_LISTS_SUBFOLDERS_FROM_TRAIN_AND_VAL_FOLDERS
train_ids = next(os.walk(training_path))[1]
train_ids.sort(key=int)
test_ids = [os.path.splitext(p)[0] for p in next(os.walk(test_path))[2]]
test_ids.sort

#CREATE_EMPTY_ARRAYS_TO_BE_FILLED_IN_AFTER_IMAGES_ARE_RESIZED
x_train = np.zeros((len(train_ids), img_width, img_height, img_channels), dtype=np.uint8)
y_train = np.zeros((len(train_ids), img_width, img_height, 1), dtype=np.bool)
# x_test = np.zeros((len(test_ids), img_width, img_height, img_channels), dtype=np.uint8)

print("Resizing raw and mask images...")
for n, id_ in tqdm(enumerate(train_ids), total=len(train_ids)):#len(train_ids)):
    path = os.path.join(training_path,id_)
    img = cv2.imread(path + '/raw.png')
    img = resize(img, (img_width, img_height), mode='constant', preserve_range=True)
    x_train[n] = img
    mask = cv2.imread(path + '/labeled.png')
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = np.expand_dims(resize(mask, (img_width, img_height), mode='constant', preserve_range=True), axis=-1)
    y_train[n] = mask
#number = random.randint(0,len(train_ids))
#imshow(x_train[number])
#plt.show()
#imshow(np.squeeze(y_train[number]))
#plt.show()
#exit(0)

# print("Resizing test images...")
# for n, id_ in tqdm(enumerate(test_ids), total=len(test_ids)):
#     test = cv2.imread(test_path + '/' + id_ + '.png')
#     test = resize(test, (img_width, img_height), mode='constant', preserve_range=True)
#     x_test[n] = test

# print("Done!")


#number = random.randint(0,len(train_ids))
#imshow(x_test[number])
#plt.show()

##START_OF_ARCHITECTURE## This architecture is the U-net architecture, refer to Olaf, Fischer and Brox's paper about it: https://link.springer.com/chapter/10.1007/978-3-319-24574-4_28
##INPUT_LAYER##
inputs = tf.keras.layers.Input((img_width, img_height, img_channels))
s = tf.keras.layers.Lambda(lambda x: x/255.0)(inputs) #Standardize the image pixel values between 0 and 1 for easier processing

##CONTRACTING_PATH## Refer to paper for architecture
c1 = tf.keras.layers.Conv2D(32, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
c1 = tf.keras.layers.Dropout(0.1)(c1)
c1 = tf.keras.layers.Conv2D(32, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
p1 = tf.keras.layers.MaxPooling2D((2,2))(c1)

c2 = tf.keras.layers.Conv2D(64, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
c2 = tf.keras.layers.Dropout(0.1)(c2)
c2 = tf.keras.layers.Conv2D(64, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
p2 = tf.keras.layers.MaxPooling2D((2,2))(c2)

c3 = tf.keras.layers.Conv2D(128, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
c3 = tf.keras.layers.Dropout(0.2)(c3)
c3 = tf.keras.layers.Conv2D(128, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
p3 = tf.keras.layers.MaxPooling2D((2,2))(c3)

c4 = tf.keras.layers.Conv2D(256, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
c4 = tf.keras.layers.Dropout(0.2)(c4)
c4 = tf.keras.layers.Conv2D(256, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
p4 = tf.keras.layers.MaxPooling2D((2,2))(c4)

c5 = tf.keras.layers.Conv2D(512, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
c5 = tf.keras.layers.Dropout(0.3)(c5)
c5 = tf.keras.layers.Conv2D(512, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

##EXPANSIVE_PATH##
u6 = tf.keras.layers.Conv2DTranspose(256, (2,2), strides=(2,2), padding='same')(c5)
u6 = tf.keras.layers.concatenate([u6, c4])
c6 = tf.keras.layers.Conv2D(256, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
c6 = tf.keras.layers.Dropout(0.2)(c6)
c6 = tf.keras.layers.Conv2D(256, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)

u7 = tf.keras.layers.Conv2DTranspose(128, (2,2), strides=(2,2), padding='same')(c6)
u7 = tf.keras.layers.concatenate([u7, c3])
c7 = tf.keras.layers.Conv2D(128, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
c7 = tf.keras.layers.Dropout(0.2)(c7)
c7 = tf.keras.layers.Conv2D(128, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)

u8 = tf.keras.layers.Conv2DTranspose(64, (2,2), strides=(2,2), padding='same')(c7)
u8 = tf.keras.layers.concatenate([u8, c2])
c8 = tf.keras.layers.Conv2D(64, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
c8 = tf.keras.layers.Dropout(0.1)(c8)
c8 = tf.keras.layers.Conv2D(64, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)

u9 = tf.keras.layers.Conv2DTranspose(32, (2,2), strides=(2,2), padding='same')(c8)
u9 = tf.keras.layers.concatenate([u9, c1])
c9 = tf.keras.layers.Conv2D(32, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
c9 = tf.keras.layers.Dropout(0.1)(c9)
c9 = tf.keras.layers.Conv2D(32, (3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)

outputs = tf.keras.layers.Conv2D(1, (1,1), activation='sigmoid')(c9)
##END_OF_ARCHITECTURE##

model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()


# model.fit(
#     x=None, y=None, batch_size=None, epochs=1, verbose=1, callbacks=None,
#     validation_split=0.0, validation_data=None, shuffle=True, class_weight=None,
#     sample_weight=None, initial_epoch=0, steps_per_epoch=None,
#     validation_steps=None, validation_batch_size=None, validation_freq=1,
#     max_queue_size=10, workers=1, use_multiprocessing=False
# )
#look at tf callbacks; provides good info how to figure how many epochs is best for you
#more info go to https://www.tensorflow.org/versions/r1.15/api_docs/python/tf (this is for r1.15, go to ur own tf version)

h5_name = "tumoursphere_" + date_time + "_Trial_" + trial + ".h5"
model_name = "U_net_" + date_time + "_Trial_" + trial + ".model"

##FITTING_THE_MODEL
checkpointer = tf.keras.callbacks.ModelCheckpoint(h5_name, verbose=1, save_best_only=True)
#('tumoursphere.h5', verbose=1, save_best_only=True)

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=5, monitor='val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='logs/{}'.format(model_name)),
    tf.keras.callbacks.ModelCheckpoint(h5_name, verbose=1, save_best_only=True)
 ]

results = model.fit(x_train, y_train, batch_size=4, epochs=100, validation_split=0.2, callbacks=callbacks)
model.save(model_name)