import os, datetime, re, argparse, json


def get_numbers(file_name):
    file_name_no_ext = os.path.splitext(file_name)[0]
    found = re.findall('\d+$', file_name_no_ext)
    if len(found) == 0:
        return ""
    digits = found[0]
    last_7_digits = digits[-7:]
    file_suffix = last_7_digits.zfill(7)
    return file_suffix

def handle_files(file_name, patch_dir, base_files, destination_dir):
    file_number = get_numbers(file_name)
    file_path = os.path.join(patch_dir, file_name)
    if base_files:
        corresponding_base_file = base_files[file_number] if file_number in base_files else None
    else:
        corresponding_base_file = file_name
        
    if corresponding_base_file:
        destination_file_path = os.path.join(destination_dir, corresponding_base_file)
        if os.path.exists(destination_file_path):
            os.remove(destination_file_path)
        os.link(file_path, destination_file_path)
        return 1
    return 0

def create_new_folder(base_tiff, patch_tiff, destination_parent,folders_to_handle):
    total_images = 0
    total_patched = 0
    if os.path.exists(destination_parent):
        i = 1
        while(os.path.exists(f'{destination_parent}_V{i}')):
            i += 1
        destination_folder = f'{destination_parent}_V{i}'
    else:
        destination_folder = destination_parent

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print('Folder created', destination_folder)

    for folder in folders_to_handle:
        base_dir = os.path.join(base_tiff, folder)
        patch_dir = os.path.join(patch_tiff, folder)
        destination_dir = os.path.join(destination_folder, folder)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        base_files_set = {}
        if os.path.exists(base_dir):
            base_files = os.listdir(base_dir)
            for files in base_files:
                base_files_set[get_numbers(files)] = files

            for base_file in base_files:
                base_file_path = os.path.join(base_dir, base_file)
                destination_file_path = os.path.join(destination_dir, base_file)
                total_images += 1
                os.link(base_file_path, destination_file_path)
            
        if os.path.exists(patch_dir):
            patch_files = os.listdir(patch_dir)
            for file_name in patch_files:
                total_patched += handle_files(file_name, patch_dir, base_files_set, destination_dir)

    print("|JSTART|"+json.dumps({"output": destination_folder, "totalmatched": "", "totalimages": total_images})+"|JEND|")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some TIFF files.")
    parser.add_argument("-b", "--base_tiff_location", type=str, default="./testfolders/BaseTIFF", help="Base TIFF location")
    parser.add_argument("-p", "--patch_tiff_location", type=str, default="./testfolders/PatchTIFF", help="Patch TIFF location")
    parser.add_argument("-n", "--new_folder_location", type=str, default="./testfolders", help="New folder location")

    args = parser.parse_args()

    create_new_folder(args.base_tiff_location, args.patch_tiff_location, args.new_folder_location, folders_to_handle=['TXTD','TXLS'])