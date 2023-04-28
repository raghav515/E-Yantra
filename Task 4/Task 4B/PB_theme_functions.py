'''
*****************************************************************************************
*
*        		     ===============================================
*           		       Pharma Bot (PB) Theme (eYRC 2022-23)
*        		     ===============================================
*
*  This script contains all the past implemented functions of Pharma Bot (PB) Theme 
*  (eYRC 2022-23).
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			1067
# Author List:		Joel Jojo Painuthara, Raghavendra Pandurang Jadhav, Pooja M, Dhiren Bhandary
# Filename:			PB_theme_functions.py
# Functions:		
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
from zmqRemoteApi import RemoteAPIClient
import traceback
import zmq
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node and set it's value as edge value 
			Eg. : { "D3":{"C3":1, "E3":1, "D2":1, "D4":1}, 
					"D5":{"C5":1, "D2":1, "D6":1 }  }

			Why edge value 1? -->> since every road is equal

	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    

	paths = {}

	##############	ADD YOUR CODE HERE	##############
	
	mono = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	for i in range(0, 6):
		for j in range(0, 6):
			nodes = {}
			if j!=5 and mono[100+(100*(j+1)), 100+(100*i)] != 255 and mono[50+(100*(j+1)), 100+(100*i)] == 0:
				nodes[chr(65+i)+chr(49+j+1)] = 1
			if j!=0 and mono[100+(100*(j-1)), 100+(100*i)] != 255 and mono[150+(100*(j-1)), 100+(100*i)] == 0:
				nodes[chr(65+i)+chr(49+j-1)] = 1
			if i!=5 and mono[100+(100*j), 100+(100*(i+1))] != 255 and mono[100+(100*j), 50+(100*(i+1))] == 0:
				nodes[chr(65+i+1)+chr(49+j)] = 1
			if i!=0 and mono[100+(100*j), 100+(100*(i-1))] != 255 and mono[100+(100*j), 150+(100*(i-1))] == 0:
				nodes[chr(65+i-1)+chr(49+j)] = 1
			paths[chr(65+i)+chr(49+j)] = nodes

	##################################################

	return paths

def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	Input Arguments:
	---
	`graph` :	{ dictionary }
			dict of all connecting path
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	
	nodes = ['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6','C1','C2','C3','C4','C5','C6','D1','D2','D3','D4','D5','D6','E1','E2','E3','E4','E5','E6','F1','F2','F3','F4','F5','F6']
	unvisited = nodes.copy()
	dis = [999 for x in range(0,len(unvisited))]
	prev_node = ['' for x in range(0,len(unvisited))]
	dis[unvisited.index(start)] = 0
	prev_node[unvisited.index(start)] = start
	cur_node = start
	while len(unvisited)!=0:
		for i in graph[cur_node].keys():
			if i not in unvisited:
				continue
			ind = unvisited.index(i)
			ind_node = nodes.index(i)
			if dis[unvisited.index(cur_node)]+1 < dis[ind]: 
				dis[ind] = dis[unvisited.index(cur_node)] + 1
				prev_node[ind_node] = cur_node
		dis.remove(dis[unvisited.index(cur_node)])
		unvisited.remove(cur_node)
		if len(unvisited)==0:
			break
		cur_node = unvisited[dis.index(min(dis))] 
	cur_node = end
	while cur_node!=start:
		backtrace_path.append(cur_node)
		cur_node = prev_node[nodes.index(cur_node)]
	backtrace_path.append(start)
	backtrace_path.reverse()

	##################################################

	return backtrace_path

def paths_to_moves(paths, traffic_signal, orientation = 0):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]

	##############	ADD YOUR CODE HERE	##############
	
	for i in range(0,len(paths)-1):
		if paths[i][0] == paths[i+1][0]:
			if paths[i][1] > paths[i+1][1]:
				if orientation == 0:
					list_moves.append('STRAIGHT')
				elif orientation == 1:
					list_moves.append('LEFT')
				elif orientation == 2:
					list_moves.append('REVERSE')
				elif orientation == 3:
					list_moves.append('RIGHT')
				orientation = 0
			elif paths[i][1] < paths[i+1][1]:
				if orientation == 0:
					list_moves.append('REVERSE')
				elif orientation == 1:
					list_moves.append('RIGHT')
				elif orientation == 2:
					list_moves.append('STRAIGHT')
				elif orientation == 3:
					list_moves.append('LEFT')
				orientation = 2
		elif paths[i][1] == paths[i+1][1]:
			if paths[i][0] < paths[i+1][0]:
				if orientation == 0:
					list_moves.append('RIGHT')
				elif orientation == 1:
					list_moves.append('STRAIGHT')
				elif orientation == 2:
					list_moves.append('LEFT')
				elif orientation == 3:
					list_moves.append('REVERSE')
				orientation = 1
			elif paths[i][0] > paths[i+1][0]:
				if orientation == 0:
					list_moves.append('LEFT')
				elif orientation == 1:
					list_moves.append('REVERSE')
				elif orientation == 2:
					list_moves.append('RIGHT')
				elif orientation == 3:
					list_moves.append('STRAIGHT')
				orientation = 3
		if paths[i+1] in traffic_signal:
			list_moves.append('WAIT_5')

	##################################################

	return list_moves, orientation

def detect_ArUco_details(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the id of the ArUco marker is the key and a list of details of the marker
    is the value for each item in the dictionary. The list of details include the following
    parameters as the items in the given order
        [center co-ordinates, angle from the vertical, list of corner co-ordinates] 
    This order should be strictly maintained in the output

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `ArUco_details_dict` : { dictionary }
            dictionary containing the details regarding the ArUco marker
    
    Example call:
    ---
    ArUco_details_dict = detect_ArUco_details(image)
    """    
    ArUco_details_dict = {} #should be sorted in ascending order of ids
    ArUco_corners = {}
    
    ##############	ADD YOUR CODE HERE	##############

    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,parameters=arucoParams)
    ArUco_D = {}
    Corners = {}
    for i in range(len(ids)):
        sumx,sumy = 0,0
        co = []
        for j in range(4):
            sumx = sumx + corners[i][0][j][0]
            sumy = sumy + corners[i][0][j][1]
            temp = [corners[i][0][j][0],corners[i][0][j][1]]
            co.append(temp)
        mid = [int(sumx/4),int(sumy/4)]
        diffy = corners[i][0][0][1] - corners[i][0][3][1]
        diffx = corners[i][0][0][0] - corners[i][0][3][0]
        orient =int((np.arctan2(diffx,-1*diffy)*180)/np.pi)
        orient = -1 * orient
        ArUco_D[int(ids[i][0])] = [mid,orient]
        Corners[int(ids[i][0])] = co
    for i in sorted(ArUco_D.keys()):
        ArUco_details_dict[i] = ArUco_D[i]
        ArUco_corners[i] = Corners[i]
   
    ##################################################
    
    return ArUco_details_dict, ArUco_corners 

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

	###############  ADD YOUR CODE HERE  ######################
    
    try:
        ArUco_details_dict, ArUco_corners = detect_ArUco_details(np.asarray(image))
        Aruco_Corner_Keys = list(ArUco_corners.keys())
        if 1 in Aruco_Corner_Keys and 2 in Aruco_Corner_Keys and 3 in Aruco_Corner_Keys and 4 in Aruco_Corner_Keys:
            pts = [0,0,0,0]
            for ids, details in ArUco_corners.items():
                if ids<5:
                    pts[ids-1] = details[(ids+1)%4]
                    if ids == 1:
                        pts[ids-1][0] += 10
                        pts[ids-1][1] += 10
                    elif ids == 2:
                        pts[ids-1][0] -= 10
                        pts[ids-1][1] += 10
                    elif ids == 3:
                        pts[ids-1][0] -= 10
                        pts[ids-1][1] -= 10
                    elif ids == 4:
                        pts[ids-1][0] += 10
                        pts[ids-1][1] -= 10    
            print(pts)
            pts1 = np.float32(pts)
            pts2 = np.float32([[511,511],[0,511],[0,0],[511,0]])
            matrix = cv2.getPerspectiveTransform(pts1,pts2)
            warped_image = cv2.warpPerspective(image,matrix,(512,512))
            cv2.imshow("Warp",warped_image)
    except:
        pass
	###########################################

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

	#################  ADD YOUR CODE HERE  ################

    try:
        task_1b = __import__('task_1b')
        ArUco_details_dict, ArUco_corners = task_1b.detect_ArUco_details(np.asarray(image))
        if 5 in ArUco_details_dict.keys():
            c_x = ArUco_details_dict[5][0][0]
            c_y = ArUco_details_dict[5][0][1]
            c_angle = ArUco_details_dict[5][1]
            c_x = np.interp(c_x,[0,511],[0.9550, -0.9550])
            c_y = np.interp(c_y,[0,511],[-0.9550, 0.9550])
            c_angle = c_angle-180 if 0<=c_angle<=180 else 180+c_angle
            scene_parameters = [c_x,c_y,c_angle]
    except:
        pass

	######################################################

    return scene_parameters

def set_values(scene_parameters,sim):
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
    aruco_handle = sim.getObject('/aruco_5')       #Change the name of the object
	###################  ADD YOUR CODE HERE  ###############

    if(len(scene_parameters)==3):
        sim.setObjectPosition(aruco_handle,sim.handle_world,[scene_parameters[0],scene_parameters[1],0.1])
        sim.setObjectOrientation(aruco_handle,sim.handle_world,[0,0,scene_parameters[2]*np.pi/180])

	########################################################

    return None

##############################################################


################## ADD SOCKET COMMUNICATION ##################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 3D for setting up a Socket
Communication Server in this section
"""

def setup_server(host, port):

	"""
	Purpose:
	---
	This function creates a new socket server and then binds it 
	to a host and port specified by user.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`server` : [ socket object ]
	---

	
	Example call:
	---
	server = setupServer(host, port)
	""" 

	server = None

	##################	ADD YOUR CODE HERE	##################
	
	server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((host,port))

	##########################################################

	return server

def setup_connection(server):
	"""
	Purpose:
	---
	This function listens for an incoming socket client and
	accepts the connection request

	Input Arguments:
	---
	`server` :	[ socket object ]
			socket object created by setupServer() function
	Returns:
	---
	`server` : [ socket object ]
	
	Example call:
	---
	connection = setupConnection(server)
	"""
	connection = None
	address = None

	##################	ADD YOUR CODE HERE	##################

	server.listen()
	connection, address = server.accept()

	##########################################################

	return connection, address

def receive_message_via_socket(connection):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket connection and returns the message when received.

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################

	message = connection.recv(1024).decode()

	##########################################################

	return message

def send_message_via_socket(connection, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket connection

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################

	connection.send(message.encode())

	##########################################################

##############################################################
##############################################################

######################### ADD TASK 2B ########################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 2B for reading QR code from
CoppeliaSim arena in this section
"""

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the CoppeliaSim vision sensor's 
	field of view and returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	
	##############  ADD YOUR CODE HERE  ##############

	cam = sim.getObject('/Diff_Drive_Bot/vision_sensor')
	i, res =sim.getVisionSensorImg(cam)
	img = np.frombuffer(i, np.uint8)
	img.resize([res[0], res[1], 3])
	img = cv2.flip(img,0)
	mono = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	codes = decode(mono)
	for code in codes:
		qr_message = code.data.decode()
		break

	##################################################

	return qr_message

##############################################################
##############################################################

############### ADD ARENA PARAMETER DETECTION ################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 1A and 3A for detecting arena parameters
from configuration image in this section
"""

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

    ##############	ADD YOUR CODE HERE	##############

	mono = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	for i in range(0,6):
		for j in range(0,6):
			if mono[100+(j*100)][100+(i*100)] == 76:
				traffic_signals.append(chr(65+i)+chr(49+j))
			if mono[100+(j*100)][100+(i*100)] == 78:
				end_node = chr(65+i)+chr(49+j)
			if mono[100+(j*100)][100+(i*100)] == 150:
				start_node = chr(65+i)+chr(49+j)

    ##################################################

	return traffic_signals, start_node, end_node

def detect_horizontal_roads_under_construction(image):	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############

	mono = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	for i in range(0,6):
		for j in range(0,7):
			if mono[100+(j*100)][150+(i*100)] != 0:
				horizontal_roads_under_construction.append(chr(65+i)+chr(49+j)+'-'+chr(66+i)+chr(49+j))

	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############

	mono = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	for i in range(0,7):
		for j in range(0,6):
			if mono[150+(j*100)][100+(i*100)] != 0:
				vertical_roads_under_construction.append(chr(65+i)+chr(49+j)+'-'+chr(65+i)+chr(50+j))
	
	##################################################
	
	return vertical_roads_under_construction

def detect_medicine_packages(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages = []

	##############	ADD YOUR CODE HERE	##############

	mono = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	for i in range(1,7):
		for j in range(2):
			for k in range(2):
				med = []
				cen = [30+(100*i)+(40*j),130+(40*k)]
				up = mono[cen[1]-10][cen[0]-10]
				side = mono[cen[1]][cen[0]-10]
				if mono[cen[1]][cen[0]] == 97:
					med.append('Shop_'+str(i))
					med.append('Pink')
				elif mono[cen[1]][cen[0]] == 150:
					med.append('Shop_'+str(i))
					med.append('Green')
				elif mono[cen[1]][cen[0]] == 151:
					med.append('Shop_'+str(i))
					med.append('Orange')
				elif mono[cen[1]][cen[0]] == 179:
					med.append('Shop_'+str(i))
					med.append('Skyblue') 

				if up!=255 and side!=255:
					med.append('Square')
					med.append(cen)
					medicine_packages_present.append(med)
				elif up==255 and side!=255 and mono[cen[1]][cen[0]] != 255:
					med.append('Circle') 
					med.append(cen) 
					medicine_packages_present.append(med) 
				elif mono[cen[1]][cen[0]] != 255:
					med.append('Triangle')
					cen[1]=cen[1]-1
					med.append(cen)
					medicine_packages_present.append(med)

	medicine_packages_present = sorted(medicine_packages_present,key=lambda item: (item[0], item[1]))

	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
	
	(traffic_signals, start_node, end_node) = detect_all_nodes(maze_image)
	arena_parameters['medicine_packages'] = detect_medicine_packages(maze_image)
	arena_parameters['traffic_signals'] = traffic_signals
	arena_parameters['start_node'] = start_node
	arena_parameters['end_node'] = end_node
	arena_parameters['horizontal_roads_under_construction'] = detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction'] = detect_vertical_roads_under_construction(maze_image)

    ##################################################

	return arena_parameters

##############################################################
##############################################################

####################### ADD ARENA SETUP ######################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 4A for setting up the CoppeliaSim
Arena according to the configuration image in this section
"""

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
		
#########################################################################
	
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

##############################################################
##############################################################