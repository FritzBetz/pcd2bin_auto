## About ##
This project is a Fork from https://github.com/Yuseung-Na/pcd2bin

It includes requirements.txt for easier installation,

and batch converts .pcd files from a folder, if its name is given in `--pcg_path` arg,

automatically creates target folder in directory of script


This code is about .pcd to .bin converting tool.  
PointCloud(.pcd) file includes `x, y, z, intensity, (ring, time)` data.  
You can convert all the .pcd files (sorted in ascending order by file name) in the directory.  

## How to use ##
### 0. Environment ###
Tested with Python 3.12.4 , supports later version 

### 1. Install python libraries ###
`$ pip install -r requirements.txt` 

### 2. Launch python file ###
`$ python pcd2bin.py --pcd_path={path of input pcd directory}`

#### Parameters ####
|Name|Description|Default value|
|:---|:---|:---|
|pcd_path|.pcd file path|"/home/user/lidar_pcd"|
|bin_path|.bin file path|"/home/user/lidar_bin"|
|file_name|.bin file name|"file_name"|
