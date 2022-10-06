'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############

	mono = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
	for i in range(0,7):
		for j in range(0,7):
			if mono[100+(j*100)][100+(i*100)] == 76:
				traffic_signals.append(chr(65+i)+chr(49+j))
	
	##################################################
	
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
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

	mono = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
	for i in range(0,6):
		for j in range(0,7):
			if mono[100+(j*100)][150+(i*100)] != 0:
				horizontal_roads_under_construction.append(chr(65+i)+chr(49+j)+'-'+chr(66+i)+chr(49+j))
	
	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

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

	mono = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
	for i in range(0,7):
		for j in range(0,6):
			if mono[150+(j*100)][100+(i*100)] != 0:
				vertical_roads_under_construction.append(chr(65+i)+chr(49+j)+'-'+chr(65+i)+chr(50+j))
	
	##################################################
	
	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

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
	`medicine_packages_present` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages_present = detect_medicine_packages(maze_image)
	"""    
	medicine_packages_present = []

	##############	ADD YOUR CODE HERE	##############

	mono = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
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

	return medicine_packages_present

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

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
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	
	arena_parameters['traffic_signals'] = detect_traffic_signals(maze_image)
	arena_parameters['horizontal_roads_under_construction'] = detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction'] = detect_vertical_roads_under_construction(maze_image)
	arena_parameters['medicine_packages_present'] = detect_medicine_packages(maze_image)

	##################################################
	
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()
