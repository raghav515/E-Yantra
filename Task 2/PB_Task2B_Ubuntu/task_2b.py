'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
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
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""
	##############  ADD YOUR CODE HERE  ##############

	l_joint = sim.getObject('/Diff_Drive_Bot/left_joint')
	r_joint = sim.getObject('/Diff_Drive_Bot/right_joint')
	cam = sim.getObject('/Diff_Drive_Bot/vision_sensor')
	while(1):
		i, res =sim.getVisionSensorImg(cam)
		img = np.frombuffer(i, np.uint8)
		img.resize([res[0], res[1], 3])
		frameWidth = 480
		frameHeight = 360
		img = cv2.resize(img, (frameWidth, frameHeight))
		img = cv2.flip(img,0)
		imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		lower = np.array([0, 0, 154])
		upper = np.array([179, 255, 255])
		mask = cv2.inRange(imgHsv, lower, upper)
		mask = cv2.bitwise_not(mask)
		#result = cv2.bitwise_and(img, img, mask=mask)
		#mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
		contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
		if len(contours) > 0 :
			c = max(contours, key=cv2.contourArea)
			M = cv2.moments(c)
			if M["m00"] !=0 :
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				if cx<165:
					cx = cx + 180
				elif cx>390:
					cx = cx - 190
				#print("CX : "+str(cx)+"  CY : "+str(cy))
				if cx >= 280 :
					print("Turn Left")
					sim.setJointTargetVelocity(l_joint, -0.2)
					sim.setJointTargetVelocity(r_joint, 0.2)
				if cx < 280 and cx > 200 :
					print("On Track!")
					sim.setJointTargetVelocity(l_joint, 0.5)
					sim.setJointTargetVelocity(r_joint, 0.5)
				if cx <=200 :
					print("Turn Right")
					sim.setJointTargetVelocity(l_joint, 0.2)
					sim.setJointTargetVelocity(r_joint, -0.2)
				if img[cy][cx][0] == 253 and img[cy][cx][1] == 204 and img[cy][cx][2] == 4:
					print("Node Reached")
					sim.setJointTargetVelocity(l_joint, 0)
					sim.setJointTargetVelocity(r_joint, 1)
					time.sleep(4)
				cv2.circle(img, (cx,cy), 5, (0,0,255), -1)
		cv2.imshow('Video', img)
		cv2.imshow('Mask', mask)
		if cv2.waitKey(1) and 0xFF == ord('q'):
			break
	'''
	while True:
		a = input()
		if a=='w':
			sim.setJointTargetVelocity(l_joint, 0.5)
			sim.setJointTargetVelocity(r_joint, 0.5)
		elif a=='a':
			sim.setJointTargetVelocity(l_joint, -0.2)
			sim.setJointTargetVelocity(r_joint, 0.2)
		elif a=='d':
			sim.setJointTargetVelocity(l_joint, 0.2)
			sim.setJointTargetVelocity(r_joint, -0.2)
		elif a=='s':
			sim.setJointTargetVelocity(l_joint, 0)
			sim.setJointTargetVelocity(r_joint, 0)
		elif a=='r':
			read_qr_code(sim)
		elif a=='q':
			break
	'''
	
	##################################################

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

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

	##################################################
	return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			time.sleep(5)
			control_logic(sim)

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		
		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()