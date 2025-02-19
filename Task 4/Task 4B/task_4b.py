'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 4B of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_4b.py
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
import random
##############################################################

## Import PB_theme_functions code
try:
	pb_theme = __import__('PB_theme_functions')

except ImportError:
	print('\n[ERROR] PB_theme_functions.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure PB_theme_functions.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your PB_theme_functions.py throwed an Exception, kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()

def task_4b_implementation(sim):
	"""
	Purpose:
	---
	This function contains the implementation logic for task 4B 

	Input Arguments:
	---
    `sim` : [ object ]
            ZeroMQ RemoteAPI object

	You are free to define additional input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	task_4b_implementation(sim)
	"""

	##################	ADD YOUR CODE HERE	##################
	
	global config_img, start_node, end_node, traffic_signals, connection_1,connection_2
	arena = sim.getObject('/Arena')
	alphabot = sim.getObject('/Alphabot')
	graph = pb_theme.detect_paths_to_graph(config_img)
	path = pb_theme.path_planning(graph, start_node, end_node)
	(move, orientation) = pb_theme.paths_to_moves(path,traffic_signals,0)
	move_str = ' '.join(move)
	pb_theme.send_message_via_socket(connection_2, move_str)
	warped_image = []
	scene_parameters = []
	video = cv2.VideoCapture(2)
	while video.isOpened():
		ret, frame = video.read()
		warped_image = pb_theme.perspective_transform(frame)
		scene_parameters = pb_theme.transform_values(warped_image)
		pb_theme.set_values(scene_parameters)
		cv2.imshow("Frame",frame) 
		if pb_theme.receive_message_via_socket(connection_2) == "DEST_REACHED":
			break
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("activate_qr_code", childscript_handle)
	mes = pb_theme.read_qr_code()
	sim.callScriptFunction("deactivate_qr_code", childscript_handle)
	meds = json.loads(mes)
	cur_node = end_node
	for i in meds.keys():
		(color, shape) = i.split("_")
		message = "PICKED UP: " + color + ", " + shape.title() + ", " + meds[i]
		pb_theme.send_message_via_socket(connection_1, message)
		pb_theme.send_message_via_socket(connection_2, color)
		sim.setObjectParent(sim.getObject(i), alphabot)
		sim.setObjectPosition(sim.getObject(i), alphabot, [0,0,0.1])      #Adjust position
	for i in meds.keys():
		end_node = meds[i]
		path = pb_theme.path_planning(graph, cur_node, end_node)
		(move, orientation) = pb_theme.paths_to_moves(path, traffic_signals, orientation)
		move_str = ' '.join(move)
		pb_theme.send_message_via_socket(connection_2, move_str)
		warped_image = []
		scene_parameters = []
		video = cv2.VideoCapture(2)
		while video.isOpened():
			ret, frame = video.read()
			warped_image = pb_theme.perspective_transform(frame)
			scene_parameters = pb_theme.transform_values(warped_image)
			pb_theme.set_values(scene_parameters)
			cv2.imshow("Frame",frame) 
			if pb_theme.receive_message_via_socket(connection_2) == "DEST_REACHED":
				break
		(color, shape) = i.split("_")
		message = "DELIVERED: " + color + "," + shape.title() + " AT " + meds[i]
		pb_theme.send_message_via_socket(connection_1, message)
		pb_theme.send_message_via_socket(connection_2, color)
		sim.setObjectParent(sim.getObject(i), arena)
		sim.setObjectPosition(sim.getObject(i), alphabot, [0,0,0.1])   #Adjust position
		del meds[i]
	cv2.destroyAllWindows()
	video.release()

	##########################################################


if __name__ == "__main__":
	
	host = ''
	port = 5050


	## Set up new socket server
	try:
		server = pb_theme.setup_server(host, port)
		print("Socket Server successfully created")

		# print(type(server))

	except socket.error as error:
		print("Error in setting up server")
		print(error)
		sys.exit()


	## Set up new connection with a socket client (PB_task3d_socket.exe)
	try:
		print("\nPlease run PB_socket.exe program to connect to PB_socket client")
		connection_1, address_1 = pb_theme.setup_connection(server)
		print("Connected to: " + address_1[0] + ":" + str(address_1[1]))

	except KeyboardInterrupt:
		sys.exit()

	# ## Set up new connection with Raspberry Pi
	try:
		print("\nPlease connect to Raspberry pi client")
		connection_2, address_2 = pb_theme.setup_connection(server)
		print("Connected to: " + address_2[0] + ":" + str(address_2[1]))

	except KeyboardInterrupt:
		sys.exit()

	## Send setup message to PB_socket
	pb_theme.send_message_via_socket(connection_1, "SETUP")

	message = pb_theme.receive_message_via_socket(connection_1)
	## Loop infinitely until SETUP_DONE message is received
	while True:
		if message == "SETUP_DONE":
			break
		else:
			print("Cannot proceed further until SETUP command is received")
			message = pb_theme.receive_message_via_socket(connection_1)

	try:
		# obtain required arena parameters
		config_img = cv2.imread("config_image.png")
		detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)			
		medicine_package_details = detected_arena_parameters["medicine_packages"]
		traffic_signals = detected_arena_parameters['traffic_signals']
		start_node = detected_arena_parameters['start_node']
		end_node = detected_arena_parameters['end_node']
		horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
		vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction']

		# print("Medicine Packages: ", medicine_package_details)
		# print("Traffic Signals: ", traffic_signals)
		# print("Start Node: ", start_node)
		# print("End Node: ", end_node)
		# print("Horizontal Roads under Construction: ", horizontal_roads_under_construction)
		# print("Vertical Roads under Construction: ", vertical_roads_under_construction)
		# print("\n\n")

	except Exception as e:
		print('Your task_1a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	try:

		## Connect to CoppeliaSim arena
		coppelia_client = RemoteAPIClient()
		sim = coppelia_client.getObject('sim')

		## Define all models
		all_models = []

		## Setting up coppeliasim scene
		print("[1] Setting up the scene in CoppeliaSim")
		all_models = pb_theme.place_packages(medicine_package_details, sim, all_models)
		all_models = pb_theme.place_traffic_signals(traffic_signals, sim, all_models)
		all_models = pb_theme.place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_start_end_nodes(start_node, end_node, sim, all_models)
		print("[2] Completed setting up the scene in CoppeliaSim")
		print("[3] Checking arena configuration in CoppeliaSim")

	except Exception as e:
		print('Your task_4a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	pb_theme.send_message_via_socket(connection_1, "CHECK_ARENA")

	## Check if arena setup is ok or not
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		

		if message == "ARENA_SETUP_OK":
			print("[4] Arena was properly setup in CoppeliaSim")
			break
		elif message == "ARENA_SETUP_NOT_OK":
			print("[4] Arena was not properly setup in CoppeliaSim")
			connection_1.close()
			# connection_2.close()
			server.close()
			sys.exit()
		else:
			pass

	## Send Start Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_START")
	
	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STARTED_CORRECTLY":
			print("[5] Simulation was started in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STARTED_CORRECTLY":
			print("[5] Simulation was not started in CoppeliaSim")
			sys.exit()

	## Send Start Command to Raspberry Pi to start execution
	pb_theme.send_message_via_socket(connection_2, "START")

	
	task_4b_implementation(sim)

	## Send Stop Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_STOP")

	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STOPPED_CORRECTLY":
			print("[6] Simulation was stopped in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STOPPED_CORRECTLY":
			print("[6] Simulation was not stopped in CoppeliaSim")
			sys.exit()