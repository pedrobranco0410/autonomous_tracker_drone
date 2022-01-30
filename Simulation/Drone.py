"""
Class responsible for simulating a drone with a mobile camera attached to a gimble. It contains all the methods needed to 
communicate with the simulated model in the gazebo, as well as retrieve and change its data and parameters.
"""

import roslibpy
import rospy
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Twist
import time
import math 

class Drone():


    def __init__(self, client):

        #Variables responsible for storing the drone's speed 
        self._linear_speed = [0,0,0]
        self._angular_speed = [0,0,0]

        #variables for camera rotation (radian)
        self._pitch = 0
        slef._yaw = 0

        self.drone_name = "quadrotor"
        self.camera_name = "camera"

        #Setting up the topic that will be responsible for sending the speed commands to the drone
        self.move_topic = roslibpy.Topic(client, '/cmd_vel', '/geometry_msgs/Twist')


    
    ############Drone Functions############

    def setDroneSpeed(self, linear, angular):
        '''
                Function responsible for changing the speed of the drone. The drone will maintain the speed until it is changed by a 
                new call of this same function.
           
            Inputs:
                    "linear"  -> 3-element list representing the linear velocity of the drone [Vx, Vy, Vz]
                    "angular" -> 3-element list representing the linear velocity of the drone [Wx, wy, Wz]
            Outputs:
                
        '''
        self._linear_speed = linear
        self._angular_speed = angular

        speed = {'linear': {'x': linear[0], 'y': linear[1], 'z': linear[2]}, 'angular': {'x': angular[0], 'y': angular[1], 'z': angular[2]}}

        self.move_topic.publish(roslibpy.Message(speed))

    def getDroneSpeed(self):
        '''
            The function will return the momentary linear and angular velocities of the drone
           
            Inputs:
                   
            Outputs:
                -2x3 matrix containing the two momentary linear and angular velocity vectors of the drone [[Vx, Vy, Vz],[Wx, Wy, Wz]]   
        '''
        return [self._linear_speed,self._angular_speed]
 
    def setDronePosition(self, position, orientation):
            '''
                    Function responsible for changing the drone position and orientation
            
                Inputs:
                        "position"  -> 3-element list representing the position of the drone [Px, Py, Pz]
                        "orientation" -> 3-element list representing the orientation of the drone [Ox, Oy, Oz]
                Outputs:
                
            '''
            state_msg = ModelState()
            state_msg.model_name = self.drone_name
            state_msg.pose.position.x = position[0]
            state_msg.pose.position.y = position[1]
            state_msg.pose.position.z = position[2]
            state_msg.pose.orientation.x = orientation[0]
            state_msg.pose.orientation.y = orientation[1]
            state_msg.pose.orientation.z = orientation[2]
            state_msg.pose.orientation.w = 0
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            set_state( state_msg )

    def getDronePosition(self):
        '''
            The function will return the position of the drone
           
            Inputs:
                   
            Outputs:
                -1x3 matrix containing the position [Px, Py, Pz] 
        '''
        model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        object_coordinates = model_coordinates(self.drone_name, "")

        return [object_coordinates.pose.position.x,object_coordinates.pose.position.y,object_coordinates.pose.position.z]

    def getDroneOrientation(self):
        '''
            The function will return the orientation of the drone
           
            Inputs:
                   
            Outputs:
                -1x3 matrix containing the orientation [Px, Py, Pz] 
        '''
        model_coordinates = rospy.ServiceProxy( '/gazebo/get_model_state', GetModelState)
        object_coordinates = model_coordinates(self.drone_name, "")

        return [object_coordinates.pose.orientation.x,object_coordinates.pose.orientation.y,object_coordinates.pose.orientation.z]
    
    #todo
    def take_off(self):
        return
    
    #todo
    def land_on(self):
        return


    ############Camera Functions############

    #todo
    def setCameraOrientation(self, pitch, yaw, radian=True):
        
        if(!radian):
            _pitch = pitch * math.pi / 180
            _yaw = yaw *  math.pi / 180

        if(pitch < 0)pitch = 0
        if(pitch > math.pi) pitch = math.pi

        if(yaw < -2*math.pi)yaw = -2*math.pi
        if(yaw > 2*math.pi) yaw = 2*math.pi

        return

    #todo
    def getCameraOrientation(self, degree=False):
        if(degree):
            return _pitch*180/math.pi, _yaw*180/math.pi
        return  _pitch, _yaw

    #todo
    def getCameraImage(self):

        return


    ##########Simulation Functions###########

    #todo
    def getSimulationTime(self):
        return 1

    def resetSimulation():
        setDroneSpeed(self, [0,0,1],[0,0,0])
        setDroneSpeed(self, [0,0,0],[0,0,0])
        setDronePosition(self, [0,0,1],[0,0,0])

