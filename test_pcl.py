import sys
import pcl
import math
import argparse
from CloudManager import CloudManager
import sys
import os
from PIL import Image

c = CloudManager()

def test_make_cloud():
	#test concat_points_cloud
	print()
	print(test_make_cloud.__name__)
	c.concat_points_cloud([(1, 2, 3), (4, 5, 6), (6, 7, 8)])
	c.print_cloud()

def test_r_search():
	print()
	print(test_r_search.__name__)
	#test radius search
	result = c.radius_search((1,1,1), 1, 9)
	print("result " + str(result))

def test_replace_with_pts():
	print()
	print(test_replace_with_pts.__name__)
	#test replace space
	items = [1,2,3]
	full = [(x, y, z) for x in items for y in items for z in items]
	c.concat_points_cloud(full)


def test_replace_with_empty():
	print(test_replace_with_empty.__name__)
	#test replace with empty space
	print("before " + str(c.cloud_size()))
	empty = [(1,1,1), (3,3,3)]
	c.concat_points_cloud(empty)
	print("after " + str(c.cloud_size()))

def test_depth_map():
	t = [[150, 150, 200, 200],
		 [150, 150, 200, 200],
		  [255, 255, 100, 100],
		  [255, 255, 100, 100]]

	

def test_write_cloud():
	c.save_cloud("test.txt")


test_make_cloud()
test_replace_with_pts()
test_r_search()

#test_replace_with_empty()
#test_write_cloud()
#p = pcl.PointCloud()














print("test end")