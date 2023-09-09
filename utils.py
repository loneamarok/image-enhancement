# All functions that manipulate images in different ways

import cv2
from cv2 import dnn_superres
import sys
from pathlib import Path
import global_functions as gf
import os
from PIL import Image, ImageDraw, ImageFilter

config = gf.load_configurations()

# Manipulate upscale images
def upscale_images(task_dict):
    scaling_factor = config["tasks"]["upscale"]["scaling_factor"]
    model_path = config["tasks"]["upscale"]["model_path"]
    model = config["tasks"]["upscale"]["model"]

    sr = cv2.dnn_superres.DnnSuperResImpl_create()

    sr.readModel(model_path)
    sr.setModel(model, scaling_factor)

    for img_name in task_dict.keys():
        img_path = task_dict[img_name]["src"]
        print("Upscaling: ", img_path)
        try:
            image = cv2.imread(img_path)
            result = sr.upsample(image)
            cv2.imwrite(task_dict[img_name]["dest"], result)
        except KeyboardInterrupt:
            print("Upscale of {} skipped".format(img_path))
            continue
        print("Upscale complete: ", task_dict[img_name]["dest"])

# Manipulate circle crop images
def circle_crop_images(task_dict):
    for img_name in task_dict.keys():
        img_path = task_dict[img_name]["src"]
        print("Cropping: ", img_path)
        image = Image.open(img_path)
        mask = Image.new('L', image.size)
        mask_draw = ImageDraw.Draw(mask)
        width, height = image.size
        mask_draw.ellipse((0, 0, width, height), fill=255)

        # add mask as alpha channel
        image.putalpha(mask)

        image.save(task_dict[img_name]["dest"])
        print("Crop complete: ", task_dict[img_name]["dest"])

# Manipulate background removal images
def bg_removal_images(task_dict):
    for img_name in task_dict.keys():
        img_path = task_dict[img_name]["src"]
        print("BG removing: ", img_path)
        os.system("backgroundremover -i '{}' -o '{}'".format(img_path, task_dict[img_name]["dest"]))
        print("BG remove complete: ", img_path)

# Manipulate images based onthe task
def manipulate_image(task, task_dict):
    if task == "upscale":
        upscale_images(task_dict)
    elif task == "crop_circle":
        circle_crop_images(task_dict)
    elif task == "bg_remove":
        bg_removal_images(task_dict)
    else:
        print("Not a valid task")
        exit()
