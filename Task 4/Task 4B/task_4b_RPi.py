'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 4B-Part 1 of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			PB_1067
# Author List:		Joel Jojo Painuthara, Raghavendra Pandurang Jadhav, Dhiren Bhandary, Pooja M
# Filename:			task_4b_1.py
# Functions:		control_logic, move_bot
#
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section.   ##
## You have to implement this task with the available modules ##
##############################################################

from picamera import PiCamera
from picamera.array import PiRGBArray
from threading import Thread
import numpy as np
import cv2
import time
import RPi.GPIO as GPIO
import sys
import datetime
import socket
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

########### ADD YOUR UTILITY FUNCTIONS HERE ##################

l_PWM_1 = 33
l_PWM_2 = 32
l_Enable = 31
r_PWM_2 = 40
r_PWM_1 = 38
r_Enable = 37
l_enc = 26
r_enc = 24
r_count = 0
l_count = 0
dir = ['STRAIGHT', 'STRAIGHT', 'LEFT', 'STRAIGHT', 'RIGHT', 'LEFT', 'STOP']
cur_node = 0
host = ""
port = 5050
redPin1 = 
greenPin1 = 
bluePin1 = 
redPin2 =
greenPin2 = 
bluePin2 = 

def setup_client(host, port):
	client = None
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host, port))
	return client

def receive_message_via_socket(client):
	message = None
	message = client.recv(1024).decode()
	return message

def send_message_via_socket(client, message):
	client.send(message.encode())

def l_enc_count(channel):
    global l_count
    l_count = l_count + 1


def r_enc_count(channel):
    global r_count
    r_count = r_count + 1


