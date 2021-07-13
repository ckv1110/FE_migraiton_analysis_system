import numpy as np


element_arr = []

skip = 0
element_left = 576
element_right = 432

# This process only picks the top layer, lower layers will need to -16 from previous layers
# At degree = 0, clockwise elements will decrease (-) by 4 and skip 36 every 4 elements passed. last element is 228
# Counterclockwise will start with a 36 skip before each element id is 4 above the previous and will skip by 36 after 4 elements passed.
# Last element in the counterclockwise rotation is 576


# Doing right side until 228 is reached
skip = 0
while skip < 5:
    counter = 0
    while counter < 3:
        counter += 1
        element_arr.append(element_right)
        mid_layer = element_right- 16
        element_arr.append(mid_layer)
        bot_layer = element_right - 32
        element_arr.append(bot_layer)
        element_right -= 4
    element_arr.append(element_right)
    mid_layer = element_right - 16
    element_arr.append(mid_layer)
    bot_layer = element_right - 32
    element_arr.append(bot_layer)
    element_right -= 36
    skip += 1


# Doing left side until 576 is reached
skip = 0
while skip < 3:
    counter = 0
    while counter < 3:
        counter += 1
        element_arr.append(element_left)
        mid_layer = element_left - 16
        element_arr.append(mid_layer)
        bot_layer = element_left - 32
        element_arr.append(bot_layer)
        element_left -= 4
    element_arr.append(element_left)
    mid_layer = element_left - 16
    element_arr.append(mid_layer)
    bot_layer = element_left - 32
    element_arr.append(bot_layer)
    element_left -= 36
    skip += 1



# Add middle layer and bottom layer respectively (-16 from layer above to get element)
# sub_counter = 0
# other_layer = []
# while sub_counter < len(element_arr):
#     mid_layer = element_arr[sub_counter] - 16
#     other_layer.append(mid_layer)
#     bot_layer = element_arr[sub_counter] - 32
#     other_layer.append(bot_layer)
#     sub_counter += 1
#
# sub_counter = 0
# while sub_counter < len(other_layer):
#     element_arr.append(other_layer[sub_counter])
#     sub_counter += 1

# print(len(element_arr))
np.savetxt('boundary_element_ids_ordered.txt', element_arr, delimiter=',', fmt='%3s')

