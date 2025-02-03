# ThorLabs Camera class

# work in progress - this is not currently functional. Pavel -Oct 30 2024

#stages of an active camera:

# 1. Created SDK instance (TLCameraSDK). Allows use to create any # of parallel camera objects w/ attributed serial numbers
# 2. Creation of a TLCamera object w/ specific camera attributes ("opening")
# 3. "Arming" the camera (opening image buffer)
# Closing a camera session involves reversing this order. Disarm, dispose of camera, dispose of SDK session.

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import nidaqmx

os.add_dll_directory(r"C:\Program Files\Thorlabs\Scientific Imaging\Scientific Camera Support\Scientific Camera Interfaces\SDK\Python Toolkit\dlls\64_lib")

class Camera():

    def __init__(self,name):
        self.name = name
        self.sdk = TLCameraSDK()
        self.cam_list = self.sdk.discover_available_cameras()
        if len(self.cam_list) < 1:
            print("No cameras detected")
            exit()

    def open(self):
        self.camera = self.sdk.open_camera(self.cam_list[0]) #This is a "TLCamera" object

    def close(self):
        try:
            self.camera.dispose()
        finally:
            self.sdk.dispose()

    def disconnect_check(self):
        if self.sdk._is_sdk_open == True:
            self.sdk.dispose()

    def save_image(self,image_array, imgdir, filename):
        # Save the image to the specified filename
        path = imgdir+"/"+filename
        cv2.imwrite(path, image_array)
        print(f"Image saved. Path: {path}")

    def acquire_n_frames(self,frames=1,exp=1,gain=1,poll_TO=10000):
        # Configure camera settings
        with self.camera as camera:
            camera.exposure_time_us = int(exp*1e6) # Example exposure time, seconds (user defined) to microseconds (Thor input) conversion
            camera.gain = gain  # Example gain value
            camera.frames_per_trigger_zero_for_unlimited = frames  # Capture n frames
            camera.image_poll_timeout_ms = poll_TO  # 10-second polling timeout

            camera.arm(2)
            camera.issue_software_trigger()
            
            frame = camera.get_pending_frame_or_null()
            if frame is not None:
                print(f"Frame {frame.frame_count} received!")

                # Copy and reshape the image buffer
                image_buffer_copy = np.copy(frame.image_buffer)
                numpy_shaped_image = image_buffer_copy.reshape(camera.image_height_pixels, camera.image_width_pixels)
                # Convert to 3-channel for OpenCV
                nd_image_array = np.stack((numpy_shaped_image,) * 3, -1).astype(np.uint8)
                #lab_image = cv2.cvtColor(nd_image_array, cv2.COLOR_BGR2LAB)
                plt.imshow(nd_image_array)
                return nd_image_array
                
            else:
                try: #trying again just in case (sometimes frame isn't received)
                    camera.disarm()
                    
                    camera.arm(2)
                    camera.issue_software_trigger()
            
                    frame = camera.get_pending_frame_or_null()
                except:
                    print("Unable to acquire frame.")
                else:
                    print(f"Frame {frame.frame_count} received!")

                    # Copy and reshape the image buffer
                    image_buffer_copy = np.copy(frame.image_buffer)
                    numpy_shaped_image = image_buffer_copy.reshape(camera.image_height_pixels, camera.image_width_pixels)
                    # Convert to 3-channel for OpenCV
                    nd_image_array = np.stack((numpy_shaped_image,) * 3, -1).astype(np.uint8)
                    #lab_image = cv2.cvtColor(nd_image_array, cv2.COLOR_BGR2LAB)
                    plt.imshow(nd_image_array)
                    return nd_image_array
            
            camera.disarm()
        cv2.destroyAllWindows()

class Lamp:
    def __init__(self,name):
        self.name = name

    def on(self):
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan("Dev1/ao1",self.name,0,5)
            task.write(0.5,auto_start=True)

    def off(self):
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan("Dev1/ao1",self.name,0,5)
            task.write(5,auto_start=True)


#The way the code is handled now for each image taken, it needs:
# 1. a new camera definition
# 2. a separate opening, and 
# 3. closing at the end of a given "method". 
# 4. if your code errors out in an interactive window, 
#       <cam instance>.camera.dispose() AND/OR
#       <cam instance>.sdk.dispose() should clear it for the next run
#       without needing a "restart". If that doesn't work, restart!


# Testing/Demoing image capture:

# imgdir = './cam_output_test'
# imgname = 'imtest_00.jpg'

# cam1 = Camera("cam1") #Initiate a camera instance
# cam1.open()
# arr = cam1.acquire_n_frames(1,0.5) #1 frame with 0.5 s exposure
# cam1.close()
# plt.imshow(arr)
# plt.show()
# cam1.save_image(arr,imgdir,imgname)

# cam1 = Camera("cam1") #Initiate a camera instance
# cam1.open()
# arr2 = cam1.acquire_n_frames(1,1) #1 frame with 1 s exposure
# cam1.close() #close camera instance

# plt.imshow(arr2)
# plt.show()