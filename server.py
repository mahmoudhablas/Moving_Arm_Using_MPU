import sys
from visual import *
import math
import time  
import socket               # Import socket module


time_diff = 0.01
########################################
scene.title ='Robotic Arm'

g = 9.8
M1 = 2.0
M2 = 1.0
d = 0.05 # thickness of each bar
gap = 2.*d # distance between two parts of upper, U-shaped assembly
L1 = 0.5 # physical length of upper assembly; distance between axles
L1display = L1+d # show upper assembly a bit longer than physical, to overlap axle
L2 = 1.0 # physical length of lower bar
L2display = L2+d/2. # show lower bar a bit longer than physical, to overlap axle
L3display = .3

hpedestal = 1.3*(L1+L2) # height of pedestal
wpedestal = 0.1 # width of pedestal
tbase = 0.05 # thickness of base
wbase = 8.*gap # width of base
offset = 2.*gap # from center of pedestal to center of U-shaped upper assembly
top = vector(0,0,0) # top of inner bar of U-shaped upper assembly
scene.center = top-vector(0,(L1+L2)/2.,0)

theta1 = 1.3*pi/2. # initial upper angle (from vertical)
theta1dot = 0 # initial rate of change of theta1
theta2 = 0 # initial lower angle (from vertical)
theta2dot = 0 # initial rate of change of theta2

top = vector(0,0,0) # top of inner bar of U-shaped upper assembly
pedestal = box(pos=top-vector(0,hpedestal/2.,offset),
                 height=1.1*hpedestal, length=wpedestal, width=wpedestal,
                 color=(0.4,0.4,0.5))

frame1 = frame(pos=top)
bar1 = box(frame=frame1, pos=(L1display/2.-d/2.,0,-(gap+d)/2.), size=(L1display,d,d), color=color.red)
frame1.axis = (0,-1,0)

frame2 = frame(pos=frame1.axis*L1)
bar2 = box(frame=frame2, pos=(L2display/2.-d/2.,0,0), size=(L2display,d,d), color=color.green)
frame2.axis = (0,-1,0)
frame2.pos = top+frame1.axis*L1

frame3 = frame(pos = frame2.axis*L2)
bar3 = box(frame=frame3, pos=(L3display/2.-d/2.,0,0), size=(L3display,d,d), color=color.yellow)
frame3.axis = (0,-1,0)
frame3.pos = top+frame1.axis*L1 +frame2.axis*L2

scene.autoscale = 0


#####################################################################################33
s = socket.socket()         # Create a socket object
host = "10.42.0.1" #socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.


while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   try:
      ############ 1 ###################
      ss1 = c.recv(sys.getsizeof(float))
      ss1 = ss1[2:11]
      previous_x = float(ss1)

      ############## 2 ##################
      ss2 = c.recv(sys.getsizeof(float))
      ss2 = ss2[2:11]
      previous_x2 = float(ss2)
      ############### 3 ##################
      ss3 = c.recv(sys.getsizeof(float))
      ss3 = ss3[2:11]
      previous_x3 = float(ss3)

      ssy3 = c.recv(sys.getsizeof(float))
      ssy3 = ssy3[2:11]
      previous_y3 = float(ss2)

      while True:
            ################### 1 #######################
            s1 = c.recv(sys.getsizeof(float))
            if s1[:2]=="x1":
              s1 = s1[2:11]
            else:
              s1 = previous_x
              tmp = c.recv(sys.getsizeof(float))

            delta_x = float(s1)

            frame1.rotate(axis=(0,0,1), angle=delta_x -previous_x )
            frame2.pos = top+frame1.axis*L1

            previous_x = delta_x

            ################## 2 ############################

            s2 = c.recv(sys.getsizeof(float))
            if s2[:2]=="x2":
              s2 = s2[2:11]
            else:
              s2 = previous_x2
              tmp = c.recv(sys.getsizeof(float))
            delta_x2 = float(s2)

            frame2.rotate(axis=(0,0,1), angle=delta_x2 -previous_x2 )
            frame3.pos = top+frame1.axis*L1+frame2.axis*L2 +(0,0,L3display/2)
            previous_x2 = delta_x2

            ##################### 3 #############################
            s3 = c.recv(sys.getsizeof(float))
            if s3[:2]=="x3":
              s3 = s3[2:11]
            else:
              s3 = previous_x3
              tmp = c.recv(sys.getsizeof(float))
            delta_x3 = float(s3)

            s4 = c.recv(sys.getsizeof(float))
            if s4[:2]=="y3":
              s4 = s4[2:11]
            else:
              s4 = previous_y3
              tmp = c.recv(sys.getsizeof(float))
            delta_y3 = float(s4)

            frame3.rotate(angle=(delta_x3-previous_x3), axis=vector(1,0,0))
            frame3.rotate(angle=(delta_y3-previous_y3), axis=vector(0,0,1))
            
            previous_x3 = delta_x3
            previous_y3 = delta_y3


   except KeyboardInterrupt:
      s.close()
      c.close()                # Close the connection