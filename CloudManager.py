import sys
sys.path.append('/usr/local/Cellar/')
import pcl
import math
import argparse
import sys
import os
from PIL import Image
from agent import Agent
from camera import Camera
import tools
#from AgentsManager import AgentsManager

class CloudManager:

    '''
    TODO
    - check movement
    - deal with agents problem

    Note
    - may need to change the way the remove function works, if too many points in cloud and too slow.
    instead of converting all cloud to list, remove all coordinates of empty space in incoming image
    '''
    def __init__(self, wr, hr, dark, do_round=True):
        self.cloud = pcl.PointCloud()
        #TODO what is this param
        self.octree = pcl.OctreePointCloudSearch(0.1)
        self.camera = Camera(wr, hr, dark, do_round=do_round)
        #self.agents = AgentsManager()

    '''
    Purpose: given a point cloud object, merge it into the saved big point cloud
    new_cloud = pcl.PointCloud()
    '''
    def concat_literal_cloud(self, new_cloud):
        new_pts = new_cloud.to_list()
        x, y, z = tools.find_min_max(new_pts)
        self.replace(new_cloud, x, y, z)

    '''
    Purpose: given a list of points, merge it into the saved big point cloud
    points_list = list of tuples of (x, y, z)
    '''
    def concat_points_cloud(self, points_list):
        x, y, z, = tools.find_min_max(points_list)
        self.replace(points_list, x, y, z)

    '''
    Purpose: given a whole bunch of parameters (see camera.py), convert depth image to points and merge into saved big cloud
    '''
    def concat_depth_map(self, pos, projection, p, r, y, lp, lr, ly):
        points_list = self.camera.convert(pos, projection, p, r, y, lp, lr, ly)
        x, y, z = tools.find_min_max(points_list)
        self.replace(points_list, x, y, z)

    '''
    Purpose: returns num instances of coordinates of points in radius r of input coordinate pt_pos
    pt_pos = point tuple (x, y, z)
    r = radius float
    num = max number of points to fetch
    '''
    def radius_search(self, pt_pos, r, num):
        self.octree.set_input_cloud(self.cloud)
        self.octree.add_points_from_input_cloud()
        indices, rads = self.octree.radius_search(pt_pos, r, num)
        l = self.cloud.to_list()
        coords = []
        for i in indices:
            coords.append(l[i])
        return coords

    '''
    Purpose: returns T/F if my_pos and pt_pos are within r of each other
    my_pos = point tuple (x, y, z)
    pt_pos = point tuple (x, y, z)
    '''
    def is_in_radius(self, my_pos, pt_pos, r):
        dist = pow(my_pos[0]-pt_pos[0], 2) + pow(my_pos[1]-pt_pos[1], 2) + pow(my_pos[2]-pt_pos[2], 2)
        return dist <= r

    def cloud_size(self):
        return len(self.cloud.to_list())

    '''
    Purpose: replace piece of cloud using new info
    points_list = list of points that are in new snapshot of environment
    arr_thing = (min max) of that dimension
    '''
    def replace(self, points_list, arr_x, arr_y, arr_z):
        
        temp_removed = []
        #remove points that aren't there anymore
        my_pts = self.cloud.to_list()
        for point in my_pts:
            #if in space and keeping points, don't remove, else remove
            if (point not in points_list and 
                point[0] >= arr_x[0] and point[0] <= arr_x[1] and
                point[1] >= arr_y[0] and point[1] <= arr_y[1] and
                point[2] >= arr_z[0] and point[2] <= arr_z[1]):
                temp_removed.append(point)
                my_pts.remove(point)

        #add new points
        for point in points_list:
            if point not in my_pts:
                my_pts.append(point)

        self.cloud = pcl.PointCloud(list(my_pts))

    ''''
    Purpose: utility function to write cloud to file because matplotlib is incompatible with docker instance needed for pcl
    f = string file name to write to
    '''
    def save_cloud(self, f):
        with open(f, 'w+') as doc:
            for p in self.cloud.to_list():
                doc.write(str(p[0]) + ',' + str(p[1]) + ',' + str(p[2]) + '\n')

    '''
    Purpose: print out points in cloud with their index numbers, good for verifying radius search
    '''
    def print_cloud(self):
        l = self.cloud.to_list()

        for x in range(len(l)):
            print(str(x) + ' ' + str(l[x]))

    def return_cloud(self):
        return self.cloud.to_list()





