# Upscale images in all the folders if not already

import cv2
from cv2 import dnn_superres
import sys
from pathlib import Path

# Convert test.img to test_upscale.img
def create_dest_path(path):
    for i in range(len(path)-1, -1, -1):
        if path[i] == ".":
            return path[:i] + "_upscale" + path[i:]

scaling_factor = int(sys.argv[1])

unscaled_set = set()
upscaled_set = set()

# A dictionary from image name to {src image path, dest image path}
unscaled_dict = {}

# Find the images that need an upscale image
for path in Path('../images').rglob('*.png'):
    if "upscale" in path.name:
        upscaled_set.add(path.name.replace("_upscale", ""))
    else:
        unscaled_set.add(path.name)
        unscaled_dict[path.name] = {"src": "", "dest": ""}
        unscaled_dict[path.name]["src"] = str(path.absolute())
        unscaled_dict[path.name]["dest"] = create_dest_path(str(path.absolute()))

# Difference of the sets is the images that are not scaled yet
to_be_scaled = unscaled_set - upscaled_set

# print the length of to_be_scaled set
print("Number of images to be scaled: ", len(to_be_scaled))

# Print the to_be_scaled set
print("Images: ", to_be_scaled)

# Upscale the images

# Create an SR object
sr = cv2.dnn_superres.DnnSuperResImpl_create()
path = "pretrained/EDSR_x{}.pb".format(str(scaling_factor))

sr.readModel(path)
sr.setModel("edsr", scaling_factor)

for img_name in to_be_scaled:
    img_path = unscaled_dict[img_name]["src"]
    print("Upscaling: ", img_path)
    image = cv2.imread(img_path)
    result = sr.upsample(image)
    cv2.imwrite(unscaled_dict[img_name]["dest"], result)
    print("Upscale complete: ", img_path)
