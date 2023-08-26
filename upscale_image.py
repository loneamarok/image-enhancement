# This file can be used to upscale A PARTICULAR IMAGE image using the pretrained model

import cv2
from cv2 import dnn_superres
import sys

scaling_factor = int(sys.argv[1])
img_loc = sys.argv[2]

# Image name processing to get file name for loading and storing
img_name_split = img_loc.split(".")
img_type = img_name_split[-1]
img_name = img_loc[:-(len(img_type)+1)]

# print("img_name: ", img_name)
# print("img_type: ", img_type)

# Create an SR object
sr = cv2.dnn_superres.DnnSuperResImpl_create()

# Read Image 
# TODO change to reading all the changed directories and 
# Applying the process to the images newly added

image = cv2.imread(img_loc)

# Read the desired model
# TODO change the model based on 2x 3x 4x
path = "pretrained/EDSR_x{}.pb".format(str(scaling_factor))

sr.readModel(path)
sr.setModel("edsr", scaling_factor)

result = sr.upsample(image)

cv2.imwrite("{}_upscale{}.{}".format(img_name, scaling_factor, img_type), result)