def init_pins():
    global l_Motor_1, l_Motor_2, r_Motor_1, r_Motor_2
    GPIO.setup(r_PWM_1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(r_PWM_2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(l_PWM_1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(l_PWM_2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(l_Enable, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(r_Enable, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(redPin1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(greenPin1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(bluePin1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(redPin2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(greenPin2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(bluePin2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(l_enc, GPIO.IN)
    GPIO.setup(r_enc, GPIO.IN)
    GPIO.add_event_detect(l_enc, GPIO.RISING, callback=l_enc_count)
    GPIO.add_event_detect(r_enc, GPIO.RISING, callback=r_enc_count)
    l_Motor_1 = GPIO.PWM(l_PWM_1, 100)
    l_Motor_2 = GPIO.PWM(l_PWM_2, 100)
    r_Motor_1 = GPIO.PWM(r_PWM_1, 100)
    r_Motor_2 = GPIO.PWM(r_PWM_2, 100)
    l_Motor_1.start(0)
    r_Motor_1.start(0)
    l_Motor_2.start(0)
    r_Motor_2.start(0)

##############################################################


def control_logic(image):
    """
    Purpose:
    ---
    This function is suppose to process the frames from the PiCamera and
    check for the error using image processing and with respect to error
    it should correct itself using PID controller.

    >> Process the Frame from PiCamera 
    >> Check for the error in line following and node detection
    >> PID controller

    Input Arguments:
    ---
    You are free to define input arguments for this function.

    Hint: frame [numpy array] from PiCamera can be passed in this function and it can
        take the action using PID 

    Returns:
    ---
    You are free to define output parameters for this function.

    Example call:
    ---
    control_logic()
    """

    ################## ADD YOUR CODE HERE	##################
    global dir, cur_node, l_count, r_count, l_Motor_2, r_Motor_2
    imgHsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([7, 41, 100])
    upper = np.array([35, 134, 214])
    mask = cv2.inRange(imgHsv, lower, upper)
    ret, thresh = cv2.threshold(mask, 50, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    for cnt in contours:
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = float(w)/h
            if ratio >= 0.9 and ratio <= 1.1:
                pass
            else:
                cur_node+=1
                l_Motor_1.ChangeDutyCycle(0)
                r_Motor_1.ChangeDutyCycle(0)
                l_count = 0
                r_count = 0
                while l_count<15 and r_count<15:
                    l_Motor_1.ChangeDutyCycle(20)
                    r_Motor_1.ChangeDutyCycle(20)
                #print('Node Detected')
                if dir[cur_node] == 'LEFT':
                    #print('left')     
                    l_Motor_1.ChangeDutyCycle(0)
                    r_Motor_1.ChangeDutyCycle(0)        
                    l_count = 0
                    while l_count<=20:
                        l_Motor_1.ChangeDutyCycle(25)
                        r_Motor_1.ChangeDutyCycle(0)
                elif dir[cur_node] == 'RIGHT':
                    #print('right')         
                    l_Motor_1.ChangeDutyCycle(0)
                    r_Motor_1.ChangeDutyCycle(0) 
                    r_count = 0
                    while r_count<=23:
                        l_Motor_1.ChangeDutyCycle(0)
                        r_Motor_1.ChangeDutyCycle(30)
                elif dir[cur_node] == 'STRAIGHT':
                    #print('straight')
                    pass
                elif(dir[cur_node]=='STOP'):
                    #print('stop')          
                    l_Motor_1.ChangeDutyCycle(0)
                    r_Motor_1.ChangeDutyCycle(0) 
                    return True
                break
    lower = np.array([0, 0, 125])
    upper = np.array([179, 255, 255])
    imgHsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHsv, lower, upper)
    x = 0
    detect = [False,False]
    cv2.line(image, (0, 100), (640, 100), (0, 0, 255), 2)
    for i in range(2, 200):
        if mask[100,i]!=mask[100,i+1]:
            cv2.circle(image, (i, 100), 4, (0, 255, 0), 6)
            x = x + i
            detect[0] = True
            break
    for i in range(638, 440, -1):
        if mask[100,i]!=mask[100,i-1]:
            cv2.circle(image, (i, 100), 4, (0, 255, 0), 6)
            x = x + i
            detect[1] = True
            break
    if x!=0 and detect[0] and detect[1]:
        x = int(x/2)
        cv2.circle(image, (x, 100), 4, (255, 0, 0), 6)
        l_Motor_1.ChangeDutyCycle(20)
        r_Motor_1.ChangeDutyCycle(20)
    elif detect[1] == False:
        l_Motor_1.ChangeDutyCycle(20)
        r_Motor_1.ChangeDutyCycle(17)
    elif detect[0] == False:
        l_Motor_1.ChangeDutyCycle(17)
        r_Motor_1.ChangeDutyCycle(20)
    else:
        pass
    return False

    ##########################################################


def move_bot(l_rpm_tar, r_rpm_tar):
    """
    Purpose:
    ---
    This function is suppose to move the bot

    Input Arguments:
    ---
    You are free to define input arguments for this function.

    Hint: Here you can have inputs left, right, straight, reverse and many more
        based on your control_logic

    Returns:
    ---
    You are free to define output parameters for this function.

    Example call:
    ---
    move_bot()
    """

    ################## ADD YOUR CODE HERE	##################

    ##########################################################


if __name__ == "__main__":

    """
    The goal of the this task is to move the robot through a predefied 
    path which includes straight road traversals and taking turns at 
    nodes. 

    This script is to be run on Raspberry Pi and it will 
    do the following task.

    >> Stream the frames from PiCamera
    >> Process the frame, do the line following and node detection
    >> Move the bot using control logic

    The overall task should be executed here, plan accordingly. 
    """

    ################## ADD YOUR CODE HERE	##################

    init_pins()
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
    for frame in stream:
        image = frame.array
        flag = control_logic(image)
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q") or flag:
            cv2.destroyAllWindows()
            break
    l_Motor_1.stop()
    r_Motor_1.stop()
    l_Motor_2.stop()
    r_Motor_2.stop()
    GPIO.cleanup()

    ##########################################################

    pass
