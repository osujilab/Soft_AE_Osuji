##Chris Johnson##
##This set of functions is designed to use the "stage" class to perform more complex motions.
##This includes  moving through an array and going to specific positions as determined by calibratoin

import numpy as np
from stage_class import stage
import time

x = np.array([[1,2,3], [-2,-10,-30]])

def move_through_array(pos_array, stage):
    """Moving through a 2d array one by one. Array preferably np input"""
    for i in range(pos_array.shape[1]):
        stage.move_to(pos_array[0][i],pos_array[1][i])
        time.sleep(0.5) #This doesn't allow much room for doing other functions
        #Will probably just use move_to commands.
    
def move_to_camera(stage, camera_x, camera_y):
    """Explicitly defining the ability to move to a camera"""
    stage.move_to(camera_x,camera_y) #Just a simple command, but it's good to have this print.
    time.sleep(0.5)
    print("Stage now set in camera position.")

def move_to_flush(stage, flush_x, flush_y):
    """Explicitly defining the ability to move to the flush position."""
    stage.move_to(flush_x,flush_y)
    time.sleep(0.5)
    print("Stage now set in flush position.")


##TESTS##

jeff = stage('ASRL7::INSTR', 921600)
move_through_array(x, jeff)



flush_x = 0
flush_y = 50
camera_x=-40
camera_y=-5
move_to_flush(jeff, flush_x, flush_y)
move_to_camera(jeff, camera_x, camera_y)

jeff.stage_end()