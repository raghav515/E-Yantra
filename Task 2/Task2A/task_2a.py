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
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2, detect_distance_sensor_3
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

	l_joint = sim.getObject('/Diff_Drive_Bot/left_joint')
	r_joint = sim.getObject('/Diff_Drive_Bot/right_joint')
	sim.setJointTargetVelocity(l_joint, 0)
	sim.setJointTargetVelocity(r_joint, 0)
	node = 0
	speed  = 0.1
	while 1:
		front = detect_distance_sensor_1(sim)
		right_front = detect_distance_sensor_2(sim)
		right_back = detect_distance_sensor_3(sim)
		if front >= 0.18 or front ==0:
			if right_front < right_back and right_front < 0.1479 and detect_distance_sensor_2(sim) !=0 and detect_distance_sensor_3(sim)!=0:
				sim.setJointTargetVelocity(l_joint, 4.7*speed)
				sim.setJointTargetVelocity(r_joint, 5*speed)

			elif right_front > right_back and right_back > 0.1479 and right_front !=0 and right_back!=0:
					sim.setJointTargetVelocity(l_joint, 5*speed)
					sim.setJointTargetVelocity(r_joint, 4.7*speed)
			sim.setJointTargetVelocity(l_joint, 5*speed)
			sim.setJointTargetVelocity(r_joint, 5*speed)
			if(speed<0.9 and front==0):
				speed+=0.1
			elif(speed>0.1 and front!=0):
				speed-=0.3
		else:
			sim.setJointTargetVelocity(l_joint, 0)
			sim.setJointTargetVelocity(r_joint, 0)
			if(node == 9):
				sim.setJointTargetVelocity(l_joint, 0)
				sim.setJointTargetVelocity(r_joint, 0)
				break
			if detect_distance_sensor_2(sim)==0 and detect_distance_sensor_3(sim)==0:
				sim.setJointTargetVelocity(l_joint, 0.5)
				sim.setJointTargetVelocity(r_joint, -0.5)
				time.sleep(1.5)
				while(detect_distance_sensor_1(sim)!=0 or detect_distance_sensor_2(sim)!=detect_distance_sensor_3(sim)):
					sim.setJointTargetVelocity(l_joint, 0.5)
					sim.setJointTargetVelocity(r_joint, -0.5)
				time.sleep(0.7)
			else:
				while(detect_distance_sensor_1(sim)!=0 or round(detect_distance_sensor_2(sim),2)!=round(detect_distance_sensor_3(sim),2)):
					sim.setJointTargetVelocity(l_joint, -0.5)
					sim.setJointTargetVelocity(r_joint, 0.5)
			node = node + 1
		

	# i = 1
	# while 1:
	# 	right = detect_distance_sensor_2(sim)
	# 	left = detect_distance_sensor_3(sim)
	# 	front = detect_distance_sensor_1(sim)
	# 	if front<0.24 and left==0.0 and front!=0:
	# 		while not(detect_distance_sensor_1(sim)==0  and detect_distance_sensor_3(sim)==0 and detect_distance_sensor_2(sim) < front * 0.89):
	# 			sim.setJointTargetVelocity(l_joint, -1)
	# 			sim.setJointTargetVelocity(r_joint, 1)
	# 	elif front<0.225 and right == 0.0 and front!=0:
	# 		while not(detect_distance_sensor_1(sim)==0  and detect_distance_sensor_2(sim)==0 and detect_distance_sensor_3(sim) < front * 0.89):
	# 			sim.setJointTargetVelocity(l_joint, 1)
	# 			sim.setJointTargetVelocity(r_joint, -1)
	# 	elif right<0.22 and left<0.22 and front<0.24 and front!=0 and right!=0 and left!=0:
	# 		sim.setJointTargetVelocity(l_joint, 0)
	# 		sim.setJointTargetVelocity(r_joint, 0)
	# 		break
	# 	if right>0.175 and left<0.21 and left != 0:
	# 		sim.setJointTargetVelocity(l_joint, 0.5*i)
	# 		sim.setJointTargetVelocity(r_joint, 0.5*i*(1-right-0.175))
	# 	elif right<0.175 and right!=0 and left>0.2:
	# 		sim.setJointTargetVelocity(l_joint, 0.5*i*(1-left-0.2))
	# 		sim.setJointTargetVelocity(r_joint, 0.5*i)
	# 	else:
	# 		sim.setJointTargetVelocity(l_joint, 0.5*i)
	# 		sim.setJointTargetVelocity(r_joint, 0.5*i)
	# 	if i<8 and front == 0:
	# 		i+=0.5
	# 	elif i>2 and (front != 0 or left==0 or right==0):
	# 		i-=1.5

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