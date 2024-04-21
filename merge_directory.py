# merge_directory.py
# Python 3.8.6

import os
import hashlib
from collections import defaultdict
import csv
import shutil

src_folder = "../.." # directory to Search 
folder_to_save = "/../../" # directory to copy (outside the src_folder) you have to put "/" after pat


def generate_md5(fname, chunk_size=1024):
    """
    Function which takes a file name and returns md5 checksum of the file
    """
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        # Read the 1st block of the file
        chunk = f.read(chunk_size)
        # Keep reading the file until the end and update hash
        while chunk:
            hash.update(chunk)
            chunk = f.read(chunk_size)

    # Return the hex checksum
    return hash.hexdigest()


if __name__ == "__main__":
    """
    Starting block of script
    """

    # The dict will have a list as values
    md5_dict = defaultdict(list)

    file_types_inscope = ["ppt", "pptx", "pdf", "txt", "html",
                          "mp4", "jpg", "png", "xls", "xlsx", "xml",
                          "vsd", "py", "json"]

    # Walk through all files and folders within directory
    for path, dirs, files in os.walk(src_folder):
        print("Analyzing {}".format(path))
        for each_file in files:
            if each_file.split(".")[-1].lower() in file_types_inscope:
                # The path variable gets updated for each subfolder
                file_path = os.path.join(os.path.abspath(path), each_file)
                # If there are more files with same checksum append to list
                md5_dict[generate_md5(file_path)].append(file_path)


    for key, val in md5_dict.items():
        head, tail = os.path.split(val[0])
        subdirname = os.path.basename(os.path.dirname(val[0]))
        newPath = shutil.copy(val[0], folder_to_save + subdirname + "_" + tail)

    print("Done")
