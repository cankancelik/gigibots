import rclpy
from rclpy.node import Node
import numpy as np
#import required msgs
from geometry_msgs.msg import Vector3
from diagnostic_msgs.msg import KeyValue
from sensor_msgs.msg import Image, LaserScan 




#Disclaimer ROBOT ID has been used in several type of msg

class UsersNode(Node):
    
    def __init__(self):
        #initialize super class
        super().__init__('user')
        timer_period = 0.001  # publishin period(sec)
        self.__wheelvel=Vector3()
        self.__lidar=LaserScan()
        self.__lidardistances=[]
        self.__rob_id=0
        self.__rob_type=0
        #Subscribe snapshot
        self.create_subscription(Image,'view',self.__userView_callback,10)
        #subscribe lidar data and properties from webots 
        self.create_subscription(LaserScan, 'lidarData', self.__lidarData_callback, 10)
        #subscribe camera data from webots 
        self.create_subscription(Image, 'cameraData', self.__camData_callback, 10)
        #subscribe camera data from webots 
        self.create_subscription(KeyValue, 'playerType', self.__playerType_callback, 10)
        #Publish Run Info
        self.publish_speedReq = self.create_publisher(Vector3, 'wheel_vel', 10)
        self.speedReq_timer = self.create_timer(timer_period, self.__speedRequest_callback)

    # speed request to send game master   
    def __speedRequest_callback(self):
        run_msg=Vector3()        
        run_msg.x=1.0   #Left Wheel Velocity
        run_msg.y=1.0   #Right Wheel Velocity
        run_msg.z=1.0   #Robot ID
        # Publish the info and logger            
        self.publish_speedReq.publish(run_msg)
        self.get_logger().info('Publishing: "%s"' % run_msg)
        
    # set player type and id   
    def __playerType_callback(self, specs):
        specs.key      #PLAYER ID AS STRING
        specs.value    #PLAYER TYPE
        
    # get bird eye view camera data
    def __userView_callback(self, birdeye): 
        birdeye.data

    
    #get lidar data simulated on webots                    
    def __lidarData_callback(self, lidar):
        # Properties of Lidar on the Robot
        lidar.angle_min
        lidar.angle_max
        lidar.angle_increment
        
    # get POV camera data
    def __camData_callback(self, cam):
        # Properties of Lidar on the Robot
        cam.data
  
                  

def main(args=None):
    rclpy.init(args=args)
    node = UsersNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
