import os
import shutil

def save_media(file_path, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    filename = os.path.basename(file_path)
    dest_path = os.path.join(dest_folder, filename)
    shutil.copy(file_path, dest_path)
    return dest_path
