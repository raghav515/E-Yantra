'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
from operator import le
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

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

	f = 1
	l_joint = sim.getObject('/Diff_Drive_Bot/left_joint')
	r_joint = sim.getObject('/Diff_Drive_Bot/right_joint')
	sim.setJointTargetVelocity(l_joint, 0)
	sim.setJointTargetVelocity(r_joint, 0)
	while(f):
		front = detect_distance_sensor_1(sim)
		right = detect_distance_sensor_2(sim)
		left = detect_distance_sensor_3(sim)
		#print(front,right,left)
		if right<0.5 and front<0.25 and front!=0.0 and (left>0.5 or left==0.0):
			sim.setJointTargetVelocity(l_joint, 0)
			sim.setJointTargetVelocity(r_joint, 0)
			sim.setJointTargetVelocity(l_joint, -1)
			sim.setJointTargetVelocity(r_joint, 1)
			time.sleep(2.74)
			sim.setJointTargetVelocity(l_joint, 0)
			sim.setJointTargetVelocity(r_joint, 0)
		elif left<0.5 and front<0.25 and front!=0.0 and (right>0.5 or right==0.0):
			sim.setJointTargetVelocity(l_joint, 0)
			sim.setJointTargetVelocity(r_joint, 0)
			sim.setJointTargetVelocity(l_joint, 1)
			sim.setJointTargetVelocity(r_joint, -1)
			time.sleep(2.74)
			sim.setJointTargetVelocity(l_joint, 0)
			sim.setJointTargetVelocity(r_joint, 0)
		elif right<0.3 and left<0.3 and front<0.25 and front!=0.0 and right!=0.0 and left!=0.0:
			sim.setJointTargetVelocity(l_joint, 0)
			sim.setJointTargetVelocity(r_joint, 0)
			break
		else:
			sim.setJointTargetVelocity(l_joint, 3)
			sim.setJointTargetVelocity(r_joint, 3)

	##################################################

def detect_distance_sensor_1(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############

	proxy_1 = sim.getObject('/Diff_Drive_Bot/distance_sensor_1')
	dis=sim.readProximitySensor(proxy_1)
	distance = dis[1]

	##################################################
	return distance

def detect_distance_sensor_2(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############

	proxy_2 = sim.getObject('/Diff_Drive_Bot/distance_sensor_2')
	dis=sim.readProximitySensor(proxy_2)
	distance = dis[1]

	##################################################
	return distance

def detect_distance_sensor_3(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############

	proxy_3 = sim.getObject('/Diff_Drive_Bot/distance_sensor_3')
	dis=sim.readProximitySensor(proxy_3)
	distance = dis[1]

	##################################################
	return distance

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
			control_logic(sim)
			time.sleep(5)

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