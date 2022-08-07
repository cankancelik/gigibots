import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np
from geometry_msgs.msg import Twist
import cv2.aruco as aruco



class RobotNode(Node):
    
    def __init__(self):
        #initialize super class
        super().__init__('minirobot')
        #initialize attributes of robot         
        self.robot=[0.0,0.0,0.0,0.0,0.0]
        #create position list
        self.robots=[]
        #Subscribe Playground Visual
        self.create_subscription(Image,'/image',self.on_image_received,1)
        #Publish Robot Attributes
        self.publisher = self.create_publisher(Twist, 'robotatt', 1)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.pose_callback)
        
        
    def on_image_received(self, msg, num_of_rob=3):
        img = np.array(msg.data).reshape((240, 320,3))
        frame=img
        # Coefficients Obtained by Camera Calibration
        #camera matrix coefficients
        matrix =[[5.25994127e+03, 0.00000000e+00, 1.16284255e+02],[0.00000000e+00, 2.63529855e+03, 1.99950249e+02],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
        #distortion coefficients
        distortion = [[ 2.69862233e+01, -2.94850583e+03,  1.22463053e+00, -3.03490024e-02, 9.14449800e+04]]
        #convertin to np array
        mtx=np.array(matrix)
        dist=np.array(distortion)
        
        # operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Change grayscale
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)  # Use 5x5 dictionary to find markers
        parameters = aruco.DetectorParameters_create()  # Marker detection parameters
        # lists of ids and the corners beloning to each id
        corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict,
                                                                parameters=parameters,
                                                                cameraMatrix=mtx,
                                                                distCoeff=dist)
        
        if np.all(ids is not None):  # If there are markers found by detector
            for i in range(0, len(ids)):  # Iterate in markers
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
                rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners[i], 0.02, mtx,dist)
                (rvec - tvec).any()  # get rid of that nasty numpy value array error
                aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers
                aruco.drawAxis(frame, mtx, dist, rvec, tvec, 0.01)  # Draw Axis
                #print(corners)
                x_sum = corners[i][0][0][0]+ corners[i][0][1][0]+ corners[i][0][2][0]+ corners[i][0][3][0]
                y_sum = corners[i][0][0][1]+ corners[i][0][1][1]+ corners[i][0][2][1]+ corners[i][0][3][1]
                x_centerPixel = x_sum*.25
                y_centerPixel = y_sum*.25
                # image to 2D coordinates transformation
                y_centerPixel = np.absolute(y_centerPixel-240)
                # way to find the rotation
                rhs_mid_x= (corners[i][0][1][0] + corners[i][0][2][0])*0.5
                rhs_mid_y= (corners[i][0][1][1] + corners[i][0][2][1])*0.5
                # need to transfrom mid_y to 2D Coordinates
                rhs_mid_y= np.absolute(rhs_mid_y-240)
                #calculate rotation angle
                deltay=rhs_mid_y-y_centerPixel
                deltax=rhs_mid_x-x_centerPixel
                rot=np.arctan2(deltay, deltax) * 180 / np.pi
                #no depth change
                z=float(0)
                #print(ids)
                if len(self.robots)<num_of_rob:
                    if ids[i][0] == 1:
                        self.robot=[x_centerPixel,y_centerPixel,z,float(1),rot]
                        self.robots.append(self.robot)                            
                    elif ids[i][0] ==2:
                        self.robot= [x_centerPixel,y_centerPixel,z,float(2),rot]
                        self.robots.append(self.robot)
                    elif ids[i][0] == 3:
                        self.robot= [x_centerPixel,y_centerPixel,z,float(3),rot]
                        self.robots.append(self.robot)
                    elif ids[i][0] == 4:
                        self.robot= [x_centerPixel,y_centerPixel,z,float(4),rot]
                        self.robots.append(self.robot)
                    elif ids[i][0] == 5:
                        self.robot= [x_centerPixel,y_centerPixel,z,float(5),rot]
                        self.robots.append(self.robot)
                    elif ids[i][0] == 6:
                        self.robot= [x_centerPixel,y_centerPixel,z,float(6),rot]
                        self.robots.append(self.robot)
                    elif ids[i][0] == 7:
                        self.robot= [x_centerPixel,y_centerPixel,z,float(7),rot]
                        self.robots.append(self.robot)
                    elif ids[i][0] == 8:
                        self.robot= [x_centerPixel,y_centerPixel,z,float(8),rot]
                        self.robots.append(self.robot)
                else:
                    self.robots=[]
                                
        # Display the resulting frame
        cv2.imshow('frame', frame)
        # Wait 3 milisecoonds for an interaction. Check the key and do the corresponding job.
        k = cv2.waitKey(100)
        if k == 27:
            cv2.destroyAllWindows()
            
    def pose_callback(self):
        robatt_msg = Twist()
        # twist msg msg to publish 2d pose with robot id
        for k in self.robots:
            robatt_msg.linear.x = k[0]
            robatt_msg.linear.y = k[1]
            robatt_msg.linear.z = k[2]
            robatt_msg.angular.x = k[3] #robot id 
            robatt_msg.angular.z = k[4]
            self.publisher.publish(robatt_msg)
            self.get_logger().info('Publishing: "%s"' % robatt_msg)
            

def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
