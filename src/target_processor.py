#!/usr/bin/env python3

from sensor_msgs.msg import PointCloud2
import rospkg
import rospy
import os
import ros_numpy
import math
import csv

class ProcessingNode:
    def __init__(self):
        rospy.init_node('target_point_saver', anonymous=True)
        rospy.Subscriber('/box_cropped_points', PointCloud2, self.callback) 

        try:
            name = rospy.get_param("~filename_param")
            path = rospy.get_param("~filepath_param")
        except KeyError:
            rospy.logwarn("Parameter failed to load")

        rospack = rospkg.RosPack()
        package_path = rospack.get_path('repeatability_processing')
        self.csv_file = os.path.join(package_path, path, name)

    def callback(self, msg):
        # Convert the PointCloud2 message to a NumPy array
        pc_array = ros_numpy.point_cloud2.pointcloud2_to_array(msg)
        ranges = []
        
        for point in pc_array:
            x = point['x']
            y = point['y']
            z = point['z']
            range = math.sqrt((x ** 2) + (y ** 2) + (z ** 2)) # euclidean distance where pt_2 is point on target and pt_1 is sensor (zero)
            ranges.append(range)

            print(f"X: {x:.4f}  Y: {y:.4f}  Z: {z:.4f}  Range: {range:.4f}")

        if ranges:
            with open(self.csv_file, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(ranges)
            

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        processing_node = ProcessingNode()
        processing_node.run()
    except rospy.ROSInterruptException:
        pass