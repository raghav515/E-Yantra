'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			1067
# Author List:		Joel Jojo Painuthara, Raghavendra Pandurang Jadhav, Dhiren Bhandary, Pooja M
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

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


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

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

	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	paths = detect_paths_to_graph(maze_image)
	arena_parameters["traffic_signals"] = traffic_signals
	arena_parameters["start_node"] = start_node
	arena_parameters["end_node"] = end_node
	arena_parameters["paths"] = paths

	##################################################
	
	return arena_parameters

def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
	list given below **

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

def paths_to_moves(paths, traffic_signal):

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
	
	orientation = 0
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

	return list_moves

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "test_images/"

	for file_num in range(0,10):
			
			img_key = 'maze_00' + str(file_num)
			img_file_path = img_dir_path + img_key  + '.png'
			# read image using opencv
			image = cv2.imread(img_file_path)
			
			# detect the arena parameters from the image
			arena_parameters = detect_arena_parameters(image)
			print('\n============================================')
			print("IMAGE: ", file_num)
			print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )

			# path planning and getting the moves
			back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
			moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

			print("PATH PLANNED: ", back_path)
			print("MOVES TO TAKE: ", moves)

			# display the test image
			cv2.imshow("image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()