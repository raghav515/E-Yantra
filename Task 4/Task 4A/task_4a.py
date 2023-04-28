'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*
*  This script is intended for implementation of Task 4A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_4a.py
*  Created:
*  Last Modified:		02/01/2023
*  Author:				e-Yantra Team
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_4a.py
# Functions:		[ Comma separated list of functions in this file ]
# 					
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

##############################################################

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""

    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')  

    ####################### ADD YOUR CODE HERE #########################

    count = [0,0,0,0,0]
    for i in medicine_package_details:    
        objectHandle=sim.loadModel(packages_models_directory+"/"+i[1]+"_"+i[2]+".ttm")
        if i[0] == 'Shop_1':
            sim.setObjectPosition(objectHandle,arena,[-0.835+(count[0]*0.08),0.67,0.015])
            sim.setObjectParent(objectHandle,arena)
            sim.setObjectAlias(objectHandle,i[1]+"_"+i[2])
            count[0] = count[0] + 1
        elif i[0] == 'Shop_2':  
            sim.setObjectPosition(objectHandle,arena,[-0.4775+(count[1]*0.08),0.67,0.015])
            sim.setObjectParent(objectHandle,arena)
            sim.setObjectAlias(objectHandle,i[1]+"_"+i[2])
            count[1] = count[1] + 1
        elif i[0] == 'Shop_3':  
            sim.setObjectPosition(objectHandle,arena,[-0.120+(count[2]*0.08),0.67,0.015])
            sim.setObjectParent(objectHandle,arena)
            sim.setObjectAlias(objectHandle,i[1]+"_"+i[2])
            count[2] = count[2] + 1
        elif i[0] == 'Shop_4':  
            sim.setObjectPosition(objectHandle,arena,[0.2375+(count[3]*0.08),0.67,0.015])
            sim.setObjectParent(objectHandle,arena)
            sim.setObjectAlias(objectHandle,i[1]+"_"+i[2])
            count[3] = count[3] + 1
        elif i[0] == 'Shop_5':  
            sim.setObjectPosition(objectHandle,arena,[0.595+(count[4]*0.08),0.67,0.015])
            sim.setObjectParent(objectHandle,arena)
            sim.setObjectAlias(objectHandle,i[1]+"_"+i[2])
            count[4] = count[4] + 1
        else:
            sim.setObjectPosition(objectHandle,arena,[0,0,0.015])
            sim.setObjectParent(objectHandle,arena)
            sim.setObjectAlias(objectHandle,i[1]+"_"+i[2])
        all_models.append(objectHandle)
    
    ####################################################################

    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')   

    ####################### ADD YOUR CODE HERE #########################
        
    for i in traffic_signals:
        signal = sim.loadModel(traffic_sig_model)
        sim.setObjectPosition(signal,arena,[-0.895+((ord(i[0])-65)*0.3575),0.895-((int(i[1])-1)*0.3575),0.15588])   
        sim.setObjectParent(signal,arena)
        sim.setObjectAlias(signal,"Signal_"+i)
        all_models.append(signal) 

    ####################################################################

    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')   

    ####################### ADD YOUR CODE HERE #########################

    start = sim.loadModel(start_node_model)
    end = sim.loadModel(end_node_model)
    sim.setObjectPosition(start,arena,[-0.895+((ord(start_node[0])-65)*0.3575),0.895-((int(start_node[1])-1)*0.3575),0.15588])
    sim.setObjectPosition(end,arena,[-0.895+((ord(end_node[0])-65)*0.3575),0.895-((int(end_node[1])-1)*0.3575),0.15588])
    sim.setObjectParent(start,arena)
    sim.setObjectParent(end,arena)
    sim.setObjectAlias(start,"Start_Node")
    sim.setObjectAlias(end,"End_Node")
    all_models.append(start)
    all_models.append(end)
    
    ####################################################################

    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  

    ####################### ADD YOUR CODE HERE #########################
    for i in horizontal_roads_under_construction:
        barricade = sim.loadModel(horiz_barricade_model)
        sim.setObjectPosition(barricade,arena,[-0.895+(((ord(i[0])+ord(i[3]))/2-65)*0.3575),0.895-((int(i[1])-1)*0.3575),0.0225])  
        sim.setObjectParent(barricade,arena) 
        sim.setObjectAlias(barricade,"Horizontal_missing_road_"+i)
        all_models.append(barricade)
        
    ####################################################################

    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena') 

    ####################### ADD YOUR CODE HERE #########################
    for i in vertical_roads_under_construction:
        barricade = sim.loadModel(vert_barricade_model)
        sim.setObjectPosition(barricade,arena,[-0.895+((ord(i[0])-65)*0.3575),0.895-(((int(i[1])+int(i[4]))/2-1)*0.3575),0.0225])
        sim.setObjectParent(barricade,arena)
        sim.setObjectAlias(barricade,"Vertical_missing_road_"+i)
        all_models.append(barricade)  
    ####################################################################

    return all_models

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    # path directory of images in test_images folder
    img_dir = os.getcwd() + "/test_imgs/"
    i = 0
    config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

    print('\n============================================')
    print('\nFor maze_0.png')

    # object handles of each model that gets imported to the scene can be stored in this list
    # at the end of each test image, all the models will be removed    
    all_models = []

    # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
    task_1 = __import__('task_1a')
    detected_arena_parameters = task_1.detect_arena_parameters(config_img)

    # obtain required arena parameters
    medicine_package_details = detected_arena_parameters["medicine_packages"]
    traffic_signals = detected_arena_parameters['traffic_signals']
    start_node = detected_arena_parameters['start_node']
    end_node = detected_arena_parameters['end_node']
    horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
    vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

    print("[1] Setting up the scene in CoppeliaSim")
    all_models = place_packages(medicine_package_details, sim, all_models)
    all_models = place_traffic_signals(traffic_signals, sim, all_models)
    all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
    all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
    all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
    print("[2] Completed setting up the scene in CoppeliaSim")

    # wait for 10 seconds and then remove models
    time.sleep(10)
    print("[3] Removing models for maze_0.png")

    for i in all_models:
        sim.removeModel(i)

   
    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
    
    if choice == 'y':
        for i in range(1,5):

            print('\n============================================')
            print('\nFor maze_' + str(i) +'.png')
            config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

            # object handles of each model that gets imported to the scene can be stored in this list
            # at the end of each test image, all the models will be removed    
            all_models = []

            # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
            task_1 = __import__('task_1a')
            detected_arena_parameters = task_1.detect_arena_parameters(config_img)

            # obtain required arena parameters
            medicine_package_details = detected_arena_parameters["medicine_packages"]
            traffic_signals = detected_arena_parameters['traffic_signals']
            start_node = detected_arena_parameters['start_node']
            end_node = detected_arena_parameters['end_node']
            horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
            vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

            print("[1] Setting up the scene in CoppeliaSim")
            place_packages(medicine_package_details, sim, all_models)
            place_traffic_signals(traffic_signals, sim, all_models)
            place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
            place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
            place_start_end_nodes(start_node, end_node, sim, all_models)
            print("[2] Completed setting up the scene in CoppeliaSim")

            # wait for 10 seconds and then remove models
            time.sleep(10)
            print("[3] Removing models for maze_" + str(i) + '.png')
            for i in all_models:
                sim.removeModel(i)
            