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

# Team ID:			1067
# Author List:		Joel Jojo Painuthara, Raghavendra Pandurang Jadhav, Pooja M, Dhiren Bhandary
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code, turn
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

def turn(sim):
	cam = sim.getObject('/Diff_Drive_Bot/vision_sensor')
	frameWidth = 480
	frameHeight = 360
	lower = np.array([0, 0, 154])
	upper = np.array([179, 255, 255])
	while(1):
		i, res =sim.getVisionSensorImg(cam)
		img = np.frombuffer(i, np.uint8)
		img.resize([res[0], res[1], 3])
		img = cv2.resize(img, (frameWidth, frameHeight))
		img = cv2.flip(img,0)
		imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(imgHsv, lower, upper)
		edges = cv2.Canny(mask, 50, 150, apertureSize=3)
		lines = cv2.HoughLines(edges, 1, np.pi/180, 70)
		x = 0
		i = 0
		if lines is not None:
			for r_theta in lines:
				arr = np.array(r_theta[0], dtype=np.float64)
				r, theta = arr
				if theta < np.pi/18. and theta > -1*np.pi/18.:
					a = np.cos(theta)
					b = np.sin(theta)
					x0 = a*r
					#y0 = b*r
					x1 = int(x0 + 1000*(-b))
					#y1 = int(y0 + 1000*(a))
					x2 = int(x0 - 1000*(-b))
					#y2 = int(y0 - 1000*(a))
					x = x + x1 + x2
					i = i + 2	
					#cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
		if i >= 3:
			break
				



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
	sim.setJointTargetVelocity(l_joint, 0.5)
	sim.setJointTargetVelocity(r_joint, 0.5)
	frameWidth = 480
	frameHeight = 360
	lower = np.array([0, 0, 154])
	upper = np.array([179, 255, 255])
	dir = [1,2,1,2,0,2,1,2,0,2,1,2,0,2,1,2,3]
	cp = {4:'checkpoint E',8:'checkpoint I',12:'checkpoint M'}
	app = 0
	node = 0
	while(1):
		i, res =sim.getVisionSensorImg(cam)
		img = np.frombuffer(i, np.uint8)
		img.resize([res[0], res[1], 3])
		img = cv2.resize(img, (frameWidth, frameHeight))
		img = cv2.flip(img,0)
		imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(imgHsv, lower, upper)
		edges = cv2.Canny(mask, 50, 150, apertureSize=3)
		
		lines = cv2.HoughLines(edges, 1, np.pi/180, 70)
		x = 0
		i = 0
		if lines is not None:
			for r_theta in lines:
				arr = np.array(r_theta[0], dtype=np.float64)
				r, theta = arr
				if theta < np.pi/6. and theta > -1*np.pi/6.:
					a = np.cos(theta)
					b = np.sin(theta)
					x0 = a*r
					#y0 = b*r
					x1 = int(x0 + 1000*(-b))
					#y1 = int(y0 + 1000*(a))
					x2 = int(x0 - 1000*(-b))
					#y2 = int(y0 - 1000*(a))
					x = x + x1 + x2
					i = i + 2	
					#cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
		if (img[250][120][0] == 253 and img[250][120][2] == 4) or (img[250][240][0] == 253 and img[250][240][2] == 4) or (img[250][360][0] == 253 and img[250][360][2] == 4):
			if dir[node]==1:
				sim.setJointTargetVelocity(l_joint, -0.2)
				sim.setJointTargetVelocity(r_joint, 0.8)
				time.sleep(1)
				turn(sim)
			elif dir[node]==2:
				sim.setJointTargetVelocity(l_joint, 0.8)
				sim.setJointTargetVelocity(r_joint, -0.2)
				time.sleep(1)
				turn(sim)
			elif dir[node]==0:
				sim.setJointTargetVelocity(l_joint, 0)
				sim.setJointTargetVelocity(r_joint, 0)
				arena_dummy_handle = sim.getObject("/Arena_dummy") 
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
				sim.callScriptFunction("activate_qr_code", childscript_handle, cp[node])
				qr = read_qr_code(sim)
				print(qr)
				if 'Cone' in qr:
					sim.callScriptFunction("deliver_package", childscript_handle, "package_1", cp[node])
				elif 'Cylinder' in qr:
					sim.callScriptFunction("deliver_package", childscript_handle, "package_2", cp[node])
				elif 'Cuboid' in qr:
					sim.callScriptFunction("deliver_package", childscript_handle, "package_3", cp[node])
				sim.callScriptFunction("deactivate_qr_code", childscript_handle, cp[node])
				sim.setJointTargetVelocity(l_joint, 0.5)
				sim.setJointTargetVelocity(r_joint, 0.5)
				time.sleep(1)
			elif dir[node]==3:
				sim.setJointTargetVelocity(l_joint, 0.5)
				sim.setJointTargetVelocity(r_joint, 0.5)
				time.sleep(2)
				sim.setJointTargetVelocity(l_joint,0)
				sim.setJointTargetVelocity(r_joint,0)
				break
			node = node + 1
			if dir[node]==0:
				app = 1
			else:
				app = 0
		elif i!=0:
			x = int(x/i)
			cv2.circle(img, (x, 180), 2, (0, 0, 255), 3)
			if x < 230:
				sim.setJointTargetVelocity(l_joint, 2 - (app*0.7))
				sim.setJointTargetVelocity(r_joint, 1.2 - (app*0.4))
			elif x > 250:
				sim.setJointTargetVelocity(l_joint, 1.2 - (app*0.4))
				sim.setJointTargetVelocity(r_joint, 2 - (app*0.7))
			else:
				sim.setJointTargetVelocity(l_joint, 2 - (app*0.7))
				sim.setJointTargetVelocity(r_joint, 2 - (app*0.7))
		else:
			sim.setJointTargetVelocity(l_joint, 0.7)
			sim.setJointTargetVelocity(r_joint, 0.7)
		
		cv2.circle(img, (240, 300), 2, (255,0,0), 3)
		# cv2.imshow('Video', img)
		# if cv2.waitKey(10) and 0xFF == ord('q'):
		# 	cv2.destroyAllWindows()
		# 	break
	
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