##IMPORTING_MODULES##
import tensorflow as tf
import os
import numpy as np
from tqdm import tqdm
from skimage.io import imshow
from skimage.transform import resize
import cv2
import random
import matplotlib.pyplot as plt
from PIL import Image

##WHAT_IS_YOUR_TRIAL_AND_DATE?
#date = "05062020"
#trial = "3"

#h5_name = "tumoursphere_" + date + "_Trial_" + trial + ".h5"
model_name = 'U_net_11-02-2021_18-06-26_Trial_1_scratch_v2.model'
name = 't115_scratch_uo_1'


# DIMENSIONS_OF_IMAGE##
img_width = 512
img_height = 512
img_channels = 3

physical_devices = tf.config.list_physical_devices('GPU')
try:
  tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
  # Invalid device or cannot modify virtual devices once initialized.
  pass

# TRAINING_AND_VAL_DIRECTORIES
training_path = 'train/'
test_path = name + '/'

# GETS_LISTS_SUBFOLDERS_FROM_TRAIN_AND_VAL_FOLDERS
train_ids = next(os.walk(training_path))[1]
train_ids.sort(key=int)
test_ids = [os.path.splitext(p)[0] for p in next(os.walk(test_path))[2]]
test_ids.sort

# CREATE_EMPTY_ARRAYS_TO_BE_FILLED_IN_AFTER_IMAGES_ARE_RESIZED
x_train = np.zeros((len(train_ids), img_width, img_height, img_channels), dtype=np.uint8)
y_train = np.zeros((len(train_ids), img_width, img_height, 1), dtype=np.bool)
x_test = np.zeros((len(test_ids), img_width, img_height, img_channels), dtype=np.uint8)

# print("Resizing raw and mask images...")
# for n, id_ in tqdm(enumerate(train_ids), total=len(train_ids)):
#     path = os.path.join(training_path, id_)
#     img = cv2.imread(path + '/raw.png')
#     img = resize(img, (img_width, img_height), mode='constant', preserve_range=True)
#     x_train[n] = img
#     mask = cv2.imread(path + '/labeled.png')
#     mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     mask = np.expand_dims(resize(mask, (img_width, img_height), mode='constant', preserve_range=True), axis=-1)
#     y_train[n] = mask


# number = random.randint(0,len(train_ids))
# imshow(x_train[number])
# plt.show()
# imshow(np.squeeze(y_train[number]))
# plt.show()
# exit(0)

print("Resizing test images...")
for n, id_ in tqdm(enumerate(test_ids), total=len(test_ids)):
    test = cv2.imread(test_path + '/' + id_ + '.png')
    test = resize(test, (img_width, img_height), mode='constant', preserve_range=True)
    x_test[n] = test

print("Done!")
# number = random.randint(0,len(train_ids))
# imshow(x_test[number])
# plt.show()

##LOAD_MODEL
model = tf.keras.models.load_model(model_name)

##PREDICT_STUFF
# preds_train = model.predict(x_train, verbose=1)
assert isinstance(model.predict, object)
preds_test = model.predict(x_test,batch_size=8, verbose=1)

# Each pixel is given a probability value of between 0 and 1.
# This will threshold hold predictions; anything above 0.5 will be binarized into image array and this will form our predicted mask image
# Threshold value of 0.5 seems to work the best
# preds_train_b = (preds_train > 0.5).astype(np.uint8)
preds_test_b = (preds_test > 0.5).astype(np.uint8)

test_num = len(preds_test_b)
print(test_num)
os.mkdir(os.path.join(os.getcwd(),name, "{}_predicted/".format(name)))


def make_predictions(set_path = os.path.join(os.getcwd(),name, "{}_predicted/".format(name)),i=1,count=0):
    while i <= test_num:
        # make the set_folder to put images in
        pred_img = preds_test_b[count] * 255
        #orig_img = x_test[count]
        pred_rsz = resize(pred_img, (1030, 1300), mode='constant', preserve_range=True)
        #cv2.imread(pred_rsz)
        cv2.imwrite(set_path + str(i) + "_predicted.png", pred_rsz)
        #cv2.imwrite(set_path + str(i) + "_raw.png", x_test)
        count += 1
        i += 1

make_predictions()

# Check training image 1
train1 = random.randint(0, len(preds_train) - 1) # max number minus 1 because python starts count at 0
# print(x_train[train1].shape)
cv2.imshow("%s_trained_raw" % train1, x_train[train1])
# plt.title("%s_trained_raw" %train1)
# plt.show()
#cv2.imshow("%s_trained_predicted" % train1, y_train[train1])
ytr1 = y_train[train1].astype(np.uint8) * 255 # multiply each pixel by 255 to get rid of the 0,1 boolean
cv2.imshow("%s_trained_boundary" % train1, ytr1)
#plt.title("%s_trained_boundary" %train1)
#plt.show()
tr1 = preds_train_b[train1] * 255  # multiply each pixel by 255 to get rid of the 0,1 boolean
cv2.imshow("%s_trained_predicted" % train1, tr1)
cv2.waitKey(0)
# imshow(np.squeeze(preds_train_b[train1]))
# plt.title("%s_trained_predicted" %train1)
# plt.show()


# Check training image 2
train2 = random.randint(0, len(preds_train) - 1)  # max number minus 1 because python starts count at 0
cv2.imshow("%s_trained_raw" % train2, x_train[train2])
#imshow(x_train[train2])
#plt.title("%s_trained_raw" % train2)
#plt.show()
ytr2 = y_train[train2].astype(np.uint8) * 255 # multiply each pixel by 255 to get rid of the 0,1 boolean
cv2.imshow("%s_trained_boundary" % train2, ytr2)
#imshow(np.squeeze(y_train[train2]))
#plt.title("%s_trained_boundary" % train2)
#plt.show()
tr2 = preds_train_b[train2] * 255
cv2.imshow("%s_trained_predicted" % train2, tr2)
cv2.waitKey(0)
#imshow(np.squeeze(preds_train_b[train2]))
#plt.title("%s_trained_predicted" % train2)
#plt.show()

# Do test 1
test1 = 71  #random.randint(0, len(preds_test) - 1)
real_num1 = test1 + 1
cv2.imshow("%s_testing_raw" % real_num1, x_test[test1])
#imshow(x_test[test1])
#plt.title("%s_test_raw" % test1)
#plt.show()
tst1 = preds_test_b[test1] * 255
cv2.imshow("%s_testing_predicted" % real_num1, tst1)
cv2.waitKey(0)
# pred_image = resize(preds_test_b[test1], (1030, 1300), mode='constant', preserve_range=True)
#imshow(np.squeeze(preds_test_b[test1]))
#plt.title("%s_test_predicted" % test1)
#plt.show()

# Do test 2
test2 = 3 #random.randint(0, len(preds_test) - 1)
real_num2 = test2 + 1
cv2.imshow("%s_testing_raw" % real_num2, x_test[test2])
#imshow(x_test[test2])
#plt.title("%s_test_raw" % test2)
#plt.show()
tst2 = preds_test_b[test2] * 255
cv2.imshow("%s_testing_predicted" % real_num2, tst2)
cv2.waitKey(0)
#imshow(np.squeeze(preds_test_b[test2]))
#plt.title("%s_test_predicted" % test2)
#plt.show()
