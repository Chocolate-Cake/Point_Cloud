import sys
sys.path.append('/usr/local/Cellar/')
import pcl
import math
import argparse
import sys
import os
from PIL import Image

class CloudManager:

    def __init__(self):
        self.cloud = pcl.PointCloud()
        #TODO what is this param
        self.octree = pcl.OctreePointCloudSearch(0.1)
        self.octree.set_input_cloud(self.cloud)
        self.octree.define_bounding_box()
        self.octree.add_points_from_input_cloud()

    '''
    Purpose: given depth map image, convert to list of points 
    TODO 1. need to make sure this actually works and 2. OP said it could be slow
    '''
    #src = https://codereview.stackexchange.com/questions/79032/generating-a-3d-point-cloud
    def depth_map_to_cloud(self, depth_image):
        rows, cols = depth.shape
        c, r = np.meshgrid(np.arange(cols), np.arange(rows), sparse=True)
        valid = (depth > 0) & (depth < 255)
        z = np.where(valid, depth / 256.0, np.nan)
        x = np.where(valid, z * (c - self.cx) / self.fx, 0)
        y = np.where(valid, z * (r - self.cy) / self.fy, 0)
        return np.dstack((x, y, z))

    '''
    Purpose: given current orientation of camera, current position, and point cloud relative to camera,
    merge points into saved big point cloud
    vector = [x, y, z] of direction that camera was looking when acquired cloud
    where the objective coordinate plane has x=east+/west-, y=north+/south-, z=up+/down-
    my_pos = (x, y, z) of objective location of self
    cloud = pcl.PointCloud() given relative to my_pos and vector
    TODO this is wrong, need to use polar coordinates, need to fix
    '''
    def reorient_concat_cloud(self, vector, my_pos, cloud):
        pts_list = cloud.to_list()
        converted_list = []
        for p in pts_list:
            relative_vector = [p[0]-my_pos[0], p[1]-my_pos[1], p[2]-my_pos[2]]
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
        my_pts = self.cloud.to_list()
        self.cloud = pcl.PointCloud(new_pts + my_pts)

    '''
    Purpose: given a list of points, merge it into the saved big point cloud
    points_list = list of tuples of (x, y, z)
    '''
    def concat_points_cloud(self, points_list):
        my_pts = self.cloud.to_list()
        self.cloud = pcl.PointCloud(my_pts+points_list)

    '''
    Purpose: given a depth map image, convert it to point cloud and merge cloud into saved big cloud
    depth_image = depth map image
    '''
    def concat_depth_map(self, depth_image):
        points = self.depth_map_to_cloud(depth_image)
        self.concat_points_cloud(points)

    '''
    Purpose: returns list of all points in radius r of coordinate pt_pos
    pt_pos = point tuple (x, y, z)
    r = radius float
    '''
    def radius_search(self, pt_pos, r):
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









