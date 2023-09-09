# Code to manipulate images in all ways
# Upscale, circle_crop or background removal or any other manipulation
# Manipulation is done in 2 steps:
# 1. Create a dictionary of the images that need manipulation
# 2. Manipulate the images

import cv2
from cv2 import dnn_superres
import sys
from pathlib import Path
import global_functions as gf
import os
from utils import manipulate_image

def main():
    config = gf.load_configurations()
    gf.init_folders()

    # All the manipulation tasks have only 1 argument - Manipulation task.
    # The task args are given in the conf file

    task = sys.argv[1]

    # Exit if it is not a valid task
    if task not in config["tasks"].keys():
        print("Not a valid task")
        exit()

    # Get all the images that need manipulation
    # Images that are there in the prefolder that are not there in the postfolder
    prefolder = config["tasks"][task]["prefolder"]
    postfolder = config["tasks"][task]["postfolder"]

    # A dictionary from image name to {src image path, dest image path}
    task_dict = {}

    post_set = set()
    pre_set = set()

    # Loops through all the folders in the images root folder
    for folder in os.listdir(config["images_folder_root"]):
        d = os.path.join(config["images_folder_root"], folder)
        if os.path.isdir(d):
            # Get all the image names that are post
            post_dir = os.path.join(d, postfolder)
            for img in os.listdir(post_dir):
                post_set.add(img)

            # Get all the pre images. If the name not in post, add it for manipulation
            pre_dir = os.path.join(d, prefolder)
            for img in os.listdir(pre_dir):
                if img not in post_set:
                    task_dict[img] = {"src": os.path.join(pre_dir, img), "dest": os.path.join(post_dir, img)}
                    pre_set.add(img)

    # print the number of images to be manipulated
    print("Number of images to be manipulated: ", len(task_dict))

    # Print the image names to be manipulated
    print("Images: ", task_dict.keys())

    # Manipulate the images
    manipulate_image(task, task_dict)

if __name__ == "__main__":
    main()

