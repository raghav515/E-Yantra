'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			1067
# Author List:		Joel Jojo Painuthara, Raghavendra Pandurang Jadhav, Pooja M, Dhiren Bhandary
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy 
from  numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################


#####################################################################################

def perspective_transform(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = [] 
#################################  ADD YOUR CODE HERE  ###############################
    task_1b = __import__('task_1b')
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    try:
        ArUco_details_dict, ArUco_corners = task_1b.detect_ArUco_details(numpy.asarray(image))
        if 1 in ArUco_details_dict.keys() and 2 in ArUco_details_dict.keys() and 3 in ArUco_details_dict.keys() and 4 in ArUco_details_dict.keys():
            pts = [0,0,0,0]
            for ids, details in ArUco_details_dict.items():
                if ids<5:
                    pts[ids-1] = details[0]
            pts1 = numpy.float32(pts)
            pts2 = numpy.float32([[511,511],[0,511],[0,0],[511,0]])
            matrix = cv2.getPerspectiveTransform(pts1,pts2)
            warped_image = cv2.warpPerspective(image,matrix,(512,512))
    except:
        pass
######################################################################################

    return warped_image

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    try:
        task_1b = __import__('task_1b')
        ArUco_details_dict, ArUco_corners = task_1b.detect_ArUco_details(numpy.asarray(image))
        if 5 in ArUco_details_dict.keys():
            c_x = ArUco_details_dict[5][0][0]
            c_y = ArUco_details_dict[5][0][1]
            c_angle = ArUco_details_dict[5][1]
            c_x = interp(c_x,[0,511],[0.9550, -0.9550])
            c_y = interp(c_y,[0,511],[-0.9550, 0.9550])
            c_angle = c_angle-180 if 0<=c_angle<=180 else 180+c_angle
            scene_parameters = [c_x,c_y,c_angle]
    except:
        pass

######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################

    if(len(scene_parameters)==3):
        sim.setObjectPosition(aruco_handle,sim.handle_world,[scene_parameters[0],scene_parameters[1],0.1])
        sim.setObjectOrientation(aruco_handle,sim.handle_world,[0,0,scene_parameters[2]*numpy.pi/180])

######################################################################################

    return None

if __name__ == "__main__":
    client = RemoteAPIClient()  
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
    pre_warped_image = []
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ################################
    video = cv2.VideoCapture(2)
    while video.isOpened():
        ret, frame = video.read()
        warped_image = perspective_transform(frame)
        if len(pre_warped_image) != 0 or len(warped_image) != 0:
            if len(warped_image) == 0:
                warped_image = pre_warped_image
            else:
                pre_warped_image = warped_image
            scene_parameters = transform_values(pre_warped_image)
            set_values(scene_parameters)
        else:
            pass
        cv2.imshow("Frame",frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
########################################################################################