# BG removal for all images in the folder recursively

import cv2
from cv2 import dnn_superres
import sys
from pathlib import Path
import os

# Convert test_upscale.png to test_bgr_upscale.png
def create_dest_path(path):
    for i in range(len(path)-1, -1, -1):
        if path[i] == "_":
            return path[:i] + "_bgr" + path[i:]

bg_set = set()
bgr_set = set()

# A dictionary from image name to {src image path, dest image path}
bgr_dict = {}

# Find the images (upscaled only) that need a bg removal
for path in Path('../images').rglob('*upscale.png'):
    if "bgr" in path.name:
        bgr_set.add(path.name.replace("_bgr", ""))
    else:
        bg_set.add(path.name)
        bgr_dict[path.name] = {"src": "", "dest": ""}
        bgr_dict[path.name]["src"] = str(path.absolute())
        bgr_dict[path.name]["dest"] = create_dest_path(str(path.absolute()))

# Difference of the sets is the images that are not bg removed yet
to_be_bgr = bg_set - bgr_set

# print the length of to_be_bgr set
print("Number of images that need bgr", len(to_be_bgr))

# Print the to_be_bgr set
print("Images: ", to_be_bgr)

# BG removal for the images
for img_name in to_be_bgr:
    img_path = bgr_dict[img_name]["src"]
    print("BG removing: ", img_path)
    os.system("backgroundremover -i '{}' -o '{}'".format(img_path, bgr_dict[img_name]["dest"]))
    print("BG remove complete: ", img_path)
