#
# Module:       pcd2bin.py
# Description:  .pcd to .bin converter
#
# Author:       Yuseung Na (ys.na0220@gmail.com)
# Version:      1.1
#
# Revision History
#       January 19, 2021: Yuseung Na, Created
#       December 5, 2024: Friedrich Betz, Edited

import errno
import numpy as np
import os
import argparse
from pypcd_custom import *
import csv
from tqdm import tqdm

def main():
    ## Add parser
    parser = argparse.ArgumentParser(description="Convert .pcd to .bin")
    parser.add_argument(
        "--pcd_path",
        help="Folder path containing .pcd files.",
        type=str,
        default="/home/user/lidar_pcd"
    )

    args = parser.parse_args()

    ## Get the base folder name for the bin files
    pcd_folder_name = os.path.basename(os.path.normpath(args.pcd_path))
    
    ## Make bin folder under the current directory
    bin_path = os.path.join("./", pcd_folder_name)
    try:
        if not os.path.isdir(bin_path):
            os.makedirs(bin_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    ## Find all pcd files in the provided folder
    pcd_files = []
    for (path, dir, files) in os.walk(args.pcd_path):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.pcd':
                pcd_files.append(os.path.join(path, filename))

    ## Sort pcd files by file name
    pcd_files.sort()
    print("Finished loading point clouds!")

    ## Generate csv meta file
    csv_file_path = os.path.join(bin_path, "meta.csv")
    with open(csv_file_path, "w", newline="") as csv_file:
        meta_file = csv.writer(csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

        ## Write csv meta file header
        meta_file.writerow(["pcd file name", "bin file name"])
        print("Finished generating csv meta file")

        ## Converting Process
        print("Converting Start!")
        seq = 0
        for pcd_file in (pcd_files):
            ## Get pcd file
            pc = PointCloud.from_path(pcd_file)

            ## Generate bin file name
            bin_file_name = "{}_{:05d}.bin".format(os.path.splitext(os.path.basename(pcd_file))[0], seq)
            bin_file_path = os.path.join(bin_path, bin_file_name)

            ## Get data from pcd (x, y, z, intensity)
            np_x = np.array(pc.pc_data['x'], dtype=np.float32)
            np_y = np.array(pc.pc_data['y'], dtype=np.float32)
            np_z = np.array(pc.pc_data['z'], dtype=np.float32)
            np_i = np.array(pc.pc_data['intensity'], dtype=np.float32) / 256.0

            ## Stack all data
            points_32 = np.transpose(np.vstack((np_x, np_y, np_z, np_i)))

            ## Save bin file
            points_32.tofile(bin_file_path)

            ## Write csv meta file
            meta_file.writerow([os.path.split(pcd_file)[-1], bin_file_name])

            seq += 1

    print("Conversion Complete!")

if __name__ == "__main__":
    main()