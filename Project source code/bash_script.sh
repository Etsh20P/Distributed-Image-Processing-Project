#!/bin/bash

# Update package lists and upgrade the system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python3 and pip
sudo apt-get install python3-pip -y

# Upgrade pip to the latest version
sudo -H pip3 install --upgrade pip

# Install Boto3
sudo -H pip3 install boto3

# Install OpenCV dependencies
sudo apt-get install -y libsm6 libxext6 libxrender-dev

# Install OpenCV
sudo -H pip3 install opencv-python-headless

# Install OpenCL
sudo apt-get install -y python3-pyopencl

# Install MPI and MPICH
sudo apt-get install -y python3-mpi4py mpich

# Verify installation
python3 -c "import boto3; import cv2; import pyopencl; import mpi4py; print('Boto3 version:', boto3.__version__); print('OpenCV version:', cv2.__version__); print('PyOpenCL version:', pyopencl.VERSION_TEXT); print('MPI4Py version:', mpi4py.__version__)"
