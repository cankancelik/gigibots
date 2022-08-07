import rclpy
from rclpy.node import Node
import numpy as np
import socket            
#from getch import getche, getch
#from time import sleep
#import required msgs
from geometry_msgs.msg import Vector3
from diagnostic_msgs.msg import KeyValue

TCP_IP1 ='192.168.48.101'
TCP_IP2 ='192.168.48.102'
TCP_IP3 ='192.168.48.103'
TCP_IP4 ='192.168.48.104'
TCP_PORT1 = 5005
TCP_PORT2 = 5006
TCP_PORT3 = 5007
TCP_PORT4 = 5008 #just a random port/may change..
right_velocity = '+6.2'    # her zaman 1 basamaklı olacak  -----> (sayı)   #MAX:6.2
left_velocity = '+6.2'  # her zaman 4 basamaklı olacak  -----> (sayı)(.)(sayı)(sayı)

# Create a socket object
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                

# connect to the server on NODEMCU
res1 = s1.connect_ex((TCP_IP1,TCP_PORT1))
res2 = s2.connect_ex((TCP_IP2,TCP_PORT2))
res3 = s3.connect_ex((TCP_IP3,TCP_PORT3))
res4 = s4.connect_ex((TCP_IP4,TCP_PORT4))

s1.settimeout(1)
s2.settimeout(1)
s3.settimeout(1)
s4.settimeout(1)

if (res1):
	print('bad request... an error occured while connecting to the server. :/ ')
else:
	print("Success!!! /n You are now connected to NodeMCU server!")   
if (res2):
    print('bad request... an error occured while connecting to the server. :/ ')
else:
	print("Success!!! /n You are now connected to NodeMCU server!")
if (res3):
	print('bad request... an error occured while connecting to the server. :/ ')
else:
	print("Success!!! /n You are now connected to NodeMCU server!")
if (res4):
	print('bad request... an error occured while connecting to the server. :/ ')
else:
	print("Success!!! /n You are now connected to NodeMCU server!")


#Disclaimer ROBOT ID has been used in several type of msg

class RunNode(Node):
    
    def __init__(self):
        #initialize super class
        super().__init__('run')
        self.y=0 #server period counter
        timer_period = 0.001  # publishin period(sec)
        self.__wheelvel=Vector3()
        self.__rob_id=0
        #Subscribe lidar data and properties from webots 
        self.create_subscription(Vector3, 'runInfo', self.__move_callback, 10)
        #Publish Charge Info
        self.publish_chargeReq = self.create_publisher(KeyValue, 'charge', 10)
        self.chargeReq_timer = self.create_timer(timer_period, self.__chargeRequest_callback)

    # speed request to send game master   
    def __chargeRequest_callback(self):
        charge_msg=KeyValue()        
        charge_msg.key      #Robot ID
        charge_msg.value    #empty or full
        # Publish the info and logger            
        self.publish_chargeReq.publish(charge_msg)
        #self.get_logger().info('Publishing: "%s"' % charge_msg)
        
    # set player type and id   try
    def __move_callback(self, run_cmd):
        self.__wheelvel.x=run_cmd.x #right wheel
        self.__wheelvel.y=run_cmd.y #right wheel
#        self.__wheelvel.z=run_cmd.z #ROB ID
        self.__wheelvel.z=1.0
        try:
            self.y=self.y+1
            print(self.y)
            if self.__wheelvel.z == 1.0:
                print('I am in')
                s1.send('R'.encode('utf-8'))
                s1.send(right_velocity.encode('utf-8'))
                s1.send('L'.encode('utf-8'))
                s1.send(left_velocity.encode('utf-8'))
                s1.send('E'.encode('utf-8'))
                if (self.y==10):
                    self.y = 0
                    print('trying to read from server NOW ...')
                    try:
                        input = s2.recv(1024).decode('utf-8')
                        print(input)
                        print(type(input))
                        if len(input)>2:
                            input = ""
                    except:
                        print("non taken")
            if self.__wheelvel.z == 1.0:
                print('I am in')
                s2.send('R'.encode('utf-8'))
                s2.send(right_velocity.encode('utf-8'))
                s2.send('L'.encode('utf-8'))
                s2.send(left_velocity.encode('utf-8'))
                s2.send('E'.encode('utf-8'))
                if (self.y==10):
                    self.y = 0
                    print('trying to read from server NOW ...')
                    try:
                        input = s2.recv(1024).decode('utf-8')
                        print(input)
                        print(type(input))
                        if len(input)>2:
                            input = ""
                    except:
                        print("non taken")
            if self.__wheelvel.z == 1.0:
                print('I am in')
                s3.send('R'.encode('utf-8'))
                s3.send(right_velocity.encode('utf-8'))
                s3.send('L'.encode('utf-8'))
                s3.send(left_velocity.encode('utf-8'))
                s3.send('E'.encode('utf-8'))
                if (self.y==10):
                    self.y = 0
                    print('trying to read from server NOW ...')
                    try:
                        input = s3.recv(1024).decode('utf-8')
                        print(input)
                        print(type(input))
                        if len(input)>2:
                            input = ""
                    except:
                        print("non taken")
        except:
            print('non sended')
                        
def main(args=None):
    rclpy.init(args=args)
    node = RunNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
