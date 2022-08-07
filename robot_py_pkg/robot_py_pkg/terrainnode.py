#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 21:28:18 2022

@author: mcunbagy
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np
from visualization_msgs.msg import Marker, MarkerArray



class TerrainNode(Node):
    
    def __init__(self):
        super().__init__('terrainnode')
        timer_period = 0.01  # publishing period(sec)
        # real life centers
        self.__red_centers=[]
        self.__blue_centers=[]
        self.__green_centers=[]
        self.__yellow_centers=[]
        # grid centers
        self.__r=[]
        self.__g=[]
        self.__b=[]
        self.__y=[]
        self.__nodes=[]
        self.empty=[]
        #subscribe
        self.create_subscription(Image,'/image',self.on_image_received,1)
        #publish
        self.publish_gridPoints = self.create_publisher(MarkerArray, 'grid', 10)
        self.gridPoints_timer = self.create_timer(timer_period, self.gridPoints_callback)
        
    def on_image_received(self, msg):
        self.__red_centers=[]
        self.__blue_centers=[]
        self.__green_centers=[]
        self.__yellow_centers=[]
        self.__r=[]
        self.__g=[]
        self.__b=[]
        self.__y=[]
        self.__nodes=[]
        self.empty=[]
        
        frame = np.array(msg.data).reshape((240, 320,3))
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # color limits
        low_red1 = np.array([0,80,80])
        high_red1 = np.array([15,255,255])
        low_red2 = np.array([141,80,80])
        high_red2 = np.array([179,255,255]) 
        low_blue = np.array([80,60,60])
        high_blue = np.array([140,255,255])
        low_green = np.array([35,112,112])
        high_green = np.array([79,255,255])
        low_yellow = np.array([16,80,80])
        high_yellow = np.array([38,255,255])
        #masking
        red_mask1 = cv2.inRange(hsv_frame, low_red1, high_red1)
        red_mask2 = cv2.inRange(hsv_frame, low_red2, high_red2)
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
        red1 = cv2.bitwise_and(frame, frame, mask=red_mask1)
        red2 = cv2.bitwise_and(frame, frame, mask=red_mask2)
        red  = red1 + red2
        blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)
        yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)
        #doing some stuff
        red_grey = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
        red_dilt = cv2.dilate(red_grey, (4,4), iterations=1)
        red_erod = cv2.erode(red_dilt, (4,4), iterations=1)
        red_medB = cv2.medianBlur(red_erod,3)
        blue_grey= cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
        blue_dilt= cv2.dilate(blue_grey, (4,4), iterations=1)
        blue_erod= cv2.erode(blue_dilt, (4,4), iterations=1)
        blue_medB= cv2.medianBlur(blue_erod, 3)
        green_grey= cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
        green_dilt= cv2.dilate(green_grey, (4,4), iterations=1)
        green_erod= cv2.erode(green_dilt, (4,4), iterations=1)
        green_medB= cv2.medianBlur(green_erod, 3)
        yellow_grey= cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY)
        yellow_dilt= cv2.dilate(yellow_grey, (4,4), iterations=1)
        yellow_erod= cv2.erode(yellow_dilt, (4,4), iterations=1)
        yellow_medB= cv2.medianBlur(yellow_erod, 3)
        #doing memore stuff
        contours_red ,_= cv2.findContours(red_medB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours_blue ,_= cv2.findContours(blue_medB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours_green ,_= cv2.findContours(green_medB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow ,_= cv2.findContours(yellow_medB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        self.__center_list = []
        colored_contours = [contours_red,contours_blue,contours_green, contours_yellow]
        
        for l, list in enumerate(colored_contours):
            for i, c in enumerate(list):
                M = cv2.moments(c)
                if (M["m00"] > 1000 and M["m00"]!=0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    if (l==0):
                        self.__red_centers.append([cX/250, abs(240-cY)/250, (255,0,0)])
                        cv2.drawContours(frame, list, i, (255,255,255),3)
                    elif (l==1):
                        self.__blue_centers.append([cX/250, abs(240-cY)/250, (0,0,255)])
                        cv2.drawContours(frame, list, i, (170,170,170),3)
                    elif (l==2):
                        self.__green_centers.append([cX/250, abs(240-cY)/250, (0,255,0)])
                        cv2.drawContours(frame, list, i, (85,85,85),3)
                    elif (l==3):
                        self.__yellow_centers.append([cX/250, abs(240-cY)/250, (255,255,0)])
                        cv2.drawContours(frame, list, i, (0,0,0),3)
                    else:
                        continue

                    
        x_dots = [0.08,0.24,0.40,0.56,0.72,0.88,1.04,1.20]
        y_dots = [0.08,0.24,0.40,0.56,0.72,0.88]
        for x in x_dots:
            for y in y_dots:
                self.__nodes.append([x,y]) #since opencv reaches pixels vice versa
                cv2.circle(frame, (int(x*250),int(y*250)), 5, (0,0,0), -1)
        rnmin=[]     #indexes of red nodes in nodes[]
        rdmin=[]
        for r, red_center in enumerate(self.__red_centers):
            for n, node in enumerate(self.__nodes):
                d = (red_center[1]-node[1])**2 + (red_center[0]-node[0])**2
                rdmin.append(d)
            dist = min(rdmin)
            n=rdmin.index(dist)
            rnmin.append(n)
            rdmin=[]           
                    
        bnmin=[]
        bdmin=[]
        for b, blue_center in enumerate(self.__blue_centers):
            for n, node in enumerate(self.__nodes):
                d = (blue_center[1]-node[1])**2 + (blue_center[0]-node[0])**2
                bdmin.append(d)
            dist = min(bdmin)
            n=bdmin.index(dist)
            bnmin.append(n)
            bdmin=[]
           
        gnmin=[]      #indexes of green nodes in nodes[]
        gdmin=[]
        for g, green_center in enumerate(self.__green_centers):
            for n, node in enumerate(self.__nodes):
                d = (green_center[1]-node[1])**2 + (green_center[0]-node[0])**2
                gdmin.append(d)
            dist = min(gdmin)
            n=gdmin.index(dist)
            gnmin.append(n)
            gdmin=[]
                    
        ynmin=[]        #indexes of yellow nodes in nodes[]
        ydmin=[]     
        for y, yellow_center in enumerate(self.__yellow_centers):
            for n, node in enumerate(self.__nodes):
                d = (yellow_center[1]-node[1])**2 + (yellow_center[0]-node[0])**2
                ydmin.append(d)
            dist=min(ydmin)
            n=ydmin.index(dist)
            ynmin.append(n)
            ydmin=[]
          
        self.empty=self.__nodes.copy()
        #print(self.empty)
        for index in rnmin:
            self.__r.append([self.__nodes[index],index])
            self.empty.remove(self.__nodes[index])
        for index in gnmin:
            self.__g.append([self.__nodes[index],index])
            self.empty.remove(self.__nodes[index])
        for index in bnmin:
            self.__b.append([self.__nodes[index],index])
            self.empty.remove(self.__nodes[index])
        for index in ynmin:
            self.__y.append([self.__nodes[index],index])
            self.empty.remove(self.__nodes[index])
        
        #self.__empty=list(self.__empty)        
        cv2.imshow('frame', frame)
        # Wait 3 milisecoonds for an interaction. Check the key and do the corresponding job.
        k = cv2.waitKey(100)
        if k == 27:
            cv2.destroyAllWindows()
        
    def gridPoints_callback(self):
        grid_msg=MarkerArray()
        for i in range(len(self.__r)):
            cell_msg=Marker()
            cell_msg.id=int(self.__r[i][1])
            cell_msg.pose.position.x=float(self.__r[i][0][0])
            cell_msg.pose.position.y=float(self.__r[i][0][1])
            cell_msg.color.r = 255.0
            cell_msg.color.g = 0.0
            cell_msg.color.b = 0.0
            grid_msg.markers.append(cell_msg)
        for j in range(len(self.__g)):
            cell_msg=Marker()
            cell_msg.id=int(self.__g[j][1])
            cell_msg.pose.position.x=float(self.__g[j][0][0])
            cell_msg.pose.position.y=float(self.__g[j][0][1])
            cell_msg.color.r = 0.0
            cell_msg.color.g = 255.0
            cell_msg.color.b = 0.0
            grid_msg.markers.append(cell_msg)
        for k in range(len(self.__b)):
            cell_msg=Marker()
            cell_msg.id=int(self.__b[k][1])
            cell_msg.pose.position.x=float(self.__b[k][0][0])
            cell_msg.pose.position.y=float(self.__b[k][0][1])
            cell_msg.color.r = 0.0
            cell_msg.color.g = 0.0
            cell_msg.color.b = 255.0
            grid_msg.markers.append(cell_msg)
        for l in range(len(self.__y)):
            cell_msg=Marker()
            cell_msg.id=int(self.__y[l][1])
            cell_msg.pose.position.x=float(self.__y[l][0][0])
            cell_msg.pose.position.y=float(self.__y[l][0][1])
            cell_msg.color.r = 255.0
            cell_msg.color.g = 255.0
            cell_msg.color.b = 0.0
            grid_msg.markers.append(cell_msg)
        for m in range(len(self.empty)):
            cell_msg=Marker()
            idd = self.__nodes.index(self.empty[m])
            cell_msg.id=int(idd)
            cell_msg.pose.position.x=float(self.empty[m][0])
            cell_msg.pose.position.y=float(self.empty[m][1])
            cell_msg.color.r = 255.0
            cell_msg.color.g = 255.0
            cell_msg.color.b = 255.0
            grid_msg.markers.append(cell_msg)
        self.publish_gridPoints.publish(grid_msg)        
        self.get_logger().info('Publishing: "%s"' % grid_msg.markers)
            
def main(args=None):
    rclpy.init(args=args)
    node = TerrainNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
