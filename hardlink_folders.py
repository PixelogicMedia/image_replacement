import os
import re
import datetime
import logging


def handle_files(file_name, patch_dir, base_files, destination_dir):
    match = re.search(r'(\d{7})', file_name) 
    if match:
        file_suffix = match.group(1)
        file_path = os.path.join(patch_dir, file_name)

        corresponding_base_file = None
        for base_file in base_files:
            if file_suffix in base_file:
                corresponding_base_file = base_file
                break

        if corresponding_base_file:
            destination_file_path = os.path.join(destination_dir, corresponding_base_file)
            if os.path.exists(destination_file_path):
                print('Destination file exists, removing: %s', destination_file_path)
                os.remove(destination_file_path)
            os.link(file_path, destination_file_path)

def create_new_folder(base_tiff, patch_tiff, destination_parent):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination_folder = os.path.join(destination_parent, current_time)
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print('Folder created', destination_folder)

    folders_to_handle = ['TXTD','TXLS']

    for folder in folders_to_handle:
        base_dir = os.path.join(base_tiff, folder)
        print('The base directories handling now is', base_dir)
        patch_dir = os.path.join(patch_tiff, folder)
        print('The patch directories handling now is', patch_dir)
        destination_dir = os.path.join(destination_folder, folder)
        
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        base_files = os.listdir(base_dir)
        
        for base_file in base_files:
            base_file_path = os.path.join(base_dir, base_file)
            destination_file_path = os.path.join(destination_dir, base_file)
            os.link(base_file_path, destination_file_path)

        if os.path.exists(patch_dir):
            patch_files = os.listdir(patch_dir)
            for file_name in patch_files:
                handle_files(file_name, patch_dir, base_files, destination_dir)

    print(f"Folder {destination_folder} created with hardlinks to assets from BaseTIFF and PatchTIFF.")

Base_TIFF_Location = "./testfolders/BaseTIFF"
Patch_TIFF_Location = "./testfolders/PatchTIFF"
New_Folder_Location = "./testfolders"

create_new_folder(Base_TIFF_Location, Patch_TIFF_Location, New_Folder_Location)