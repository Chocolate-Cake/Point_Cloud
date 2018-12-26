import sys
sys.path.append('/usr/local/Cellar/')
import pcl
import math
import argparse
import sys
import os
from PIL import Image
from grapher import graph
from agent import Agent
#from AgentsManager import AgentsManager
 

class CloudManager:

    def __init__(self):
        self.cloud = pcl.PointCloud()
        #TODO what is this param
        self.octree = pcl.OctreePointCloudSearch(0.1)
        self.octree.set_input_cloud(self.cloud)
        self.octree.add_points_from_input_cloud()
        #self.agents = AgentsManager()

    '''
    Purpose: given depth map image, convert to list of points 
    TODO 1. need to make sure this actually works and 2. OP said it could be slow
    '''
    #src = https://codereview.stackexchange.com/questions/79032/generating-a-3d-point-cloud
    def depth_map_to_cloud(self, depth_image, my_pos, fov):
        rows, cols = depth.shape
        c, r = np.meshgrid(np.arange(cols), np.arange(rows), sparse=True)
        valid = (depth > 0) & (depth < 255)
        z = np.where(valid, depth / 256.0, np.nan)
        x = np.where(valid, z * (c - my_pos[0]) / fov[0], 0)
        y = np.where(valid, z * (r - my_pos[1]) / fov[1], 0)
        return np.dstack((x, y, z))

    '''
    Purpose: given current orientation of camera, current position, and point cloud relative to camera,
    merge points into saved big point cloud
    vector = [x, y, z] of direction that camera was looking when acquired cloud
    where the objective coordinate plane has x=east+/west-, y=north+/south-, z=up+/down-
    my_pos = (x, y, z) of objective location of self
    cloud = pcl.PointCloud() given relative to my_pos and vector
    '''
    def reorient_concat_cloud(self, vector, my_pos, cloud):

        #polar coordinates relative to world
        r = sqrt(pow(vector[0], 2) + pow(vector[1], 2) + pow(vector[2], 2))
        #angle from z axis [0,0,1]
        theta = math.arccos(vector[2]/r)
        #angle from x axis [1, 0] using only x y components of vector
        phi = math.arccos(vector[0]/sqrt(pow(vector[0], 2) + pow(vector[1], 2)))

        '''
        inverse of matrix applied to z axis [0, 0, r] gave us vector of camera view
        apply matrix to everything in camera view to reorient 3d space to match world
        '''
        #TODO 
        rotation_matrix = [[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]

        pts_list = cloud.to_list()
        converted_list = []
        for p in pts_list:
            relative_vector = [p[0]-my_pos[0], p[1]-my_pos[1], p[2]-my_pos[2]]

            #TODO apply rotation matrix to relative vector
            #transformed_vector = []
            sum_vector = [relative_vector[0] + vector[0], relative_vector[1] + vector[1], relative_vector[2] + vector[2]]
            objective_pos = (my_pos[0] + sum_vector[0], my_pos[1] + sum_vector[1], my_pos[2] + sum_vector[2])
            converted_list.append(objective_pos)
        self.concat_points_cloud(converted_list)

    '''
    Purpose: given a point cloud object, merge it into the saved big point cloud
    new_cloud = pcl.PointCloud()
    '''
    def concat_literal_cloud(self, new_cloud):
        new_pts = new_cloud.to_list()
        self.replace(new_cloud)

    '''
    Purpose: given a list of points, merge it into the saved big point cloud
    points_list = list of tuples of (x, y, z)
    '''
    def concat_points_cloud(self, points_list):
        self.replace(points_list)

    '''
    Purpose: given a depth map image, convert it to point cloud and merge cloud into saved big cloud
    depth_image = depth map image
    '''
    def concat_depth_map(self, depth_image):
        points = self.depth_map_to_cloud(depth_image)
        self.replace(points)

    '''
    Purpose: returns # of points in radius r of coordinate pt_pos
    pt_pos = point tuple (x, y, z)
    r = radius float
    '''
    #TODO make this return actual useful info
    def radius_search(self, pt_pos, r):
        self.octree.set_input_cloud(self.cloud)
        self.octree.add_points_from_input_cloud()
        points = self.octree.radius_search(pt_pos, r)
        return points

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
    '''
    def replace(self, points_list):
        #find 2 points that would define the 3D space
        min_x = min([tup[0] for tup in points_list])
        max_x = max([tup[0] for tup in points_list])
        min_y = min([tup[1] for tup in points_list])
        max_y = max([tup[1] for tup in points_list])
        min_z = min([tup[2] for tup in points_list])
        max_z = max([tup[2] for tup in points_list])

        temp_removed = []
        #remove points that aren't there anymore
        my_pts = self.cloud.to_list()
        for point in my_pts:
            #if in space and keeping points, don't remove, else remove
            if (point not in points_list and 
                point[0] >= min_x and point[0] <= max_x and
                point[1] >= min_y and point[1] <= max_y and
                point[2] >= min_z and point[2] <= max_z):
                temp_removed.append(point)
                my_pts.remove(point)

        #add new points
        for point in points_list:
            if point not in my_pts:
                my_pts.append(point)

        self.cloud = pcl.PointCloud(list(my_pts))
        print(temp_removed)

    def save_cloud(self, f):
        with open(f, 'w+') as doc:
            for p in self.cloud.to_list():
                doc.write(str(p[0]) + ',' + str(p[1]) + ',' + str(p[2]) + '\n')

    def print_cloud(self):
        print(self.cloud.to_list())

    def return_cloud(self):
        return self.cloud.to_list()

    #def return_agents(self):
    #    return self.agents.return_agents()






