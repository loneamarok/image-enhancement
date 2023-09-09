import json
import os

# Add all folder names here
ORIGINAL_FOLDER = "original"
UPSCALED_FOLDER = "upscaled"
CROP_CIRCLE_FOLDER = "crop_circle"
BG_REMOVED_FOLDER = "bg_removed"

FOLDER_LIST = [ORIGINAL_FOLDER, UPSCALED_FOLDER, CROP_CIRCLE_FOLDER, BG_REMOVED_FOLDER]

# Function to init all the images folders with the necessary subfolders
def init_folders():
    config = load_configurations()
    # Loop though all the folders in the root images folder
    for folder in os.listdir(config["images_folder_root"]):
        d = os.path.join(config["images_folder_root"], folder)
        if os.path.isdir(d):
            # Create the necessary subfolders if they don't exist
            subfolders = os.listdir(d)
            for folder_name in FOLDER_LIST:
                if folder_name not in subfolders:
                    os.mkdir(os.path.join(d, folder_name))
        
# Function to load configurations
def load_configurations():
    f = open("global.json")
    data = json.load(f)
    return data
